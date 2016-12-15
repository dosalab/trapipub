from fabric.api import local, run, cd, env, sudo

env.hosts=['ubuntu@ec2-54-64-56-135.ap-northeast-1.compute.amazonaws.com']

def pre_deploy():
    "Things that should be done before deployment"
    local("git push")

def deploy(tree='master'):
    pre_deploy()
    with cd("/home/ubuntu/track-pull"):
        run("git pull")
        run("git archive --prefix={tree}/ --output=../{tree}.tar {tree}".format(tree=tree))
        run("tar xvf {tree}.tar".format(tree=tree))
        run("rm {}.tar".format(tree))

    sudo("service supervisor stop")

    with cd("/home/ubuntu"):
        run("rm track-system")
        run("ln -s track-pull/{} track-system".format(tree))

    sudo("service supervisor restart")
