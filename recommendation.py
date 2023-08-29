import csv
import sqlite3
import unicodedata

global total_count

text = []
skills_list = []
filename = 'data.csv'  # Update the filename with your CSV file

#DB Connection Function Object
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

import csv

def read_csv(file):
    """Reading data from CSV files (skill list)."""
    extracted_data = []
    with open(file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            header = row['Header']
            skills = [skill.strip() for skill in row['Skills'].split(',')]
            extracted_data.append({'Header': header, 'Skills': skills})
                
    return extracted_data

def select_for_skills(account_id):
    conn = sqlite3.connect('database.db')
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

def job_calc(job, text): 
    count = 0 
    for uni_word in job: 
        if uni_word in text: 
            count +=1
    return count

def accuracy(skill_list, job_list, account_id):
    for job in job_list: 
        job_skills = set(job['Skills'])
        user_skills = set(skill_list)
        jaccard_sim = jaccard_similarity(user_skills, job_skills)
        match = jaccard_sim * 100
        update_table(match, account_id, job['Header'], job['Skills'])          

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0  # To handle cases where both sets are empty
    return intersection / union

def update_table(match, account_id, job_header, job_skills):
    conn = get_db_connection()
    conn.execute("INSERT INTO recommendateJobs (account_id, jobheader, jobskill, match) VALUES (?, ?, ?, ?)",
                 (account_id, job_header, ', '.join(job_skills), match))
    conn.commit()
    conn.close()

def main(session_id): 
    jobswithskills_list = read_csv(filename)
    #Print the extracted data
    for entry in jobswithskills_list:
        print("Header:", entry['Header'])
        print("Skills:", ', '.join(entry['Skills']))
    
    conn = get_db_connection()
    # Query the database to retrieve the account_id based on the provided session_id
    query = 'SELECT account_id FROM Accounts WHERE userid = ?'
    result = conn.execute(query, [session_id])
    # Directly assign the fetched value to account_id
    account_id = result.fetchone()

    if account_id:
        account_id = account_id[0]  # Use indexing to get the value
    else:
        print(f"No account found for session {session_id}")

    userSkills = select_for_skills(account_id)
    
    for entry in jobswithskills_list:
        skillihave = job_calc(userSkills,entry['Skills'])

    match = accuracy(userSkills,jobswithskills_list,account_id)



