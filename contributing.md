#How to run this Fastapi APP

## Linux VM setup

- Get a Centos/RHEL VM running on VirtualBox or Cloud
- Create a user (eg:fastapi)
- Create the directories in /opt - app and app/src
- Copy the contents of project to /opt/app/src
- Use the env.example file and create ur custom env file in fastapi home directory /home/fastapi
- Install Docker in VM
- Build the Docker image(refer below
- Run the Docker image(refer below)
- Access the project from http://server-ip/docs or http://server-ip/ or http://server-ip/redoc
- Dont forget to enable the firewall for nginx service



# How to Run this APP locally

## Build the Image
```
docker build -t IMAGE_NAME project_directory
```

## Run the Docker Image with FLask
```
docker run -dp 8000:8000 -w /app -v "$(pwd):/app" IMAGE-NAME sh -c "uvicorn main:app --host=0.0.0.0"
```

## Or Run the APP by Gunicorn

```
docker run -dp 8000:8000 -w /app -v "$(pwd):/app" IMAGE-NAME
```
