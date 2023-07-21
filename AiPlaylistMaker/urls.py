from django.contrib import admin
from django.urls import path, include
import chat.views

urlpatterns = [
    # Define a default view for the root URL
    path('', chat.views.api_key_entry_view, name='api_key_entry'),
    path('chat/', chat.views.chat_view, name='chat'),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('accounts/', include('allauth.urls')),
]
