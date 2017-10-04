# Automated Docker environment with NGINX

Creating an automated Docker environment with NGINX composed by one single Container running an NGINX proxy.

api1-3 is test app (flask python app which returns api1, api2, api3 when you go on nginx proxy).
Specify hostnames like api1 in nginx/site.conf

test_rest.py is a python script that imitates a RESTful service


## Getting Started


### Prerequisites

What things you need to install the software and how to install them

Install Pytest
```
sudo pip3 install pytest
```


## Running 

To run app, go to project directory where you will see docker-compose.yml file and fire the below Build command to start the whole environment

```
"docker-compose up --build" 
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






