## Going Parallel

Because we have deployed multiple docker containers on our backend infrastructure,
we have the processing capability of executing pipeline jobs in parallel.
If the Gitlab configuration has different jobs listed in the same stage without any dependencies,
it will leverage concurrency to execute those jobs.

We have two different places in our architecture to take advantage of concurrency.
* First of all there is a concurrency setting in each gitlab runner **toml** configuration file.
* Secondly we can take advantage of the multiple containers that are deployed also.

For the sake of this exercise, we are going to follow these detailed steps.

1. Edit the **toml** configuration files and increased the concurrency setting to 2.
2. Redeploy the docker services to reflect the changes.
3. Edit the pipeline YAML file and configure four parallel jobs with a different ScareCrow malware command in each of the four jobs.
4. Execute the pipeline and observe the parallel jobs in action.

### Step 1: Changing the TOML configuration files

We already produced the TOML files to stand up our stack, so this step is as simple as editing each of the files and changing the concurreny option to 2.  Listed below is one of these files and as you can observe, it is very clear that concurrency is set to one and can be edited for our purposes.

![Alt text](image.png)

We can proceed with editing each of the TOML files and updating this number. This has in fact already been completed for you.

