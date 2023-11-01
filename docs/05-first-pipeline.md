## Your First CI/CD Pipeline

We are now ready to write our first CI/CD pipeline. CI/CD pipelines in Gitlab use a YAML configuration file which is saved in the root directory of a repository and named "**.gitlab-ci.yml**".

The documentation for the grammar used in this YAML file is located here at https://docs.gitlab.com/ee/ci/.

For this first effort, I have created a three stage pipeline that will generate some ScareCrow malware payload artifacts, ZIP them up and make available after the pipeline run completes.

Gitlab will automatically create a standard ZIP file for any artifacts that exist at the end of a pipeline run, however I like to use a 7Zip file within the outer ZIP file so that I can apply a passphrase.

### Pipeline Stages

In a typical CI/CD pipeline we would see stages such as *build*, *test*, and *deploy* for example. For our purposes we have a similar arrangement however we are not really doing any testing in this initial effort.

I am going to name our pipeline stages:
* PreProcess
* BakeMalware
* PostProcess

It is useful to know that Gitlab CI/CD will predefine a number of environment variables which we can leverage within our pipeline YAML file. These environment variables are documented here at https://docs.gitlab.com/ee/ci/variables/predefined_variables.html.

For the purposes of our pipeline, we make use of the **$CI_COMMIT_SHORT_SHA** variable to create a unique directory for each run of the pipeline.

**PreProcess** will be used to prepare the ground.  It might be some directory structure we need to create, or anything else we think we need before creating the malware payload itself.  In our case, we are creating a directory and creating a symbolic link to the **garble** binary so that ScareCrow will not have to download it.

**BakeMalware** will be used to actually execute ScareCrow a number of times in order to create the required binary artifacts we desire.

**PostProcess** will be used for 7ZIP archive creation purposes. The 7ZIP archive will be created in a directory which is then further zipped and made available as an artifact to download when the pipeline completes.

### The Pipeline Trigger

It is typically for a CI/CD pipeline to be triggered whenever a "**git commit**" occurs, however we can exert a little more control over this using a *workflow* statement in our YAML file.

For the purposes of generating malware loaders, we will need to supply some shellcode, thus we create a "**shellcode**" directory and configure the workflow such that any file changes in the "**shellcode**" directory will trigger a pipeline run.



