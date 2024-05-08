from flask import Flask, render_template, request
from model.model import Model
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Użyj tego samego klucza, który został użyty w formularzu HTML
    url = request.form['url-input']
    is_phish = make_prediction(url)
    return render_template('index.html', url=url, is_phish=is_phish)


def make_prediction(url):
    is_phish = None
    model = Model(url, os.path.join('static', 'random_forest_model.pkl'))
    prediction: float = model.predict()
    if prediction[0] == 1:
        is_phish = True
    elif prediction[0] == 0:
        is_phish = False
    print(prediction[0])
    return is_phish


if __name__ == '__main__':
    app.run(debug=True)

