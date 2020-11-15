## Tracking Number of People at Golden Earthtreks Climibing Gym
My attempt at tracking the number of people currently in my gym to avoid large crowds.

### Requirements
  - Python3 
  - Docker
  - Raspberry Pi 4
  - Raspian Desktop OS
  - USB Mouse and Keyboard  
  - Low voltage Labs Pi Traffic Light 

### Project Steps
1. Attach traffic lights to GPIO 9, 10, 11
2. SSH into pi or plug pi into display with keyboard open a terminal session
3. Clone this repository 
3. Install docker and set up Postgres image
I used Docker to create a Postgres database from the CLI. The first step is to install docker. Refer to the docker documentation here: 
    - https://docs.docker.com/engine/install/debian/
After you have installed Docker, create a Docker Postgres image. Type the following command into the CLI: 
    - `$ docker run --name pgserv -d -p 5432:5432 -v "$PWD":/home/data -e POSTGRES_PASSWORD='password' postgres`
    - This will CREATE and START the docker image 
      - In the future, type this command into the CLI to start the docker image: `docker start pgserv`
5 Create database and table for data landing place
Once the docker image has been created, use this command to login to the Postgres CLI: 
    -`psql -U postgres -h localhost -p 5432`
6. Type the following commands in the Postgres CLI: 
    - `CREATE DATABASE earthtreks`
    - `\connect earthtreks`
    - `CREATE TABLE public.time_series_golden (datetime character varying(100), num_climbers int, capacity int, percent_full float);`
7. Exit out of the Postgres CLI 
8. cd to cloned repository directory and run this command to turn on the pi traffic light, scrape the gym data, and download it to the Postgres database: 
    - `python3 main.py`
9. Voila!
