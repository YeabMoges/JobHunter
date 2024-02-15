# Yeabsira Moges
# CNE 340 Winter 2024
# 02-13-2024
# Reference
# https://stackoverflow.com/questions/15633653/mysql-date-subnow-interval-1-day-24-hours-or-weekday
# https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect


import json
import time

import html2text
import mysql.connector
import requests


# Connect to database
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1', database='cne340')
    return conn


# Create the table structure
def create_tables(cursor):
    # Creates table
    # Must set Title to CHARSET utf8 unicode Source: http://mysql.rjweb.org/doc.php/charcoll.
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (id INT PRIMARY KEY auto_increment, Job_id varchar(50) , 
    company varchar (300), Created_at DATE, url varchar(30000), Title LONGBLOB, Description LONGBLOB ); ''')


# Query the database.
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


# Add a new job
def add_new_job(cursor, jobdetails):
    # extract all required columns
    description = html2text.html2text(jobdetails['description'])
    date = jobdetails['publication_date'][0:10]
    job__id = jobdetails['id']
    job_comp = jobdetails['company_name']
    job_url = jobdetails['url']
    job_title = jobdetails['title']
    query = cursor.execute("INSERT INTO jobs( Job_id, company, Created_at, url, Title, Description) "
                           "VALUES(%s,%s,%s,%s,%s,%s)", (job__id, job_comp, date, job_url, job_title, description))
    cursor.execute(query, (job__id, job_comp, date, job_url, job_title, description))
    return cursor


# Check if new job
def check_if_job_exists(cursor, jobdetails):
    description = html2text.html2text(jobdetails['description'])
    query = f'SELECT * FROM jobs WHERE description = %s'
    cursor.execute(query, (description,))
    return cursor


# Deletes job
def delete_job(cursor, jobdetails):   # use id
    description = html2text.html2text(jobdetails['description'])
    query = f'DELETE FROM jobs WHERE description = %s'
    cursor.execute(query, (description,))
    return cursor


# Grab new jobs from a website, Parses JSON code and inserts the data into a list of dictionaries do not need to edit
def fetch_new_jobs():
    query = requests.get("https://remotive.io/api/remote-jobs")
    datas = json.loads(query.text)

    return datas


def jobhunt(cursor):

    jobpage = fetch_new_jobs()  # Gets API website and holds the json data in it as a list
    add_or_delete_job(jobpage, cursor)


def add_or_delete_job(jobpage, cursor):
    for jobdetails in jobpage['jobs']:
        check_if_job_exists(cursor, jobdetails)
        is_job_found = len(
            cursor.fetchall()) > 0
        if is_job_found:
            delete_job(cursor, jobdetails)
            print(f'Existing Jobs found in DB')
        else:
            add_new_job(cursor, jobdetails)
            print(f'New Job found : {jobdetails["title"]}')
    delete_14days_query = f'DELETE FROM jobs WHERE created_at < DATE_SUB(NOW(), INTERVAL 14 DAY)'
    cursor.execute(delete_14days_query)


def main():
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor)
    while (1):

        jobhunt(cursor)
        time.sleep(14400)  # 14400 Sleep for 4h, this is run every four hour


if __name__ == '__main__':
    main()
