from fabric.api import local, run, cd, env, sudo

env.hosts=['ubuntu@ec2-54-64-56-135.ap-northeast-1.compute.amazonaws.com']

def pre_deploy():
    "Things that should be done before deployment"
    local("py.test")
    local("git push")

def deploy(tree='master'):
    pre_deploy()
    with cd("/home/ubuntu/deployments/trapi"):
        run("git pull")
        run("git archive --prefix={tree}/ --output=../{tree}.tar {tree}".format(tree=tree))


    sudo("sudo service supervisor stop")

    with cd("/home/ubuntu/deployments/"):
        run("rm -Rf {tree}".format(tree=tree))
        run("tar -xvf {tree}.tar".format(tree=tree))
        run("rm {}.tar".format(tree))

    with cd("/home/ubuntu"):
        run("rm -f current")
        run("ln -s deployments/{} current".format(tree))
    sudo("sudo service supervisor restart")
