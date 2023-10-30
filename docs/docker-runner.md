# Malware As A Service (MAAS)

## Creating a Docker container as a GITLAB Runner

I found it very effective to execute GitLab runner inside a Docker container.
Having said this, one of the challenges to solve is that GitLab requires a unique token
per registered runner. Assuming that you will end up with multiple runners, it is
possible to register them in advance on the GitLab server and collect a file
of GitLab tokens.

After a runner is successfully registered, it will create a configuration file
which ends in a "**.toml**" extension. This file will contain the shell executor
configuration and gitlab token supplied by the gitlab server.

The steps to initially begin the runner configuration are as follows:
1. Build a Docker container with enough configuration such that the gitlab runner is installed.
2. Execute the container and manually register the runner with the intent of taking a copy of the "**.toml**" configuration file.
3. Extract the "**.toml**" configuration file and save to a file named "**1.toml**" outside of the Docker container.

I like to build my docker containers using Ubuntu. Listed below is a minimal docker file which
grabs a runner script from gitlab.com, executes it and then follows up with a package
installation of the gitlab-runner. Note: the *runner-script.sh* file is designed to add the appropriate
app package sources so that the subsequent *apt-get install* will work correctly. 

```
FROM ubuntu:latest
RUN apt-get -qqy update
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" -o runner-script.sh
RUN chmod 755 ./runner-script.sh && ./runner-script.sh
RUN apt-get install -y gitlab-runner
CMD /bin/bash
```

### Installing and registering the first GitLab runner



