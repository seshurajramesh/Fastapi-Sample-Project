#How to run this Fastapi APP

## Linux VM setup

- Get a Centos/RHEL VM running on VirtualBox or Cloud
- Create a user (eg:fastapi)
- Create the directories in /opt - app and app/src
- Copy the contents of project to /opt/app/src
- Use the env.example file and create ur custom env file in fastapi home directory /home/fastapi
- Install Docker in VM
- Build and run the Docker image using docker-compose
- Access the project from http://server-ip/docs or http://server-ip/ or http://server-ip/redoc
- Dont forget to enable the firewall for nginx service



# How to Run this APP locally

```
docker compose up
```
# How to Run this APP locally if any changes made

```
docker compose up --build
```
