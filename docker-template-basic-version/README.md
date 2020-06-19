# Challenges Package Template

We deploy each challenge as a **single** [docker](https://docs.docker.com/get-docker/) container. This package contains everything that is needed for the challenge to run.

This template packages a `flask/python3` application and a bot based on `headless firefox`.

## tl;dr

- Write the challenge information in the [metadata.yaml](./metadata.yaml) file
- Install everything into the same container: application, database and bot
- Expose a single HTTP port (preferably port `80`)
- Make sure that the container still works without an Internet connection

The next sections will give a more in depth description of the template. Note however that it is not mandatory to use this template: every container image that satisfies the above requirements can be deployed on the **seclab** server.

## Metadata

Challenge metadata is written in the [metadata.yaml](./metadata.yaml) file. 

|||
--- | ---
**name** | Name of the challenge
**description** | *HTML formatted* description of the challenge
**tags** | List of tags to be displayed in the challenge page
**points** | Bonus points for the challenge (`0.5`)
**flag** | Challenge flag
**network_info** |
**.hostname** | Public hostname of the challenge (must be a subdomain of seclab.dais.unive.it)
**.port** | Public port (default `443`: a reverse proxy will atomatically handle the HTTPS certificates)
**.container_port** | Port exposed by the container


## Dockerfile

A dockerfile describes all the instructions that are needed to build a container image. A dockerfile must start with a `FROM` instruction that defines the parent image, on which all the subsequent commands are executed.

In this example, we are starting form the `18.04 LTS` release of the `ubuntu` distribution and we are installing everything we need with the `apt` package manager.

```dockerfile
FROM ubuntu:18.04
ENV BOT_URL=https://example.seclab.dais.unive.it
RUN apt-get update && apt-get install -y uwsgi python3 ...
...
```

The `ENV` instruction defines an environment variable that will be available both during the build and during run-time.

The rest of the dockerfile creates the `example` user and installs the application into its own virtual environment in `/home/example`; then it creates the `selenium` user and installs the bot into the `/home/selenium` folder; finally it sets-up the container entrypoint.

The resulting image will expose the application via HTTP on port `80`.

> ### PHP applications
> 
> For PHP applications you can optionally use the [mattrayner/lamp:latest-1804](https://github.com/mattrayner/docker-lamp) image as parent image. This image contains a standard LAMP stack with Apache, MySQL and PHP. Every php file that is placed in the `/app` folder is served by apache on port `80`.
> 
> ```dockerfile
> FROM mattrayner/lamp:latest-1804
> # Add your php files into the /app folder
> ADD ./index.php /app
> CMD ["/run.sh"]
> ```
> You can refer to the [project page](https://github.com/mattrayner/docker-lamp) for more information.

### Bot

The [bot](./bot/bot.py) for this challenge is a simple selenium-webdriver script that starts the headless version of Firefox, logs into the website as admin and waits five second before exiting.
The bot script is run every 4 second by a [wrapper script](./bot/bot.sh) whose main responsibility is to periodically run the bot making sure that each run does not share profile information (sessions, cookies, etc...).



#### Connections to `localhost`

The bot connects to the URL specified in the `BOT_URL` environment variable that we defined at line 2 of the [Dockerfile](./Dockerfile).

In production, `BOT_URL` points to a public website, as it is mandatory for the bot to connect to the challenge the same way regular users connect to it. This is the case because of the SOP: if we set, for example, `BOT_URL` to `http://localhost`, the bot would be in the `http://localhost` origin instead of the one regular users are browsing.

Setting `BOT_URL` to a public website, however, means that the bot need to access the Internet to be able to reach the challenge. This is not always the case, as the **seclab** server drops any connection to the Internet from internal networks.

This issue is solved by making use of the `/etc/hosts` file and mapping the `BOT_URL` hostname to `127.0.0.1`, so that the bot will connect to `localhost` using the external URL.

> For this reason, we update the `/etc/hosts` file in the container entrypoint (`CMD`) if the mapping is not present.
> 
> ```dockerfile
> CMD (grep "${BOT_URL#*//}" /etc/hosts || echo "127.0.0.1 ${BOT_URL#*//}" >> /etc/hosts) 
>  && ...
> ```

If the challenge is deployed behind an HTTPS reverse proxy (as it is usually done for **seclab** challenges), the bot needs to connect to the HTTPS version of the website so that the SOP is not violated.
As an example, let's consider the case in which

- `BOT_URL` is `https://example.seclab.dais.unive.it` (← HTTPS)
- `example.seclab.dais.unive.it` is mapped to `127.0.0.1` in `/etc/hosts`
- The web application listens on port `80`

When the bot tries to connect to `BOT_URL` with HTTPS it connects to port `443` of `127.0.0.1`. Since there is no service running on that port the connection is refused.

Our application accepts only HTTP connections, as HTTPS is handled externally by the **seclab** reverse proxy, but we still want the bot to connect locally using HTTPS.
For this reason we need to start a local HTTPS proxy that listens of port `443` and forwards the connections to port `80`.
This is done using the `socat` utility (see [supervisor.conf](./supervisor.conf) and the next section for information on how this command is run in the container):
```
socat OPENSSL-LISTEN:443,reuseaddr,pf=ip4,fork,cert=/etc/ssl/certs/ssl-cert-snakeoil.pem,key=/etc/ssl/private/ssl-cert-snakeoil.key,verify=0,cipher=HIGH:MD5:3DES TCP4:127.0.0.1:80
```

With this `socat` proxy in place we can change the `BOT_URL` however we like and the bot can still reach the application: if the url is an HTTP url the bot connects directly to the service, whereas if the url is an HTTPS url the bot connects to the service through the `socat` proxy.


> #### Public Resources and CDNs
> **Warning**: avoid using public resources or CDNs in your html templates!
> Since the bot will **not** have access to the Internet, you need to bundle every resource that is needed for the challenge to load into the challenge package. The recommended solution is to make a `/static` folder and refer only to this folder in &lt;script&gt;, &lt;img&gt;, &lt;style&gt; (etc...) tags.

### Putting All Together: Supervisor

Multiple programs can be run in a single container using a process control system, which starts and monitors the execution of the different daemons. 
[Supervisord](http://supervisord.org/) is the most used process manager in docker deployments and it is configured by means of a configuration file ([supervisor.conf](./supervisor.conf)).

General settings are specified in the `[supervisord]` section.
Each program needs its own `[program:]` definition. As an example, the following snippet configures supervisord to run our python application using [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/):

```ini
[program:uwsgi]
command=/usr/bin/uwsgi --plugin python36 --module 'app:create_app()' --venv /home/example/.venvs/example --vacuum --http-socket '0.0.0.0:80' --chdir /home/example
autostart=true
autorestart=true
user=example
group=example
directory=/home/example
environment=INSTANCE_PATH="/home/example/instance"
```

Most of the fields are self-explanatory: we are running `uwsgi` passing command line arguments; the program is executed as user:group `example:example` in the `/home/example` directory; we are creating an environment variable `INSTANCE_PATH` and we are asking supervisord to restart the program on failure.

The `[program:bot]` and `[program:proxy]` sections respectively configure supervisord to run the bot and the `socat` HTTPS proxy that is mentioned in the previous section.

## Testing the Container

```sh
$ docker build -t challenge-template .
$ docker run --rm -ti -p 80:80 challenge-template
```

You can connect to the challenge at `localhost:80`. 
Note that if the application is listening on a different port the `-p` option need to be changed accordingly (e.g., `-p 80:5000` if the app listens on port `5000`). It is recommended, however, to make the container always listen on port `80`.

## Extra

### Multi-Stage Builds

Optionally you can use [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to create the container. As an example, if your application is written in PHP, you can run [composer](https://getcomposer.org/) in its own build stage and then copy the generated `vendor` folder in the final image. This way the composer executable and its dependencies do not need to be installed in the challenge container:

```docker
# This build stage generates the `/app/vendor` folder
FROM composer as deps
ADD ./app/composer.json ./app/composer.lock /app/
RUN composer install --ignore-platform-reqs --no-scripts

# Final Container
FROM php:7
ADD ./app/ /var/www/html/
# Copy the `/app/vendor` folder from the `deps` build stage
COPY --from=deps /app/vendor/ /var/www/html/vendor/
WORKDIR /app
CMD "php -S 0.0.0.0:80"
```
