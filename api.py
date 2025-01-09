from flask import Flask, request, jsonfy
from tensorflow.keras.models import load_model
import pandas as pd
import joblib
from utils import *

app =Flask(__name__)

model = load_model('meu_modelo.keras')
selector_carregado=joblib('./objects/selector.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    input_data=request.get_json()

    df = pd.DataFrame(input_data)

    df = load_scalers(df,['tempoprofissao','renda','idade', 'dependentes','valorsolicitado','valortotalbem','proporcaosolicitadototal'])
    df = load_encoders(df,['profissao', 'tiporesidencia', 'escolaridade','score','estadocivil','produto'])

    df = selector_carregado.transfom(df)

    predictions = model.predict(df)

    return jsonfy(predictions.tolist())

if __name__ == '__name__':
    app.run(debug=True)