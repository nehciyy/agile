import sqlite3

connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
   connection.executescript(f.read())
cur = connection.cursor()

# List of data to insert into Users table
userData_to_insert = [
    ("aaronlim123@gmail.com","Password001"),
    ("emilysmith@example.com", "Password002"),
    ("johndoe@example.com", "Password003"),
]

#List of data to insert into Accounts table
accountData_to_insert = [
    (1, "Aaron", "Lim", "2000/01/01", "Male"),
    (2, "Emily", "Smith", "1995/03/15", "Female"),
    (3, "John", "Doe", "1988/11/30", "Male"),
]

# ("Aaron Lim", "aaronlim123@gmail.com", "Password001", "01/01/2000", "M"),
# ("Emily Smith", "emilysmith@example.com", "Password002", "03/15/1995", "F"),
# ("John Doe", "johndoe@example.com", "Password003", "11/30/1988", "M"),

cur.executemany(
    "INSERT INTO Users (email,password) VALUES (?,?)",
    userData_to_insert
)

cur.executemany(
    "INSERT INTO Accounts (userid, First_name, Last_name, date_of_birth, gender) VALUES (?,?,?,?,?)",
    accountData_to_insert
)

connection.commit()
print("Database Created: Connection Opened")
connection.close()
