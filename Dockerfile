FROM python:3.10

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libhdf5-dev


WORKDIR /app

COPY ./web_gui ./web_gui
COPY ./feature_extraction ./feature_extraction
COPY ./model ./model
COPY requirements_app.txt .

RUN pip install -r requirements_app.txt

EXPOSE 9999


CMD ["python", "/app/web_gui/app.py"]
