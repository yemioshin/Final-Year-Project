Summary

Overview is a simple, easy to use app for keeping track of small scale projects.
It allows the user the ability to create project tasks and give each task a genre.
It also has a dashboard and a chart feature to allow insight to all the projects created

Demo
To view this project without running it, please click: https://overview-386107.ew.r.appspot.com.

To run the code locally, please follow the instructions below. If you do not have python 3 installed, please install it:

Git clone this repository to a local directory:
git clone https://campus.cs.le.ac.uk/gitlab/ug_project/22-23/oo161.git

Navigate into the project-tracker-flask directory:
cd oo161

Create a virtual environment:
virtualenv venv

Ensure that your virtual environment runs Python 3.4:
virtualenv -p /usr/bin/python3.4 venv

Activate your virtual environment
source venv/bin/activate

Install the packages required to run this project
pip install -r requirements.txt

Create the migrations repository
flask db init

Create the migration script
flask db migrate

Run the migration script to apply changes to the database
flask db upgrade

Run the project
python run.py
