# Third Party Packages
from rest_framework.renderers import JSONRenderer
from copy import deepcopy


class CustomRenderer(JSONRenderer):
    media_type = "application/json"
    format = "json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200


        if status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)


        payload = deepcopy(data)


        message = "Successful"


        if isinstance(payload, dict) and "response_message" in payload:
            message = payload["response_message"]
            payload = {k: v for k, v in payload.items() if k != "response_message"}


        return super().render({
            "code": status_code,
            "msg": message,
            "data": payload,
        }, accepted_media_type, renderer_context)

