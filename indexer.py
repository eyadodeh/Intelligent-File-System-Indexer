import os
import ast
import re
import json
import argparse

FILE_TYPE_LABELS = {
    # Images
    '.jpg': '[IMG]', '.jpeg': '[IMG]', '.png': '[IMG]', '.gif': '[IMG]',
    '.bmp': '[IMG]', '.tiff': '[IMG]', '.svg': '[IMG]', '.webp': '[IMG]',

    # Documents
    '.txt': '[DOC]', '.doc': '[DOC]', '.docx': '[DOC]', '.pdf': '[DOC]',
    '.odt': '[DOC]', '.rtf': '[DOC]', '.md': '[DOC]',

    # Spreadsheets
    '.xls': '[XLS]', '.xlsx': '[XLS]', '.ods': '[XLS]', '.csv': '[XLS]',

    # Presentations
    '.ppt': '[PPT]', '.pptx': '[PPT]', '.odp': '[PPT]',

    # Source code
    '.py': '[PY]', '.java': '[JAVA]', '.c': '[C]', '.cpp': '[C++]',
    '.js': '[JS]', '.ts': '[TS]', '.html': '[HTML]', '.htm': '[HTML]',
    '.css': '[CSS]', '.php': '[PHP]', '.rb': '[RUBY]', '.swift': '[SWIFT]',
    '.go': '[GO]', '.sh': '[SH]', '.xml': '[XML]', '.json': '[JSON]',
    '.yaml': '[YAML]', '.yml': '[YAML]', '.bat': '[BATCH]',

    # Compressed/Archives
    '.zip': '[ARCHIVE]', '.rar': '[ARCHIVE]', '.7z': '[ARCHIVE]',
    '.tar': '[ARCHIVE]', '.gz': '[ARCHIVE]', '.bz2': '[ARCHIVE]',

    # Audio
    '.mp3': '[AUDIO]', '.wav': '[AUDIO]', '.ogg': '[AUDIO]',
    '.flac': '[AUDIO]', '.aac': '[AUDIO]',

    # Video
    '.mp4': '[VIDEO]', '.avi': '[VIDEO]', '.mov': '[VIDEO]',
    '.wmv': '[VIDEO]', '.mkv': '[VIDEO]',

    # Executables / Binaries
    '.exe': '[BIN]', '.bin': '[BIN]', '.msi': '[BIN]',
    '.apk': '[APK]', '.iso': '[ISO]',

    # Others
    '.log': '[LOG]', '.ini': '[CONFIG]', '.cfg': '[CONFIG]',
    '.db': '[DB]', '.sqlite': '[DB]', '.bak': '[BACKUP]'
}

def get_file_label(filename):
    ext = os.path.splitext(filename)[1].lower()
    return FILE_TYPE_LABELS.get(ext, '')

