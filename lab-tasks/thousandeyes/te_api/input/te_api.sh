#!/bin/bash
export AWS_PAGER=""
#export VAULT_ADDR=$VAULT_ADDR
#export VAULT_TOKEN=$SSH_TOKEN
#vault login --no-print $SSH_TOKEN
#TE_OATHTOKEN=$(vault kv get --field=token concourse/main/te-api)
export TE_OATHTOKEN=$TE_OATHTOKEN
python3 -m pip install requests
python3 te_api_agent_server_tests.py


