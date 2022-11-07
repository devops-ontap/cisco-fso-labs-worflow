#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
curl -LO https://dl.k8s.io/release/v1.22.0/bin/linux/amd64/kubectl
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
curl -LO https://github.com/kubernetes/kops/releases/download/v1.22.0/kops-linux-amd64
cp kops-linux-amd64 kops
chmod +x ./kops
mv ./kops /usr/local/bin/
export NAME=lab-kube.k8s.local
export KOPS_STATE_STORE=s3://lab-kube.k8s.local
#The s3 bucket needs to be created - this was done manually - require to automate into pipeline
#kops create cluster --zones=us-east-1a ${NAME}
kops update cluster ${NAME} --yes --admin
kops export kubeconfig $NAME --admin
#Need to get the kubeconfig file to yaml and then write it to the vault so in the subsequent tasks it can be called from the vault.....
#vault login --no-print $SSH_TOKEN
#cp ~/.kube/config .
#vault kv put concourse/cisco-fso-labs/lab-kube-config kubeconfig=@config
kops validate cluster --wait 10m
tar -xzvf smm*
#./smm install -a --cluster-name $NAME



