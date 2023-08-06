==============
Redfish driver
==============

Overview
========

The ``redfish`` driver enables managing servers compliant with the
Redfish_ protocol.

Prerequisites
=============

* The Sushy_ library should be installed on the ironic conductor node(s).

  For example, it can be installed with ``pip``::

      sudo pip install sushy

Enabling the Redfish driver
===========================

#. Add ``redfish`` to the list of ``enabled_hardware_types``,
   ``enabled_power_interfaces``, ``enabled_management_interfaces`` and
   ``enabled_inspect_interfaces`` as well as ``redfish-virtual-media``
   to ``enabled_boot_interfaces`` in ``/etc/ironic/ironic.conf``.
   For example::

    [DEFAULT]
    ...
    enabled_hardware_types = ipmi,redfish
    enabled_boot_interfaces = ipmitool,redfish-virtual-media
    enabled_power_interfaces = ipmitool,redfish
    enabled_management_interfaces = ipmitool,redfish
    enabled_inspect_interfaces = inspector,redfish

#. Restart the ironic conductor service::

    sudo service ironic-conductor restart

    # Or, for RDO:
    sudo systemctl restart openstack-ironic-conductor

Registering a node with the Redfish driver
===========================================

Nodes configured to use the driver should have the ``driver`` property
set to ``redfish``.

The following properties are specified in the node's ``driver_info``
field:

- ``redfish_address``: The URL address to the Redfish controller. It must
                       include the authority portion of the URL, and can
                       optionally include the scheme. If the scheme is
                       missing, https is assumed.
                       For example: https://mgmt.vendor.com. This is required.

- ``redfish_system_id``: The canonical path to the ComputerSystem resource
                         that the driver will interact with. It should include
                         the root service, version and the unique resource
                         path to the ComputerSystem. This property is only
                         required if target BMC manages more than one
                         ComputerSystem. Otherwise ironic will pick the only
                         available ComputerSystem automatically. For
                         example: /redfish/v1/Systems/1.

- ``redfish_username``: User account with admin/server-profile access
                        privilege. Although not required, it is highly
                        recommended.

- ``redfish_password``: User account password. Although not required, it is
                        highly recommended.

- ``redfish_verify_ca``: If redfish_address has the **https** scheme, the
                         driver will use a secure (TLS_) connection when
                         talking to the Redfish controller. By default
                         (if this is not set or set to True), the driver
                         will try to verify the host certificates. This
                         can be set to the path of a certificate file or
                         directory with trusted certificates that the
                         driver will use for verification. To disable
                         verifying TLS_, set this to False. This is optional.

- ``redfish_auth_type``: Redfish HTTP client authentication method. Can be
                         "basic", "session" or "auto".
                         The "auto" mode first tries "session" and falls back
                         to "basic" if session authentication is not supported
                         by the Redfish BMC. Default is set in ironic config
                         as ``[redfish]auth_type``.


The ``openstack baremetal node create`` command can be used to enroll
a node with the ``redfish`` driver. For example:

.. code-block:: bash

  openstack baremetal node create --driver redfish --driver-info \
    redfish_address=https://example.com --driver-info \
    redfish_system_id=/redfish/v1/Systems/CX34R87 --driver-info \
    redfish_username=admin --driver-info redfish_password=password \
    --name node-0

For more information about enrolling nodes see :ref:`enrollment`
in the install guide.

Features of the ``redfish`` hardware type
=========================================

Boot mode support
^^^^^^^^^^^^^^^^^

The ``redfish`` hardware type can read current boot mode from the
bare metal node as well as set it to either Legacy BIOS or UEFI.

.. note::

   Boot mode management is the optional part of the Redfish specification.
   Not all Redfish-compliant BMCs might implement it. In that case
   it remains the responsibility of the operator to configure proper
   boot mode to their bare metal nodes.

Out-Of-Band inspection
^^^^^^^^^^^^^^^^^^^^^^

The ``redfish`` hardware type can inspect the bare metal node by querying
Redfish compatible BMC. This process is quick and reliable compared to the
way the ``inspector`` hardware type works i.e. booting bare metal node
into the introspection ramdisk.

.. note::

   The ``redfish`` inspect interface relies on the optional parts of the
   Redfish specification. Not all Redfish-compliant BMCs might serve the
   required information, in which case bare metal node inspection will fail.

.. note::

   The ``local_gb`` property cannot always be discovered, for example, when a
   node does not have local storage or the Redfish implementation does not
   support the required schema. In this case the property will be set to 0.

Virtual media boot
^^^^^^^^^^^^^^^^^^

