# MAAS

## Getting started

In todays modern defense stack environment, penetration testers are faced with significant obstacles for initial access operations. There are many technologies deployed in environments design to thwart attempts at executing various binary artifacts on an endpoint and prevent initial access from succeeding.

Having said this, the best approach to tackling a good defense is to come prepared with a better offense!  This project describes a DevOps approach I have named "Malware As A Service" which leverages the CI/CD capabilities of the community gitlab software to build a malware artifact generation pipeline.

Here at Black Hills Information Security, after presenting this concept at Wild West Hackin' Fest, I believe that the work presented here makes me the unofficial "father of malware as a service", and that other penetration testing companies can benefit from this work.

## The Challenge

As penetration testers, we must produce unique, highly evasive and successful artifacts for initial access operations of Red Team and assumed compromise style engagements. In short, we are tasked with emulating real world threat actors and must use sophisticated malware techniques to be successful.

The MAAS approach allows us to address the significant challenges we face today which include the following:
* Not all penetration testers want to be developers.
* The quality of various Proof of Concept (POC) source code on the Internet varies widely, and in many cases is of low quality.
* Static artifact analysis as a first line of defense will defeat many compiled POC entities.
* Defense vendors leveraging Windows kernel callback notifications to dynamically respond to suspicious processes.
* Defense vendors now employing sophisticated analysis techniques including but not limited to:
    * Subscribing to Event Tracing for Windows
    * Memory page scanning
    * Stack call back tracing and analysis
    * Process tree analysis
    * Windows DLL API hooking
    * Kernel driver block listing

* There are a number of developers who provide malware frameworks out there but there is a tendency to use default switches, and not customize to fit a target customer profile.





## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing


## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
This project is licensed with the MIT License.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
