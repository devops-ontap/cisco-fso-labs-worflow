Current Release for Vault 
Chart -  vault-0.20.1    APP VERSION 1.10.3
$helm pull https://github.com/hashicorp/vault-helm/releases/tag/v0.21.0

git checkout https://github.com/hashicorp/vault-helm.git
git checkout tags/v0.20.1
helm install prod-vault hashicorp/vault --namespace prod-vault --version 0.20.1 -f /Users/sconrod/dev/cisco-fso-lab-gen/HELM/Vault/prod-vault-values.yaml


Helm Install
==========
helm -n prod-vault install prod-vault concourse/concourse -f prod-vault-values.yaml

kubectl -n prod-vault get po
kubectl -n prod-vault exec prod-vault-0 /bin/sh
vault operator init
vault operator unseal
#present three keys
vault login
vault secrets enable -version=1 -path=concourse kv

Create 3 Policies:

Concourse

path "concourse/*" {
capabilities = ["read"]
}

cisco-fso-labs

path "concourse/cisco-fso-labs/*" {
capabilities = ["read", "create","update", "list"]
}

main

path "concourse/main/*" {
capabilities = ["read", "create","update", "list"]
}

Until IAM STS Auth is configured (complex and not necessarily required for lab)

- [] Add the AWS Keys in the following format required by the pipeline. Check Pipeline Params.

- [] vault auth enable approle
- [] vault write auth/approle/role/concourse policies=concourse period=24h
- [] vault read auth/approle/role/concourse/role-id
- [] vault write -f auth/approle/role/concourse/secret-id
- [] update the concourse helm chart with the role-id and secret-id


- [] Update the vault with ssh-token/token under the cisco-fso-labs
vault token create --policy cisco-fso-labs --period 24h
**If you make this 1h keep in mind time ntp***