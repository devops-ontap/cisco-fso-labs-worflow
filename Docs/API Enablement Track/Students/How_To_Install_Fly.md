How to Install Fly
====================

Download the version of fly for your OS.
There is a tiny icon at the bottom right-hand corner of the screen here:
http://ci.devops-ontap.com:8080

MAC & Linux
============
After downloading the fly tool, run these commands:

#sudo mkdir -p /usr/local/bin
#sudo mv ~/Downloads/fly /usr/local/bin
#sudo chmod 0755 /usr/local/bin/fly

If anyone is using Windows ...
If you are using Windows, please install Docker Desktop for Windows and Run fly in a Docker Container 
Corporate Windows Images tend to be hardened or have Group Policies and other software installed that can conflict or cause issues with fly.
It is best in this case to run fly in a docker container

Recording on How To Here:
Webex meeting recording: Windows - Running Fly in Docker
Password: GzuJnTP6
Recording link: https://cisco.webex.com/cisco/ldr.php?RCID=ccfa9c868877c5a146d9016fa31bdfb4

1. Install Docker Desktop
   https://docs.docker.com/get-docker/
2. Start Docker Desktop


docker pull sconrod/ubuntu-fly:latest
docker images -a
docker run -itd imageid
docker ps
docker exec -it containerid

Now you are on the container and you can run fly
Edit your files using vim


MAC
=====
If you get an error when you first try to use fly on a mac saying 
it cannot open fly as it is from a unknown Developer, follow these steps:

If you’re sure you trust the app developer, you can override your security settings and allow the app to install and open.

Open Finder. Select Go. Go to Folder. Type in: /usr/local/bin/fly
Locate the app you’re trying to open.
Control+Click the app.
Select Open.
Click Open.
The app should be saved as an exception in your security settings, allowing you to open it in the future.

Log in to Concourse via Fly:
========================
fly --target=ci login --concourse-url=http://prod-ci.devops-ontap.com:8080 --username= --password=
