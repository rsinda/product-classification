FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
WORKDIR /APP/
COPY requirements.txt /APP/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app app/
WORKDIR /APP/app
CMD ["ls"]
CMD ["python","main_app.py"]