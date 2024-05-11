import logging
import requests
from config import conf
logger = logging.getLogger('itchat')
# nocobase配置
NocobaseAPIUrl = conf().get("nocobase_api_url")
NocobaseApiKey = conf().get("nocobase_api_key")

def nocobase_update(wechat_nickname,qr_url,status):
    try:
        if status == 1:
            headers = {
                "content-type": "multipart/form-data",
                "Authorization": NocobaseApiKey
            }
            try:
                update_data = {
                    "wechat_nickname": wechat_nickname,
                    "qr": "",
                    "qr_url": qr_url,
                    "status": status
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": NocobaseApiKey
                }
                response = requests.post(
                    NocobaseAPIUrl + "/api/dow_status_monitoring:updateOrCreate?filterKeys[]=wechat_nickname",
                    headers=headers,
                    json=update_data
                )
                response.raise_for_status()
                logger.info("Record updated successfully.")
            except requests.RequestException as e:
                logger.error(f"Error uploading attachment: {e}")
        elif status == 0:
            update_data = {
                "wechat_nickname": wechat_nickname,
                "qr": "",
                "qr_url": qr_url,
                "status": status
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": NocobaseApiKey
            }
            try:
                response = requests.post(
                    NocobaseAPIUrl + "/api/dow_status_monitoring:updateOrCreate?filterKeys[]=wechat_nickname",
                    headers=headers,
                    json=update_data
                )
                response.raise_for_status()
                logger.info("Record updated successfully.")
            except requests.RequestException as e:
                logger.error(f"Error updating record: {e}")
            
    except Exception as e:
            logger.error(e)