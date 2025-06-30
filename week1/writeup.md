## Task 1: Containerizing a Flask Web Application

I began with a simple Flask-based To-Do list application that uses a SQLite database. The first step was to create a Dockerfile to define the application's environment.

Key Dockerfile Steps:

FROM python:3.11-slim: Started with an official, lightweight Python base image to ensure a consistent runtime.

WORKDIR /app: Established a clean working directory inside the container.

COPY requirements.txt . & RUN pip install ...: Used a layered approach to copy and install dependencies, leveraging Docker's build cache for faster rebuilds.

COPY . .: Copied the application source code into the image.

CMD ["flask", "run"]: Initially used the built-in Flask development server to get the app running.

Achieving Data Persistence with Volumes

The SQLite database is a single file (test.db). When a container is removed, all its data is lost. To solve this, I used a Docker Volume to map the database file from the container to my host machine.

i tested it initially with docker run commnd:

```
docker run -v $(pwd)/test.db:/app/test.db my-app
```

Moving to a Production Server with Gunicorn

The Flask development server is not suitable for production. I upgraded the application to use Gunicorn, a robust, production-ready WSGI server.

Added gunicorn to requirements.txt.

Modified the Dockerfile's CMD instruction:

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

Live-Reloading and Development via Bind Mounts

To speed up development, I needed to see code changes without constantly rebuilding the image. I implemented a bind mount, which creates a live link between my local source code and the code inside the running container.

i even mde a Docker-compose.yml file

```
services:
  task-app:
    build: .
    volumes:
      # This line maps my current project directory to the /app directory
      # inside the container, enabling live-reloading.
      - .:/app
```

Dynamic Configuration with Environment Variables

I modified the application to change its appearance based on an environment variable (APP_ENV).

Python (app.py): Used os.environ.get('APP_ENV', 'development') to read the variable.

HTML (index.html): Used Jinja2's {% if app_env == 'production' %} to dynamically render different titles and headers.

Docker Compose: Injected the variable into the container.

```
services:
  task-app:
    # ...
    environment:
      - APP_ENV=production
```

This allowed me to toggle the application's behavior between "development" and "production" modes simply by changing one line in the compose file.



## Task 2: Permissions Management and Container Security

Instead of applying these principles to the Flask app, I created a new, dedicated Dockerfile to build a secure shell server using socat (a powerful version of netcat).

Dockerfile:

RUN useradd -ms /bin/bash user: Created a dedicated, non-root user named user.

chown user:user /home/editable: Created a specific "sandbox" directory and gave ownership to the user.

CMD ["socat", ..., "EXEC:'su -s /bin/bash user'"]: The startup command starts a listening server that, upon connection, forces the client into a shell running as the unprivileged user.


Testing the "Jailed" Environment

After building and running the container, I connected to it and confirmed the security was effective:

whoami confirmed I was user, not root.

I could create and delete files only within the /home/editable sandbox.

apt-get update failed with Permission Denied, proving I could not install malicious software.

su - root failed with Authentication Failure, proving privilege escalation was not possible.



## Task 3: Multi-Container Networking

I created a project with two distinct services, a client and a server, each with its own Dockerfile. A docker-compose.yml file was used to define the entire system.

Custom Network: A top-level networks block was defined to create a private bridge network named my-net.

```
networks:
  my-net:
    driver: bridge
    ipam:
      config:
        - subnet: 10.10.0.0/16
```

Service Connection: Both the client and server services were configured to join this network.

Static IPs: Each service was assigned a predictable, static IP address within the subnet (10.10.0.5 and 10.10.0.6), making them easy to find.

The entire environment was launched with a single docker compose up command. The test was then performed:

Used docker exec -it shell-client /bin/sh to get a shell inside the client container.
From the client's shell, I ran nc 10.10.0.6 1234 to connect to the server's static IP.
