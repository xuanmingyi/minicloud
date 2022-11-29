#!/usr/bin/env python3
from jinja2 import Template
import libvirt
import uuid


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
      <mac address='52:54:00:10:c0:d9'/>
      <model type='virtio' />
    </interface>
    <graphics type='vnc' port='-1' keymap='de'/>
  </devices>
</domain>
"""


def main():
    conn = libvirt.open("qemu:///system")
    u = str(uuid.uuid4())
    name = u[:8]
    data = {
        "name": name,
        "cpu": 1,
        "memory": 1024 * 128,
        "image": "/home/sin/vms/linux2/linux2.img"
    }
    template = Template(xml_template)
    xml = template.render(**data)
    conn.defineXML(xml)


main()
