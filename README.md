# egress-fw-updater



## Getting started

```
oc new-project egress-test
oc create configmap -n egress-test egress-update-domains --from-file=domains.allow
oc create configmap -n egress-test egress-update-script --from-file=egress_fw.py
oc create -f ocp_files/namespace/ServiceAccount.yaml
oc create -f ocp_files/cluster/ClusterRole.yaml
oc create -f ocp_files/cluster/ClusterRoleBinding.yaml
oc create -f ocp_files/namespace/CronJob.yaml
```