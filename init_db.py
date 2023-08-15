import sqlite3

connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

# List of data to insert
data_to_insert = [
    ("Aaron Lim", "aaronlim123@gmail.com", "Password001", "01/01/2000", "M"),
    ("Emily Smith", "emilysmith@example.com", "Password002", "03/15/1995", "F"),
    ("John Doe", "johndoe@example.com", "Password003", "11/30/1988", "M"),
]

cur.executemany(
    "INSERT INTO Users (user_name, email, password_hash, date_of_birth, gender) VALUES (?,?,?,?,?)",
    data_to_insert,
)


connection.commit()
print("Database Created: Connection Opened")
connection.close()
