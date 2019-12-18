import uuid
import json
from flask import abort
from sample.db import sql as db, redis_store


# An example using SQLAlchemy


class FooModel(db.Model):
    read_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/schemas/foo.json",
        "title": "Foo",
        "description": "Representation of a Foo",
        "type": "object",
        "properties": {"id": {"type": "string"}, "name": {"type": "string"}},
        "additionalProperties": False,
        "required": ["id", "name"],
    }

    write_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/schemas/foo.json",
        "title": "Foo Write",
        "description": "Representation of a user creating or updating a Foo",
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
        "required": ["name"],
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    @staticmethod
    def get_or_404(id):
        return FooModel.query.get_or_404(id)

    @staticmethod
    def create(from_json):
        foo = FooModel(name=from_json["name"])
        db.session.add(foo)
        db.session.commit()
        return foo

    def update(self, from_json):
        self.name = from_json["name"]
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_json(self):
        return {"id": self.id, "name": self.name}


# An example using Redis


class BarModel(object):
    read_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/schemas/bar.json",
        "title": "Bar",
        "description": "Representation of a Bar",
        "type": "object",
        "properties": {"id": {"type": "string"}, "name": {"type": "string"}},
        "additionalProperties": False,
        "required": ["id", "name"],
    }

    write_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/schemas/bar.json",
        "title": "Bar Write",
        "description": "Representation of a user creating or updating a Bar",
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
        "required": ["name"],
    }

    @staticmethod
    def key(id):
        return "bar/{}".format(id)

    @staticmethod
    def get_or_404(id):
        stored_value = redis_store.get(BarModel.key(id))

        if not stored_value:
            abort(404)

        return BarModel(stored_value)

    @staticmethod
    def create(from_json):
        id = uuid.uuid4().hex
        from_json["id"] = id

        stored_value = json.dumps(from_json)
        redis_store.set(BarModel.key(id), stored_value)

        return BarModel(stored_value)

    def __init__(self, stored_value):
        self.stored_value = stored_value

    def update(self, from_json):
        current = self.as_json()
        current.update(from_json)

        self.stored_value = json.dumps(current)
        redis_store.set(BarModel.key(self.as_json()["id"]), self.stored_value)

        return self

    def delete(self):
        redis_store.delete(BarModel.key(self.as_json()["id"]))

    def as_json(self):
        return json.loads(self.stored_value)
