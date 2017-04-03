#coding: utf-8
import pandas as pd
import json
from sklearn.externals import joblib

def retornarDadosCurso(curso):    
    if curso == 'si':
        dados = pd.read_csv('dados/si_clean_com_matricula.csv')
    elif curso == 'eca':
        dados = pd.read_csv('dados/eca_clean_com_matricula.csv')
    dados.drop('NOTAS', axis=1, inplace=True)
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
    
def retornarScore(curso, tipo_predicao):
    score = pd.read_csv('dados/score_tecnicas.csv')
    score = score.loc[((score['Curso']==curso) & (score['Tipo']==tipo_predicao)), 'Score']
    return(score.values)
    
def realizarPredicao(dados_aluno, curso, tipo_predicao):
    if curso == 'si':
        if tipo_predicao == 'aprovado':
            model = joblib.load('model/model_si_aprovado.pkl')
        elif tipo_predicao == 'evasao':
            model = joblib.load('model/model_si_evasao.pkl')
    elif curso == 'eca':
        if tipo_predicao == 'aprovado':
            model = joblib.load('model/model_eca_aprovado.pkl')
        elif tipo_predicao == 'evasao':
            model = joblib.load('model/model_eca_evasao.pkl')
    return model.predict(dados_aluno), retornarScore(curso, tipo_predicao)
    
    
def retornarCaracteristicaCluster(curso, tipo_predicao, cluster):
    caracteristica = pd.read_csv('dados/caracteristicas_clusters.csv', sep=';', encoding='latin-1')
    caracteristica = caracteristica.loc[((caracteristica['Curso']==curso) & (caracteristica['Tipo']==tipo_predicao) & (caracteristica['Cluster']==cluster)), 'Descricao']
    return(caracteristica.values)
    
def predicaoCluster(matricula, curso, tipo_predicao):  

    dados = retornarDadosCurso(curso)
    # selecionando as caracteristicas do aluno
    aluno = dados.loc[dados['MATRICULA']==matricula][:]  
    aluno.drop('MATRICULA', axis=1, inplace=True)    
    aluno.drop('APROVADO', axis=1, inplace=True)
    aluno.drop('COD_DISCIPLINA', axis=1, inplace=True)
    aluno.drop('SIT_MATRICULA', axis=1, inplace=True)
    aluno = aluno.head(1)
    
    aluno.to_csv('aluno_temp.csv', index=False)
    
    from weka.clusterers import Clusterer
    import weka.core.jvm as jvm
    from weka.core.converters import Loader
    import weka.core.serialization as serialization     
        
    jvm.start()
    
    if curso == 'si':
        if tipo_predicao == 'reprovacao':
            model = serialization.read_all("model/kmeans_si_reprovacao.model")
        elif tipo_predicao == 'evasao':
            model = serialization.read_all("model/kmeans_si_evasao.model")
    elif curso == 'eca':
        if tipo_predicao == 'reprovacao':
            model = serialization.read_all("model/kmeans_eca_reprovacao.model")
        elif tipo_predicao == 'evasao':
            model = serialization.read_all("model/kmeans_eca_evasao.model")
    cluster = Clusterer(jobject=model[0])
    
    
    loader = Loader(classname="weka.core.converters.CSVLoader")
    dado_aluno = loader.load_file("aluno_temp.csv")
    for aluno in dado_aluno:
        cluster_aluno_pertence = cluster.cluster_instance(aluno)
    
    #jvm.stop()    
    
    caracteristica = retornarCaracteristicaCluster(curso, tipo_predicao, cluster_aluno_pertence)
    
    return caracteristica
  
    
