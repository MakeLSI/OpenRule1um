# Netlist converter  v0.1  23 Sep., 2021 copy left by R. Okawa (okawa@ifdl.jp)
# Note: Supports hierarchical SPICE netlist
import sys
import codecs  # available for python 2/3
import xml.etree.ElementTree as ET



### get arguments from command line
args = sys.argv

### get path of the intermediate netlist file (XML)
### Note: included '\' in the path on Windows KiCad 5.1.10
imd_file_path = repr(args[1]).replace('\\\\', '/').replace('\'', '')

### get path of output file
out_file_path = args[2]

### parse xml file
tree = ET.parse(imd_file_path)
root = tree.getroot()

### open output file
out_file = codecs.open(out_file_path, 'w', 'utf-8')

### get schematic(s)
sources = root.findall('design/sheet/title_block/source')
source_text = [child.text for child in sources]
subckts = set([item for item in source_text])

out_file.write('* KiCad Eeschema')



### each schematic
for subckt in subckts:
    out_file.write('\n')

    ### write subckt name
    out_file.write('.subckt ' + subckt.replace('.sch', ''))

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
                                        or True \
                                            and '/' not in net.attrib['name'] \
                                            and not(net.attrib['name'].startswith('Net'))  \
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
    sheets1 = root.findall('design/sheet')
    for sheet1 in sheets1:
        sheets2 = root.findall('design/sheet')
        for sheet2 in sheets2:
            sheet1_name = sheet1.attrib['name']
            sheet2_name = sheet2.attrib['name']
            if sheet1_name != sheet2_name and sheet1_name != '/':
                if sheet1_name.startswith(sheet2_name):
                    sheet1_source = sheet1.find('title_block/source').text
                    if sheet1_source != subckt:
                        out_file.write('X' + str(x_number))
                        x_nets = []  # subcircuit instance nets
                        comps = root.findall('components/comp')
                        for comp in comps:
                            comp_ref = comp.attrib['ref']
                            comp_sheetpath = comp.find('sheetpath')
                            comp_sheetpath_name = comp_sheetpath.attrib['names']
                            if sheet1_name == comp_sheetpath_name:
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
                                                    if '/Net' not in net.attrib['name']:
                                                        x_nets.append(net.attrib['code'])
                                                        break
                                    
                        for subckt_net in x_nets:
                            out_file.write(' ' + subckt_net)
                        
                        out_file.write(' ' + sheet1_source.replace('.sch', '') + '\n')
                        
                        x_number += 1
    
    out_file.write('.ends ' + subckt.replace('.sch', '') + '\n')

out_file.close
