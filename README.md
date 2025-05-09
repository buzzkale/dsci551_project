# ChatDB - USC DSCI 551

## Datasets

European Football: https://www.kaggle.com/datasets/technika148/football-database?select=games.csv
* This dataset was modified to be much smaller for computing purposes.

Bike Store Dataset: https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database?select=products.csv

## Implementation Guide

Requirements:
* MySQL (in EC2)
* MongoDB (in EC2)
* OpenAI API key
* Libraries: pymysql, openai, pymongo, fastapi

Setup prerequisites:
* In order for the code to access EC2, you must add the security group inbound rules:
    * Type: MySQL/Aurora; Protocol: TCP; Port Range: 3306; Source: Anywhere-IPv4
    * Type: Custom TCP; Protocol: TCP; Port Range: 27017; Source: Anywhere-IPv4

Databases requirements:
* MySQL database: bikestore
    * Table 1: brands
        * create table brands (brand_id int primary key, brand_name varchar(30));
        * LOAD DATA INFILE '/var/lib/mysql-files/brands.csv' into table brands fields terminated by ',' lines terminated by '\r\n' ignore 1 rows;
    * Table 2: categories
        * create table categories (category_id int primary key, category_name varchar(40));
        * LOAD DATA INFILE '/var/lib/mysql-files/categories.csv' into table categories fields terminated by ',' lines terminated by '\r\n' ignore 1 rows;
    * Table 3: products
        * create table products (product_id int primary key, product_name varchar(50), brand_id int, category_id int, model_year year, list_price float, foreign key (brand_id) references brands(brand_id), foreign key (category_id) references categories(category_id));
        * LOAD DATA INFILE '/var/lib/mysql-files/products.csv' into table products fields terminated by ',' lines terminated by '\r\n' ignore 1 rows;

* MongoDB database: euro_football
    * Collection 1: games
        * mongoimport -d eurofootball -c games --type csv --file games.csv --headerline
    * Collection 2: leagues
        * mongoimport -d eurofootball -c leagues --type csv --file leagues.csv --headerline
    * Collection 3: teams
        * mongoimport -d eurofootball -c teams --type csv --file teams.csv --headerline

After fulfilling all these requirements and downloading the database, enter your OpenAI API key into your terminal to store in your environment:
* export OPENAI_API_KEY="your-key-here"

If running MySQL, comment out line 4 in app.py. If running MongoDB. comment out line 5 in app.py.

Now, start app.py. Note that an EC2 machine can only run MySQL and MongoDB one at a time, not simultaneously. It may be necessary to run this command in the terminal:
* uvicorn app:app --reload

A successful run should display the following lines in the code:

INFO:     Will watch for changes in these directories: ['/Users/user/Downloads/dsci551/dsci551_project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7159] using WatchFiles
INFO:     Started server process [7161]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Copy http://127.0.0.1:8000 (do not use keyboard shortcuts) and paste the url into your browser. The program should be able to run at this point.