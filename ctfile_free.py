# CTFile Downloader Free
# Version: 0.0.1
# Author: Sujit Biswas
# Date: 2026-06-06
# Description: CTFile Downloader Free is a tool that allows you to download files from CTFile.

# Usages:
# You need a public share URL from ctfile.com to download files.
# Example CTFile: https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688
# Example SOURCE: https://www.lookae.com/warping-wheels-300/

import os
import random
import re
import sys
import time
from rich import print
import cloudscraper
from urllib.parse import parse_qs, urlparse

from tqdm import tqdm


class FreeCTFileDownloader:
    """Free CTFile public share downloader."""
    
    def __init__(self):
        """Initialize the FreeCTFileDownloader."""
        
        root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(root_path)
        
        self.batch_folder = os.path.join(root_path, "CTFile Batch Text")
        os.makedirs(self.batch_folder, exist_ok=True)
        
        self.download_folder = os.path.join(root_path, "CTFile Downloaded")
        os.makedirs(self.download_folder, exist_ok=True)
        
        self.scraper = cloudscraper.create_scraper()
        
        self.BASE_URL = "https://www.ctfile.com"
        self.WEB_API_BASE = "https://webapi.ctfile.com"
        self.WEBAPI_GETFILE = "https://webapi.ctfile.com/getfile.php"
        self.WEBAPI_GET_DOWN_URL = "https://webapi.ctfile.com/get_down_url.php"

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
        """Get batch links from CTFile Batch Text folder."""
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

    @staticmethod
    def _ok(data=None, message: str = "OK") -> dict:
        """Build a success response."""
        return {"status": True, "message": message, "data": data}

    @staticmethod
    def _fail(message: str, data=None) -> dict:
        """Build a failure response."""
        return {"status": False, "message": message, "data": data}

    @staticmethod
    def _api_message(payload: dict, fallback: str) -> str:
        """Pull a human-readable message from a CTFile JSON body."""
        if not isinstance(payload, dict):
            return fallback
        for key in ("msg", "message", "error", "info"):
            if payload.get(key):
                return str(payload[key])
        res = payload.get("res")
        if isinstance(res, str):
            return res
        if isinstance(res, dict):
            for v in res.values():
                if v:
                    return str(v)
        return fallback

    @staticmethod
    def _parse_url(url: str) -> dict:
        """Parse share URL into type, uid_fid, and password."""
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        parts = path.split("/")

        resource_type = parts[0] if parts else "f"
        uid_fid = parts[1] if len(parts) > 1 else parts[0]
        password = parse_qs(parsed.query).get("p", [None])[0]

        return {
            "type": resource_type,
            "uid_fid": uid_fid,
            "password": password,
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

    def get_download_link(self, ctfile_link: str) -> dict:
        """Get direct download URL for a public share (getfile + get_down_url).
        Args:
            ctfile_link: str - CTFile public share URL
        Returns:
            {status: True/False, message: str, data: { download_url: str, file_name: str, file_size: str } }
        """
        try:
            info = self._parse_url(ctfile_link)
            passcode = info["password"] or ""

            file_info_params = {
                "path": info["type"],
                info["type"]: info["uid_fid"],
                "passcode": passcode,
            }
            file_info_resp = self.scraper.get(
                self.WEBAPI_GETFILE,
                params=file_info_params,
            )
            file_info_json = file_info_resp.json()
            if file_info_json.get("code") != 200:
                return self._fail(
                    self._api_message(file_info_json, "getfile failed"),
                    file_info_json,
                )

            file_data = file_info_json.get("file") or file_info_json
            userid = file_data.get("userid")
            file_id = file_data.get("file_id")
            file_chk = file_data.get("file_chk")

            if not all([userid, file_id, file_chk]):
                return self._fail(
                    f"missing fields: userid={userid}, file_id={file_id}, file_chk={file_chk}",
                    file_info_json,
                )
            get_down_url_params = {
                "uid": userid,
                "fid": file_id,
                "file_chk": file_chk,
                "start_time": file_data.get("start_time", int(time.time())),
                "wait_seconds": file_data.get("wait_seconds", 0),
                "rd": random.random(),
            }
            get_down_url_resp = self.scraper.get(
                self.WEBAPI_GET_DOWN_URL,
                params=get_down_url_params,
            )
            get_down_url_json = get_down_url_resp.json()
            if get_down_url_json.get("code") != 200:
                return self._fail(
                    self._api_message(get_down_url_json, "get_down_url failed"),
                    get_down_url_json,
                )

            return self._ok(
                {
                    "download_url": get_down_url_json.get("downurl"),
                    "file_name": get_down_url_json.get("file_name") or file_data.get("file_name"),
                    "file_size": get_down_url_json.get("file_size") or file_data.get("file_size"),
                }
            )

        except Exception as e:
            return self._fail(f"download_link error: {e}")

    def ctfile_downloader(self, source_url_or_ctfile_url: str) -> dict:
        """Download file from SOURCE URL or CTFile URL
        Args:
            source_url_or_ctfile_url: str - SOURCE URL or CTFile URL to download file from
        Returns:
            {status: True/False, message: str, data: { file_name: str, file_size: str, file_url: str } }
        """
        
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
            
            download_link_result = None
            for attempt in range(1, 5):
                download_link_result = self.get_download_link(ctfile_link)
                if download_link_result.get("status"):
                    break

                print(f'>>-- CTFILE: Get download link failed, retrying ({attempt}/4)')
                time.sleep(1)

            if not download_link_result.get("status"):
                return download_link_result
            
            print(f'>>-- CTFILE: Download link retrieved successfully')
            
            download_url = download_link_result.get("data").get("download_url")
            file_name = download_link_result.get("data").get("file_name")
            file_size = download_link_result.get("data").get("file_size")
            
            print(f'>>-- CTFILE: Trying download URL: {download_url}')
            download_resp = self.download_file(download_url, file_name)
            if download_resp is True:
                return {
                    "status": True,
                    "message": "CTFILE: Download successful",
                    "data": download_link_result.get("data"),
                }
            
            return download_resp if isinstance(download_resp, dict) else {
                "status": False,
                "message": "CTFILE: Download failed",
                "data": download_link_result.get("data"),
            }

    def ctfile_main(self):
        """Main function to download files from CTFile"""
        print(f"""
╔══════════════════════════════════════════════╗
║            CTFILE DOWNLOADER FREE            ║
╚══════════════════════════════════════════════╝
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
# ──────────────────────────────────────────────────
#  Test
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    client = FreeCTFileDownloader()
    client.ctfile_main()