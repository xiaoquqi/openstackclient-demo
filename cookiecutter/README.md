## Usage

pip install cookiecutter
cookiecutter https://git.openstack.org/openstack-dev/cookiecutter.git

$ cookiecutter https://git.openstack.org/openstack-dev/cookiecutter.git
Cloning into 'cookiecutter'...
remote: Counting objects: 561, done.
remote: Compressing objects: 100% (237/237), done.
remote: Total 561 (delta 315), reused 539 (delta 297)
Receiving objects: 100% (561/561), 76.44 KiB | 0 bytes/s, done.
Resolving deltas: 100% (315/315), done.
Checking connectivity... done.
module_name (default is "replace with the name of the python module")? superadmin
repo_group (default is "openstack")? stackforge
repo_name (default is "replace with the name for the git repo")? superadmin
launchpad_project (default is "replace with the name of the project on launchpad")? superadmin
project_short_description (default is "OpenStack Boilerplate contains all the boilerplate you need to create an OpenStack package.")?demo project for Openstack
Initialized empty Git repository in /home/sysadmin/trainning/cookiecutter/superadmin/.git/
[master (root-commit) 28250d5] Initial Cookiecutter Commit.
 27 files changed, 630 insertions(+)
 create mode 100644 .coveragerc
 create mode 100644 .gitignore
 create mode 100644 .gitreview
 create mode 100644 .mailmap
 create mode 100644 .testr.conf
 create mode 100644 CONTRIBUTING.rst
 create mode 100644 HACKING.rst
 create mode 100644 LICENSE
 create mode 100644 MANIFEST.in
 create mode 100644 README.rst
 create mode 100644 babel.cfg
 create mode 100755 doc/source/conf.py
 create mode 100644 doc/source/contributing.rst
 create mode 100644 doc/source/index.rst
 create mode 100644 doc/source/installation.rst
 create mode 100644 doc/source/readme.rst
 create mode 100644 doc/source/usage.rst
 create mode 100644 openstack-common.conf
 create mode 100644 requirements.txt
 create mode 100644 setup.cfg
 create mode 100644 setup.py
 create mode 100644 superadmin/__init__.py
 create mode 100644 superadmin/tests/__init__.py
 create mode 100644 superadmin/tests/base.py
 create mode 100644 superadmin/tests/test_superadmin.py
 create mode 100644 test-requirements.txt
 create mode 100644 tox.ini
