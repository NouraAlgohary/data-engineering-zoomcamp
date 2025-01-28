1. Introduction to Docker
2. Ingesting NY Taxi Data to Postgres
3. Connecting pgAdmin and Postgres
4. Dockerizing the Ingestion Script
   
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

-------------
# 3. Connecting pgAdmin and Postgres

## pgAdmin Container
pgAdmin: is a free open-source tool for manageing PostgreSQL databases.

We do not need to install pgAdmin as we have Docker and we can install pgAdmin image.

To run pgAdmin container:
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
- ```PGADMIN_DEFAULT_EMAIL``` and ```PGADMIN_DEFAULT_PASSWORD``` are the environment variable that we use to log in.
- We map port ```8080``` port at our host machine to port ```80```. All instructions that are sent to port ```8080``` will be forwarded to port ```80``` on the container.

To open pgAdmin we use the URL
```
localhost:8080
```
We can't communicate with the postgres database we created, as they are two isolated containers. We need to connect both containers using Docker Network

## Docker Network Create
```
docker network create pg-network1
```
- ```docker network create``` is the command needed to create a network followed by its name.

## Add Postgres to Docker Network
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network1 \
    --name=pg-database-new \
    postgres:13
```
- ```--network```: network name (the one we created)
- ```--name```: Postgres container name that will be used to find it by other containers.

To make sure the data sill there
```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
```
SELECT COUNT(1) FROM yellow_taxi_data
```
## Add pgAdmin to Docker Network
Now, we will run pgAdmin in the same network
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8085:80 \
  --network=pg-network1 \
  --name=pgadmin_5 \
  --memory="1g" \
  dpage/pgadmin4
```
- ```--network```: network name (the one we created)
- ```name```: pgAdmin container name.
- ```memory```: Determines how much memory to be used 

I had a problem because of the names so I tried multiple things to reach out to these.

## Create a New Server on pgAdmin

After logging into pgAdmin using the credentials you created:  
- **Email**: `admin@admin.com`  
- **Password**: `root`  

You can set up a new server to connect to your PostgreSQL database.

### Steps to Create a New Server

1. **Open pgAdmin**:  
   - Access pgAdmin in your browser at `http://localhost:8083` (or the port you mapped pgAdmin to).  

2. **Add a New Server**:  
   - In the pgAdmin dashboard, choose **Create Server**
   <img width="730" alt="Screenshot 2025-01-24 at 10 39 30 AM" src="https://github.com/user-attachments/assets/76ef4fda-21ea-45d3-aab0-dd713e1b76b6" />


3. **Fill Out the Server Details**:  
   - **General Tab**:  
     - **Name**: Choose a name for your server (e.g., `ny_taxi_server`).  
   - **Connection Tab**:  
     - **Hostname/Address**: Use the container name of your PostgreSQL database (`pg-database-new`).  
     - **Port**: `5432` (default PostgreSQL port).  
     - **Maintenance Database**: `ny_taxi` (the database you created).  
     - **Username**: `root` (the PostgreSQL username).  
     - **Password**: `root` (the PostgreSQL password).

   
<img width="730" alt="Screenshot 2025-01-24 at 11 13 14 AM" src="https://github.com/user-attachments/assets/9e2aa3d5-c243-47a0-9d99-35b78a7bb683" />

4. **Save the Configuration**:  
   - Click **Save** to create the server.  

---

### Docker Command Reference

The PostgreSQL container was created using the following command:  
```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network1 \
    --name=pg-database-new \
    postgres:13
```
--------------
# 4. Dockerizing the Ingestion Script
Currently, we manually run a Python notebook to download data and ingest it into a PostgreSQL database. To simplify this process and prepare for automation, we converted the notebook into a Python script and added it to our Dockerfile. This step lays the foundation for integrating the ingestion process into an automated pipeline in the future, making the workflow more efficient and easier to manage.

### Structuring the Script
#### 1. Turn the notebook into a Script
```
jupyter nbconvert --to=script ingesting_yellow_taxi_data.ipynb
```
- ```--to```: specifies the format we want to convert it to.
- ```ingesting_yellow_taxi_data.ipynb```: name of the new file.

#### 2. Refactor the Script 
Then, We encapsulated the core logic of the script within the main(params) function and added the if __name__ == '__main__': block to enable the script to accept command-line arguments. This structure allows the script to be executed directly with customizable parameters, making it more flexible and easier to integrate into automated workflows or pipelines.

-```main(params)```: This function contains the core logic of the script. It takes a params object (created by argparse) and uses its attributes (like user, password, host, etc.) to perform the data ingestion. This keeps the logic clean and focused.
-```if __name__ == '__main__':```: This block ensures that the script only runs when executed directly (not when imported as a module). It uses argparse to parse command-line arguments, creates a params object, and passes it to ```main(params)```.

#### 3. Testing
We can drop the table we have in the database and recreate it using this script.
```
python3 ingestion_script.py \                                                      
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
```
### Dockerize the Script


--------------
# General Commands I needed
Remove/Destroy all running and stopped containers
```
docker rm -f $(docker ps -aq) 
```

To find out information about some container like network name.
```
docker inspect {conainer_name}
```


