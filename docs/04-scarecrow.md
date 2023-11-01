## Adding ScareCrow to the Docker Container

It is now time to make our Docker container more useful by compiling and adding the ScareCrow binary into the mix.

As usual, I have already done the heavy lifting for you and this document represents a review of the tasks I have completed as follows:

### Compile ScareCrow

1. Clone the ScareCrow Repo from https://github.com/Tylous/ScareCrow.git
2. Follow the directions to compile ScareCrow using your Linux distribution of choice. I find that Ubuntu is a good choice here.
3. Copy the **ScareCrow** binary into the repo "**runners/bin**" directory.
4. ScareCrow has a dependency of using a tool called **garble**. Optionally you can use "**go install**" to get a copy of **garble** and also copy that into the "**runners/bin**" directory.  If ScareCrow does not find **garble** it will get it and install into a "**.lib**" directory whereever ScareCrow is executed from but this will take up extra time.

### Create a revised Dockerfile

At this time, we now need to ensure that ScareCrow is able to function inside our docker container. I completed the following items in order to achieve this.

* Copied the **Dockerfile.DRAFT1** to a file named **Dockerfile.DRAFT2**.
* Added in some additional needed support tools
    * apt-get install -y wget
    * apt-get install -y p7zip-full
* Added in the additional dependencies that **ScareCrow** requires into the new dockerfile. 
    * apt-get install -y osslsigncode
    * apt-get install -y gcc-mingw-w64-x86-64-win32
    * used wget to get the latest golang and un-tarred in /usr/local
    * added some symbolic link commands so that ScareCrow finds what it needs in the current directory and search path.
    * made sure that both the /runner and the /payloads directory were owned by the **runner** user account.

Here is a full listing of the revised file named **Dockerfile.DRAFT2**.

```
FROM ubuntu:latest
RUN apt-get -qqy update
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" -o runner-script.sh
RUN chmod 755 ./runner-script.sh && ./runner-script.sh
RUN rm -f runner-script.sh
RUN apt-get install -y gitlab-runner
RUN apt-get install -y wget
RUN apt-get install -y osslsigncode
RUN apt-get install -y p7zip-full
RUN apt-get install -y gcc-mingw-w64-x86-64-win32

## add runner username
## reinstall gitlab-runner
RUN userdel gitlab-runner
RUN useradd runner -d /runner
RUN mkdir /runner
RUN mkdir /payloads
RUN gitlab-runner uninstall
RUN gitlab-runner install -user runner

## Install golang and copy files
WORKDIR /runner
RUN wget https://go.dev/dl/go1.21.3.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.21.3.linux-amd64.tar.gz
RUN rm -f go1.21.3.linux-amd64.tar.gz
COPY config_toml /etc/config_toml
COPY bin /usr/local/bin
RUN ln -s /usr/local/go/bin/go /usr/local/bin/go
#
RUN chown -R runner:runner /runner
RUN chown -R runner:runner /payloads
CMD gitlab-runner run --working-directory /runner --config /etc/config_toml/$TASK_SLOT.toml --user runner

```




