import redis
import os
import redis

from flask import Blueprint, Flask, request, current_app
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
    app.config['REDIS_URL'] = 'redis://redis:6379/0'
    app.config['QUEUES'] = "default"
    # set config
 #   app_settings = os.getenv("APP_SETTINGS")
 #   app.config.from_object(app_settings)

    # set up extensions
   

    # register blueprints
   # from app import main_blueprint

   # app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app

app = create_app()

api = Api(
    app, version='1.0', title='DSVGO Checker API',
    description='A simple TodoMVC API',
)
#api.init_app(app)

#model = api.model('Model', {
#    'domain': fields.String, 
#})
#ns = api.namespace('api', description='dsvgo operations')



@api.route("/tasks")
class RunTasks(Resource):
    def post(self):
    # Default to 200 OK
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json

        else:
            return 'Content-Type not supported!'
        
        
        if data:
            with Connection(redis.from_url(current_app.config["REDIS_URL"])):
                q = Queue()
                task = q.enqueue(create_task, data)
            response_object = {
                "status": "success",
                "data": {
                    "task_id": task.get_id()
                }
            }
            return response_object
 #   @api.marshal_with(model, envelope='resource')
 #   @ns.doc('list_todos')
 #   @ns.marshal_list_with(api)
   




#@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
@api.route("/tasks/<string:task_id>")
class GetTaskID(Resource):
    def get(self,task_id):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
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
        return response_object

application = app
if __name__ == '__main__':
    app.run(debug=True)
        


