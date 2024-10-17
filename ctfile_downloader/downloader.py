import requests
from .utils import get_credentials
from .dlmanager import download_file
import logging

# Global session object for making HTTP requests
session = requests.Session()


def get_file_data(url, passcode, username, password):
    """Retrieves file data from CTFile."""
    uid_fid = url.split("/")[-1].split("?")[0]
    payload = {
        "ref": url,
        "action": "login",
        "task": "login",
        "email": username,
        "password": password,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.ctfile.com",
        "Referer": f"https://www.ctfile.com/p/login?ref={url}",
    }

    # Login request
    session.post(
        f"https://www.ctfile.com/p/login?ref={url}", data=payload, headers=headers
    )

    # Get file details
    web_api = (
        f"https://webapi.ctfile.com/getfile.php?path=f&f={uid_fid}&passcode={passcode}"
    )
    response = session.post(web_api)

    return response.json().get("file")


def process_links(url_list, config):
    """Processes direct CTFile links."""
    username, password = get_credentials(config)
    headers = config["headers"]

    # Update session headers
    session.headers.update(headers)

    while url_list:
        url = url_list.pop(0).strip()
        logging.info(f"Processing CTFile link: {url}")

        passcodes = config.get("passcodes", [])
        file_downloaded = False
        for passcode in passcodes:
            if not file_downloaded:
                file_data = get_file_data(url, passcode, username, password)
                if (
                    file_data
                    and file_data.get("vip_dx_url")
                    and file_data.get("vip_lt_url")
                ):
                    file_name = file_data.get("file_name")
                    telecom_mirror = file_data.get("vip_dx_url")
                    unicom_mirror = file_data.get("vip_lt_url")

                    logging.info(f"File Name: {file_name}")
                    logging.info(f"Telecom Mirror: {telecom_mirror}")
                    logging.info(f"Unicom Mirror: {unicom_mirror}")

                    try:
                        download_file(
                            unicom_mirror, file_name, config["download_folder"]
                        )
                        file_downloaded = True
                    except Exception as e:
                        logging.error(f"Error downloading from Unicom Mirror: {e}")
                        download_file(
                            telecom_mirror, file_name, config["download_folder"]
                        )
                        file_downloaded = True
                else:
                    logging.warning(
                        "Direct Download Link Not Found or Invalid Passcode"
                    )
                    break
