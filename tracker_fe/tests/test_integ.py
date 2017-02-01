import requests

def test_index_page(server):
    resp = requests.get("http://127.0.0.1:8000/")
    assert "Hello, world. You are at the tracking system" in resp.content.decode('utf-8')
    

    