def alphanum_key(s):
    """Sort helper: handles case-insensitive and numeric sorting."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]




def insert_path(tree, path_parts):
    part = path_parts[0]
    if len(path_parts) == 1:
        tree["__files__"].append(part)
    else:
        if part not in tree["__dirs__"]:
            tree["__dirs__"][part] = {"__dirs__": {}, "__files__": []}
        insert_path(tree["__dirs__"][part], path_parts[1:])

def generate_tree(paths):
    tree = {"__dirs__": {}, "__files__": []}
    for path in paths:
        parts = path.strip("/").split("/")
        insert_path(tree, parts)
    return tree

def sort_items(files, dirs, sort_by_name, sort_by_ext, group_by_type):
    sorted_dirs = sorted(dirs, key=alphanum_key)
    
    if group_by_type:
        def file_sort_key(f):
            label = get_file_label(f)
            ext = os.path.splitext(f)[1].lower()
            return (label, ext if sort_by_ext else '', alphanum_key(f) if sort_by_name else '')
        sorted_files = sorted(files, key=file_sort_key)
    elif sort_by_ext:
        sorted_files = sorted(files, key=lambda f: (os.path.splitext(f)[1].lower(), alphanum_key(f)))
    elif sort_by_name:
        sorted_files = sorted(files, key=alphanum_key)
    else:
        sorted_files = files  

    return sorted_dirs, sorted_files

def print_tree(tree, indent=0, sort_by_name=True, sort_by_ext=True, group_by_type=False, label_files=False):
    dirs = tree["__dirs__"].keys()
    files = tree["__files__"]

    sorted_dirs, sorted_files = sort_items(files, dirs, sort_by_name, sort_by_ext, group_by_type)

    for d in sorted_dirs:
        print(" " * indent + d)
        print_tree(tree["__dirs__"][d], indent + 2, sort_by_name, sort_by_ext, group_by_type, label_files)

    for f in sorted_files:
        label = f" {get_file_label(f)}" if label_files else ""
        print(" " * indent + f + label)

def tree_to_dict(tree, sort_by_name=True, sort_by_ext=True, group_by_type=False, label_files=False):
    dirs = tree["__dirs__"].keys()
    files = tree["__files__"]

    sorted_dirs, sorted_files = sort_items(files, dirs, sort_by_name, sort_by_ext, group_by_type)

    result = {}
    for d in sorted_dirs:
        result[d] = tree_to_dict(tree["__dirs__"][d], sort_by_name, sort_by_ext, group_by_type, label_files)

    if label_files:
        labeled_files = [f + " " + get_file_label(f) for f in sorted_files]
        result["__files__"] = labeled_files
    else:
        result["__files__"] = sorted_files

    return result

def read_static_list():
    print("Please enter the list (including brackets), e.g.:")
    print('[')
    print('"images/2020/photo2.jpg",')
    print('"docs/readme.TXT",')
    print('"scripts/test1.py"')
    print(']')
    print("End input by typing a line containing only ]")

    lines = []
    while True:
        line = input()
        lines.append(line)
        if line.strip() == ']':
            break
    input_str = '\n'.join(lines)

    try:
        file_list = ast.literal_eval(input_str)
        if isinstance(file_list, list) and all(isinstance(i, str) for i in file_list):
            return file_list
        else:
            print("Input is not a valid list of strings.")
            return None
    except Exception as e:
        return None

def convert_to_static_list(folder_path):
    file_list = []
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, folder_path)
            unix_style_path = rel_path.replace(os.sep, "/")
            file_list.append(unix_style_path)
    return sorted(file_list)

def main():
    while True:
        parser = argparse.ArgumentParser(description="Intelligent File System Indexer")
        parser.add_argument('--json', action='store_true', help="Output the result as JSON")
        parser.add_argument('--sort-by-name', action='store_true', default=True, help="Sort items by name (default)")
        parser.add_argument('--sort-by-extension', action='store_true', help="Sort files by extension")
        parser.add_argument('--group-by-type', action='store_true', help="Group files by detected file type")
        parser.add_argument('--label-files', action='store_true', help="Label files with type tags like [IMG], [DOC], [PY]")

        args = parser.parse_args()

        print("Welcome to the Intelligent File System Indexer. Please choose an input method:")
        print("1 - Static list")
        print("2 - Real folder")
        print("3 - Exit")
        choice = input("--> ").strip()

        if choice == '1':
            static_list = read_static_list()
            if static_list is None:
                print("Invalid static list input.",end="\n")
                continue
            paths = static_list

        elif choice == '2':
            folder_path = input("Enter the folder path:\n--> ").strip()
            if not os.path.isdir(folder_path):
                print("Invalid folder path.")
                continue
            paths = convert_to_static_list(folder_path)

        else:
            print("Please enter a valid choice number (1, 2, or 3)")
            continue 

        tree = generate_tree(paths)

        if args.json:
            output = tree_to_dict(tree, args.sort_by_name, args.sort_by_extension, args.group_by_type, args.label_files)
            print(json.dumps(output, indent=2))
        else:
            print("Directory Tree:")
            print_tree(tree, indent=0, sort_by_name=args.sort_by_name, sort_by_ext=args.sort_by_extension,
                       group_by_type=args.group_by_type, label_files=args.label_files)
        print("")

if __name__ == "__main__":
    main()
