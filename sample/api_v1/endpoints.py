import jsonschema

from flask import abort, request, Blueprint
from flask_restplus import Api, Resource

from .models import FooModel, BarModel

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint, doc="/docs", title="Sample API", version="1.0", description="Sample API",
)

foo = api.namespace("foo", description="Core operations on Foo resources")

foo_read_schema_model = foo.schema_model("Foo", FooModel.read_schema)
foo_write_schema_model = foo.schema_model("Write Foo", FooModel.write_schema)


class FooResource(Resource):
    @staticmethod
    def validate_write_request(value):
        try:
            jsonschema.validate(request.json, FooModel.write_schema)
        except jsonschema.ValidationError as e:
            abort(400, e.message)


@foo.route("/")
class FooList(FooResource):
    @foo.expect(foo_write_schema_model)
    @foo.response(201, "Created", foo_read_schema_model)
    @foo.response(400, description="Invalid Foo")
    def post(self):
        """
        Creates a new Foo
        """

        self.validate_write_request(request.json)
        foo = FooModel.create(request.json)

        return foo.as_json(), 201


@foo.route("/<string:id>")
class Foo(FooResource):
    @foo.response(200, "Success", foo_read_schema_model)
    @foo.response(404, description="Not Found")
    def get(self, id):
        """
        Gets a Foo
        """

        foo = FooModel.get_or_404(id)

        return foo.as_json()

    @foo.expect(foo_write_schema_model)
    @foo.response(200, "Success", foo_read_schema_model)
    @foo.response(400, description="Invalid Foo")
    @foo.response(404, description="Not Found")
    def put(self, id):
        """
        Updates a Foo
        """

        foo = FooModel.get_or_404(id)

        self.validate_write_request(request.json)
        foo.update(request.json)

        return foo.as_json()

    @foo.response(204, description="No Content")
    @foo.response(404, description="Not Found")
    def delete(self, id):
        """
        Deletes a Foo
        """

        foo = FooModel.get_or_404(id)

        foo.delete()

        return "", 204


# If all your models follow the basic CRUD pattern as above, consider
# a function such as this for generating new routes from a Model:
def routes_from_model(base_route, description, Model):
    ns = api.namespace(base_route, description=description)
    read_schema_model = ns.schema_model(Model.read_schema["title"], Model.read_schema)
    write_schema_model = ns.schema_model(
        Model.write_schema["title"], Model.write_schema
    )

    class BaseResource(Resource):
        @staticmethod
        def validate_write_request(value):
            try:
                jsonschema.validate(request.json, Model.write_schema)
            except jsonschema.ValidationError as e:
                abort(400, e.message)

    @ns.route("/")
    class List(BaseResource):
        @ns.expect(write_schema_model)
        @ns.response(201, "Created", read_schema_model)
        @ns.response(400, description="request JSON failed validation")
        def post(self):
            """
            Creates a new Model
            """

            self.validate_write_request(request.json)
            model = Model.create(request.json)

            return model.as_json(), 201

    @ns.route("/<string:id>")
    class ById(BaseResource):
        @ns.response(200, "Success", read_schema_model)
        @ns.response(404, description="Not Found")
        def get(self, id):
            """
            Gets a Model by id
            """

            model = Model.get_or_404(id)

            return model.as_json()

        @ns.expect(write_schema_model)
        @ns.response(200, "Success", read_schema_model)
        @ns.response(400, description="request JSON failed validation")
        @ns.response(404, description="Not Found")
        def put(self, id):
            """
            Updates a Model by id
            """

            model = Model.get_or_404(id)

            self.validate_write_request(request.json)
            model.update(request.json)

            return model.as_json()

        @ns.response(204, description="No Content")
        @ns.response(404, description="Not Found")
        def delete(self, id):
            """
            Deletes a Model by id
            """

            model = Model.get_or_404(id)

            model.delete()

            return "", 204


# and then using it with:
routes_from_model("bar", "Core operations on Bar resources", BarModel)
