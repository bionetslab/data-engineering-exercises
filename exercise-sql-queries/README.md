# Database hands-on excercise
This exercise uses a mock database installable via docker. Follow these instructions to run the database.

## Prerequisites
Install docker on your computer following the instructions on the website: https://docs.docker.com/get-started/introduction/


### Setup the database and the data base admin page
1. ``` docker compose up -d db adminer ```
2. ``` docker build . --tag populate ```
3. This command executes the script populate_db.py. The data base will be created. Afterwards can go to ```localhost:8080``` to view the dashboard. ``` docker run --rm     --network setup_mynetwork     --env DB_HOST=db     --env DB_USER=root     --env DB_PASSWORD=mysecretpassword     --env DB_NAME=mydb populate /app/populate_db.py ``` 
4. If you created the database correctly, you can run the script ```add_records.py``` to insert some fake data from the data folder in the repository. ``` docker run --rm     --network setup_mynetwork     --env DB_HOST=db     --env DB_USER=root     --env DB_PASSWORD=mysecretpassword     --env DB_NAME=mydb populate /app/add_records.py ```
5. Now you can query the database.
