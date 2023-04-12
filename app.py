from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/exchange_rate', methods=['GET'])
def exchange_rate():
	moeda = request.args.get('moeda')
	dataInicial = request.args.get('dataInicial')
	dataFinalCotacao = request.args.get('dataFinalCotacao')
	url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda=" + moeda + "&@dataInicial=" + dataInicial + "&@dataFinalCotacao=" + dataFinalCotacao + "&$top=100&$format=json&$select=cotacaoVenda,dataHoraCotacao,tipoBoletim"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		df = pd.json_normalize(data["value"])
