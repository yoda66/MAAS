## Adding ScareCrow to the Docker Container

It is now time to make our Docker container more useful by compiling and adding the ScareCrow binary into the mix.

As usual, I have already done the heavy lifting for you and this document represents a review of the tasks I have completed as follows:

1. Compile ScareCrow
2. Create a Revised Dockerfile
3. Rebuild the container and test ScareCrow
4. Re-deploy the Docker Stack


### Compile ScareCrow

* Clone the ScareCrow Repo from https://github.com/Tylous/ScareCrow.git
* Follow the directions to compile ScareCrow using your Linux distribution of choice. I find that Ubuntu is a good choice here.
* Copy the **ScareCrow** binary into the repo "**runners/bin**" directory.
* ScareCrow has a dependency of using a tool called **garble**. Optionally you can use "**go install**" to get a copy of **garble** and also copy that into the "**runners/bin**" directory.  If ScareCrow does not find **garble** it will get it and install into a "**.lib**" directory whereever ScareCrow is executed from but this will take up extra time.

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

### Rebuild the Container and Test ScareCrow

After we build the container, we are going to execute it in interactive mode, and mount the shared *payloads* volume.  Within the container the **/runner** directory is where the GitLab server will checkout our repo for CI/CD pipeline purposes, and the **/payloads** shared volume is where we will write our built payloads from **ScareCrow**.

Assuming success, we should see the output below as we test.

```
$ docker build -t maas -f Dockerfile.DRAFT2 .
<... output omitted ...>

$ docker run -v maas_payloads:/payloads -it maas /bin/bash

root@32cde439576b:/runner# cd /payloads/
root@32cde439576b:/payloads# echo "stuff" >shellcode
root@32cde439576b:/payloads# ScareCrow -I shellcode -Loader binary -nosign

  _________                           _________
 /   _____/ ____ _____ _______   ____ \_   ___ \_______  ______  _  __
 \_____  \_/ ___\\__  \\_  __ \_/ __ \/    \  \/\_  __ \/  _ \ \/ \/ /
 /        \  \___ / __ \|  | \/\  ___/\     \____|  | \(  <_> )     /
/_______  /\___  >____  /__|    \___  >\______  /|__|   \____/ \/\_/
        \/     \/     \/            \/        \/
                                                        (@Tyl0us)
        “Fear, you must understand is more than a mere obstacle.
        Fear is a TEACHER. the first one you ever had.”

[*] Encrypting Shellcode Using ELZMA Encryption
[+] Shellcode Encrypted
[+] Patched ETW Enabled
[+] Patched AMSI Enabled
[+] Sleep Timer set for 2416 milliseconds
[*] Creating an Embedded Resource File
[+] Created Embedded Resource File With OneDrive's Properties
[*] Compiling Payload
[+] Payload Compiled
[+] Binary Compiled
[!] Sha256 hash of OneDrive.exe: a4db52706d35e4dffe8421ae1b22e3852a49ca3b5726fd494e10ac699818ccf1

```

### Redeploy the Docker Stack

After you have verified that the container builds successfully and that ScareCrow is working as expected, you will need to redeploy the docker stack.  Note that when you remove a running stack, it takes a little bit of time for docker to kill all of the containers so you will wait for about 30 seconds before deploying the stack again otherwise you will see errors when the stack attempts to configure the network backend.

Use the following commands:

```
$ docker stack rm maas
Removing service maas_maas
Removing network maas_default

$ sleep 30

$ docker stack deploy -c docker-compose.yml maas
Ignoring unsupported options: build, restart
Creating network maas_default
Creating service maas_maas

```