The idea behind virtual media boot is that BMC gets hold of the boot image
one way or the other (e.g. by HTTP GET, other methods are defined in the
standard), then "inserts" it into node's virtual drive as if it was burnt
on a physical CD/DVD. The node can then boot from that virtual drive into
the operating system residing on the image.

The major advantage of virtual media boot feature is that potentially
unreliable TFTP image transfer phase of PXE protocol suite is fully
eliminated.

Hardware types based on the ``redfish`` fully support booting deploy/rescue
and user images over virtual media. Ironic builds bootable ISO images, for
either UEFI or BIOS (Legacy) boot modes, at the moment of node deployment out
of kernel and ramdisk images associated with the ironic node.

To boot a node managed by ``redfish`` hardware type over virtual media using
BIOS boot mode, it suffice to set ironic boot interface to
``redfish-virtual-media``, as opposed to ``ipmitool``.

.. code-block:: bash

  openstack baremetal node set --boot-interface redfish-virtual-media node-0

If UEFI boot mode is desired, the user should additionally supply EFI
System Partition image (ESP_) via ``[driver-info]/bootloader`` ironic node
property or ironic configuration file in form of Glance image UUID or a URL.

.. code-block:: bash

  openstack baremetal node set --driver-info bootloader=<glance-uuid> node-0

If ``[driver_info]/config_via_floppy`` boolean property of the node is set to
``true``, ironic will create a file with runtime configuration parameters,
place into on a FAT image, then insert the image into node's virtual floppy
drive.

When booting over PXE or virtual media, and user instance requires some
specific kernel configuration, ``[instance_info]/kernel_append_params``
property can be used to pass user-specified kernel command line parameters.
For ramdisk kernel, ``[instance_info]/kernel_append_params`` property serves
the same purpose.

Virtual Media Ramdisk
~~~~~~~~~~~~~~~~~~~~~

The ``ramdisk`` deploy interface can be used in concert with the
``redfish-virtual-media`` boot interface to facilitate the boot of a remote
node utilizing pre-supplied virtual media.

Instead of supplying an ``[instance_info]/image_source`` parameter, a
``[instance_info]/boot_iso`` parameter can be supplied. The image will
be downloaded by the conductor, and the instance will be booted using
the supplied ISO image. In accordance with the ``ramdisk`` deployment
interface behavior, once booted the machine will have a ``provision_state``
of ``ACTIVE``.

.. code-block:: bash

  openstack baremetal node set \
      --instance_info boot_iso=http://url/to.iso node-0

This initial interface does not support bootloader configuration
parameter injection, as such the ``[instance_info]/kernel_append_params``
setting is ignored.


.. _`dhcpless_booting`:

Layer 3 or DHCP-less ramdisk booting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DHCP used by PXE requires direct L2 connectivity between the node and the
service since it's a User Datagram Protocol (UDP) like other protocols used by
the PXE suite, there is no guarantee that packets will be delivered.

One of the solutions is the reliance on virtual media boot capability coupled
with another feature of hardware type - its ability to provide
network configuration that is placed in the config-drive_ of the node, the
configuration follows the same schema that OpenStack Nova uses for the
``network_data.json``. The config drive filesystem information is on the IPA
ramdisk ISO image from which the node is booted.

The Glean_ tool is available in the simple-init_ element that needs to be used
when creating the ramdisk image. The ironic ramdisk will probe all removable
media devices on the node in search of media labeled as `config-2`. If found,
this tool will consume static network configuration and set up node's
networking stack accordingly without calling out for DHCP.

When ironic is running within OpenStack, no additional configuration is required
on the ironic side - config drive with ramdisk network configuration will be
collected from Networking service and written on the IPA ramdisk ISO.

Alternatively, the user can build and pass node network configuration, in
form of a network_data_ JSON blob, to ironic node being managed via the
``--network-data`` CLI option. Node-based configuration takes precedence over
the configuration generated by the Network service.

.. code-block:: bash

  openstack baremetal node set \
    --network-data ~/network_data.json <node>

Node-based configuration can be useful in standalone ironic deployment
scenario.

.. note::

  Make sure to use add the simple-init_ element when building the IPA ramdisk.

Firmware update using manual cleaning step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``redfish`` hardware type supports updating the firmware on nodes using a
manual cleaning step.

The firmware update cleaning step allows one or more firmware updates to be
applied to a node. If multiple updates are specified, then they are applied
sequentially in the order given. The server is rebooted once per update.
If a failure occurs, the cleaning step immediately fails which may result
in some updates not being applied. If the node is placed into maintenance
mode while a firmware update cleaning step is running that is performing
multiple firmware updates, the update in progress will complete, and processing
of the remaining updates will pause.  When the node is taken out of maintenance
mode, processing of the remaining updates will continue.

