# Malware As A Service (MAAS)

## Creating a Docker Stack for Deployment

At this point in time, you should have the correct runner names and tokens saved in files **1.toml**, **2.toml**, **3.toml**, and **4.toml**.  These four files will be used by the gitlab runner inside of the docker container when we stack up the entire configuration using a **docker stack**.

Before we deploy a docker stack, we need a common docker volume for file storage, and we need an appropriately formatted **docker-compose.yml** file which will be used to configure our stack.

### Step 1: Edit the Dockerfile.template, save and build the new container

Our new Dockerfile will be saved to **Dockerfile.DRAFT1** and contains these required additional steps.

* Add a new user called "runner" with the *useradd* command.
* Make a working directory called **/runner**.
* Change ownership of the **/runner** directory to "**runner:runner**" using chown.
* Uninstall/reinstall gitlab-runner within the container
* Set the working directory to **/runner**
* Copy all of the "**config_toml**" directory to the container **/runner** directory
* Execute the gitlab-runner as the final step of the container launch.

We take advantage of a special variable called **$TASK_SLOT** when we launch the gitlab-runner in the container which enables us to pick up a unique *.tomL* configuration file for each of the four launched containers.

Listed below is our modified **Dockerfile.DRAFT1** file which accomplishes all of the above steps.

```
FROM ubuntu:latest
RUN apt-get -qqy update
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" -o runner-script.sh
RUN chmod 755 ./runner-script.sh && ./runner-script.sh
RUN rm -f runner-script.sh
RUN apt-get install -y gitlab-runner
RUN useradd runner
RUN mkdir /runner
RUN chown -R runner:runner /runner
RUN gitlab-runner uninstall
RUN gitlab-runner install -user runner
WORKDIR /runner
COPY config_toml /runner/config_toml
CMD gitlab-runner run --working-directory /runner --config /runner/config_toml $TASK_SLOT.toml --user runner
```

### Step 2: Rebuild the **maas** docker container

Execute the appropriate Docker build command to perform this action as follows:
```
docker build -t maas -f Dockerfile.DRAFT1 .


```

### Step 3: Create/review the **docker-compose.yml** file.

Fortunately for you, I have done the legwork required to build a docker compose file which will run your 4 different containers as a docker service with a common docker volume.  Listed below is the **docker-compose.yml** file we will be using.

```
version: "3"

volumes:
  payloads:

services:
  maas:
    build:
      context: .
    image: maas:latest
    restart: always
    volumes:
        - payloads:/payloads
    environment:
        NODE_HOSTNAME: "{{.Node.Hostname}}"
        TASK_SLOT: "{{.Task.Slot}}"
    deploy:
        mode: replicated
        replicas: 4
```
