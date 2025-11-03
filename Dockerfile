FROM apache/superset:5.0.0-dev

USER root

COPY requirements.txt requirements.txt

RUN uv pip install --no-cache-dir -r requirements.txt

USER superset