import pandas as pd
from datetime import datetime
import numpy as np
import random as python_random
import joblib

from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
import tensorflow as tf

from utils import *
import const

seed = 41
np.random.seed(seed)
python_random.seed(seed)
tf.random.set_seed(seed)

#dados brutos
df = fech_data_from_db(const.consulta_sql)

#conversão dos tipos
df['idade'] = df['idade'].astype(int)
df['valorsolicitado'] = df['valorsolicitado'].astype(float)
df['valortotalbem'] = df['valortotalbem'].astype(float)

#tratamento dos nulos
substitui_nulos(df)

#corrigir erros de digitação
profissoes_validas = ['Advogado', 'Arquiteto', 'Cientista de Dados', 'Contador','Dentista','Empresário', 'Engenheiro','Médico','Programador']
corrigir_erros_digitacao(df,'profissao',profissoes_validas)

#tratamento de outliers
df = tratar_outliers(df, 'tempoprofissao',0,70)
df = tratar_outliers(df, "idade", 0, 110)

#Feature Engineering
df['proporcaosolicitadototal'] = df['valorsolicitado'] / df['valortotalbem']
df['proporcaosolicitadototal']=df['proporcaosolicitadototal'].astype(float)

# Dividindo os dados
X = df.drop('classe', axis=1)
y = df['classe']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

# Normalização 

X_train = save_scalers(X_train,['tempoprofissao','renda','idade', 'dependentes','valorsolicitado','valortotalbem','proporcaosolicitadototal'])
X_test = save_scalers(X_test,['tempoprofissao','renda','idade', 'dependentes','valorsolicitado','valortotalbem','proporcaosolicitadototal'])

#codificação
mapeamento = {'ruim': 0, 'bom': 1}
y_train = np.array([mapeamento[item] for item in y_train])
y_test = np.array([mapeamento[item] for item in y_test])
X_train = save_encoders(X_train,['profissao', 'tiporesidencia', 'escolaridade','score','estadocivil','produto'])
X_test = save_encoders(X_test,['profissao', 'tiporesidencia', 'escolaridade','score','estadocivil','produto'])

#Seleção de Atributos
model = RandomForestClassifier()
# A instancia o RFE
selector = RFE(model, n_features_to_select=10, step=1)
selector=selector.fit(X_train, y_train)
# Transformação dos dados
X_train = selector.transform(X_train)
X_test = selector.transform(X_test)
joblib.dump(selector, './objects/selector.joblib')

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

#configurando o otimizador
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)

#compilando modelo
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

#Treinamento do modelo
model.fit(
    X_train,
    y_train,
    validation_split=0.2, #usa 20% dos dados para validação
    epochs=500,   #número máximo de epocas
    batch_size=10,
    verbose=1
)
model.save('meu_modelo.keras')

#previsões

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5).astype(int)

#Avaliando
print("Avaliação do modelo nos dados de teste: ")
model.evaluate(X_test, y_test)

#metricas de classificação
print("\nRelatório de Classificação: ")
print(classification_report(y_test,y_pred))
