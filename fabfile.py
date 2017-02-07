from fabric.api import local, run, cd, env, sudo

env.hosts=['ubuntu@ec2-54-64-56-135.ap-northeast-1.compute.amazonaws.com']

def pre_deploy():
    "Things that should be done before deployment"
    local("py.test")
    local("git push")

def deploy(tree='master'):
    pre_deploy()
    with cd("/home/ubuntu/deployments/repos/trapi"):
        run("git pull")
        run("git archive --prefix={tree}/ --output=../trapi-deploy/{tree}.tar {tree}".format(tree=tree))


    sudo("sudo service supervisor stop")

    with cd("/home/ubuntu/deployments/repos/trapi-deploy"):
        run("rm -Rf {tree}".format(tree=tree))
        run("tar -xvf {tree}.tar".format(tree=tree))
        run("rm {}.tar".format(tree))

    with cd("/home/ubuntu"):
        run("rm -f current")
        run("ln -s deployments/repos/trapi-deploy/{} current".format(tree))

    with cd("/home/ubuntu/current"):
        run(". /home/ubuntu/track_env/bin/activate && python manage.py collectstatic --settings tracker.settings.prod --noinput")
            
    sudo("sudo service supervisor restart")
