from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from machines.views import VulnerableMachineViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from machines.views import RegisterView, CurrentUserView

router = routers.DefaultRouter()
router.register(r'machines', VulnerableMachineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/me/', CurrentUserView.as_view(), name='current_user'),
]

