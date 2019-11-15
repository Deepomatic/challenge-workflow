from rest_framework import serializers
from api.models import NeuralNetwork


class InputSerializer(serializers.Serializer):
    url = serializers.URLField()


class NeuralNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeuralNetwork
        exclude = ['external_id']
