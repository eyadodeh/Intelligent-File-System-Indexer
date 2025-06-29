#  Intelligent File System Indexer

A Python-based tool that reads a list of file paths or scans a real directory, then generates a well-structured, sorted, and indented file tree. Supports custom sorting, type labeling, and JSON export via command-line options.




## Installation

Follow these steps to install and run the Intelligent File System Indexer:


```bash
git clone hhttps://github.com/eyadodeh/Intelligent-File-System-Indexer.git
cd intelligent-file-system-indexer
python indexer.py
```

## Command-Line Options

```python
Option	                Description
--json	                Output the directory tree as a JSON object
--sort-by-name	        Sort items by name (default is enabled)
--sort-by-extension	    Sort files by extension
--group-by-type	        Group files by type (e.g., [IMG], [DOC], [PY])
--label-files	        Add labels like [IMG] next to filenames in output
```

## Examples
Simple Case (deafult)
```python
python indexer.py 
```
Json Output
```python
python indexer.py --json 
```
Group Files by type (e.g., [IMG], [DOC], [PY])
```python
python indexer.py ---group-by-type
```

## License

Eyad Odeh 
