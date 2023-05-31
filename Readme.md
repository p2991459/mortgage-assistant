# A Mortgage assistant which helps to find the best mortgage deal from the database. It can also answer general questions.

## Installation on localhost:

1. Create a new environment using the following command:
   
python -m venv venv


2. Install the required packages using the command:

pip install -r requirements.txt

## You must modify the langchain db file to handle the db connectivity error

try:
    cursor = connection.execute(text(command))
except Exception as e:
    return "Invalid query to execute"
<PATH OF YOUR VENV DIRECTORY> site-packages\langchain\sql_database.py



In Windows, activate the virtual environment using:

./venv/Scripts/activate


In Linux, activate the virtual environment using:

source ./venv/bin/activate

