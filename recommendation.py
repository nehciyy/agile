import csv
import sqlite3
import unicodedata

global total_count

text = []  # A list for storing some text data 
skills_list = []  # A list for storing skills data 
filename = 'data.csv'  # CSV file containing job data

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Connect to a SQLite database
    conn.row_factory = sqlite3.Row  # Use dictionary-like rows
    return conn

import csv

# Function to read data from a CSV file (skills list)
def read_csv(file):
    extracted_data = []
    with open(file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            header = row['Header']
            skills = [skill.strip().lower() for skill in row['Skills'].split(',')]  # Convert skills to lowercase
            imagePath = row['Image_Path']
            extracted_data.append({'Header': header, 'Skills': skills, 'imagePath': imagePath})
            print(extracted_data)
    return extracted_data

# Function to select skills for a given account_id from the database
def select_for_skills(account_id):
    conn = sqlite3.connect('database.db')  # Connect to the database
    c = conn.cursor()
    skills = []
    query = 'SELECT DISTINCT skills FROM Skills WHERE account_id = ?'
    result = conn.execute(query, (account_id,))
    row = result.fetchall()
    conn.close()
    if row:
        for skill in row:
            skills.append(skill[0])
    return skills

# Function to calculate the number of matching skills between a job and user skills
def job_calc(job, text):
    count = 0
    for uni_word in job:
        if uni_word in text:
            count += 1
    return count


def accuracy(skill_list, job_list, account_id):
    for job in job_list: 
        job_skills = set(job['Skills'])
        user_skills = set(skill_list)
        jaccard_sim = jaccard_similarity(user_skills, job_skills)
        match = jaccard_sim * 100
        update_table(match, account_id, job['Header'], job['Skills'],job['imagePath'])

# Function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0  # Handle cases when both sets are empty
    return intersection / len(set2)

# Function to update a database table with job recommendations and match percentage
def update_table(match, account_id, job_header, job_skills, imagePaths):
    conn = get_db_connection()  # Get a database connection
    conn.execute("INSERT INTO recommendateJobs (account_id, jobheader, jobskill, match, imagePaths) VALUES (?, ?, ?, ?, ?)",
                 (account_id, job_header, ', '.join(job_skills), match, imagePaths))
    conn.commit()
    conn.close()

# Main function
def main(session_id):
    jobswithskills_list = read_csv(filename)  # Read job data from the CSV file

    conn = get_db_connection()  # Get a database connection
    # Query the database to retrieve the account_id based on the provided session_id
    query = 'SELECT account_id FROM Accounts WHERE userid = ?'
    result = conn.execute(query, [session_id])
    # Directly assign the fetched value to account_id
    account_id = result.fetchone()
    if account_id:
        account_id = account_id[0]  # Use indexing to get the value
    else:
        print(f"No account found for session {session_id}")
    userSkills = select_for_skills(account_id)  # Get skills for the user
    
    match = accuracy(userSkills, jobswithskills_list, account_id)  # Calculate the match percentage
