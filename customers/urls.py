
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import *

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'professions', ProfessionViewSet)
router.register(r'datasheet', DataSheetViewSet)
router.register(r'document', DocumentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
