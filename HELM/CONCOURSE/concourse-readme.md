Current Release - October 17, 2022 by Sherri Conrod

Helm Install/Upgrade of Concourse 
===========
Current Release
==========
- [] New install make sure the image tag and chart:
  imageTag: "7.8.1" chart: "concourse-17.0.15"
  https://github.com/concourse/concourse-chart/releases/

Concourse keeps adding in new features and integrations on a weekly cadence. 
If you wish to upgrade the image tag or chart version, you should first test it with a new deploy in a separate environment

- [] Before installing, update the ci user password in the values file on line 2788 from $PASSWORD to something new
- [] Update your vault url and also your concourse web external url
- [] Generate an approle_id and secret_id in vault and update the values file - there are two place to update this, search on "vaultAuthParam"

- [] Test out your approle_id and secret_id :

curl -k -XPOST -d '{"role_id":"c5b11052-e660-1615-2d99-4337dea60166","secret_id":"00d19ad5-8a45-ab8e-0ae3-d27bb5493914"}' http://prod-vault.devops-ontap.com:8200/v1/auth/approle/login | jq


Helm Upgrades
======

Before doing a helm upgrade of concourse you must generate a new secret_id
After doing a Helm upgrade of concourse you must re-create teams and assign appropriate roles

fly -t cisco-fso-labs set-team --team-name cisco-fso-labs --local-user us-west-1a -c roles/owner.yml

Login
====

fly --target=prod login --concourse-url=http://prod-ci.devops-ontap.com:8080 -n main --username=ci --password=""


Set-Pipeline Example:
========
fly -t prod set-pipeline -p cisco-fso-labs e -c pipeline-v3.yml -l /Users/sconrod/dev/cisco-fso-lab-gen/params/main-us-west-2a.yml -v aws.region=us-west-2 -v az.name=us-west-2a -v vault.addr=http://prod-vault.devops-ontap.com:8200

(you can also put the variables passed to this command in your parameters file)

Setup Teams and Roles
==========

fly -t cisco-fso-labs set-team --team-name cisco-fso-labs --local-user us-west-1a -c roles/owner.yml