# Flask_Airplane_Project

Original Plane data is stored in input.txt
I made the assumption that a Plane (id) could only exist in one place at one time.
I needed to remove some of the original data in order for this to be true.
Field unique_id is a combination of id and datetime.

I created and ran ImportTextFile.py to load the original data from the input.txt
file into a sqlite database, database.db.

app.py is the program to run to start the project.  Default port is 5000.

## Sample tests:

GET http://127.0.0.1:5000/planes

GET http://127.0.0.1:5000/planes?pagination=true&page=2&limit=2

GET http://127.0.0.1:5000/planes/22016-10-15T12:00:00-05:00

DELETE http://127.0.0.1:5000/planes/12016-10-12T12:00:00-05:00

POST http://127.0.0.1:5000/planes
with body:
{
  "id": "9",
  "description": "new plane number 9",
  "datetime": "2018-10-13T12:00:00-05:00",
  "longitude": 20,
  "latitude": 12,
  "elevation": 15
}

PUT http://127.0.0.1:5000/planes/22016-10-15T12:00:00-05:00
with body:
{
  "id": "10",
  "description": "new plane number 10",
  "datetime": "2018-10-13T12:00:00-05:00",
  "longitude": 20,23,
  "latitude": 12.25,
  "elevation": 15.5
}
