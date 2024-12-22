from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get('response')
        status_code = response_data.status_code

        response = {'data': data}
        if 200 <= status_code < 300:
            response['statusCode'] = status_code
            response['message'] = response_data.status_text

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)