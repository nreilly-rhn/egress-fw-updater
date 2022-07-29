#!/usr/bin/python3

import argparse, copy, glob, json, os, ipaddress, subprocess, sys
from operator import ne


class CustomArgumentParser(argparse.ArgumentParser):
    class _CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
        def _get_help_string(self, action):
            help = super()._get_help_string(action)
            if action.dest != 'help':
                help += ' [env: {}]'.format(action.dest.upper())
            return help

    def __init__(self, *, formatter_class=_CustomHelpFormatter, **kwargs):
        super().__init__(formatter_class=formatter_class, **kwargs)

    def _add_action(self, action):
        action.default = os.environ.get(action.dest.upper(), action.default)
        return super()._add_action(action)

def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
#        print("IP address {} is valid. The object returned is {}".format(address, ip))
        return True
    except ValueError:
#        print("IP address {} is not valid".format(address))
        return False

def validate_ip_network(address):
    try:
        ip = ipaddress.ip_network(address)
#        print("IP address {} is valid. The object returned is {}".format(address, ip))
        return True
    except ValueError:
#        print("IP address {} is not valid".format(address))
        return False


parser = CustomArgumentParser(description='Generate OpenShift egress firewall rules for a project using EgressNetworkPolicy.')
parser.add_argument('-n', '--namespace', help="Namespace for EgressNetworkPolicy object")
parser.add_argument('-d', '--dir', help="The directory to search for *.allow files")
parser.add_argument('-o', '--output', choices=['json','yaml'], default='json', help="Output format for EgressNetworkPolicy declaration")
parser.add_argument('-w', '--write', help="Write output to file")
parser.add_argument('-g', '--glob', default='*.allow', help="Glob pattern for allow files")

args = parser.parse_args()

if not args.namespace:
    exit(parser.usage())

if not args.dir:
    args.dir = os.getcwd()

DefaultAllowHosts = []

domain_files = glob.glob(os.path.join(args.dir, args.glob))

sdn = json.loads(subprocess.run([ "oc", "get", "Network.config.openshift.io", "cluster", "-ojson"], stdout=subprocess.PIPE).stdout)["spec"]["networkType"]
apiservers = []
apiservers = json.loads(subprocess.run([ "oc", "get", "ep", "kubernetes", "-n", "default", "-ojson" ], stdout=subprocess.PIPE).stdout)["subsets"]

print(json.dumps(apiservers, indent=2))

#ips = apiservers.stdout
print (sdn)
#print (json.dumps(ips, indent=2))

#for apiserver in apiservers["addresses"]:
#    for key, value in apiserver.items():
#      DefaultAllowHosts.append(value)
#
#print(DefaultAllowHosts)
#
#if sdn.lower() == "openshiftsdn":
#    apiVersion = "network.openshift.io/v1"
#    kind = "EgressNetworkPolicy"
#elif sdn.lower() == "ovnkubernetes":
#    apiVersion = "k8s.ovn.org/v11"
#    kind = "EgressFirewall"
#
#o = {
#    "apiVersion": apiVersion,
#    "kind": kind,
#    "metadata": {
#        "name": "default",
#        "namespace": args.namespace
#    },
#    "spec": {
#        "egress": []
#    }
#}
#allow = {
#    "to": {
#        "cidrSelector": ''
#    },
#    "type": "Allow"
#}
#deny = {
#    "to": {
#        "cidrSelector": ''
#    },
#    "type": "Deny"
#}
#allow_all = {
#    "to": {
#        "cidrSelector": '0.0.0.0/0'
#    },
#    "type": "Allow"
#}
#allow_api = {
#    "to": {
#        "cidrSelector": '172.18.0.0/24'
#    },
#    "type": "Allow"
#}
#deny_all = {
#    "to": {
#        "cidrSelector": '0.0.0.0/0'
#    },
#    "type": "Deny"
#}
#
#for f in domain_files:
#    if f.endswith((".allow")):
#        entry = allow
#        implicit = deny_all
#    elif f.endswith((".deny")):
#        entry = deny
#        implicit = allow_all
#    else:
#        continue
#
#    with open(f) as fp:
#        for line in fp:
#            l = line.strip()
#            if ( l.startswith("#") or len(l.split()) == 0):
#                continue
#            if( validate_ip_address(l)):
#                cidr = ipaddress.ip_address(l).with_prefixlen
#                entry['to']['cidrSelector'] = cidr
#                o['spec']['egress'].append(copy.deepcopy(entry))
#            elif(validate_ip_network(l)):
#                cidr = ipaddress.ip_network(l).with_prefixlen
#                entry['to']['cidrSelector'] = cidr
#                o['spec']['egress'].append(copy.deepcopy(entry))
#            else:
#                dig = subprocess.run(["dig", "+short", l ], encoding='utf-8', stdout=subprocess.PIPE)
#                ips = dig.stdout
#                for ip in ips.splitlines():
#                    cidr = ipaddress.ip_network(ip).with_prefixlen
#                    entry['to']['cidrSelector'] = cidr
#                    o['spec']['egress'].append(copy.deepcopy(entry))
#    if f.endswith((".allow")):
#        for DefaultAllowHost in DefaultAllowHosts:
#            o['spec']['egress'].append(DefaultAllowHost)
#    o['spec']['egress'].append(implicit) 
#
#if args.write:
#    out = open(args.write, 'w')
#else:
#    out = sys.stdout
#
#if args.output == 'yaml':
#    import yaml
#    print(yaml.dump(o), file=out)
#else:
#    print(json.dumps(o), file=out)
#    print(json.dumps(o, indent=2) )
