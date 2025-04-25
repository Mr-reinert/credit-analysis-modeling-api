# Credit Analysis Modeling API

Este projeto é uma solução completa para análise de crédito com uso de aprendizado de máquina, explicabilidade de modelos (XAI) e uma interface interativa com o usuário.

## 🚀 Funcionalidades

- 🧠 **Modelo Preditivo com Redes Neurais**: Treinamento supervisionado para prever a probabilidade de inadimplência.
- 🔍 **Explicabilidade com XAI**: Geração de explicações para auxiliar na tomada de decisão.
- 🌐 **API com Flask**: Interface RESTful para integração com aplicações externas.
- 🖥️ **WebApp com Streamlit**: Interface amigável para entrada de dados e visualização dos resultados.

---

## 📁 Estrutura do Projeto

```
├── api.py                 # API REST com Flask
├── webapp.py              # Interface do usuário com Streamlit
├── modelcreation.py       # Script de criação e salvamento do modelo
├── modelcreationn.ipynb   # Jupyter notebook para exploração e modelagem
├── utils.py               # Funções utilitárias
├── xai.py                 # Técnicas de explicabilidade
├── config.yaml            # Arquivo de configuração
└── requirements.txt       # Dependências do projeto
```

---

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Mr-reinert/credit-analysis-modeling-api.git
cd credit-analysis-modeling-api
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## ▶️ Como Usar

### Rodando a API
```bash
python api.py
```
A API ficará disponível em `http://localhost:5000`.

### Rodando o WebApp (Streamlit)
```bash
streamlit run webapp.py
```
Acesse `http://localhost:8501` no seu navegador.

---

## 🧠 Modelo

O modelo foi treinado com dados fictícios/tabulares e utiliza uma rede neural simples. Para melhor desempenho, recomenda-se fine-tuning com dados reais e balanceamento de classes.
