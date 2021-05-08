Using Tunnel CLI extensions to OpenStack Client
================================================

List of released CLI commands available in openstack client. These commands
can be referenced by doing ``openstack help vpnserver``.

============
vpnserver
============

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver create

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver delete

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver list

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver set

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver unset

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver show

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver stats show

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver status show

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver failover

========
listener
========

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver listener *

====
pool
====

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver pool *

======
member
======

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver member *

=============
healthmonitor
=============

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver healthmonitor *

========
l7policy
========

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver l7policy *

======
l7rule
======

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver l7rule *

=====
quota
=====

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver quota *

=======
amphora
=======

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver amphora *

========
provider
========

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver provider *

======
flavor
======

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver flavor *

=============
flavorprofile
=============

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver flavorprofile *

================
availabilityzone
================

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver availabilityzone *

=======================
availabilityzoneprofile
=======================

.. autoprogram-cliff:: openstack.vpn_server.v2
    :command: vpnserver availabilityzoneprofile *
