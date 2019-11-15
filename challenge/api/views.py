from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import NeuralNetwork
from api.serializers import NeuralNetworkSerializer, InputSerializer
from deepomatic.api.client import Client
from deepomatic.api.inputs import ImageInput


client = Client(api_key=settings.DEEPOMATIC_API_KEY, user_agent_prefix='challenge')

def perform_infer(nn, input_data, is_base64=False):
    if nn.external_id == -1:
        ptr = client.RecognitionSpec.retrieve(nn.name)
    else:
        ptr = client.RecognitionVersion.retrieve(nn.external_id)
    params = {'source': input_data}
    if is_base64:
        params['encoding'] = 'base64'
    infer = ptr.inference(inputs=[ImageInput(**params)])
    return infer

class NeuralNetworkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NeuralNetworkSerializer
    queryset = NeuralNetwork.objects.all()

    def get_serializer_class(self):
        if self.action == 'infer':
            return InputSerializer
        else:
            return NeuralNetworkSerializer

    @action(methods=['POST'], detail=True)
    def infer(self, request, pk, **kwargs):
        nn = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        infer = perform_infer(nn, serializer.validated_data['url'])
        return Response(infer)
