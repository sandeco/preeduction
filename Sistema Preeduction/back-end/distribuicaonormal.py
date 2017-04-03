import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
from operator import itemgetter
from flask import make_response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def retornarDadosCurso(curso):    
    if curso == 'si':
        dados = pd.read_csv('dados/si_clean_com_matricula.csv')
    elif curso == 'eca':
        dados = pd.read_csv('dados/eca_clean_com_matricula.csv')
    dados.drop('N_FALTAS', axis=1, inplace=True)
    return dados      
      
def retornarCursoAluno(matricula):
    curso = pd.read_csv('dados/si_clean_com_matricula.csv')
    if matricula in curso.MATRICULA.values:
        curso = 'si'
    else:
        curso = pd.read_csv('dados/eca_clean_com_matricula.csv')
        if matricula in curso.MATRICULA.values:
            curso = 'eca'
    
    return curso
    
def valorAreaAprovado(n):
    # primeiro ponto do grafico
    valor1 = 6
    # segundo ponto do grafico
    valor2 = 10
    
    # calcular distribuicao cumulativa
    valor_area_aprovado = norm.cdf(valor2, n.mean(), n.std()) - norm.cdf(valor1, n.mean(), n.std())
    
    return valor_area_aprovado
    
def valorAreaReprovado(n):
    # primeiro ponto do grafico
    valor1 = 0
    # segundo ponto do grafico
    valor2 = 5.9
    valor_area_reprovado = norm.cdf(valor2, n.mean(), n.std()) - norm.cdf(valor1, n.mean(), n.std())
    
    return valor_area_reprovado

def graficoDistribuicaoNormal(n, x):
    y_grafico = (norm.pdf(x, loc=n.mean(), scale=n.std())*100)
    return y_grafico

def probabilidadesNotas(n):
    probabilidades = [] # armazenar a nota e sua probabilidade
    aux = 0.0
    for i in range(21):
        p = stats.norm(n.mean(), n.std()).pdf(aux)
        p = p[0]
        #print("A probabilidade do aluno tirar nota " + str(aux) + " e: " + str(p*100) + "%")
        probabilidades += [(aux, p*100)]
        aux += 0.5
    
    probabilidades = sorted(probabilidades,key=itemgetter(1), reverse=True)
    
    return probabilidades

def notaAluno(matricula, curso):
    curso = str(curso)
    matricula = int(float(matricula))
    dados = retornarDadosCurso(curso)
    aluno = dados.loc[dados['MATRICULA']==matricula][:]
    notas = aluno['NOTAS']
    
    return pd.DataFrame(notas)  

def returnPontosGrafico(matricula, curso):
    n = notaAluno(matricula, curso)

    x = np.linspace(0.0, 10.0)
    y_grafico = graficoDistribuicaoNormal(n, x)
    return x, y_grafico    

def dadosDistribuicaoNormal(matricula):
    
    matricula = int(matricula)
    curso = retornarCursoAluno(matricula)
    
    n = notaAluno(matricula, curso)
    x, y_grafico = returnPontosGrafico(matricula, curso)

    probabilidades = probabilidadesNotas(n)
    
    valor_area_aprovado = valorAreaAprovado(n)
    valor_area_reprovado = valorAreaReprovado(n)
    
    aux = json.dumps({
      "probabilidades": str(probabilidades), 
      "porcentagem_aprovado": str(valor_area_aprovado), 
      "porcentagem_reprovado": str(valor_area_reprovado)})
    
    return aux
    
def png_grafico(matricula):
    matricula = int(matricula)
    curso = retornarCursoAluno(matricula)
    x, y = returnPontosGrafico(matricula, curso)
    
    fig=Figure()
    ax=fig.add_subplot(111)
    
    ax.plot(x, y, '-')
    ax.set_xlabel('Notas')
    ax.set_ylabel('Probabilidade %')
    
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response