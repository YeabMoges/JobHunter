
# Yeabsira Moges
# CNE 340 Winter 2024
# 02-13-2024


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
    # Python is in latin-1 and error (Incorrect string value: '\xE2\x80\xAFAbi...') will occur if Description is not in unicode format due to the json data
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
               "VALUES(%s,%s,%s,%s,%s,%s)", ( job__id, job_comp, date, job_url, job_title, description))
     # %s is what is needed for Mysqlconnector as SQLite3 uses ? the Mysqlconnector uses %s
    delete_14days_query = f'DELETE FROM jobs WHERE created_at < DATE_SUB(NOW(), INTERVAL 14 DAY)'
    cursor.execute(query,(job__id, job_comp, date, job_url, job_title, description))
    cursor.execute(delete_14days_query)
    return cursor


# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ##Add your code here
    description = html2text.html2text(jobdetails['description'])
    query = f'SELECT * FROM jobs WHERE description = %s'
    cursor.execute(query, (description,))
    return cursor

# Deletes job
def delete_job(cursor, jobdetails):
    ##Add your code here
    description = html2text.html2text(jobdetails['description'])
    query = f'DELETE FROM jobs WHERE description = %s'
    cursor.execute(query, (description,))
    return cursor


# Grab new jobs from a website, Parses JSON code and inserts the data into a list of dictionaries do not need to edit
def fetch_new_jobs():
    query = requests.get("https://remotive.io/api/remote-jobs")
    datas = json.loads(query.text)

    return datas


# Main area of the code. Should not need to edit
def jobhunt(cursor):

    jobpage = fetch_new_jobs()  # Gets API website and holds the json data in it as a list

    add_or_delete_job(jobpage, cursor)


def add_or_delete_job(jobpage, cursor):

    for jobdetails in jobpage['jobs']:  # EXTRACTS EACH JOB FROM THE JOB LIST. It errored out until I specified jobs. This is because it needs to look at the jobs dictionary from the API. https://careerkarma.com/blog/python-typeerror-int-object-is-not-iterable/
        check_if_job_exists(cursor, jobdetails)
        is_job_found = len(
        cursor.fetchall()) > 0  # https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect
        if is_job_found:
            delete_job(cursor, jobdetails)
            print(f'Existing Jobs found in DB')
        else:
            add_new_job(cursor, jobdetails)
            print(f'New Job found : {jobdetails["title"]}')
            # INSERT JOB
            # Add in your code here to notify the user of a new posting. This code will notify the new user




def main():

    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor)

    while (1):  # Infinite Loops. Only way to kill it is to crash or manually crash it. We did this as a background process/passive scraper
        jobhunt(cursor)
        time.sleep(14400)  # 14400 Sleep for 4h, this is ran every four hour because API or web interfaces have request limits. Your reqest will get blocked.

if __name__ == '__main__':
    main()

