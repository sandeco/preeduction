from flask import Flask
import distribuicaonormal

app = Flask(__name__)

@app.route("/")
def listarServicos():

    return u"""
    <html>
       <head><title>Serviços disponíveis</title></head>
       <body>
          <h1>Serviços disponíveis de distribuição normal nesta porta:</h1>
          <ul>
            <li> */matricula* para ter todas as informações da distribuição normal do aluno. </li>
            <li> Exemplo: /20131011090192 </li>
            <li> */matricula/curvanormal* para retornar uma imagem em png com o grafico da curva normal do aluno. </li>
            <li> Exemplo: /20131011090192/curvanormal </li>
          </ul>
       </body>
    </html>
    """

@app.route("/<matricula>")
def json_distribuicao_normal(matricula):
    return distribuicaonormal.dadosDistribuicaoNormal(matricula)
	
@app.route("/<matricula>/curvanormal")
def png_grafico(matricula):
    return distribuicaonormal.png_grafico(matricula)


app.run(host='0.0.0.0', port=5001)
