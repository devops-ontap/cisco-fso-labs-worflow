#!/bin/sh
export AWS_PAGER=""
cp config ~/.aws
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $SSH_TOKEN
rm -rf ~/.kube
mkdir ~/.kube
vault kv get -field kubeconfig concourse/cisco-fso-labs/lab-kube-config > ~/.kube/config
#Install kubernetes metrics server into default namespace
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl get deploy,svc -n kube-system | egrep metrics-server
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes"
kubectl create ns rabbitmq
helm repo add appdynamics-charts https://ciscodevnet.github.io/appdynamics-charts
kubectl create ns appdynamics-lab
vault kv get -field data concourse/cisco-fso-labs/appd-helm-values | base64 -d > values.yaml
#helm install -f ./values.yaml appdynamics-lab appdynamics-charts/cluster-agent -n appdynamics-lab
helm upgrade -f ./values.yaml appdynamics-lab appdynamics-charts/cluster-agent -n appdynamics-lab
helm -n appdynamics-lab ls
kubectl get pods -n appdynamics-lab


