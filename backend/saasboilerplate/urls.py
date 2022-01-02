"""saasboilerplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from usermanagement import views as userviews
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"users", userviews.CurrentUserViewSet, basename="user")
router.register(r"workspaces", userviews.WorkspaceViewSet, basename="workspace")
router.register(r"products", userviews.ProductViewSet, basename="product")
# router.register(r"groups", userviews.GroupViewSet, basename="group")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/admin/", admin.site.urls),
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api/fp/", include("django_drf_filepond.urls")),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/login/reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/stripe/", include("djstripe.urls", namespace="djstripe")),
]
