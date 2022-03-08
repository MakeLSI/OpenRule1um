# Netlist converter  v0.4  2 Mar., 2022 copy left by R. Okawa (okawa@ifdl.jp)
# Note: Supports hierarchical SPICE netlist
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

### get schematic(s)
subckts_dic = {}
sheets = root.findall('design/sheet')
for sheet in sheets:
    if sheet.find('title_block/source').text not in subckts_dic:
        subckts_dic[sheet.find('title_block/source').text] = sheet.attrib['name']

### for detecting error by check number of IOs each subckt has
num_io = {}

### write header of netlist
tool_ver = root.find('design/tool').text
out_file.write('* KiCad ' + tool_ver)



### each schematic
subckts = subckts_dic.keys()
for subckt in subckts:
    out_file.write('\n')

    ### write subckt name
    out_file.write('.subckt ' + subckt.split('.')[0])

    ### parse subckt I/O pin
    subckt_nets = []
    subckt_source = []
    sheets = root.findall('design/sheet')
    for sheet in sheets:
        sheet_name = sheet.attrib['name']
        sheet_source = sheet.find('title_block/source').text
        comps = root.findall('components/comp')
        if sheet_source == subckt and (sheet_source not in subckt_source):
            for comp in comps:
                comp_ref = comp.attrib['ref']
                comp_sheetpath = comp.find('sheetpath')
                comp_sheetpath_name = comp_sheetpath.attrib['names']
                libsource = comp.find('libsource')
                libsource_part = libsource.attrib['part']
                libpart = root.find("libparts/libpart[@part='" + str(libsource_part) + "']")
                if comp_sheetpath_name.startswith(sheet_name):
                    pins = libpart.findall('pins/pin')
                    for pin in pins:
                        pin_num = pin.attrib['num']
                        nets = root.findall('nets/net')
                        for net in nets:
                            nodes = net.findall('node')
                            for node in nodes:
                                if node.attrib['ref'] == comp_ref and node.attrib['pin'] == pin_num:
                                    ### conditions of the below
                                    ### 1. for only top circuit
                                    ### 2. for sub circuit
                                    ### 3. for global label or net as pin
                                    if     True \
                                            and sheet_name == '/' \
                                            and net.attrib['name'].count('/') == 1 \
                                            and net.attrib['name'].startswith('/') \
                                            and net.attrib['code'] not in subckt_nets \
                                            and '/Net' not in net.attrib['name'] \
                                        or True \
                                            and sheet_name != '/' \
                                            and net.attrib['name'].startswith('/') \
                                            and net.attrib['code'] not in subckt_nets \
                                            and '/Net' not in net.attrib['name'] \
                                            and net.attrib['name'].count('/') <= sheet_name.count('/') \
                                        or True \
                                            and '/' not in net.attrib['name'] \
                                            and not(net.attrib['name'].startswith('Net'))  \
                                            and not(net.attrib['name'].startswith('unconnected'))  \
                                            and net.attrib['code'] not in subckt_nets \
                                        :
                                        subckt_nets.append(net.attrib['code'])
                                        break
            
            subckt_source.append(sheet_source)

    ### write net number of IO of subckt
    for subckt_net in subckt_nets:
        out_file.write(' ' + subckt_net)

    out_file.write('\n')

    ### write comment the relation of net number and net name
    sheet_source_top = root.find('design/sheet/title_block/source').text
    for subckt_net in subckt_nets:
        net = root.find("nets/net[@code='" + str(subckt_net) + "']")
        if sheet_source_top == subckt and net.attrib['code'] in subckt_nets:
            out_file.write('* net ' + net.attrib['code'] + ' ' + net.attrib['name'] + '\n')
    


    ### parse and write components in subckt
    parsed_sheet = []
    sheets = root.findall('design/sheet')
    for sheet in sheets:
        sheet_name = sheet.attrib['name']
        sheet_source = sheet.find('title_block/source').text
        if sheet_source == subckt and sheet_source not in parsed_sheet:
            comps = root.findall('components/comp')
            for comp in comps:
                comp_ref = comp.attrib['ref']
                comp_sheetpath = comp.find('sheetpath')
                comp_sheetpath_name = comp_sheetpath.attrib['names']
                if sheet_name == comp_sheetpath_name:
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

        parsed_sheet.append(sheet_source)



    ### parse and write subcircuit instance in subckt
    x_number = 1  # subcircuit instance id
    sheets = root.findall('design/sheet')
    for sheet in sheets:
        sheet_name = sheet.attrib['name']
        if sheet_name.startswith(subckts_dic[subckt]) \
           and \
           subckts_dic[subckt].count('/') + 1 == sheet_name.count('/'):
            out_file.write('X' + str(x_number))
            x_nets = []  # subcircuit instance nets
            comps = root.findall('components/comp')
            for comp in comps:
                comp_ref = comp.attrib['ref']
                comp_sheetpath = comp.find('sheetpath')
                comp_sheetpath_name = comp_sheetpath.attrib['names']
                if sheet_name == comp_sheetpath_name \
                    or \
                   comp_sheetpath_name.startswith(sheet_name) \
                       and \
                   sheet_name.count('/') + 1 <= comp_sheetpath_name.count('/'):
                    libsource = comp.find('libsource')
                    libsource_part = libsource.attrib['part']
                    libpart = root.find("libparts/libpart[@part='" + str(libsource_part) + "']")
                    pins = libpart.findall('pins/pin')
                    for pin in pins:
                        pin_num = pin.attrib['num']
                        nets = root.findall('nets/net')
                        for net in nets:
                            nodes = net.findall('node')
                            if net.attrib['code'] not in x_nets:
                                for node in nodes:
                                    if node.attrib['ref'] == comp_ref and node.attrib['pin'] == pin_num:
                                        ### condition of the below
                                        ### ignore net name such as 'xxx/xxx/Netxxx' or '/Netxxx'
                                        if 'Net' not in net.attrib['name'] and \
                                           'unconnected' not in net.attrib['name'] and \
                                           net.attrib['name'].count('/') <= sheet_name.count('/'):
                                            x_nets.append(net.attrib['code'])
                                            break

            for subckt_net in x_nets:
                out_file.write(' ' + subckt_net)
            
            sheet_source = sheet.find('title_block/source').text
            out_file.write(' ' + sheet_source.split('.')[0] + '\n')
            out_file.write('* ' + 'X' + str(x_number) + ' is ' + sheet_name + '\n')

            ### parse IO error check
            if sheet_source.split('.')[0] not in num_io:
                num_io[sheet_source.split('.')[0]] = len(x_nets)
            else:
                if num_io[sheet_source.split('.')[0]] != len(x_nets):
                    ### error when the number of IOs compares with the parsed same instance is different
                    out_file.write('*### ^ ERROR: the IO(s) of this instance did not parse correctly ###\n')
                    print('ERROR(' + subckt.split('.')[0] + '): please press any key & check output file')
                    input()
                    break
            
            
            x_number += 1
    
    out_file.write('.ends ' + subckt.split('.')[0] + '\n')

out_file.close

# delete the intermediate netlist file
# os.remove(imd_file_path)
