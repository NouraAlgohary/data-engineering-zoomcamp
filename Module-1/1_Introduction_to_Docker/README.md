# Introduction to Docker

## Discover Docker 
#### Ex1
After installing docker, we need to validate that it runs properly
```
docker run hello-world
```
- hello-world is a pre-installed docker image
- This will open Docker Hub, search for the image and download required packages

#### Ex2
Another example is to open ubuntu bash 
```
docker run -it ubuntu bash
```
- ```-it```: is used for interactive mode (like to open bash command that receives commands after the image is runned)
- ```rm -rf /```: deletes everything fom our image container only, but not from other containers 
```
exit
```
exits the image

#### Ex3
```
docker run -it python:3.9
```
- This command opens a python image ```image:version```
- It uses python shell, so we can't use bash command to install packages

```
docker run -it entrypoint:bash python:3.9
```
- The entrypoint in Docker is like the ```__main__``` function in Python, it defines where the container starts.
- By setting entrypoint bash, the container starts with a Bash shell instead of the default Python interpreter.
- From the Bash shell, you can run python to open the Python shell.
python

## Build Docker images
#### Ex4
Now, I want to build my own Docker image with customized configurations. However, using a manual setup is not the best choice for several reasons:

**Why Manual Setup is Not Ideal:**
- Not Reproducible: Manual steps are hard to repeat or document.
- No Version Control: Changes cannot be tracked or rolled back.
- Time-Consuming: Requires repeating commands every time.
- Inconsistent: Environments may differ across setups.
- No Layered Builds: Lacks Docker’s caching for faster rebuilds.
- Hard to Share: Difficult to share exact setups with others.
- No Scalability: Manual setups don’t scale for multiple containers.
- No Documentation: No clear record of the environment setup. 

So, I create a Dockerfile using some editor <br /><br />
_Dockerfile_
```
FROM python:3.9

RUN pip install pandas

ENTRYPOINT ["bash"]
```
- ```FROM```: image name
- ```RUN```: runs the command we want when the image starts
- ```ENTRYPOINT```: declares the entrypoint using a list of arguments

```
docker build -t image1:v1 .
```
- ```build```: builds an image from a file called (_Dockerfile_)
- ```-t```: enables to put a tag for the image (```image:tag```), and we can use a tag as a version for the image
- ```.```: builds an image in the current directory

```
docker run -it image1:v1
```
- runs the image we've created earlier


## Build a docker container to run a data pipeline (python script)
A Data Pipeline is a series of processing steps that is used to automate the flow of data.
_pipeline.py_
```
import pandas as pd

print("Pandas installation was successful! Yeah!")
```

_Dockerfile_
```
FROM python:3.9

RUN pip install pandas

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT ["bash"]
```
- ```WORKDIR```: it sets the current directory into the container we build, so we do not need to manually navigate to the script's location
- ```COPY```: copies the script from local computer to the container we buils making it available to run inside the container

## Passing arguments and Running the script 
_pipeline.py_
```
import sys
import pandas as pd

print(sys.argv)

# sys.argv[0] --> file name
# sys.argv[1] --> first argument
day = sys.argv[1]

print(f"job finished successfully for for day = {day}")
```
_Dockerfile_
```
FROM python:3.9

RUN pip install pandas
WORKDR /app
COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]
```
- Instead of starting a Bash shell (```ENTRYPOINT ["bash"]```), Arguments List is modified to run python as soon as the container is run
- ```["python", "pipeline.py"]```: Specifies the command and its arguments.
- ```python```: The command to run the Python interpreter.
- ```pipeline.py```: The script to execute.

```
docker build -t image3:v1 .
```
```
docker build -it image3:v1 22-01-2025
```
- the date is our arguement
