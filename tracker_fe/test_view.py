from django.test import TestCase
from .views import index 
import pytest
from django.urls import reverse

def test_index_view(client):
    response = client.get(reverse('tracker_fe:index'))
    assert "Hello, world. You are at the tracking system" in response.content
