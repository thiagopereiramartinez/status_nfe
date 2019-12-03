# API de consulta de status da NF-e pelo Portal Nacional
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
from requests import get
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def main():

    result = {}

    # Requisitar página de status
    request = get("http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=Skeuqr8PQBY=")
    html = request.content

    # Fazer o parse do HTML
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id="ctl00_ContentPlaceHolder1_gdvDisponibilidade2")

    items = list()

    for tr in table.find_all("tr"):
        # Eliminar o cabeçalho
        if tr.th != None:
            continue

        # Fazer parse do TD
        info = list()

        for td in tr.find_all("td"):
            if td.img != None:
                info.append(td.img["src"].split("_")[1])
                continue

            info.append(td.get_text())

        items.append(info)

    return jsonify({
        "autorizadores": list(map(lambda x: {
            "autorizador": x[0],
            "autorizacao": x[1],
            "retorno_autorizacao": x[2],
            "inutilizacao": x[3],
            "consulta_protocolo": x[4],
            "status_servico": x[5],
            "tempo_medio": x[6],
            "consulta_cadastro": x[7],
            "recepcao_evento": x[8]
        }
    , items)),
        "meta": {
            "ultima_verificacao": table.caption.span.get_text().split(" - ")[1].split(": ")[1],
            "versao": table.caption.span.get_text().split(" - ")[2]
        }
    })

# Executar se estiver executando pelo terminal
if __name__ == "__main__":
    app.run()
