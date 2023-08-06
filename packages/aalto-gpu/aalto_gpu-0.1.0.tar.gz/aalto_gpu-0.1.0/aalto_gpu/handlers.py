import json
import os
import requests

from notebook.base.handlers import APIHandler
from notebook.utils import url_path_join
import tornado

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post, 
    # patch, put, delete, options) to ensure only authorized user can request the 
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /aalto-gpu/get_example endpoint!"
        }))

class RouteHandlerSendJob(APIHandler):
    @tornado.web.authenticated
    def get(self):
        environment = dict(os.environ)
        #self.finish(json.dumps({
        #    "data": "This is /aalto-gpu/send_job endpoint!"
        #}))
        self.finish(json.dumps(environment))

    @tornado.web.authenticated
    def post(self):
        # input data is a dictionary with a key "notebook_path"
        input_data = self.get_json_body()
        nb_path = input_data["notebook_path"]
        env = os.environ
        fwd_req_data = {"notebookPath": input_data["notebook_path"],
                        "username": env.get("JUPYTERHUB_USER"),
                        "uid": env.get("NB_UID"),
                        "job-token": env.get("JOB_TOKEN"),
                        "image": "testgpu:3.0.0"}
        fwd_req_url = "https://jupyter-job-server.jupyter-jobs/job"
        try:
            response_object = requests.post(fwd_req_url, data = fwd_req_data)
            status_code = response_object.status_code
            if status_code == 200:
                queue_pos = response_object.json().get("queue")
                self.finish(json.dumps({
                    "dialog_body": "{} successfully sent to the job-server\nPosition in queue: {}".format(nb_path, queue_pos)
                    }))
            else:
                self.finish(json.dumps({
                    "dialog_body": "Bad job-server response:\n{}: {}".format(status_code, response_object.reason)
                    }))
        except requests.exceptions.RequestException as e:
            self.finish(json.dumps({
                "dialog_body": "Couldn't reach the job-server:\n{}".format(str(e))
            }))


def setup_handlers(web_app):
    host_pattern = ".*$"
    
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "aalto-gpu", "get_example")
    route_pattern_send_job = url_path_join(base_url, "aalto-gpu", "send_job")
    handlers = [(route_pattern, RouteHandler),
                (route_pattern_send_job, RouteHandlerSendJob)]
    web_app.add_handlers(host_pattern, handlers)
