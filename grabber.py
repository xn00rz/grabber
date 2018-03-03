import sys
import requests
import argparse
import os

# my modules
from modules import colors
from modules import banner

def check_arg(args=None):

    parser = argparse.ArgumentParser(description="Script to get banner grabber" + colors.Cores.red)
    parser.add_argument('-i', '--ip', help='ip address', required=True, default='127.0.0.1')
    results = parser.parse_args(args)
    return(results.ip)

def parsing_dict(headers_dict):

    for k,v in headers_dict.items():
        print(str(k) + colors.Cores.red + ":" + str(v) + colors.Cores.yellow)
        if str(k) == 'Server' or str(k) == 'server':
            print("Getting information from Vulners API " + colors.Cores.orange)
            os.system('python3 vulners_module.py ' + str(v))



def validating_ip(ip):

    
    parts = ip.split('.')
    if int(parts[3]) > 255 or int(parts[2]) > 255 or int(parts[1]) > 255 or int(parts[0]) > 255:
        print("this cannot exceed 255..")
        sys.exit(1)

    if int(parts[3]) < 0 or int(parts[2]) < 0 or int(parts[1]) < 0 or int(parts[0]) < 0:
        print("this cannot less than 0..")
        sys.exit(1)
    
    print('The last octed is ' + parts[3] + colors.Cores.green)
    end_ip = input('Type the end addr you like: ' + colors.Cores.lightblue)

    if int(end_ip) > 255  or int(end_ip) < 0:
        print('ipts dont match..' + colors.Cores.red)
    
    count = int(parts[3])
    ips = open('ipts.txt', 'w')
    while count < int(end_ip):
        parts[3] = str(count)
        ip_write = '.'.join(parts)
        ips.write(ip_write + '\n')
        count += 1
    ips.close()

    print("Processing.. requests now..\/" + colors.Cores.green)
 

def making_head_request():

    ofile = open('ipts.txt', 'r')
    for line in ofile.readlines():
        new_line = line.rstrip()
        request_http = 'http://' + new_line + '/'
        print('\n')
        print('\n')

        try:
            r = requests.head(request_http, timeout=8, allow_redirects=True)
            print('[-] Response for: ' + request_http + colors.Cores.pink)
            parsing_dict(r.headers)
            status_code = r.status_code
            print('[-] Status code for: ' + request_http + str(status_code) + colors.Cores.pink)
        except requests.exceptions.RequestException as e:
            print(colors.Cores.purple + '[!] Connections problems/Timeout for: ' + colors.Cores.red + request_http )
            pass
        except (KeyboardInterrupt, SystemExit):
            raise
        


if __name__ == '__main__':
    banner.Banner.ennvy()
    i = check_arg(sys.argv[1:])
    print("[+] IP => ", i)
    validating_ip(i)
    making_head_request()
