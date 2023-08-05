import hashlib
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.wechat import App
from .models import WeChatResponseMaterial, WeChatResponseEvent
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer


class WeChatResponseMaterialView(CustomModelViewSet):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer


class WeChatResponseEventView(CustomModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer

    def perform_create(self, serializer):
        event_key = hashlib.md5(b'123').hexdigest()[8:-8]
        result = App(self.request.data.get('appid')).qrcode.create({
            'action_name': 'QR_LIMIT_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': event_key},
            }
        })
        qrcode_ticket = result['ticket']
        serializer.save(event_key=event_key, qrcode_ticket=qrcode_ticket)
