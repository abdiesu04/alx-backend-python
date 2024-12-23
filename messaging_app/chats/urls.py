from django.urls import path, include
from rest_framework import routers

# Create a router and register the viewsets
router = routers.DefaultRouter()
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Ensures the router's URLs are included
]
