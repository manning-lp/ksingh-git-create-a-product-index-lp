# create-a-product-index-lp-author
Repository for liveProject: Create a Product Index

## Contents
The initial setup of the project contains the files you need to run the complete setup:
- config/shoes_index.json: The template for the shoe index configuration, used when creating a new index
- data/shoes.mjson:  Contains a valid json document on each line representing one shoe per line.
- infra/docker-compose.yml: A Docker compose file for the containers running Elasticsearch and Kibana. Both contains expose an http port. That way you can use your browser against _localhost_ to interact with the containers.
- infra/.env: Specifies the version of Elasticsearch and Kibana to use
- modules/importer/importer.py: code to handle importing the sneaker data
- modules/search/search.py: code to interact with Elasticsearch
- modules/log_config.py: configures the logging system in our python project
- Dockerfile-importer: Docker specification file to run the importer using Docker
- README.md: This file
- requirements.txt: Contains the libraries used by this project. Use this to setup your local python environment
- run_importer.py: Used by the Docker container, but also possible to use from your local python environment to run the importer

## Running the project
### Running Elasticsearch and Kibana
You can start Elasticsearch and Kibana using the provided docker-compose.yml file. Of course you need to have docker
installed on your system. With the more recent Docker installs you start the cluster with the following command:
```shell
    docker compose up
```
The environment configuration, like version of Elasticsearch and Kibana, is defined in the .env file. The ports of 
Elasticsearch (_9200_) and Kibana (_5601_) are expose to the local operating system. Therefore you can access them using
_localhost_.

Check if the elasticsearch cluster is running using your browser: http://localhost:9200 and http://localhost:5601. A 
direct link to the Kibana console that we use a lot is http://localhost:5601/app/dev_tools#/console.

### Running the importer
There are two ways to run the importer. The first one is to run the importer directly from the command line or from 
your IDE. The second way is using Docker. If you are used to Python, using virtual environments, that is faster and 
easier during development.
#### Using python directly
The importer is a Python script that you can run from the command line. The following command will run the importer:
```shell
    python run_importer.py
```
#### Using Docker
The first step is to create a Docker image for the importer. The following command will create the image:
```shell
    docker build -t sneakers-to-the-max-importer -f Dockerfile-importer .
```
The image can be used to run the importer. The following command will run the importer:
```shell
    docker run --network infra_es-net --env ELASTICSEARCH_HOST=http://es-container:9200 sneakers-to-the-max-importer
```

## Setting up your python local environment
You can find more information about using python virtual environments here:
https://docs.python.org/3/tutorial/venv.html

Using the following commands works on most linux based systems:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
