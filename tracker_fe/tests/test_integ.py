import requests

def test_index_page(live_server):
    resp = requests.get(live_server.url)
    assert "Hello, world. You are at the tracking system" in resp.content.decode('utf-8')
    

    
