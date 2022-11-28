#!/usr/bin/env python3
from jinja2 import Template
import libvirt

xml_template = """
<domain type='kvm'>
  <name>aaaa</name>
  <memory>131072</memory>
  <vcpu>1</vcpu>
  <os>
    <type arch="x86_64">hvm</type>
    <boot dev="hd"/>
  </os>
  <clock sync="localtime"/>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <source file='/home/sin/vms/linux1/linux1.img'/>
      <target dev='hda'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <mac address='24:42:53:22:43:45'/>
    </interface>
    <graphics type='vnc' port='-1' keymap='de'/>
  </devices>
</domain>
"""


def main():
    conn = libvirt.open("qemu:///system")
    data = {}
    template = Template(xml_template)
    xml = template.render(**data)
    conn.defineXML(xml)

main()
