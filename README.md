# Jenkins CI/CD Pipeline Demo Project

A minimal end-to-end CI/CD project: every push to GitHub triggers a Jenkins
pipeline that builds a Docker image of a small Python (Flask) app and pushes
it to DockerHub.

## Architecture

```
Developer  --push-->  GitHub Repo  --webhook-->  Jenkins
                                                     |
                                       1. Junaid - Build Docker Image
                                       2. Junaid - Login to Dockerhub
                                       3. Junaid - Push Image to Dockerhub
                                                     |
                                                     v
                                                DockerHub Registry
```

## Project contents

| File             | Purpose                                                        |
|------------------|------------------------------------------------------------------|
| `junaid.py`      | Flask app that reports the Jenkins build number/time it was built with |
| `requirements.txt` | Python dependencies                                          |
| `Dockerfile`     | Builds the app into a container image, stamping in build metadata |
| `Jenkinsfile`    | Declarative pipeline: build image -> login -> push to DockerHub |
| `.dockerignore`  | Keeps unnecessary files out of the Docker build context        |

## Why this proves CI/CD is working

The app's `/` endpoint returns the `jenkins_build_number` and
`image_built_at_utc` that were baked into the image at build time. After
each Jenkins run produces and pushes a new image, pulling and running the
freshly pushed image shows a new build number and a new timestamp — visible,
concrete proof that a code commit flowed all the way through to a new image
in DockerHub.

## Run locally (without Jenkins, for quick testing)

```bash
pip install -r requirements.txt
python junaid.py
# visit http://localhost:5000
```

## Run via Docker (after Jenkins has pushed an image)

```bash
docker pull YOUR_DOCKERHUB_USERNAME/junaid-cicd-demo:latest
docker run -p 5000:5000 YOUR_DOCKERHUB_USERNAME/junaid-cicd-demo:latest
curl http://localhost:5000
```

## Pipeline stages (Jenkinsfile)

1. **Junaid - Build Docker Image** — runs `docker build`, tagging the image
   with both the Jenkins `BUILD_NUMBER` and `latest`.
2. **Junaid - Login to Dockerhub** — authenticates to DockerHub using
   credentials stored securely in Jenkins (credential ID:
   `dockerhub-credentials`), never hardcoded in the Jenkinsfile.
3. **Junaid - Push Image to Dockerhub** — pushes both tags to DockerHub.

See the full setup walkthrough for installing Jenkins, configuring
DockerHub credentials, and wiring up the GitHub webhook.
