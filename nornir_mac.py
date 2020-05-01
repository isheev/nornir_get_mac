import re, json
from collections import defaultdict

def tree(): return defaultdict(tree)

commands=[  'show mac address-table',
#            'show vlan brief',
            ]

def get_cmd_output(): 
    from nornir import InitNornir
    from nornir.plugins.tasks import networking
    result_dic=defaultdict(tree)
    nr = InitNornir(config_file="config.yaml")
    for cmd in commands:
        result = nr.run(task=networking.netmiko_send_command, command_string=cmd)
        for device, response in result.items():
            result_dic[device][cmd] = response.result
    return result_dic

with open('cmd_output_dict.json', 'w') as f:   json.dump(get_cmd_output(), f)
with open('cmd_output_dict.json', 'r') as f:   data=json.load(f)

result=[['device','vlan','port','mac']]
for key_dev in data:
    show_mac_table_list=data[key_dev]['show mac address-table'].splitlines()
    for line in show_mac_table_list:
        m = re.search('.*(\d+)\s+(\S+)\s+dynamic.*\ +(.*\d)', line, re.IGNORECASE)
        if m:
            vlan, mac, port = m.groups()[0], m.groups()[1], m.groups()[1]
            result.append([key_dev,vlan,port,mac])

with open('result.csv', 'w') as f:
    for row in result: 
        f.write(str(','.join(row) +"\n"))
print('Done!')


