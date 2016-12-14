from django.test import TestCase
from .views import index 
import pytest
from django.urls import reverse


class indextest(TestCase):
    def test_index_view(self):
        #res=index(self)
        response = self.client.get(reverse('tracker_fe:index'))
        self.assertEqual("Hello, world. You are at the tracking system" , response.content)
    

