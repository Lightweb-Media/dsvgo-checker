# manage.py



import os
import redis

from flask import Flask
from flask.cli import FlaskGroup
from rq import Connection, Worker

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
 #   from app import main_blueprint

#    app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app

app = create_app()
cli = FlaskGroup(create_app=create_app)
@cli.command("run_worker")
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUES"])
        worker.work()


if __name__ == "__main__":
    cli()
