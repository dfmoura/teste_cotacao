from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='EUR'&@dataInicial='04-01-2023'&@dataFinalCotacao='04-11-2023'&$top=100&$format=json&$select=cotacaoVenda,dataHoraCotacao,tipoBoletim"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data["value"])
        df = df[["cotacaoVenda", "dataHoraCotacao", "tipoBoletim"]]
        df = df[df["tipoBoletim"] == "Fechamento"]
        return render_template("index.html", data=df.to_html())
    else:
        return "Failed to retrieve data."

if __name__ == "__main__":
    app.run()
