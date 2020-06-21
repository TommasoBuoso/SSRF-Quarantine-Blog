# SSRF - Quarantine blog

## Introduction

SSRF challenge for the security course.
This repository will provides 3 version of the ctf challenge:
- a basic version without any security defences;
- a blacklist version;
- a whitelist version.
  
Each directory contains a docker containt that you can run with the command:

```
docker-compose up
```

Every version of the callenge has a frontend and a backend server. You can access the frontend server through 'http://localhost:5000'.
You can't access directly to the backend server thats il located in the docker machine at 'http://localhost:5001', you can find the flag on the end point 'admin'.

## SSRF vulnerability

Server-side request forgery is a web security vulnerability that allows an attacker to induce the server-side application to make HTTP requests to an arbitrary host of the attacker’s choosing.

Typically SSRF targets the vulnerable application or other back-end services, that work with the vulnerable application, to make privilege escalation and perform unauthorized actions.

## Methodology

In the home page there is a drop down menu in wich we can choose the page of the blog that we want to visit. By submitting our choice, the site perform a POST request that has in the body of the request the parameter:

```
text=http://localhost:80/post1
```

### Credits:
- https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog repository from which I took part of the frontend code (the html structure and its interaction with flask);

- https://github.com/jakewright/tutorials/tree/master/docker/02-docker-compose repository from which I took part of the code for the docker container;

- https://secgroup.dais.unive.it/wp-content/uploads/2020/03/more_server.pdf and https://portswigger.net/web-security/ssrf nozioni teoriche e pratiche su SSRF.