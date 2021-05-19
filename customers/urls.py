
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import *

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet,basename='customer')
router.register(r'professions', ProfessionViewSet,basename='profession')
router.register(r'datasheet', DataSheetViewSet,basename='datasheet')
router.register(r'document', DocumentViewSet,basename='document')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
