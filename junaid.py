"""
junaid.py
A tiny Flask web app used to demonstrate an end-to-end CI/CD pipeline:
GitHub -> Jenkins -> Docker Build -> DockerHub Push

Every time Jenkins builds a new image, it stamps the image with the
Jenkins BUILD_NUMBER and the build timestamp as environment variables.
That means every time you redeploy a freshly-pushed image, you can see
the build number and timestamp change in the browser/curl output --
which is a simple, visual way to prove the pipeline actually ran.
"""

from flask import Flask, jsonify
import os
import socket
import datetime

app = Flask(__name__)

# These get baked in at "docker build" time via --build-arg / ENV
# (see Dockerfile). They default to "local-dev" values so the app
# also runs fine outside of Jenkins/Docker, e.g. `python junaid.py`.
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "local-dev")
BUILD_TIME = os.environ.get("BUILD_TIME", "unknown")
APP_VERSION = os.environ.get("APP_VERSION", "0.0.1")

# Simple in-memory counter just to show the app is alive and stateful
request_count = 0


@app.route("/")
def home():
    global request_count
    request_count += 1
    return jsonify({
        "message": "Hello from Junaid's Jenkins CI/CD Pipeline Demo!",
        "app_version": APP_VERSION,
        "jenkins_build_number": BUILD_NUMBER,
        "image_built_at_utc": BUILD_TIME,
        "container_hostname": socket.gethostname(),
        "current_server_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "total_requests_served_since_start": request_count,
    })


@app.route("/health")
def health():
    # Useful for Docker HEALTHCHECK or future Kubernetes liveness probes
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)