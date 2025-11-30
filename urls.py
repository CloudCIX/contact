from django.urls import include, path


urlpatterns = [
    path('v5.0/', include('contact.urls_v5_0')),
    # Default route → latest version
    path('', include('contact.urls_v5_0')),
]
