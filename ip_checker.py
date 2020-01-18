from typing import List


def decompose(input_IP):
    ip_n_subn = input_IP.rsplit('/', 1)
    ip = ip_n_subn[0].split('.', 3)
    return (ip ,ip_n_subn)


def pre_validate(input_ip):
    try: 
        return [item for item in input_ip if int(item)]
    except ValueError as v:
        print(v)

def iPs_in_subnet():
    pass

def calc_host_id(input_IP, subnet_mask):
    subnm_ = decompose(subnet_mask)[0]
    or_ = (lambda tuppy: int(tuppy[0]) & int(tuppy[1]))
    pack = list(zip(input_IP, subnm_))
    return list(map(or_, pack))


def validate_ip(input_IP):
    ip, ip_n_subn = decompose(input_IP)
    ip = pre_validate(ip)
    if ip and len(ip) == 4 and  0 <= int(ip_n_subn[1]) <= 32:
        valid_IP_parts = [item for item in ip if 0 <= int(item) <= 255]
        if len(valid_IP_parts) == 4:
            return input_IP
    else:
        return None


def net_class(input_IP):
    ip, _ = decompose(input_IP)
    if int(ip[0]) <= 127:
        if int(ip[0]) == 10 and 0 <= int(ip[1]) <= 255:
            return ('Private class A Network', 'A','-')
        else:
            return ('Public class A Network', 'A', '+')
    elif int(ip[0]) <= 191:
        if int(ip[0]) == 172 and 16 <= int(ip[1]) <= 31 and 0 <= int(ip[2]) <= 255:
            return ('Private class B Network', 'B', '-')
        else:
            return ('Public class B Network', 'B', '+')
    elif int(ip[0]) <= 223:
        if int(ip[0]) == 192 and int(ip[1]) == 168:
            return ('Private class C Network', 'C', '-')
        else:
            return ('Public class C Network', 'C', '+')
    elif (ip[0]) <= 239:
        return ('Class D Network', 'D', '#')
    else:
        return ('Class E Network', 'E', '#')


def calc_subnetmask(suffix):
    base_two_result = 2 ** (32 - int(suffix))
    if base_two_result <= 255:
        return f'255.255.255.{256 - base_two_result}'
    elif base_two_result <= 65_535:
        buff_floor = (base_two_result // 256)
        return f'255.255.{256 - buff_floor}.0'
    elif base_two_result <= 16_777_215:
        buff_floor = (base_two_result // 65536)
        return f'255.{256 - buff_floor}.0.0'
    elif base_two_result <= 4_294_967_296:
        buff_floor = (base_two_result // 16_777_215)
        return f'{256 - buff_floor}.0.0.0'
    else:
        'Invalid subnetmask!'


def ip_information():
    print('Your IP:')
    input_IP = input()
    if '/' not in input_IP:
        while '/' not in input_IP:
            print('Please enter a suffix for subnetting e.g: `/32 - /0`')
            suffix = input()
            if suffix[0] != '/':
                continue
            if 0 <= int(suffix.strip('/')) <= 32:
                input_IP = input_IP + suffix
    while not validate_ip(input_IP):
        print('Please enter a valid IP:')
        input_IP = input()
    net_class_out = net_class(input_IP)
    if net_class_out:
        print()
        print('|-==========- RESULTS: -==========-|')
        print()
        print(net_class_out)
        subnetmask = calc_subnetmask(decompose(input_IP)[1][1])
        print(f'Subnetmask: {subnetmask}')
        host_id = calc_host_id(decompose(input_IP)[0], subnetmask)
        print(f'Host ID: {host_id[0]}.{host_id[1]}.{host_id[2]}.{host_id[3]}')
    else:
        print('Something went wrong, please contact the developer')


if __name__ == '__main__':
    ip_information()