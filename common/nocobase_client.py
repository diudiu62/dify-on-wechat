from io import BytesIO
import logging
import requests
import os
from datetime import datetime
from config import conf
logger = logging.getLogger('itchat')
# nocobase配置
NocobaseAPIUrl = conf().get("nocobase_api_url")
NocobaseApiKey = conf().get("nocobase_api_key")
def nocobase_update(wechat_nickname,qr_url,status):
    print("11111")
    try:
        print("222")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if status == "1":
            print("333")
            # 上传附件
            headers = {
                "content-type": "multipart/form-data",
                "Authorization": NocobaseApiKey
            }
            try:
                print("444")
                # 发送GET请求，获取图片内容
                response = requests.get(qr_url)
                image_content = response.content
                # 构建一个字典，包含要上传的文件
                image_file = {
                    'file': (qr_url.split('/')[-1], image_content, 'image/jpeg')
                }
                response = requests.post(
                    f"{NocobaseAPIUrl}/api/attachments:create?attachmentField=dow_status_monitoring.wechat_qr",
                    headers=headers,
                    files=image_file
                )
                print("777")
                print(response.text)
                response.raise_for_status()
                logger.info("Attachment uploaded successfully.")
                update_data = {
                    "wechat_nickname": wechat_nickname,
                    "qr": response.json()["url"],
                    "qr_url": qr_url,
                    "status": status
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": NocobaseApiKey
                }
                response = requests.post(
                    f"{NocobaseAPIUrl}/api/dow_status_monitoring:update?filterByTk=1",
                    headers=headers,
                    json=update_data
                )
                print("888")
                print(response.text)
                response.raise_for_status()
                logger.info("Record updated successfully.")
            except requests.RequestException as e:
                logger.error(f"Error uploading attachment: {e}")
        elif status == "0":
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
                    f"{NocobaseAPIUrl}/api/dow_tatus_monitoring:update?filterByTk=1",
                    headers=headers,
                    json=update_data
                )
                response.raise_for_status()
                logger.info("Record updated successfully.")
            except requests.RequestException as e:
                logger.error(f"Error updating record: {e}")
            
    except Exception as e:
            logger.error(e)