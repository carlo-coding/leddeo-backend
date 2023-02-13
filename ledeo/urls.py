from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("video/", include("video.urls")),
    path("language/", include("language.urls")),
    path("account/", include("account.urls")),
    path("plans/", include("plans.urls")),
    path("support/", include("faq.urls")),
    path("user/", include("history.urls")),
    path("health/", include("health.urls")),
    path("fonts/", include("fonts.urls")),
    path("acceptance/", include("acceptance.urls"))
]
urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path("api/v1/", include(urlpatterns))
]
