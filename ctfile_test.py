from urllib.parse import urlparse, parse_qs
import cloudscraper
from rich import print


# URL = "https://url62.ctfile.com/f/680462-17569800872413-e51bf9?p=6688"

WEBAPI_GETFILE = "https://webapi.ctfile.com/getfile.php"
VALIDATE_URL = "https://rest.ctfile.com/v1/browser/file/validate"
DOWNLOAD_URL = "https://rest.ctfile.com/v1/browser/file/download"
SAVE_URL = "https://rest.ctfile.com/v1/browser/file/save"
LIST_FILES = "https://rest.ctfile.com/v1/browser/file/list"
USER_LIST_FILES = "https://rest.ctfile.com/v1/public/file/list"
FETCH_URL = "https://rest.ctfile.com/v1/public/file/fetch_url"
FILE_META = "https://rest.ctfile.com/v1/public/file/meta"
SESSION_TOKEN = ""

scraper = cloudscraper.create_scraper()

def get_xtlink(url):
    # xtlink = "xtc680462-f17569802098418-88034b-6688"

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    query_params = parse_qs(parsed_url.query)
    passcode = query_params.get('p', [''])[0]
    params = {
        "path": path_parts[0],
        path_parts[0] : path_parts[1],
        "passcode": passcode,
    }

    response = scraper.get(
        WEBAPI_GETFILE,
        params=params,
    )
    data = response.json()

    if data.get("code") != 200:
        return {
            "status": False,
            "message": "CTFile WebAPI GetFile Failed",
            "data": data
        }

    return {
        "status": True,
        "message": "CTFile WebAPI GetFile Successfully",
        "data": {
            "xtlink": data["file"]["xtredirect"],
            "file_id": data["file"]["file_id"],
        }
    }

def validate(xtlink):
    xtlink_resp = get_xtlink(URL)
    if not xtlink_resp.get("status"):
        return xtlink_resp
    
    xtlink = xtlink_resp.get("data")
    
    payload = {
        "xtlink": xtlink.get("xtlink"),
        "session": SESSION_TOKEN,
    }
    response = scraper.post(VALIDATE_URL, json=payload)
    data = response.json()
    if data.get("code") != 200:
        return {
            "status": False,
            "message": "CTFile Validate Failed",
            "data": data
        }
    return {
        "status": True,
        "message": "CTFile Validate Successfully",
        "data": data
        }

def get_url_info(url):
    """
    Parse share URL into fields for browser/file/save API.

    URL: https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688
    ids format: "f17569802098418" (one file) or "f123,d456" (comma-separated)
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    query_params = parse_qs(parsed_url.query)
    passcode = query_params.get("p", [""])[0]

    resource_type = path_parts[0] if path_parts else "f"
    uid_fid = path_parts[1] if len(path_parts) > 1 else path_parts[0]
    parts = uid_fid.split("-")

    # uid-fid-checksum -> middle segment is numeric file_id
    file_id = parts[1] if len(parts) > 1 else parts[0]
    file_key = f"f{file_id}"

    return {
        "type": resource_type,
        "uid_fid": uid_fid,
        "password": passcode,
        "file_id": file_id,
        "file_key": file_key,
        "ids": file_key,
    }

def list_files(xtlink):
    payload = {
        "xtlink": xtlink,
        "session": SESSION_TOKEN,
        
    }
    response = scraper.post(LIST_FILES, json=payload)
    data = response.json()
    if data.get("code") != 200:
        return {
            "status": False,
            "message": "CTFile List Files Failed",
            "data": data
        }
    file_ids = []
    results = data.get("results")
    for result in results:
        if result.get("key"):
            file_id = result.get("key")
            file_ids.append(file_id)
            
    if not file_ids:
        return {
            "status": False,
            "message": "CTFile List Files Failed",
            "data": data
        }
    return {
        "status": True,
        "message": "CTFile List Files Successfully",
        "data": {
            "file_ids": file_ids,
            "folder_id": data.get("folder_id"),
            "folder_path": data.get("folder_path"),
        }
    }

def save_files(xtlink, file_ids):
    payload = {
        "xtlink": xtlink,
        "ids": file_ids,
        "session": SESSION_TOKEN,
    }
    response = scraper.post(SAVE_URL, json=payload)
    data = response.json()
    if data.get("code") != 200:
        return {
            "status": False,
            "message": "CTFile Save Files Failed",
            "data": data
        }
    return {
        "status": True,
        "message": "CTFile Save Files Successfully",
        "data": data
    }

def user_list_files():
    payload = {
        "session": SESSION_TOKEN,
    }
    response = scraper.post(USER_LIST_FILES, json=payload)
    data = response.json()
    if data.get("code") != 200:
        return {
            "status": False,
            "message": "CTFile User List Files Failed",
            "data": data
        }
    files = []
    results = data.get("results")
    for result in results:
        if result.get("key"):
            file_id = result.get("key")
            weblink = result.get("weblink")
            files.append({
                "file_id": file_id,
                "weblink": weblink,
                "default_passcode": data.get("default_passcode"),
            })
            

    return {
        "status": True,
        "message": "CTFile User List Files Successfully",
        "data": {
            "files": files,
            "folder_id": data.get("folder_id"),
        }
    }

def download():
    payload = {
        "file_id": 17569802098418,
        "session": SESSION_TOKEN,
    }
    
    response = scraper.post(DOWNLOAD_URL, json=payload)
    data = response.json()
    
    print(data)

if __name__ == "__main__":
    URL = "https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688"
    xtlink_resp = get_xtlink(URL)
    xtlink_data = xtlink_resp.get("data")
    print(xtlink_data)
    
    xtlink = xtlink_data.get("xtlink")
    file_id = xtlink_data.get("file_id")
    
    # list_files_resp = list_files(xtlink)
    # list_files_data = list_files_resp.get("data")
    # file_ids = list_files_data.get("file_ids")

    
    # save_files_resp = save_files(xtlink, file_ids)
    # save_files_data = save_files_resp.get("data")
    
    # user_list_files_resp = user_list_files()
    # print(user_list_files_resp)
    
    download_resp = download()
    print(download_resp)
    # info = get_url_info(URL)
    # print(info)
