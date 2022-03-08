# Netlist converter  v0.2  8 Mar., 2022 copy left by R. Okawa (okawa@ifdl.jp)
# Note: The circuit is extracted as a subckt.
import os
import sys
import codecs  # available for python 2 or 3
import xml.etree.ElementTree as ET



### get arguments from command line
args = sys.argv

### get path of the intermediate netlist file (XML format)
### Note: included '\' in the path on Windows KiCad 5.1.10
imd_file_path = repr(args[1]).replace('\\\\', '/').replace('\'', '')

### get path of output file
### Note: Multiple extension to single extension
out_file_path_tmp = args[2]
out_file_path = out_file_path_tmp.split('.')[0] + '.cir'

### parse xml file
tree = ET.parse(imd_file_path)
root = tree.getroot()

### open output file
out_file = codecs.open(out_file_path, 'w', 'utf-8')

### get the top of schematic
sheets = root.findall('design/sheet')
for sheet in sheets:
    if sheet.attrib['name'] == '/':
        sheet_source_top = sheet.find('title_block/source').text

### write header of netlist
tool_ver = root.find('design/tool').text
out_file.write('* KiCad ' + tool_ver + '\n')

### write subckt name
out_file.write('.subckt ' + sheet_source_top.split('.')[0])

### parse subckt I/O pin
subckt_nets = []
net_names = []
comps = root.findall('components/comp')
for comp in comps:
    comp_ref = comp.attrib['ref']
    libsource = comp.find('libsource')
    libsource_part = libsource.attrib['part']
    libpart = root.find("libparts/libpart[@part='" + str(libsource_part) + "']")
    pins = libpart.findall('pins/pin')
    for pin in pins:
        pin_num = pin.attrib['num']
        nets = root.findall('nets/net')
        for net in nets:
            nodes = net.findall('node')
            for node in nodes:
                if node.attrib['ref'] == comp_ref and node.attrib['pin'] == pin_num:
                    if  net.attrib['name'].startswith('/') \
                    and net.attrib['name'].count('/') < 2 \
                    and not(net.attrib['name'].startswith('Net'))\
                    and not(net.attrib['name'].startswith('/Net'))\
                    and net.attrib['code'] not in subckt_nets:
                        subckt_nets.append(net.attrib['code'])
                        net_names.append([net.attrib['code'], net.attrib['name']])
                        break

### write net number of IO of subckt
for subckt_net in subckt_nets:
    out_file.write(' ' + subckt_net)

out_file.write('\n')

### write comment the relation of net number and net name
for net_relation in net_names:
    out_file.write('* net ' + net_relation[0] + ' ' + net_relation[1] + '\n')

### parse and write components in subckt
comps = root.findall('components/comp')
for comp in comps:
    comp_ref = comp.attrib['ref']
    comp_sheetpath = comp.find('sheetpath')
    comp_sheetpath_name = comp_sheetpath.attrib['names']
    out_file.write(comp_ref)
    libsource = comp.find('libsource')
    libsource_part = libsource.attrib['part']
    libpart = root.find("libparts/libpart[@part='" + str(libsource_part) + "']")
    pins = libpart.findall('pins/pin')
    for pin in pins:
        pin_num = pin.attrib['num']
        nets = root.findall('nets/net')
        for net in nets:
            nodes = net.findall('node')
            for node in nodes:
                if node.attrib['ref'] == comp_ref and node.attrib['pin'] == pin_num:
                    out_file.write(' ' + net.attrib['code'])
                    break

    spice_model = comp.find("fields/field[@name='Spice_Model']").text
    out_file.write(' ' + spice_model)
    out_file.write('\n')

    out_file.write('* ' + comp_ref + ' is in ' + comp_sheetpath_name + '\n')

out_file.write('.ends ' + sheet_source_top.split('.')[0] + '\n')
out_file.close

# delete the intermediate netlist file
# os.remove(imd_file_path)
