FROM python:3.10

WORKDIR /app

COPY ./web_gui ./web_gui
COPY ./feature_extraction ./feature_extraction
COPY model/model.py ./saved_models/model.py
COPY requirements_app.txt .

RUN pip install -r reqirements_app.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
