#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
#Get All Values from Vault
vault login --no-print $SSH_TOKEN





#python3 aws-delete-vpc-all.py
