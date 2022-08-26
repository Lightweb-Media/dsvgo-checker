import redis
import os
import redis

from flask import Flask
from flask.cli import FlaskGroup
from rq import Connection, Worker
import os
from tasks import create_task
from rq import Queue, Connection
#from flask import Blueprint, jsonify, request, current_app
from flask_restx import Resource, Api, fields


#main_blueprint = Blueprint("main", __name__,)
def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
   

    # register blueprints
   # from app import main_blueprint

   # app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app

app = create_app()

api = Api(
    app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)
api.init_app(app)
model = api.model('Model', {
    'domain': fields.String,
  
})
ns = api.namespace('api', description='TODO operations')
@api.route("/<string:tasks>'",endpoint='tasks')
@api.doc(body={'domain': 'An domain'})


class RunTasks(Resource):
    @api.marshal_with(model, envelope='resource')
    @ns.doc('list_todos')
    @ns.marshal_list_with(api)
    def run_task(self):
        # Default to 200 OK
        task_type = Flask.request.form["domain"]

        with Connection(redis.from_url(Flask.current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(create_task, task_type)
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id()
            }
        }
        return response_object


#@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(Flask.current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return Flask.jsonify(response_object)

application = app

        


