from rest_framework.routers import DefaultRouter
from api.views import NeuralNetworkViewSet

urlpatterns = [
]


router = DefaultRouter()
router.register(r'^model', NeuralNetworkViewSet)

urlpatterns += router.urls
