from io import BytesIO
import logging
import requests
import os
from datetime import datetime
from config import conf
logger = logging.getLogger('itchat')
# nocobase配置
NocobaseConfig = conf()
NocobaseAPIUrl = NocobaseConfig.get("nocobase_api_url")
NocobaseApiKey = NocobaseConfig.get("nocobase_api_key")
def nocobase_update(wechat_nickname,qr_url,status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == "1":
        # 上传附件
        headers = {
            "content-type": "multipart/form-data",
            "Authorization": NocobaseApiKey
        }
        image_url = qr_url
        try:
            with requests.get(image_url, stream=True) as image_response:
                image_response.raise_for_status()
                image_data = BytesIO(image_response.content)
                image_file = ("image", image_data, "image/jpeg")
                logger.info(f"Downloaded image from {image_url} at {timestamp}")
                response = requests.post(
                    f"{NocobaseAPIUrl}/api/attachments:create?attachmentField=qr_url.pic",
                    headers=headers,
                    files=image_file
                )
                response.raise_for_status()
                logger.info("Attachment uploaded successfully.")
                update_data = {
                    "wechat_nickname": wechat_nickname,
                    "qr": response.json()["url"],
                    "qr_url": image_url,
                    "status": status
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": NocobaseApiKey
                }
                response = requests.post(
                    f"{NocobaseAPIUrl}/api/dow_tatus_monitoring:update?filterByTk=1",
                    headers=headers,
                    json=update_data
                )
                response.raise_for_status()
                logger.info("Record updated successfully.")
        except requests.RequestException as e:
            logger.error(f"Error uploading attachment: {e}")
    elif status == "0":
        update_data = {
            "wechat_nickname": wechat_nickname,
            "qr": "",
            "qr_url": image_url,
            "status": status
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": NocobaseApiKey
        }
        try:
            response = requests.post(
                f"{NocobaseAPIUrl}/api/dow_tatus_monitoring:update?filterByTk=1",
                headers=headers,
                json=update_data
            )
            response.raise_for_status()
            logger.info("Record updated successfully.")
        except requests.RequestException as e:
            logger.error(f"Error updating record: {e}")