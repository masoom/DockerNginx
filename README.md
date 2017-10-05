# Automated Docker environment with NGINX

Creating an automated Docker environment with NGINX composed by one single Container running an NGINX proxy.

docker-compose.yml - This file specifies all containers which will run on docker-compose up command.
 
nginx.conf - main nginx configuration

site.conf - virtual host configuration file with proxy options and some performance tuning like caching and ssl options).

api1-3 is test app (flask python app which returns api1, api2, api3 when you go on nginx proxy).
Specify hostnames like api1 in nginx/site.conf

test_rest.py - python script that imitates a RESTful service


### Prerequisites

Install Pytest
```
sudo pip3 install pytest
≈

Install NGINX Web Server

```
sudo apt-get update
sudo apt-get install nginx
```

## Running 

To run app, go to project directory where you will see docker-compose.yml file and fire the below Build command to start the whole environment. Deployment is automatic and portable in every single-host Docker environment.

```
docker-compose up --build 
```

### To Stop


```
docker-compose stop 

```

### To Restart

```
docker-compose restart 
```

## Docker Compose

```
version: "2"
services:
# NGINX container with startup parameters, volumes\links\port exposing
  nginx:
    build: ./nginx
    ports:
      - 80:80
      - 443:443
    links:
      - api1:api1
      - api2:api2
      - api3:api3
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/site.conf:/etc/nginx/sites-enabled/site.conf:ro
      - ./nginx/ssl/domain.crt:/etc/nginx/ssl/domain.crt:ro
      - ./nginx/ssl/domain.key:/etc/nginx/ssl/domain.key:ro
      - ./nginx/logs:/var/log/nginx:rw
# First Backend with Test app
  api1:
    build: ./api1
# Second Backend with Test app
  api2:
    build: ./api2
# Third Backend with Test app
  api3:
    build: ./api3
    
```

## SSL Certificates

Self Signed SSL is the type of certificate used in the above solution.
All config files\SSL certificates and logs are mounted in container at startup.

Creates a directory ssl that will be used to hold all SSL information & mounting certificates from host.
```
sudo mkdir /etc/nginx/ssl
```

Configure Nginx to Use SSL.

To configure NGINX to use SSL, Modify NGINX configuration by adjusting server block. Add these lines in the server block, 
```
server {
        listen 443;
        server_name _;
        
		ssl on;

		ssl_certificate     /etc/nginx/ssl/domain.crt;
		ssl_certificate_key /etc/nginx/ssl/domain.key;
```

## Exposing Ports
NGINX exposing port 80 and 443 to outside. 
```
nginx:
    ports:
      - 80:80
      - 443:443
```
## Persistent NGINX Configuration

All configs and other files will be stored on host machine and attached to any running container on startup. This will be implemented in docker-compose file. Docker Compose preserves all volumes used by your services. When docker-compose up runs, if it finds any containers from previous runs, it copies the volumes from the old container to the new container. This process ensures that any data you’ve created in volumes isn’t lost.

## Security

All shared files which are mounted in container are read-only(can't be modifed inside container, only from host)

