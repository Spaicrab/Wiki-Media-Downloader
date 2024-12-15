# Wiki-Media-Downloader

Script for the automatic download of media files from any Wiki's MIME search page.<br>
Intended to be used for archival purposes.

## Requirements and Installation

- Python >= 3.8
- [Requests Module](https://pypi.org/project/requests/)

Install Python if you haven't already from the [Official Site](https://www.python.org/downloads/).<br>
To install the Requests Module, open a powershell window and run ``python -m pip install requests`` (this requires Python to be already installed).

Download the script from the [Latest Release](https://github.com/Spaicrab/Wiki-Media-Downloader/releases/latest).

## Usage

This script can be run by itself or from the command line.<br>
If you're unsure on what to do, right click the ``wiki-media-downloader.py`` file and open it with Python, it will take you from there.

### Command Line Syntax (For Advanced Users)

```
wiki-media-downloader <WIKI_URL> <MIME_TYPE> [-h (--help)] [-d (--output-directory) <OUTPUT_DIRECTORY>] [-o (--offset) <OFFSET>] [-a (--amount) <AMOUNT>] [-v (--verbose)]
```

``<WIKI_URL>`` Wiki domain - e.g. 'simple.wikipedia.org'

``<MIME_TYPE>`` MIME type - e.g. 'image/png'

``[-d (--output-directory) <OUTPUT_DIRECTORY>]`` Output directory - default: new directory named after the wiki domain

``[-o (--offset) <OFFSET>]`` Start offset - default: 0

``[-a (--amount) <AMOUNT>]`` Amount of files to download - default: 100

``[-v (--verbose)]`` Print detailed information - default: disabled