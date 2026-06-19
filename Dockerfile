# Dockerfile for Junaid's CI/CD demo app

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY junaid.py .

# Build-time arguments injected by Jenkins so the running app can
# prove which pipeline build produced this exact image.
ARG BUILD_NUMBER=local
ARG BUILD_TIME=unknown
ENV BUILD_NUMBER=$BUILD_NUMBER
ENV BUILD_TIME=$BUILD_TIME
ENV APP_VERSION=1.0.0

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "junaid.py"]
