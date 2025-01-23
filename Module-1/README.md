1. Introduction to Docker
2. Ingesting NY Taxi Data to Postgres
# 1. Introduction to Docker

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
 ----------------------------------
 # 2. Ingesting NY Taxi Data to Postgres
- Data ingestion: is the process of collecting, importing, and transferring data from various sources into a system (like a database) for storage, processing, or analysis.
- Required: jupyter, pgcli, SQLAlchemy

## Running Postgres in a container
This is a containerized version of Postgres(No installation required). <br /> 
:one:
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```
- ```e```: declares *environmental variables* 
    - ```POSTGRES_USER```: Sets the database superuser.
    - ```POSTGRES_PASSWORD```: Sets the password for the superuser.
    - ````POSTGRES_DB```: Creates a default database.
- ```v```: declares volume path to persist data ```A:B```
    - A is a directory on your local machine where the data will be stored.
    - B is the directory in the container where the database stores its data.
- ```p```: Maps a port on your local machine to the container.

To log into the postgres database, we can use this command<br /> 
:two: 
```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
- ```-h```: the host (localhost in this case)
- ```-p```: port number
- ```-u```: username
- ```-d```: databse name
Then we can enter the password when requested.

Run some simple Postgres queries.<br /> 
:three:
- ```\dt```: shows all tables in the db.
<img width="305" alt="Screenshot 2025-01-23 at 9 44 39 AM" src="https://github.com/user-attachments/assets/ec98b9d2-6256-464a-a733-e4ac481503a6" />

- ```SELECT 1```

## Using Python to ingest data to Postgres
We want to get the data from the original website, create the structure of the table, and finally load the data into the table.
1. Download the data.
```
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
```
2. Check data using number of lines
```
wc -l yellow_tripdata_2021-01.parquet                     
```
-```wc```: Count words.
- ```-l```: Instead of count words, count lines.

3. Import data into jupyter notebook
```
jupyter notebook
```
This opens jupyter,then we can upload our dataset,then create a new notebook and write this code.
```
import pandas as pd

yellow_taxi_data = pd.read_parquet('yellow_tripdata_2021-01.parquet')

yellow_taxi_data.to_csv('yellow_tripdata_2021-01.csv', index=False)

yellow_taxi_data.head()
```
<img width="722" alt="Screenshot 2025-01-23 at 11 04 55 AM" src="https://github.com/user-attachments/assets/f702bdb5-1a66-4f58-98af-0312af38280d" />

<img width="501" alt="Screenshot 2025-01-23 at 11 04 01 AM" src="https://github.com/user-attachments/assets/55feeace-0a6a-4acb-839f-5820cbca0f68" />

In 2025, data is provided as ```PARQUET```, so I coverted it into ```csv``` because its easier for me.

4. Create a schema for the dataset in Postgres
```
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

engine.connect()

pd.io.get_schema(yellow_taxi_data, name="yellow_taxi_data")
```
- ```from sqlalchemy import create_engine```: Imports the create_engine function from the sqlalchemy library, which is used to create a database connection.
- ```engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')```: Creates a connection to a PostgreSQL database as '{database type}://{username}:{password}@{host}:{port}/{database name}'
- ```engine.connect()```: Establishes a connection to the database using the engine object.
- ```pd.io.get_schema(yellow_taxi_data, name="yellow_taxi_data")```: Generates SQL schema with the same table structure as ```yellow_taxi_data``` and specifies the table name "yellow_taxi_data"

## Write DataFrame to a SQL table in the Database
In the last part we created a SQL table statement that is useful for insepecting or manually creating a table in the database, however we want to write the dataframe into database directly.

In the video, Alexey divided the dataset into chuncks while loading it, but as I already loaded the whole dataset, I will divide it into smaller batches for the insertion into database process. (I am not sure if this is the best practice)

```
df_structure = yellow_taxi_data.head(0)

df_structure.to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")
```
- ```df.head(n)```: Shows the first n rows of the dataframe. We want only the structure or the first 0 rows.
- ```df_structure.to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")```: Creates a table using the engine we specified named "yellow_taxi_data". ```if_exists="replace"```: if there is another table with the same name, replace it.

I want to check if the table is created in the database so I returned to PostgreSQL.

```
\dt
```
<img width="335" alt="Screenshot 2025-01-23 at 9 44 54 AM" src="https://github.com/user-attachments/assets/9f6389c6-81e9-4b7f-87bd-55c57f0bcf36" />


## Insert data into the database table
```
i = 0
chunk_size = 10000

while i < len(yellow_taxi_data):
    t_start = time.time()

    yellow_taxi_data[i:i + chunk_size].to_sql(
        name="yellow_taxi_data", 
        con=engine, 
        if_exists="append"
    )

    i += chunk_size
    t_end = time.time()

    print('Inserted another chunk... took %.3f second(s)' % (t_end - t_start))

print("Insertion is compelete")
```
- Inserts data from yellow_taxi_data (likely a DataFrame) into a SQL table in chunks of 10,000 rows.
- ```if_exists="append"```: Adds new rows to the existing table without deleting previous data.Why not replace? replace would delete the existing table and recreate it, losing all previous data.
- Time is recorded before and after each insertion to print how much time it took
<img width="383" alt="Screenshot 2025-01-23 at 11 13 08 AM" src="https://github.com/user-attachments/assets/c8b04c51-1c95-4b24-b2df-d2cdbe41ae63" />

 <br /> 
 
Check Number of Rows
```
SELECT COUNT(*) FROM yellow_taxi_data
```
<img width="462" alt="Screenshot 2025-01-23 at 10 28 15 AM" src="https://github.com/user-attachments/assets/b2ad50fd-7537-4b94-a07e-d5dd51288004" />


To print first 10 rows of data 
```
SELECT *
FROM yellow_taxi_data
LIMIT 10
```
<img width="581" alt="Screenshot 2025-01-23 at 10 38 58 AM" src="https://github.com/user-attachments/assets/3a0c5724-535e-4b2b-b842-0b52cf7742a7" />

--------------
Remove/Destroy all running and stopped containers
```
docker rm -f $(docker ps -aq) 
```

