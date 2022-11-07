#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
#https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
#https://kops.sigs.k8s.io/getting_started/install/
curl -Lo kops https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
chmod +x kops
mv kops /usr/local/bin/kops
export NAME=aiops-kube.k8s.local
export KOPS_STATE_STORE=s3://aiops-kube.k8s.local
#The s3 bucket needs to be created - this was done manually - require to automate into pipeline
kops create cluster --zones=us-east-2c ${NAME} --yes
kops update cluster ${NAME} --yes --admin
kops rolling-update cluster --yes
kops export kubeconfig $NAME --admin
#Need to get the kubeconfig file to yaml and then write it to the vault so in the subsequent tasks it can be called from the vault.....
#vault login --no-print $SSH_TOKEN
#cp ~/.kube/config .
#vault kv put concourse/cisco-fso-labs/lab-kube-config kubeconfig=@config
kops validate cluster --wait 10m
helm repo add bitnami https://charts.bitnami.com/bitnami
#tar -xzvf smm*
#helm install metrics-server bitnami/metrics-server
#helm upgrade --namespace default metrics-server bitnami/metrics-server --set apiService.create=true
#SMM_REGISTRY_PASSWORD=wKzJN5l1byAalMYkHCIzwu3m2y0o3Gv8 ./smm activate --host=registry.eticloud.io --prefix=smm --user=sa-2cac3ae7-443d-467d-b72e-d5208c8e14d5
#./smm install -a --cluster-name lab-kube



