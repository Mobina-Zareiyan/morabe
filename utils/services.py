# Local Apps
from morabe import settings

# Third Party Packages
import requests



def send_normal_sms(mobiles, message_text):

    # چک برا لیست بودن برا api
    if isinstance(mobiles, str):
        mobiles = [mobiles]

    url = 'https://api.mediana.ir/sms/v1/send/sms'
    payload = {
        "type": "Informational",
        "recipients": mobiles,
        "messageText": message_text
    }

    headers = {
        "Authorization": settings.MEDIANA_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if response.status_code == 200:
            return {"success": True, "data": data}
        return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
