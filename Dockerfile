FROM python:3.5-alpine
WORKDIR /app
COPY gradebook-server/requirements.txt /app
RUN apk --update add --no-cache mariadb-dev g++ && \
    pip install -r requirements.txt && \
    apk del g++ mariadb-dev && \
    apk add --no-cache mariadb-client-libs

ENV FLASK_APP=main.py
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=0
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

