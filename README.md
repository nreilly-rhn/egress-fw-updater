# egress-fw-updater

Creates and maintains egressfirewall objects for OpenShift4 clusters on OpenshiftSDN and OVNKubernetes.

### ServiceAccount creation

Several cluster resources need to be created, the pod needs to run under a service account with additions RBAC permissions to create the egress firewall rules. Examples can be found under "ocp_files/{cluster,namespace}"

### Create Allow/Deny configmaps

FQDN's, IP Addresses, network ranges on seperate lines in files named "\*.allow" or "\*.deny". There can be multiple files created. Examples can be found in directories "domains_allow" and "domains_._deny"

### Script variables

|  --namespace | Namespace for EgressNetworkPolicy (OpenshiftSDN) or EgressFirewall (OVNKubernetes) object. |
|  --dir | - The directory to search for rule files. |
|  --output | - Output format for EgressNetworkPolicy declaration, can be either YAML or JSON, defaults to JSON. |
|  --write | - Write output to file |
|  --glob | - Glob pattern for rule files, defaults to '*.allow'. |

## Install example

#### Create example project

```
oc new-project egress-test
```
#### Create config for egress rules
```
oc create configmap -n egress-test egress-update-domains --from-file=domains_allow/
```
OR
```
oc create configmap -n egress-test egress-update-domains --from-file=domains_deny/
```
#### Create script for egress rules
```
oc create configmap -n egress-test egress-update-script --from-file=egress_fw.py
```

#### Create service account and RBAC configuration
```
oc create -f ocp_files/namespace/ServiceAccount.yaml
oc create -f ocp_files/cluster/ClusterRole.yaml
oc create -f ocp_files/cluster/ClusterRoleBinding.yaml
```

#### Create cronjob to run script
```
oc create -f ocp_files/namespace/CronJob.yaml
```