# Vivanta Python Lambda Template
## Warning: Python 3.8 is used in lambdas

## Setup
  - Set up the `image` and `container_name` in `docker-compose.yaml`(ommit -environment names in this step)
  - Choose an available port and set in `docker-compose.yaml` (default: 9001)
  - Do `docker-compose up -d` to launch it
  - If you needd a connection with the database, create a `.env` file at the root and define your connection variables, also you will need to set up the connection between the containers by using `docker network connect {network-name} {db-container-name}`. A default network to bridge this container with any other would be created by the composer file with a name of `{container-name}_lambda_postgres_network`


Go like this to update: docker-compose down && docker-compose up -d
(for local dev) Connect DB with network like this docker network connect vivanta-whoop-initialization_lambda_postgres_network vivanta_db
use requirements.txt to add libraries

## Testing
You can test this lambda by calling the following endpoint with a POST request
```http://localhost:{port-in-docker-compose-yaml}/2015-03-31/functions/function/invocations```

If you want to see the logs, use `tail -f docker logs` to keep them open (or use Docker GUI)


## Building project for lambdas
- Run `bash deployment.sh`, and folow the prompts. If you don't have a URI for the container, just leave it blank and set it in `deployment.sh` file after you obtain it in your first run
