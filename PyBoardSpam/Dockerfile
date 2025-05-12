FROM python:3.11.4

ENV FLASK_APP=pyboardspam.py
ENV FLASK_DEBUG=true

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip \
&& pip install flask

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]