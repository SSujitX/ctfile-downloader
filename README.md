# CTFile Downloader

CTFileDownloader is a Python package that allows users to download files from CTFile using URLs or batch processing. It is designed for efficient file downloading, handling both individual and batch URL inputs. If you find it useful, please consider starring the repository on GitHub to support the project!

## Changelog

- Version 0.1.0:
  - Initial release: Basic functionality to download files from CTFile.
  - Batch processing of text files containing multiple URLs.
  - Error handling for invalid URLs.
  - Support for multiple download mirrors (Telecom and Unicom).

# You will need a premium account on `ctfile.com` to use this tool. Please log in to your account at [ctfile.com](https://www.ctfile.com/p/login).

## Demo

![CTFileDownloader Demo]()

## Environment Setup

### For Windows:

1. Make sure you have Python 3.9+ installed. You can download it from [here](https://www.python.org/downloads/).
2. Optionally, create and activate a virtual environment for isolation:

```sh
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

### For Mac/Linux:

1. Ensure that Python 3.9+ is installed. You can check your version or install it using Homebrew:

```sh
# Check if Python 3.9+ is installed
python3 --version

# If not installed, use Homebrew to install Python
brew install python3
```

2. Optionally, create and activate a virtual environment for isolation:

```sh
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

## Usage

You can use CTFileDownloader in two ways, using a standalone CLI executable file or as a git repository.

### Using ctfiledownloader.py as git repositor

```sh
git clone https://github.com/SSujitX/ctfiledownloader.git
```

Clone the ctfiledownloader repository to your local machine.

Install the dependencies with `pip install -r requirements.txt`

```sh
pip install -r requirements.txt
```

```python
python ctfiledownloader.py
```

### Using CTFile Downloader v1.0.0 standalone executable file (windows cli only)

Run the `CTFile Downloader v1.0.0` standalone executable file (windows cli only).

You must need a premium account of [ctfile.com](https://www.ctfile.com/p/login)

## Disclaimer

CTFileDownloader is not for sale or for distribution. It is a tool to help users download files from CTFile using their own login credentials. You must use your own username and password for access.

The developer is not responsible for any misuse of this tool. Please ensure you comply with CTFile's terms of service when using the downloader.
