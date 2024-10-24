![](https://api.visitorbadge.io/api/VisitorHit?user=SSujitX&repo=ctfile-downloader&countColor=%237B1E7A)

# CTFile Downloader

CTFileDownloader is a Python package that allows users to download files from CTFile using URLs or batch processing. It is designed for efficient file downloading, handling both individual and batch URL inputs. If you find it useful, please consider starring the repository on GitHub to support the project!

## Changelog

- Version 0.1.0:
  - Initial release: Basic functionality to download files from CTFile.
  - Batch processing of text files containing multiple URLs.
  - Error handling for invalid URLs.
  - Support for multiple download mirrors (Telecom and Unicom).

# You will need a premium account on `ctfile.com` to use this tool. Please log in to your account at [ctfile.com](https://www.ctfile.com/p/login) & set your password and username in the `config.yml` file.

## Usage

You can use CTFileDownloader in two ways, using a standalone CLI executable file or as a git repository.

When you run either the `ctfiledownloader.py` script or the standalone `CTFile Downloader v1.0.0.exe`, the following steps will be executed:

1. **Initial Configuration**:
   - If this is your first time running the tool and no configuration file (`config.yml`) is found, you will be prompted to enter your CTFile **username** and **password**. This information is required for logging into your CTFile account, which must be a premium account. The credentials will be saved in a configuration file, so you won’t have to enter them again for future use.
2. **Single Link Download**:
   - After the configuration is complete, you can input a CTFile URL manually. The tool will start downloading the file associated with the provided link.
3. **Batch Processing**:

   - If you want to process multiple links at once, you can create a text file inside the `CTFile Batch Text` folder.
   - Each line of the text file should contain a valid CTFile URL, such as:

     ```
     https://url70.ctfile.com/f/2827370-1385012509-835ddf?p=4431
     https://url70.ctfile.com/f/2827370-1385012510-abcd123?p=6688
     ```

   - When you run the tool and press **Enter** without entering any URL, it will automatically check for text files in the `CTFile Batch Text` folder. If any text files are found, the tool will process the links in those files one by one and download the corresponding files from CTFile.


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


### Key Points:

- Ensure that your `CTFile Batch Text` folder contains `.txt` files, with each CTFile URL on a new line.
- You must have a premium CTFile account for this tool to function correctly. You can log in to your account at [ctfile.com](https://www.ctfile.com/p/login).
- The tool supports both single and batch file downloads seamlessly.

---

### Using ctfiledownloader.py as git repositor

```sh
git clone https://github.com/SSujitX/ctfile-downloader.git
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
