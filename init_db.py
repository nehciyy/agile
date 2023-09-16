import sqlite3

# Establish a connection to the SQLite database named "database.db"
connection = sqlite3.connect("database.db")

# Open the schema.sql file and execute the SQL statements in it to create tables and define the schema
with open("schema.sql") as f:
    connection.executescript(f.read())

# Create a cursor object for executing SQL commands
cur = connection.cursor()

# List of data to insert into the Users table
userData_to_insert = [
    ("aaronlim123@gmail.com", "Password001", 0),
    ("emilysmith@example.com", "Password002", 0),
    ("johndoe@example.com", "Password003", 0),
    ("admin@example.com", "admin123", 1)
]

# List of data to insert into the Accounts table
accountData_to_insert = [
    (1, "Aaron", "Lim", "2000/01/01", "Male"),
    (2, "Emily", "Smith", "1995/03/15", "Female"),
    (3, "John", "Doe", "1988/11/30", "Male"),
    (4, "Admin", "User", "2000/01/01", "Male"),
]

# Use executemany to insert multiple rows into the Users table
cur.executemany(
    "INSERT INTO Users (email, password, is_admin) VALUES (?, ?, ?)",
    userData_to_insert
)

# Use executemany to insert multiple rows into the Accounts table
cur.executemany(
    "INSERT INTO Accounts (userid, First_name, Last_name, date_of_birth, gender) VALUES (?, ?, ?, ?, ?)",
    accountData_to_insert
)

# Commit the changes made to the database
connection.commit()

# Print a message to indicate that the database has been created and the connection is closed
print("Database Created: Connection Opened")

# Close the database connection
connection.close()
