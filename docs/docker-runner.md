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

