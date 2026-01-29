# Third Party Packages
from rest_framework.renderers import JSONRenderer



class CustomRenderer(JSONRenderer):
    media_type = "application/json"
    format = 'json'
    def render(self, data, accepted_media_type=None, renderer_context=None):

        try:
            if isinstance(data, dict) and "code" in data and "msg" in data:
                return super().render(data, accepted_media_type, renderer_context)


            response = renderer_context.get("response", None)
            print(data)
            response_message = "Successful"
            if isinstance(data , dict) and "response_message" in data:
                response_message = data.pop("response_message", response_message)


            response_data = {
                "code": response.status_code if response else 200,
                "msg": response_message,
                "data": data,
            }

            return super().render(response_data, accepted_media_type, renderer_context)

        except Exception as e:

            response_data = {
                "code": 500,
                "msg": "Internal server error",
                "data": None,
            }
            return super().render(response_data, accepted_media_type, renderer_context)

