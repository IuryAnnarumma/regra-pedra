import requests
import xml.etree.ElementTree as ET

# Info

Panorama = '10.4.193.20'
api_key = 'LUFRPT1tSFV5UFAyZEtYakNIeGVhSDBxNjAwYVkyWlU9S0xOQXFLejFTTTFuT2xTMFFqczdRRERmcWhlRlUzcTF3dU1EUXYwU1k1dklXdWRtUm9RdEpaQ1o3VHBnTUpwUQ=='

# API para comunicacao com o firewall/panorama
url = f'https://{10.4.193.20}/api/?type=config&action=get&xpath=/config/predefined/application'


def get_keygen(ip, user, passwd, device) -> dict:

    headers = { 'X-PAN-KEY' : '' }
    auth_data = { 'type' : 'keygen' , "user" : user, 'password' : passwd  }

    try:
        auth_response = requests.post(f"https://{ip}/api", data=auth_data, verify=False, timeout=5)

        if auth_response.status_code == 200:
            auth_root = ET.fromstring(auth_response.text)
            key = auth_root.find(".//key").text
            headers['X-PAN-KEY'] = key

        else:
            logging.error(f'Device: {device} - {auth_response.status_code}')

    except requests.exceptions.RequestException as e:
        logging.error(f'Device: {device} - {e}')

    return headers

    API_Key = headers