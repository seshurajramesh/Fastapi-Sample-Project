#How to run this Fastapi APP

## Linux VM setup

- Get a Centos/RHEL VM running on VirtualBox or Cloud
- Create a user (eg:fastapi)
- Create the directories in /opt - app and app/src
- Copy the contents of project to /opt/app/src
- create venv in /opt/app
- Install the python extensions using requirements file
- Use the env.example file and create ur custom env file in fastapi home directory /home/fastapi
- Copy the gunicorn service contents to new service file in /etc/systemd/system/fastapi.service
- start and enable the fastapi.service
- Access the project from http://server-ip/docs or http://server-ip/ or http://server-ip/redoc
- Dont forget to enable the firewall for nginx service