#!/usr/bin/env python3
import shutil
import os

from jinja2 import Template
import libvirt
import uuid
import random


xml_template = """
<domain type='kvm'>
  <name>{{ name }}</name>
  <memory>{{ memory }}</memory>
  <vcpu>{{ cpu }}</vcpu>
  <os>
    <type arch="x86_64">hvm</type>
    <boot dev="hd"/>
  </os>
  <clock sync="localtime"/>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' />
      <source file='{{ image }}'/>
      <target dev='hda'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <mac address='{{ mac }}'/>
      <model type='virtio' />
    </interface>
    <graphics type='vnc' port='-1' keymap='de'/>
  </devices>
</domain>
"""


image_path = "/home/sin/vms/cirros-0.6.1-x86_64-disk.img"
disk_path = None
name = str(uuid.uuid4())


def random_mac():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0x7f), random.randint(0x00, 0x7f)]
    return ":".join(map(lambda x: "%02x" % x, mac))


def copy_image_to_disk():
    global disk_path
    global name
    disk_base_path = os.path.join("/home/sin/vms", name)
    os.mkdir(disk_base_path)
    disk_path = os.path.join(disk_base_path, "disk.img")
    shutil.copyfile(image_path, disk_path)


def main():
    conn = libvirt.open("qemu:///system")

    copy_image_to_disk()

    data = {
        "name": name,
        "cpu": 1,
        "memory": 1024 * 128,
        "image": disk_path,
        "mac": random_mac()
    }
    template = Template(xml_template)
    xml = template.render(**data)
    conn.defineXML(xml)


main()
