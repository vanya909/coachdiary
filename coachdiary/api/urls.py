from auth.users.api.urls import urlpatterns as users_api_urlpatterns
from standards.api.urls import urlpatterns as standards_api_urlpatterns

urlpatterns = [
    *users_api_urlpatterns,
    *standards_api_urlpatterns,
]