When updating the BMC firmware, the BMC may become unavailable for a period of
time as it resets. In this case, it may be desireable to have the cleaning step
wait after the update has been applied before indicating that the
update was successful. This allows the BMC time to fully reset before further
operations are carried out against it. To cause the cleaning step to wait after
applying an update, an optional ``wait`` argument may be specified in the
firmware image dictionary. The value of this argument indicates the number of
seconds to wait following the update. If the ``wait`` argument is not
specified, then this is equivalent to ``wait 0``, meaning that it will not
wait and immediately proceed with the next firmware update if there is one,
or complete the cleaning step if not.

The ``update_firmware`` cleaning step accepts JSON in the following format::

    [{
        "interface": "management",
        "step": "update_firmware",
        "args": {
            "firmware_images":[
                {
                    "url": "<url_to_firmware_image1>",
                    "wait": <number_of_seconds_to_wait>
                },
                {
                    "url": "<url_to_firmware_image2>"
                },
                ...
            ]
        }
    }]

The different attributes of the ``update_firmware`` cleaning step are as follows:

.. csv-table::
    :header: "Attribute", "Description"
    :widths: 30, 120

    "``interface``", "Interface of the cleaning step.  Must be ``management`` for firmware update"
    "``step``", "Name of cleaning step.  Must be ``update_firmware`` for firmware update"
    "``args``", "Keyword-argument entry (<name>: <value>) being passed to cleaning step"
    "``args.firmware_images``", "Ordered list of dictionaries of firmware images to be applied"

Each firmware image dictionary, is of the form::

    {
      "url": "<URL of firmware image file>",
      "wait": <Optional time in seconds to wait after applying update>
    }

The ``url`` argument in the firmware image dictionary is mandatory, while the
``wait`` argument is optional.


.. note::
   Only ``http`` and ``https`` URLs are currently supported in the ``url``
   argument.

.. note::
   At the present time, targets for the firmware update cannot be specified.
   In testing, the BMC applied the update to all applicable targets on the
   node. It is assumed that the BMC knows what components a given firmware
   image is applicable to.

To perform a firmware update, first download the firmware to a web server that
the BMC has network access to. This could be the ironic conductor web server
or another web server on the BMC network. Using a web browser, curl, or similar
tool on a server that has network access to the BMC, try downloading
the firmware to verify that the URLs are correct and that the web server is
configured properly.

Next, construct the JSON for the firmware update cleaning step to be executed.
When launching the firmware update, the JSON may be specified on the command
line directly or in a file. The following
example shows one cleaning step that installs two firmware updates. The first
updates the BMC firmware followed by a five minute wait to allow the BMC time
to start back up. The second updates the firmware on all applicable NICs.::

    [{
        "interface": "management",
        "step": "update_firmware",
        "args": {
            "firmware_images":[
                {
                    "url": "http://192.0.2.10/BMC_4_22_00_00.EXE",
                    "wait": 300
                },
                {
                    "url": "https://192.0.2.10/NIC_19.0.12_A00.EXE"
                }
            ]
        }
    }]

Finally, launch the firmware update cleaning step against the node. The
following example assumes the above JSON is in a file named
``firmware_update.json``::

    openstack baremetal node clean <ironic_node_uuid> --clean-steps firmware_update.json

In the following example, the JSON is specified directly on the command line::

    openstack baremetal node clean <ironic_node_uuid> --clean-steps '[{"interface": "management", "step": "update_firmware", "args": {"firmware_images":[{"url": "http://192.0.2.10/BMC_4_22_00_00.EXE", "wait": 300}, {"url": "https://192.0.2.10/NIC_19.0.12_A00.EXE"}]}}]'

.. note::
   Firmware updates may take some time to complete. If a firmware update
   cleaning step consistently times out, then consider performing fewer
   firmware updates in the cleaning step or increasing
   ``clean_callback_timeout`` in ironic.conf to increase the timeout value.

.. warning::
   Warning: Removing power from a server while it is in the process of updating
   firmware may result in devices in the server, or the server itself becoming
   inoperable.

.. _Redfish: http://redfish.dmtf.org/
.. _Sushy: https://opendev.org/openstack/sushy
.. _TLS: https://en.wikipedia.org/wiki/Transport_Layer_Security
.. _ESP: https://wiki.ubuntu.com/EFIBootLoaders#Booting_from_EFI
.. _network_data: https://specs.openstack.org/openstack/nova-specs/specs/liberty/implemented/metadata-service-network-info.html
.. _config-drive: https://docs.openstack.org/nova/queens/user/config-drive.html
.. _Glean: https://docs.openstack.org/infra/glean/
.. _simple-init: https://docs.openstack.org/diskimage-builder/latest/elements/simple-init/README.html