def predicaoEvasao(matricula):
    matricula = int(matricula)
    curso = retornarCursoAluno(matricula)
    dados = retornarDadosCurso(curso)
    
    matricula = int(matricula)
    
    
    # selecionando as caracteristicas do aluno
    predict = dados.loc[dados['MATRICULA']==matricula][:]  
    predict.drop('MATRICULA', axis=1, inplace=True)    
    predict.drop('APROVADO', axis=1, inplace=True)
    predict.drop('COD_DISCIPLINA', axis=1, inplace=True)
    predict.drop('SIT_MATRICULA', axis=1, inplace=True)
    predict = predict.iloc[0]
    
    predicao, score = realizarPredicao(predict, curso, 'evasao')
    
    cluster = None
    if predicao == 1:
        cluster = predicaoCluster(matricula, curso, 'evasao')
    
    json_resposta = json.dumps({
      "predicao": str(int(predicao)),
      "score": str(score),
      "cluster": str(cluster)}, ensure_ascii=False).encode('utf8')
       
    return json_resposta
    

def predicaoDisciplina(matricula, disciplina):
    matricula = int(matricula)
    curso = retornarCursoAluno(matricula)
    dados = retornarDadosCurso(curso)
    
    
    disciplina = int(disciplina)
    
    # selecionando as caracteristicas do aluno
    predict = dados.loc[dados['MATRICULA']==matricula][:]  
    predict.drop('MATRICULA', axis=1, inplace=True)    
    predict.drop('APROVADO', axis=1, inplace=True)
    predict.drop('SIT_MATRICULA', axis=1, inplace=True)
    predict = predict.iloc[0]
    predict['COD_DISCIPLINA'] = disciplina
    
    #dados.to_csv('temptemp.csv', index=False)
    
    predicao, score = realizarPredicao(predict, curso, 'aprovado')
      
    
    cluster = None
    if predicao == 0:
        predict.drop('COD_DISCIPLINA', inplace=True)
        cluster = predicaoCluster(matricula, curso, 'reprovacao')
        #cluster = ''.join(cluster)
    
    aux = json.dumps({
      "predicao": str(int(predicao)),
      "score": str(score),
      "cluster": str(cluster)}, ensure_ascii=False).encode('utf8')
      
    return aux
    
    
def retornaDisciplinasCurso(curso):
    curso = str(curso)
    dados = retornarDadosCurso(curso)
    
    return dados['COD_DISCIPLINA'].unique()
    
def retornaDisciplinasAluno(curso, matricula):
    curso = str(curso)
    dados = retornarDadosCurso(curso)
    matricula = int(float(matricula))
    aluno = dados.loc[dados['MATRICULA']==matricula][:]
    disciplinas = aluno.loc[aluno['APROVADO']==1, 'COD_DISCIPLINA']
    
    return disciplinas.unique()
    
def retornaNomeDisciplinas(disciplinas, curso):
    if curso == 'si':
        dados = pd.read_csv('dados/disciplinas_si.csv')
    elif curso == 'eca':
        dados = pd.read_csv('dados/disciplinas_eca.csv')
        
    existentes = dados[dados['COD_DISCIPLINA'].isin(disciplinas)]
    
    existentes = existentes.sort_values(by='DISCIPLINA')    
    
    existentes['COD_DISCIPLINA'] = existentes['COD_DISCIPLINA'].astype(str) + ' - ' + existentes['DISCIPLINA'].astype(str)
    
    lista = existentes['COD_DISCIPLINA'].tolist()
    
    return lista
    
def DisciplinasNaoCursada(matricula):
    matricula = int(matricula)
    curso = retornarCursoAluno(matricula)
    disciplinas_curso = retornaDisciplinasCurso(curso)
    disciplinas_aluno = retornaDisciplinasAluno(curso, matricula)
    
    disciplinas_nao_cursada = list(set(disciplinas_curso) - set(disciplinas_aluno))
    disciplinas_com_nome = retornaNomeDisciplinas(disciplinas_nao_cursada, curso)
    
    json_resposta = json.dumps( {
        "disciplinas": str(disciplinas_com_nome)}, ensure_ascii=False).encode('utf8')
        
    return json_resposta