import unittest
from indexer import (
    generate_tree, get_file_label, alphanum_key, tree_to_dict
)

class TestIndexer(unittest.TestCase):

    def test_get_file_label(self):
        self.assertEqual(get_file_label("photo.jpg"), "[IMG]")
        self.assertEqual(get_file_label("document.pdf"), "[DOC]")
        self.assertEqual(get_file_label("script.py"), "[PY]")
        self.assertEqual(get_file_label("unknown.xyz"), "") 

    def test_alphanum_sorting(self):
        items = ["file10.txt", "file2.txt", "file1.txt"]
        sorted_items = sorted(items, key=alphanum_key)
        self.assertEqual(sorted_items, ["file1.txt", "file2.txt", "file10.txt"])

    def test_generate_tree_structure(self):
        paths = [
            "images/photo.jpg",
            "docs/readme.txt",
            "scripts/test.py"
        ]
        tree = generate_tree(paths)
        self.assertIn("images", tree["__dirs__"])
        self.assertIn("photo.jpg", tree["__dirs__"]["images"]["__files__"])

    def test_tree_to_dict_with_labels(self):
        paths = ["docs/readme.txt", "scripts/main.py"]
        tree = generate_tree(paths)
        output = tree_to_dict(tree, label_files=True)
        self.assertIn("readme.txt [DOC]", output["docs"]["__files__"])
        self.assertIn("main.py [PY]", output["scripts"]["__files__"])

if __name__ == '__main__':
    unittest.main()
