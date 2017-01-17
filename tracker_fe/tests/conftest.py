import pytest

@pytest.fixture
def server(xprocess):
    def preparefunc(cwd):
        print (str(cwd))
        n = cwd.new(basename="").new(basename="").dirpath().chdir()
        print ("Working directory is {}".format(n))
        return ("Quit the server with CONTROL-C", ["python", "../../manage.py", "runserver", "9000"])
    
    logfile = xprocess.ensure("tracker-server", preparefunc)
