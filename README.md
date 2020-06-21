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

Typically, SSRF targets the vulnerable application or other back-end services, that work with the vulnerable application, to make privilege escalation and perform unauthorized actions.

## Methodology

In the home page there is a drop down menu in which we can choose the page of the blog that we want to visit. By submitting our choice, the site perform a POST request that has in the body of the request the parameter:

```
text=http://localhost:80/post1
```

This payload forward the request directly to the servers form the inside of the docker machine, so through this parameter we can forge a request directly to the server not visible from the Internet, so we perform a privilege escalation.

## Attack

Through the parameter shown in the previous section, we forge a request to the server sitting on 'http://localhost:5001':

```
text=http://localhost:5001
```

Then, we get the response page:

```
Admin backend
```

so our basic SSRF was successful, now we can simply append the enpoind 'admin' to the request for recover the flag.

This is the solution to the basic version of the ctf challenge, but for the black-whitelist version of the challenge we have to play a little more with the body of the request.

## Solution

### Whitelist fixing

Don't perform whitelisting by yourself but using a library for perform the parsing and the opening of the url, for example urllib.parse and urllib.request that, in python3, also solve some vulnerability of their previous version, like:

```
http://1.1.1.1 &@2.2.2.2# @3.3.3.3/
      [urllib2] [request]  [urllib]
```

(Orange Tsai;
A new era of ssrf - exploiting url parser in trending programming
languages!;
Black Hat 2017)

### General fixing

One possible fix to this vulnerability could be change the action of the drop down menu by performing a POST request to a specific endpoint (and not to an arbitrary url passed by parameter), with its associated function in the server, that return the blog's page required.

## Credits:
- https://github.com/jakewright/tutorials/tree/master/docker/02-docker-compose repository from which I took part of the code for the docker container;

- https://secgroup.dais.unive.it/wp-content/uploads/2020/03/more_server.pdf and https://portswigger.net/web-security/ssrf nozioni teoriche e pratiche su SSRF.