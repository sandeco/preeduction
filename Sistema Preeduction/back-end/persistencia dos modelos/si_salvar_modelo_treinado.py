from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn import svm, naive_bayes, neighbors
import pandas as pd

# lendo dados limpo do curso de si
dados = pd.read_csv('../dados/si_clean.csv')

dados.drop('NOTAS', axis=1, inplace=True)
dados.drop('N_FALTAS', axis=1, inplace=True)
dados.drop('MATRICULA', axis=1, inplace=True)


# montando dados para treinamento 
train_data_aprovado = dados[:]
train_data_aprovado.drop('APROVADO',axis=1, inplace=True)
train_data_aprovado.drop('SIT_MATRICULA',axis=1, inplace=True)

train_data_evasao = dados[:]
train_data_evasao.drop('APROVADO',axis=1, inplace=True)
train_data_evasao.drop('SIT_MATRICULA',axis=1, inplace=True)
train_data_evasao.drop('COD_DISCIPLINA',axis=1, inplace=True)

# target
target_data_aprovado = dados['APROVADO']
target_data_evasao = dados['SIT_MATRICULA']

def retornaModeloTreinado(model, validacao):
    if validacao == 'aprovado':
        X = train_data_aprovado
        y = target_data_aprovado
    elif validacao == 'evasao':
        X = train_data_evasao
        y = target_data_evasao
    
    return model.fit(X, y)

# escolhidos para aprovado/reprovado
logistic_regression_aprovado = LogisticRegression(penalty='l1')
svm_aprovado = svm.SVC()
knn_aprovado = neighbors.KNeighborsClassifier(weights='distance')
naive_bayes_aprovado = naive_bayes.BernoulliNB()

# escolhidos para evasao
logistic_regression_evasao = LogisticRegression(solver='newton-cg')
svm_evasao = svm.SVC()
knn_evasao = neighbors.KNeighborsRegressor(n_neighbors=7)
naive_bayes_evasao = naive_bayes.BernoulliNB()

# salvando os modelos treinados

joblib.dump(retornaModeloTreinado(knn_aprovado, 'aprovado'), 'model/model_si_aprovado_knn.pkl')
joblib.dump(retornaModeloTreinado(knn_evasao, 'evasao'), 'model/model_si_evasao_knn.pkl')
print('ok')