import sqlite3
import os
import re
# from UniqueId import UniqueId

file_name = "input.txt"
file_exists = os.path.isfile(file_name)
if file_exists:
    file = open(file_name)
    lines = []
    count = 0
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    lines = file.readlines()
    cur.execute("""CREATE TABLE planes
                (unique_id TEXT, id TEXT, description TEXT, datetime TEXT,
                latitude REAL, longitude REAL, elevation REAL,
                PRIMARY KEY (unique_id))""")

    for line in lines:
        count += 1
        if (count > 1):
            array = re.split(r"\t+", line.rstrip("\t").rstrip("\n"))
            unique_id = str(array[0]) + str(array[2])
            cur.execute("""INSERT INTO planes(unique_id, id, description,
                        datetime, latitude, longitude, elevation)
                        VALUES (?,?,?,?,?,?,?)""",
                        (str(unique_id), str(array[0]), str(array[1]),
                         str(array[2]), float(array[3]),
                         float(array[4]), float(array[5])))
    con.commit()
    con.close()
    file.close()

    # UniqueId.write_unique_id(str(count))
