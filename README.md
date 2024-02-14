
# Project Title and Description

**Job Hunter**

**Description:**

Job Hunter is a Python script designed to retrieve remote job listings from the Remotive API and store them in a MySQL database. 

- Fetches remote job listings from the Remotive API.
- Stores job listings in a MySQL database hosted on a WAMP server.
- Runs in a continuous loop, periodically checking for new job openings.
- Displays Job title to the user when new job openings are found.
- Implements a sleep timer to prevent excessive API requests.

**Usage:**

1. Ensure Python is installed on your system.
2. Install the required Python packages, including `requests` for making HTTP requests and a MySQL connector library for database interaction.
3. Configure the MySQL database connection settings in the script to connect to your WAMP server.
4. Run the script and enjoy automatic job updates!

**API Information**

Retrieves job listings from: `https://remotive.io/api/remote-jobs`


**Installation:**

1. Clone the repository from [GitHub](https://github.com/YeabMoges/JobHunter).
2. Install the required dependencies using pip:
    ```
    pip install requests mysql-connector-python
    ```
3. Configure the MySQL database connection settings in the script.
4. Run the script using Python:
    ```
    python job_hunter.py
    ```


