from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Plane(db.Model):
    __tablename__ = "planes"
    unique_id = db.Column(db.String(80), primary_key=True)
    id = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.String(80), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)

    def convert_to_json(self):
        return {
            "unique_id": self.unique_id,
            "id": self.id,
            "description": self.description,
            "datetime": self.datetime,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "elevation": self.elevation
        }

    def add_plane(_id, _description, _datetime, _longtitude,
                  _latitiude, _elevation):
        next_id = _id + _datetime
        new_entry = Plane(unique_id=next_id, id=_id,
                          description=_description, datetime=_datetime,
                          longitude=_longtitude, latitude=_latitiude,
                          elevation=_elevation)
        db.session.add(new_entry)
        db.session.commit()

    def delete_plane(_unique_id):
        deleted = Plane.query.filter_by(unique_id=_unique_id).delete()
        db.session.commit()
        return bool(deleted)

    def get_planes(use_pagination, page, limit):
        if (not use_pagination):
            return_data = [Plane.convert_to_json(plane) for plane in
                           Plane.query.all()]
            return return_data
        else:
            p = Plane.query.paginate(page, limit, False)
            return_data = [Plane.convert_to_json(plane) for plane in
                           p.items]
            pages = {
                "page": page,
                "perPage": limit,
                "total": p.total,
                "pages": p.pages,
            }
            if p.has_next:
                next_url = url_for("get_planes", page=p.next_num)
                pages["nextUrl"] = next_url
            else:
                pages["nextUrl"] = None

            if p.has_prev:
                prev_url = url_for("get_planes", page=p.prev_num)
                pages["prevUrl"] = prev_url
            else:
                pages["prevUrl"] = None
            return return_data, pages

    def get_plane(_unique_id):
        result = Plane.query.filter_by(unique_id=_unique_id).first()
        if str(result) == "None":
            return str(result)
        else:
            return Plane.convert_to_json(result)

    def __repr__(self):
        plane_object = {
            "unique_id": self.unique_id,
            "id": self.id,
            "description": self.description,
            "datetime": self.datetime,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "elevation": self.elevation
        }
        return json.dumps(plane_object)
