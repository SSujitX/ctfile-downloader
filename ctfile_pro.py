# CTFile Downloader Pro
# Version: 0.0.1
# Author: Sujit Biswas
# Date: 2026-06-06
# Description: CTFile Downloader Pro is a tool that allows you to download files from CTFile.

# Usages:
# You need a premium account on ctfile.com to get faster vip speed downloads.
# You need a folder in root called "_ctfiledata".
# Inside "_ctfiledata" you need to create two files: "creds.json" and "cookies.json".

# "creds.json" should have the following structure:

# {
#     "email": "your_email@example.com",
#     "password": "your_password"
# }

# "cookies.json" should have the following structure:
# use extension in chrome https://chromewebstore.google.com/detail/cookie-selector/klmnplbabblfkhlganacalkafdbhchne
# Example cookies from ctfile after login:

# {
#     "ua_checkmutilogin": "",
#     "ctfile_session_pref": "",
#     "ctfile_session": "",
#     "ct_uid": ""
# }

import time
from urllib.parse import urlparse, parse_qs
import cloudscraper
from rich import print
import json
import os
import sys
from tqdm import tqdm
import re

class CTFileDownloader:
    """ CTFile Downloader Pro is a tool that allows you to download files from CTFile. """
    
    def __init__(self):
        """ Initialize the CTFile Downloader Pro """
        
        root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(root_path)
        
        self.ctfile_data_folder = os.path.join(root_path, "_ctfiledata")
        os.makedirs(self.ctfile_data_folder, exist_ok=True)
        
        self.batch_folder = os.path.join(root_path, "CTFile Batch Text")
        os.makedirs(self.batch_folder, exist_ok=True)
        
        self.download_folder = os.path.join(root_path, "CTFile Downloaded")
        os.makedirs(self.download_folder, exist_ok=True)
        
        self.scraper = cloudscraper.create_scraper()

        self.BASE_URL = "https://www.ctfile.com"
        self.WEBAPI_GETFILE = "https://webapi.ctfile.com/getfile.php"
        self.CTFILE_LOGIN = 'https://rest.ctfile.com/p8/public/login/login'
        self.REF_PATH = 'https://home.ctfile.com/#item-files/action-index'
    
        
    def _load_credentials_and_cookies(self) -> dict:
            
        """Load credentials and cookies from creds.json and cookies.json file
        
        Returns:
            {status: True/False, message: str, 
            data: { credentials: dict, cookies: dict },
            cookies: dict - cookies for the CTFILE session
            credentials: dict - credentials for the CTFILE session
            }
        """
        
        self.cookies_path = os.path.join(self.ctfile_data_folder, "cookies.json")
        self.credentials_path = os.path.join(self.ctfile_data_folder, "creds.json")
        
        if not os.path.exists(self.cookies_path) or not os.path.exists(self.credentials_path):
            return {
                "status": False,
                "message": "CTFILE: Credentials or Cookies file not found.",
                "data": None
            }
        
        with open(self.cookies_path, "r") as f:
            cookies = json.load(f)
        
        with open(self.credentials_path, "r") as f:
            credentials = json.load(f)
        
        return {
            "status": True,
            "message": "CTFILE: Credentials and Cookies loaded successfully.",
            "data": {
                "credentials": credentials,
                "cookies": cookies
            }
        }
    
    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Return True if input looks like a CTFile or web SOURCE URL."""
        url = url.strip()
        if not url:
            return False
        lower = url.lower()
        if "ctfile.com" in lower:
            return True
        return lower.startswith("http://") or lower.startswith("https://")

    def _get_batch_links(self):
        """Get batch links from batch folder."""
        if not os.path.isdir(self.batch_folder):
            return [], None

        text_files = [
            name for name in os.listdir(self.batch_folder)
            if os.path.isfile(os.path.join(self.batch_folder, name))
        ]
        if not text_files:
            return [], None
        
        url_list = []
        text_file_path = None
        for text_file in text_files:
            text_file_path = os.path.join(self.batch_folder, text_file)
            with open(text_file_path, "r", encoding="utf-8") as file:
                url_list.extend(file.read().splitlines())
                
        return url_list, text_file_path
    
    def get_url_info(self, url: str) -> dict:
        """
        Parse a ctfile share URL.
        Args:
            url: str - CTFile URL https://url70.ctfile.com/f/2827370-8774219194-843030?p=4431
        Returns:
            {status: True/False, message: str, data: { type: str, uid_fid: str, password: str } }
        """
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        parts = path.split("/")

        resource_type = parts[0] if parts else "f"
        uid_fid = parts[1] if len(parts) > 1 else parts[0]

        query_params = parse_qs(parsed.query)
        password = query_params.get("p", [None])[0]
        
        if not all([resource_type, uid_fid, password]):
            return {
                "status": False,
                "message": "CTFile URL Info Retrieval Failed",
                "data": None
            }

        return {
            "status": True,
            "message": "CTFile URL Info Retrieved Successfully",
            "data": {
                "type": resource_type,
                "uid_fid": uid_fid,
                "password": password,
            }
        }
    
    def _get_xtlink(self, url: str) -> str:
        
        """Get xtlink from CTFile URL
        Args:
            url: str - CTFile URL
        Returns:
            {status: True/False, message: str, data: str }
            data: str - xtlink
            
        """
        # xtlink = "xtc680462-f17569802098418-88034b-6688"

        url_info = self.get_url_info(url)
        if not url_info.get("status"):
            return url_info
        
        info: dict = url_info.get("data")
        
        params = {
            "path": info["type"],
            info["type"] : info["uid_fid"],
            "passcode": info["password"],
        }

        response = self.scraper.get(
            self.WEBAPI_GETFILE,
            params=params,
        )
        
        data = response.json()

        if data.get("code") != 200:
            return None

        return data["file"]["xtredirect"]

    def webapi_login(self, email: str, password: str) -> dict:
        """Login to CTFile API
        Args:
            url: str - CTFile URL
        Returns:
            {status: True/False, message: str, data: { session_token: str } }
        """
        
        login_payload = {
            'email': email,
            'password': password,
            'ref': self.REF_PATH,
        }
        
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': self.BASE_URL,
        'referer': self.BASE_URL,

        }
        
        login_resp = self.scraper.post(self.CTFILE_LOGIN, json=login_payload, headers=headers)
        login_json: dict = login_resp.json()

        if login_json.get("code") != 200:
            return {
                "status": False,
                "message": "CTFile Login Failed",
                "data": login_json
            }
        return {
            "status": True,
            "message": "CTFile Login Successfully",
            "data": login_json,
            
            "cookie": login_resp.cookies,
        }
    
    def webapi_getfile(self, type: str, uid_fid: str, password: str) -> dict:
        """Get file info from CTFile API
        Args:
            type: str - CTFile type (f, d, etc.)
            uid_fid: str - CTFile UID and FID
            password: str - CTFile password
        Returns:
            {status: True/False, message: str, 
            data: { file_name: str, file_size: str, vip_dx_url: str, vip_lt_url: str, vip_yd_url: str, us_downurl_a: str, vip_cdn_url: str } }
        """
        
        webapi_getfile_params = {
            "path": type,
            type: uid_fid,
            "passcode": password,
        }

        webapi_getfile_resp = self.scraper.get(self.WEBAPI_GETFILE, 
                              params=webapi_getfile_params,
                              cookies=self.scraper_cookies)
        
        webapi_getfile_json: dict = webapi_getfile_resp.json()
        if webapi_getfile_json.get("code") != 200:
            return {
                "status": False,
                "message": "CTFile WebAPI GetFile Failed",
                "data": webapi_getfile_json
            }

        file: dict = webapi_getfile_json.get("file") or {}
        file_name = file.get("file_name")
        file_size = file.get("file_size")
        vip_dx_url = file.get("vip_dx_url")
        vip_lt_url = file.get("vip_lt_url")
        vip_yd_url = file.get("vip_yd_url")
        us_downurl_a = file.get("us_downurl_a")
        vip_cdn_url = file.get("vip_cdn_url")
        
        return {
            "status": True,
            "message": "CTFile WebAPI GetFile Successfully",
            "data": {
                "file_name": file_name,
                "file_size": file_size,
                "vip_dx_url": vip_dx_url,
                "vip_lt_url": vip_lt_url,
                "vip_yd_url": vip_yd_url,
                "us_downurl_a": us_downurl_a,
                "vip_cdn_url": vip_cdn_url,
            }
        }
    
    def download_file(self, download_url: str, filename: str,) -> dict:
        """Download file from CTFile URL
        Args:
            download_url: str - CTFile Download URL
            filename: str - Filename to save the file
        Returns:
            True if download successful, False otherwise
        """

        if not download_url:
            return {
                "status": False,
                "message": "CTFILE: Download URL not found.",
                "data": None
            }

        resp = self.scraper.get(download_url, stream=True)
        if resp.status_code != 200:
            return {
                "status": False,
                "message": f"CTFILE: Download URL failed with status {resp.status_code}.",
                "data": download_url
            }

        file_path = os.path.join(self.download_folder, filename)
        total = int(resp.headers.get('content-length', 0))
        
        with open(file_path, 'wb') as file, tqdm(
            desc = filename,
            total = total,
            unit = 'iB',
            unit_scale = True,
            unit_divisor = 1024,
        
        )  as bar:  
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        print(f"\n>>-- Download {filename} Successfully <<--\n")
        return True

    def fetch_ctfile_links(self, source_url: str) -> list:
        """Fetch CTFile links from a URL
        Args:
            source_url: str - SOURCE URL to fetch CTFile links from
        Returns:
            list of CTFile links
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
            }
            req = self.scraper.get(source_url, headers=headers)

            pattern = r'https?://(?:url\d+\.)?ctfile\.com/[^\s"\'<>)\]]+'
            found = re.findall(pattern, req.text)

            links = []
            seen = set()
            for link in found:
                link = link.rstrip('.,;)\'"')
                if link not in seen:
                    seen.add(link)
                    links.append(link)

            if not links:
                return False

            return links

        except Exception:
            return False
        
    def ctfile_downloader(self, source_url_or_ctfile_url: str) -> dict:
        """Download file from SOURCE URL or CTFile URL
        Args:
            source_url_or_ctfile_url: str - SOURCE URL or CTFile URL to download file from
        Returns:
            {status: True/False, message: str, data: { file_name: str, file_size: str, file_url: str } }
        """
        # ---------------------------------------
        creds_and_cookies = self._load_credentials_and_cookies()
        
        if not creds_and_cookies.get("status"):
            return creds_and_cookies
        
        credentials: dict = creds_and_cookies.get("data").get("credentials")
        cookies: dict = creds_and_cookies.get("data").get("cookies")
        
        email: str = credentials.get("email")
        email_password: str = credentials.get("password")
        
        self.scraper_cookies = cookies
        
        print(f'>>-- CTFILE: Credentials and Cookies loaded successfully')
        # ---------------------------------------
        
        
        url = source_url_or_ctfile_url.strip()

        if "ctfile.com" in url.lower():
            ctfile_links = [url]
        else:
            ctfile_links = self.fetch_ctfile_links(url)
            if not ctfile_links:
                return {
                    "status": False,
                    "message": "CTFile links not found in SOURCE URL",
                    "data": None
                }

        print(f'>>-- CTFILE: CTFile links ready ({len(ctfile_links)})')
        
        for ctfile_link in ctfile_links:
            
            print(f'>>-- CTFILE: Fetching URL - {ctfile_link}')
            
            url_info = self.get_url_info(ctfile_link)
            if not url_info.get("status"):
                return url_info
            
            print(f'>>-- CTFILE: File info retrieved successfully from CTFile API')
            
            info: dict = url_info.get("data")
            type = info.get("type")
            uid_fid = info.get("uid_fid")
            password = info.get("password")
            
            # login is not working beacause it ask qr scan sometimes
            
            # login_resp = self.webapi_login(email, password)
            # if not login_resp.get("status"):
            #     return login_resp
            
            webapi_getfile_resp = None
            for attempt in range(1, 11):
                webapi_getfile_resp = self.webapi_getfile(type, uid_fid, password)
                if webapi_getfile_resp.get("status"):
                    break

                print(f'>>-- CTFILE: WebAPI getfile failed, retrying ({attempt}/10)')
                time.sleep(1)

            if not webapi_getfile_resp.get("status"):
                return webapi_getfile_resp
            
            print(f'>>-- CTFILE: WebAPI getfile retrieved successfully\n')
            
            webapi_getfile_data: dict = webapi_getfile_resp.get("data")
            
            file_name: str = webapi_getfile_data.get("file_name")
            file_size: str = webapi_getfile_data.get("file_size")
            
            vip_dx_url: str = webapi_getfile_data.get("vip_dx_url")
            vip_lt_url: str = webapi_getfile_data.get("vip_lt_url")
            vip_yd_url: str = webapi_getfile_data.get("vip_yd_url")
            us_downurl_a: str = webapi_getfile_data.get("us_downurl_a")
            vip_cdn_url: str = webapi_getfile_data.get("vip_cdn_url")

            download_urls: list[tuple[str, str]] = [
                ("vip_lt_url", vip_lt_url),
                ("vip_dx_url", vip_dx_url),
                ("vip_yd_url", vip_yd_url),
                ("us_downurl_a", us_downurl_a),
                ("vip_cdn_url", vip_cdn_url),
            ]

            last_error = None
            for url_name, download_url in download_urls:
                if not download_url:
                    continue

                print(f'>>-- CTFILE: Trying download URL: {url_name}')
                download_resp = self.download_file(download_url, file_name)
                if download_resp is True:
                    return {
                        "status": True,
                        "message": "CTFILE: Download successful",
                        "data": {
                            "file_name": file_name,
                            "file_size": file_size,
                            "download_url": download_url,
                        },
                    }

                last_error = download_resp
                print(f'>>-- CTFILE: {url_name} failed, trying next URL')

            return last_error or {
                "status": False,
                "message": "CTFILE: No download URL found.",
                "data": webapi_getfile_data
            }
        
    def ctfile_main(self):
        """Main function to download files from CTFile
        Returns:
            None
        """
        
        # write a text like CTFILE DOWNLOADER better design
        print(f"""
╔═════════════════════════════════════════════╗
║            CTFILE DOWNLOADER PRO            ║
╚═════════════════════════════════════════════╝
        """)
        
        
        while True:
            
            print(f' ----------------------------- Rules -----------------------------')
            print(f' ---- Enter SOURCE URL or CTFile URL with passcode ----')
            print(f' ---- Example CTFile: https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688')
            print(f' ---- Example SOURCE: https://www.lookae.com/warping-wheels-300/')
            print(f' ---- Press Enter to follow batch links (multiple source links)')
            print(f' ----------------------------- Rules -----------------------------\n')
            
            try:
                main_input = input(">>-- ENTER LINK: ").strip()
            except (EOFError, RuntimeError):
                print(">>-- CTFILE: No console input, using batch folder")
                main_input = ""
            
            print(f'\n--------------------------------------')
            print(f'>>-- CTFILE: Starting download process')
            
            
            if main_input:
                print(f'\n>>-- CTFILE: Getting links from input')
                
                raw_urls = [u.strip() for u in main_input.split(",") if u.strip()]
                invalid_urls = [u for u in raw_urls if not self._is_valid_url(u)]
                if invalid_urls:
                    print(f'>>-- CTFILE: Invalid link(s): {", ".join(invalid_urls)}')
                    print(f'>>-- CTFILE: Enter a SOURCE/CTFile URL, or press Enter for batch mode')
                    print(f'--------------------------------------\n')
                    continue

                url_list = raw_urls
                if not url_list:
                    print(f'>>-- CTFILE: No link entered')
                    print(f'>>-- CTFILE: Enter a SOURCE/CTFile URL, or press Enter for batch mode')
                    print(f'--------------------------------------\n')
                    continue
                
            else:
                print(f'\n>>-- CTFILE: Getting batch links from batch folder')
                
                url_list, text_file_path = self._get_batch_links()
                url_list = [u.strip() for u in url_list if u and u.strip()]
                if not url_list:
                    print(f'>>-- CTFILE: Batch folder is empty — add .txt files to "CTFile Batch Text/"')
                    print(f'>>-- CTFILE: Or enter a SOURCE/CTFile URL instead')
                    print(f'--------------------------------------\n')
                    continue

            print(f'>>-- CTFILE: Total links to download: {len(url_list)}\n')

            failed_downloads = []
            
            for index, url in enumerate(url_list):
                
                if not url:
                    continue
                
                print(f'>>-- CTFILE: Downloading file from {url}')
                
                result = self.ctfile_downloader(url)
                if not result.get("status"):
                    failed_downloads.append({
                        "url": url,
                        "result": result,
                    })

                    message = result.get("message") if isinstance(result, dict) else result
                    print(f'>>-- CTFILE: Download failed for {url}')
                    print(f'>>-- CTFILE: Reason: {message}\n')
                
            if failed_downloads:
                print(f'>>-- CTFILE: Downloading process completed with {len(failed_downloads)} failed link(s)')
            else:
                print(f'>>-- CTFILE: Downloading process completed successfully')
            print(f'--------------------------------------\n')


if __name__ == "__main__":
    ctfile_downloader = CTFileDownloader()
    ctfile_downloader.ctfile_main()