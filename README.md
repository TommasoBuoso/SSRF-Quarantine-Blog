# SSRF - Quarantine blog
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
