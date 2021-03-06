"""
All tasks should have Usage: lines in their docstrings.
See existing tasks for examples.  This allows users
to see an overview of tasks by just running
``fab --list``.

Add tasks that should be exported to ``__ALL__``.
"""

from fabric.api import env, local, require, task
from fabric.tasks import execute

from .ansible import check_role_versions, install_roles

#
# KEEP TASKS IN ALPHABETICAL ORDER
#
__ALL__ = [
    'bootstrap',
    'check_role_versions',
    'create_superuser',
    'deploy',
    'install_roles',
]


#
# KEEP TASKS IN ALPHABETICAL ORDER
#
@task
def bootstrap():
    """
    Usage: fab <ENV> bootstrap
    """
    install_roles()
    execute(check_role_versions)
    deploy("bootstrap_python")
    deploy("site", extra_vars='{"unmanaged_users": [ubuntu]}')


@task
def create_superuser(email):
    """
    Usage: fab <ENV> create_superuser:dpoirier@caktusgroup.com
    """
    require('environment')
    deploy('create_superuser', extra_vars={'EMAIL': email})
    print("YOU SHOULD NOW DO A PASSWORD RESET")


@task
def deploy(play=None, extra_vars=None, branch=None):
    """
    Usage: fab <ENV> deploy[:playbook=NNNN][:extra_vars=aaa=1,bbb=2][:branch=xxx]
    """
    require('environment')
    execute(check_role_versions)
    cmd = ["ansible-playbook",
           "-i deployment/environments/{env}/inventory".format(env=env.environment)]
    playbook = play or "web"
    cmd.append("deployment/playbooks/{playbook}.yml".format(playbook=playbook))
    cmd.append("--user {user}".format(user=env.user))
    if extra_vars:
        cmd.append("--extra-vars='{extra_vars}'".format(extra_vars=extra_vars))
    if branch:
        cmd.append("-e repo_branch=%s" % branch)
    local(" ".join(cmd))

