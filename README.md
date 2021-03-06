# Automated Docker environment with NGINX

Setting up an automated multi-container Docker environment with a container running NGINX proxy & another container running simple Flask python app.

docker-compose.yml - This file specifies all containers which will run on docker-compose up command.
 
nginx.conf - main nginx configuration

site.conf - virtual host configuration file with proxy options and some performance tuning like caching and ssl options).

api1-3 is test app (flask python app which returns api1, api2, api3 when you go on nginx proxy).
Specify hostnames like api1 in nginx/site.conf

test_rest.py - python script that imitates a RESTful service

### Prerequisites

Install NGINX 

```
sudo apt-get install -y nginx

```

Install Docker Compose 
```
sudo pip install docker-compose
```

Install python-pip:
```
sudo apt-get -y install python-pip
```

Install Pytest
```
sudo pip3 install pytest
```

Install Flask
```
$ sudo pip install Flask
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

## Running Tests Locally. 

Go to the main directory where the test.rest.py file is located which imitates a RESTful service
```
python test_rest.py
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

### Dockerize a Flask App
Create a new file app.py inside the main dir and add the following python code
```
from flask import Flask
@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    
```

## SSL Certificates

Self Signed SSL is the type of certificate used in the above solution & attached to NGINX container on setup.
All config files\SSL certificates and logs are mounted in container at startup.  

Creates a directory ssl that will be used to hold all SSL information & mounting certificates from host.
```
sudo mkdir /etc/nginx/ssl
```

Configure Nginx to Use SSL.

To configure NGINX to use SSL, Modify NGINX configuration by adjusting server block. Add these lines in the server block
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

## Keepalive Connections

Keepalive connections reduce the CPU and network overhead needed to open and close connections. In my solution, I have Set an Idle keepalive connection to remain open for 20 ms    
```
    keepalive_timeout 20;
```

## Required Software

Docker 17.06.0 or above
<br />python 2.7.14 or above
<br />Ubuntu 14.04 64 bit
<br />Flask 0.12.2 
