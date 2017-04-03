#! /usr/bin/env python
import ast
import csv
import datetime

import flask
import requests
from dateutil.relativedelta import relativedelta
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user,current_user
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from werkzeug.utils import redirect

from manager import app, login_manager
from forms import AlunoForm, LoginForm,AlunoPesquisa
from models import Usuario, Aluno



global user


@login_manager.user_loader
def load_user(user):
    return Usuario.query.filter(Usuario.id_user == user).first()

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if request.method == 'POST':
        matricula = request.form['matricula'].replace(" ", "")
        senha = request.form['senha']


        user = Usuario.query.filter_by(login=matricula).first()

        if senha==user.senha:
            login_user(user)
            print(user)
            return redirect(url_for('dashboard'))
        else:
            error = '* Usuario ou senha invalidos'

    return render_template('login.html', form=form,error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/dashboard",methods=['GET', 'POST'])
@login_required
def dashboard():



    form = AlunoPesquisa()



    if request.method == 'POST':



        if form.validate_on_submit():

            matricula = request.form['matricula'].replace(" ", "")
            #curso = request.form['curso']



            aluno = Aluno.query.filter_by(MATRICULA=matricula).first()

            if aluno == None:

                data = requests.get('http://127.0.0.1:5001/' + matricula).json()

                data_evasao = requests.get('http://127.0.0.1:5002/' + matricula + '/evasao').json()
                evasao_predicao = ast.literal_eval(data_evasao["predicao"])
                evasao_score = ast.literal_eval(data_evasao["score"])
                evasao_cluster = ast.literal_eval(data_evasao["cluster"])
                if evasao_predicao == 1:            
                    evasao_cluster = ''.join(evasao_cluster)

                disciplinas_nao_cursadas = requests.get('http://127.0.0.1:5002/' + matricula + '/disciplinas').json()
                disciplinas = ast.literal_eval(disciplinas_nao_cursadas["disciplinas"])
                #disciplinas = []
                # print(data)

                probabilidades = ast.literal_eval(data["probabilidades"])
                aprovado = ast.literal_eval(data["porcentagem_aprovado"])
                reprovado = ast.literal_eval(data["porcentagem_reprovado"])
                probArray = []
                for c in probabilidades:
                    barData = {
                        'Nota': c[0],
                        'Probabilidade %': int(c[1]),

                    }

                    # append comment_dict to ['comments']
                    probArray.append(barData)

                    # insert idea dictionary into public_ideas list
                #print(probArray)

                ordenado  = sorted(probArray[:5], key=lambda k: k['Nota'])

                #print(ordenado)
                probabilidade_evasao = 0
                if(evasao_predicao==0):
                    probabilidade_evasao = 100-float(evasao_score[0]*100)

                else: probabilidade_evasao = float(evasao_score[0]*100)

                return render_template('dashboard.html',
                                       title='Sign In',
                                       form=form, matricula=matricula, probArray=ordenado,
                                       aprovado=aprovado,
                                       reprovado=reprovado,
                                       user=g.user.nome,
                                      # evasao_predicao=evasao_predicao,
                                       evasao_score=probabilidade_evasao,
                                       evasao_cluster=evasao_cluster,
                                       disciplinas=disciplinas,
                                       )
                                       #cursoaluno=curso)

            else:
                data_evasao = requests.get('http://127.0.0.1:5002/' + matricula + '/evasao').json()
                evasao_predicao = ast.literal_eval(data_evasao["predicao"])
                evasao_score = ast.literal_eval(data_evasao["score"])
                evasao_cluster = ast.literal_eval(data_evasao["cluster"])
                if evasao_predicao == 1:            
                    evasao_cluster = ''.join(evasao_cluster)

                disciplinas_nao_cursadas = requests.get('http://127.0.0.1:5002/' + matricula + '/disciplinas').json()
                disciplinas = ast.literal_eval(disciplinas_nao_cursadas["disciplinas"])

                print(evasao_predicao)
                print(evasao_score)
                probabilidade_evasao = 0
                if (evasao_predicao == 0):
                    probabilidade_evasao = 100 - float(evasao_score[0] * 100)

                else:
                    probabilidade_evasao = float(evasao_score[0] * 100)

                return render_template('dashboard.html',
                                       title='Sign In',
                                       form=form, matricula=matricula,
                                       user=g.user.nome,
                                       # evasao_predicao=evasao_predicao,
                                       evasao_score=probabilidade_evasao,
                                       evasao_cluster=evasao_cluster,
                                       disciplinas=disciplinas,
                                       novato=1)
        else:

            return render_template('dashboard.html',
                                   form=form, user=g.user.nome, error="Matrícula Inválida: A matrícula deve conter 14 dígitos")
            # cursoaluno=curso)

    return render_template('dashboard.html',
                           form=form,user=g.user.nome)
          

@app.route("/alunos", methods=['GET', 'POST'])
@login_required
def alunos():
    formAluno = AlunoForm()

    if request.method == 'POST':
        if formAluno.validate():

            alunoForm = setAluno()

            aluno = Aluno.query.filter_by(MATRICULA=request.form['matricula']).first()

            if(aluno != None):
               modificaAluno(aluno,alunoForm)
               Aluno.saveAluno(aluno)
               Aluno.editAlunoCSV(aluno)


            else:
                Aluno.saveAluno(alunoForm)
                Aluno.saveAlunoCSV(alunoForm)


        else:
            error = "Por favor, preencher todos os campos"
            #print(formAluno.errors)
            alunos = Aluno.listAlunos(Aluno)
            return render_template('alunos.html', form=formAluno, user=g.user.nome,error=error,alunos=alunos)

    if request.method == 'GET':

        if request.args !=None :
            id = request.args.get('id', 0, type=int)

            print ('removendo '+str(id))
            if id != 0:
                aluno = Aluno.query.filter_by(MATRICULA=id).first()
                Aluno.removeAluno(aluno)
                Aluno.removeAlunoCSV(aluno)

    alunos = Aluno.listAlunos(Aluno)

    return render_template('alunos.html',form=formAluno,user=g.user.nome,alunos=alunos)

@app.route("/predicaodisciplina/<matricula>/<disciplina>")
def predicaodisciplina(matricula, disciplina):
    resultado = requests.get('http://127.0.0.1:5002/'+matricula+'/'+disciplina).json()
    predicao = ast.literal_eval(resultado["predicao"])
    cluster = ast.literal_eval(resultado["cluster"])
    
    
    if predicao == 0:
        cluster = ''.join(cluster)
        texto = 'Com base na predicao, o aluno <b>reprovará</b> na disciplina: ' + str(disciplina) + '. <br>Esse aluno foi classificado no grupo com as seguintes caracteristicas: ' + str(cluster)
        #texto = ''.join(texto)
    elif predicao == 1:
        texto = 'Com base na predicao, o aluno será <b>aprovado</b> na disciplina: ' + str(disciplina) + '.'
    
    return texto
    
@app.route("/removeAluno", methods=['GET', 'POST'])
def removeAluno():
    id = request.args.get('id', 0, type=int)
    Aluno.query.filter(Aluno.MATRICULA == id).delete()
    return flask.jsonify(result='ok')


@app.route("/getAlunoData")
def getAlunoData():
    id = request.args.get('id', 0, type=int)

    aluno = Aluno.query.filter_by(MATRICULA=id).first()
    return flask.jsonify(result=Aluno.serialize(aluno))


def modificaAluno(aluno, alunoForm):
    aluno.SIT_MATRICULA = alunoForm.SIT_MATRICULA
    aluno.RENDA_FAMILIAR = alunoForm.RENDA_FAMILIAR
    aluno.TIPO_ESCOLA_ORIGEM =  alunoForm.TIPO_ESCOLA_ORIGEM
    aluno.ANO_CONCLUSAO_2_GRAU = alunoForm.ANO_CONCLUSAO_2_GRAU
    aluno.ANO_INGRESSO =  alunoForm.ANO_INGRESSO
    aluno.RENDA_PER_CAPITA = alunoForm.RENDA_PER_CAPITA
    aluno.COD_ESTADO_CIVIL = alunoForm.COD_ESTADO_CIVIL
    aluno.N_FILHOS = alunoForm.N_FILHOS
    aluno.SEXO =  alunoForm.SEXO
    aluno.PROFISSAO = alunoForm.PROFISSAO
    aluno.DESC_CIDADE = alunoForm.DESC_CIDADE
    aluno.DT_NASCIMENTO = alunoForm.DT_NASCIMENTO
    aluno.NIVEL_FALA_INGLES = alunoForm.NIVEL_FALA_INGLES
    aluno.NIVEL_COMPREENSAO_INGLES = alunoForm.NIVEL_COMPREENSAO_INGLES
    aluno.NIVEL_ESCRITA_INGLES = alunoForm.NIVEL_ESCRITA_INGLES
    aluno.NIVEL_LEITURA_INGLES = alunoForm.NIVEL_LEITURA_INGLES
    aluno.CURSO = alunoForm.CURSO
    aluno.IDADE_INGRESSO = calculaIdade(alunoForm.DT_NASCIMENTO,alunoForm.ANO_INGRESSO)

def calculaIdade(dt_nascimento,ano_ingresso):
    data_nasc = datetime.datetime.strptime(dt_nascimento.replace("/", ""), '%d%m%Y').date()

    return int(ano_ingresso) -  data_nasc.year ;


def setAluno():
    matricula = request.form['matricula']
    sit_matricula = request.form['sit_matricula']
    renda_familiar = request.form['renda_familiar']
    tipo_escola = request.form['tipo_escola']
    ano_conclusao_2_grau = request.form['ano_conclusao_2_grau']
    ano_ingresso = request.form['ano_ingresso']
    renda_per_capita = request.form['renda_per_capita']
    estado_civil = request.form['estado_civil']
    numero_filhos = request.form['numero_filhos']
    sexo = request.form['sexo']
    profissao = request.form['profissao']
    cidade = request.form['cidade']
    dt_nascimento = request.form['dt_nascimento']
    nivel_fala = request.form['nivel_fala']
    nivel_compreensao = request.form['nivel_compreensao']
    nivel_escrita = request.form['nivel_escrita']
    nivel_leitura = request.form['nivel_leitura']
    curso = request.form['curso']

    a = Aluno(matricula, sit_matricula, renda_familiar, tipo_escola, ano_conclusao_2_grau,ano_ingresso,
              renda_per_capita, estado_civil, numero_filhos, sexo, profissao, cidade, dt_nascimento, nivel_fala,
              nivel_compreensao, nivel_escrita, nivel_leitura, curso, calculaIdade(dt_nascimento, ano_ingresso))

    return a





@app.route("/curvanormal/<matricula>")
def curvanormal(matricula):

    data = requests.get('http://127.0.0.1:5001/'+matricula+'/curvanormal')
    #print(data)
    return data.content


@app.route("/cluster")
def cluster():
    return render_template('cluster.html')

@app.route("/error")
def error():
    return render_template('error.html')


@app.route("/teste")
def teste():
    return render_template('teste.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'),404


def hash_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=25600)


def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)


app.run(host='0.0.0.0', port=5000)
