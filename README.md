# Project-1

# Tuition Reimbursement Management System

## Description
The Tuition Reimbursement System, TRMS, allows users to submit reimbursements for courses and training. The submitted reimbursement must be approved by that employee's supervisor, department head, and benefits coordinator. The benefits coordinator then reviews the grade received before finalizing the reimbursement.

## Technologies Used
* BootStrap 5.1.3
* PostgreSQL 14 
* HTML 5 
* CSS3 
* JavaScript 
* Python 3.10 
* Flask 2.1.2 
* Psycopg2 2.9.3
* Selenium 4.1.5

## Features
- Employees can create a reimbursement request
- The Employee's supervisor, departmen head, and benefit's coordinator (BenCo) is able to approve, or deny the request

## Setup
Clone Command:
`git clone https://github.com/Alexander-Ottosson/Project-1.git`

Create a PostgreSQL database named trms
* create 4 system environment variables and put your database connection info in them
  - database_host
  - database_username
  - database_password
  - database_port
* Run the `create_statements.sql` file on the database to create the tables and populate them with sample data
* Run the `app.py` file to begin the program

## Usage
* open project_1/front_end/login.html in a browser
* Login as a base employee Tavish DeGroot 
  * username: tdgroot
  * password: password
* On the nav, click the Create A Request link to go to the request creation form, fill it out and submit
* Go back to the login page and log in as either a supervisor, department head, or BenCo
  * Supervisor:
    * username: jodoe
    * password: password
  * Department Head:
    * username: aottosson
    * password: password
  * BenCo:
    * username: bfittz
    * password: password
* You should be able to click the view button for a request and view it's info
* If you are a Benco you should be able to alter the request amount by pressing the "Alter Amount" button
* You can approve or deny the request by lcicking the corresponding button
