-- This makes sure that foreign_key constraints are observed and that errors will be thrown for violations
PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
-- Create User Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Create Accounts Table
CREATE TABLE Accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL,
    date_of_birth TEXT NOT NULL, -- Format: YYYY-MM-DD
    gender TEXT, 
    FOREIGN KEY (userid) REFERENCES Users(user_id)
);

-- Create Skills Table
CREATE TABLE Skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    skills VARCHAR(50) NOT NULL,
    proficiency TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Experience Table
CREATE TABLE Experience (
    experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    Title VARCHAR(50) NOT NULL,
    employmentType TEXT NOT NULL, 
    start_month TEXT NOT NULL,  
    start_year TEXT NOT NULL, 
    end_month TEXT NOT NULL,
    end_year TEXT NOT NULL ,
    industry VARCHAR(50) NOT NULL,
    description VARCHAR(200), 
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Education Table
CREATE TABLE Education (
    education_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    degree VARCHAR(50) NOT NULL,
    field_of_study VARCHAR(100) NOT NULL,
    start_month TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    end_month TEXT NOT NULL,
    end_year INTEGER NOT NULL,
    grade DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Certificate Table
CREATE TABLE Certificate (
    certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    name_of_certificate VARCHAR(50) NOT NULL,
    Issuing_organization VARCHAR(50) NOT NULL,
    issue_month TEXT NOT NULL,
    issue_year INTEGER NOT NULL,
    end_month TEXT NOT NULL,
    end_year INTEGER NOT NULL,
    isExpired BOOLEAN NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create recommendedJobs Table
CREATE TABLE recommendateJobs (
    recommendateJobs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    jobheader TEXT,
    jobskill TEXT,
    match REAL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);