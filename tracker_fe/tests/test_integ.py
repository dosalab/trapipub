import requests

def test_index_page(xprocess):
    def preparefunc(cwd):
        print (str(cwd))
        n = cwd.new(basename="").new(basename="").dirpath().chdir()
        print ("Working directory is {}".format(n))
        return ("Quit the server with CONTROL-C", ["python", "../../manage.py", "runserver", "9000"])

    logfile = xprocess.ensure("tracker-server", preparefunc)
    s = requests.get("http://127.0.0.1:9000/tracker")
    assert " Hello, world. You are at the tracking system" in s.text
    

    
