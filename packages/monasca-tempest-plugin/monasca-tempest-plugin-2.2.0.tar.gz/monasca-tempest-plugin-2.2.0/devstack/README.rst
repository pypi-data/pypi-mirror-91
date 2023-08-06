====================
Enabling in Devstack
====================

**WARNING**: the stack.sh script must be run in a disposable VM that is not
being created automatically, see the README.md file in the "devstack"
repository.

1. Download DevStack::

    git clone https://opendev.org/openstack/devstack.git
    cd devstack

2. Add this repo as an external repository::

     > cat local.conf
     [[local|localrc]]
     enable_plugin monasca-tempest-plugin https://opendev.org/openstack/monasca-tempest-plugin

3. run ``stack.sh``

Running Monasca tempest tests
=============================

1. Listing Monasca tempest tests::

    tempest list-plugins

2. Running monasca tempest tests::

    cd /opt/stack/tempest
    tempest run -r monasca_tempest_tests.tests.api
    tempest run -r monasca_tempest_tests.tests.log_api
