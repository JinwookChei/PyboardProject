FROM python:3.11.4

ENV FLASK_APP=pyboard.py
ENV FLASK_DEBUG=true

WORKDIR /app

COPY . /app/
COPY entrypoint.sh /entrypoint.sh


RUN python -m pip install --upgrade pip && \
    pip install flask && \
    pip install flask-migrate && \
    pip install flask-wtf && \
    pip install requests && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]