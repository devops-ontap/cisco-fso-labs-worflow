curl https://api.thousandeyes.com/tests/agent-to-server/new.json \
-d '{"interval": 300, "agents": [{"agentId": 438241}], "testName": "API network test addition for www.thousandeyes.com", "server": "www.thousandeyes.com"}' \
-H "Content-Type: application/json" \
--header "Authorization: Bearer 1d0acd78-a470-44ad-a6d6-0892ac2db441"
