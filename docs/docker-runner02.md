# Malware As A Service (MAAS)

## Configuring Four Unique Gitlab Runners

Now we are going to use the **template.toml** file to create four different files in our **config_toml** directory.  Each of these configuration files will have identical configuration except the gitlab token used, and the **name** field.  In addition we will remove the **id** field in each configuration file.

The goal is to generate four unique configuration files to be used with four different running containers.

1. Goto the GitLab repo CI/CD settings by selecting Settings->CICD->Runners.
2. Click on **New Project Runner** to create a new gitlab runner.
    * select Linux as the operating system
    * type in a TAG named "**maas**"
    * Do NOT select the **run untagged jobs** checkbox.
    * click on **Create Runner**
    * copy the GitLab Token and save it to a file.
3. Repeat the above steps four times, saving the new token to your file each time.

