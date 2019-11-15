from django.db import models

class NeuralNetwork(models.Model):
    DETECTION = 'DET'
    CLASSIFICATION = 'CLA'
    TAGGING = 'TAG'
    KIND_OF_NN = [
        (DETECTION, 'Detection'),
        (CLASSIFICATION, 'Classification'),
        (TAGGING, 'Tagging'),
    ]

    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=3, choices=KIND_OF_NN)
    external_id = models.IntegerField()

    def __str__(self):
        return self.name

