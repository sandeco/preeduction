from flask import Flask 
import predicao

app = Flask(__name__)

@app.route("/")
def listarServicos():
    
    return u"""
    <html>
       <head><title>Serviços disponíveis</title></head>
       <body>
          <h1>Serviços disponíveis de predição nesta porta:</h1>
          <ul>
            <li> */curso/matricula/disciplina* para ter a predição se o aluno será aprovado ou nao na disciplina informada. </li>
            <li> Exemplo: /si/20131011090192/22612 </li>
            <li> */curso/matricula/evasao* para ter a predição se o aluno irá evadir ou não do curso. </li>
            <li> Exemplo: /si/20131011090192/evasao </li>
          </ul>
       </body>
    </html>
    """

@app.route("/<matricula>/<disciplina>")
def json_predicao(matricula, disciplina):
    return predicao.predicaoDisciplina(matricula, disciplina)
    
@app.route("/<matricula>/evasao")
def json_evasao(matricula):
    return predicao.predicaoEvasao(matricula)
   
@app.route("/<matricula>/disciplinas")
def json_disciplinas_nao_cursadas(matricula):
    return predicao.DisciplinasNaoCursada(matricula)
    
app.run(host='0.0.0.0', port=5002)