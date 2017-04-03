#Import Library
from sklearn.linear_model import LogisticRegression
from sklearn import svm, naive_bayes, neighbors, ensemble, cross_validation
from sklearn.cross_validation import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# lendo dados limpo do curso de si
dados = pd.read_csv('eca_clean.csv')
dados.drop('NOTAS', axis=1, inplace=True)
dados.drop('N_FALTAS', axis=1, inplace=True)


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



# função para retornar o score da tecnica passada por parametro
def returnScoreAprovado(teste, model):
    model.fit(train_data_aprovado, target_data_aprovado)
    log_entry = pd.DataFrame([[teste, model.score(train_data_aprovado, target_data_aprovado)]], columns=log_cols)
    return log_entry
    
# função para retornar o score da tecnica passada por parametro
def returnScoreEvasao(teste, model):
    model.fit(train_data_evasao, target_data_evasao)
    log_entry = pd.DataFrame([[teste, model.score(train_data_evasao, target_data_evasao)]], columns=log_cols)
    return log_entry



def plotComparativo(dados):
    sns.set_color_codes("muted")
    sns.barplot(x='Accuracy', y='Test', data=dados, color="b")
    
    plt.xlabel('Accuracy %')
    plt.title('Comparativo')
    i=0
    for index, row in dados.iterrows():
        plt.text(1, i, row['Accuracy'])
        i+=1
    
    plt.show()


log_cols=["Test", "Accuracy"]
resultados_t01 = pd.DataFrame(columns=log_cols) 
resultados_t02 = pd.DataFrame(columns=log_cols)
resultados_t04 = pd.DataFrame(columns=log_cols)
resultados_t05 = pd.DataFrame(columns=log_cols)
resultados_t06 = pd.DataFrame(columns=log_cols)
resultados_t07 = pd.DataFrame(columns=log_cols)
resultados_t08 = pd.DataFrame(columns=log_cols)
tecnicas_selecionadas_aprovado = pd.DataFrame(columns=log_cols)
tecnicas_selecionadas_evasao = pd.DataFrame(columns=log_cols)


def testLogisticRegression():
    # Teste para Logistic Regression
    
    global resultados_t01  
    
    teste = 'T0101'
    model = LogisticRegression()
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0102'
    model = LogisticRegression(penalty='l1')
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0103'
    model = LogisticRegression(fit_intercept=False)
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0104'
    model = LogisticRegression(solver='newton-cg')
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0105'
    model = LogisticRegression(solver='lbfgs')
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0106'
    model = LogisticRegression(solver='sag')
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    teste = 'T0107'
    model = LogisticRegression(solver='lbfgs')
    resultados_t01 = resultados_t01.append(returnScoreEvasao(teste, model))
    
    #plot
    plotComparativo(resultados_t01)
    
    print('Logistic Regression')
    resultados_t01


def testSvmSVC():
    # Teste para SVM SVC

    global resultados_t02    
    
    teste = 'T0201'
    model = svm.SVC()
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))
    
    """teste = 'T0202'
    model = svm.SVC(kernel='linear')
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))
    
    teste = 'T0203'
    model = svm.SVC(kernel='poly')
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))
    
    teste = 'T0204'
    model = svm.SVC(kernel='sigmoid')
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))
    
    teste = 'T0205'
    model = svm.SVC(kernel='precomputed')
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))
    
    teste = 'T0206'
    model = svm.SVC(shrinking=False)
    resultados_t02 = resultados_t02.append(returnScoreEvasao(teste, model))"""
    
    
    
    plotComparativo(resultados_t02)
    
    print('SVM SVC')
    resultados_t02


def testSvmSVR():
    # Teste para SVM SVR
    
    global resultados_t04    
    
    teste = 'T0401'
    model = svm.SVR()
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))
    
    """teste = 'T0402'
    model = svm.SVR(kernel='linear')
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))
    
    teste = 'T0403'
    model = svm.SVR(kernel='poly')
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))
    
    teste = 'T0404'
    model = svm.SVR(kernel='sigmoid')
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))
    
    teste = 'T0405'
    model = svm.SVR(kernel='precomputed')
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))
    
    teste = 'T0406'
    model = svm.SVR(shrinking=False)
    resultados_t04 = resultados_t04.append(returnScoreEvasao(teste, model))"""
    
    plotComparativo(resultados_t04)
    
    print('SVM SVR')
    resultados_t04


def testKNNClassifier():
    # Teste para KNN Classifier
    
    global resultados_t05
    
    teste = 'T0501'
    model = neighbors.KNeighborsClassifier()
    resultados_t05 = resultados_t05.append(returnScoreEvasao(teste, model))
    
    teste = 'T0502'
    model = neighbors.KNeighborsClassifier(n_neighbors=3)
    resultados_t05 = resultados_t05.append(returnScoreEvasao(teste, model))
    
    teste = 'T0503'
    model = neighbors.KNeighborsClassifier(n_neighbors=7)
    resultados_t05 = resultados_t05.append(returnScoreEvasao(teste, model))
    
    teste = 'T0504'
    model = neighbors.KNeighborsClassifier(weights='distance')
    resultados_t05 = resultados_t05.append(returnScoreEvasao(teste, model))
    
    
    
    plotComparativo(resultados_t05)
    
    print('KNN Classifier')
    resultados_t05


def testKNNRegressor():
    # Teste para KNN Regressor
    
    global resultados_t06
    
    teste = 'T0601'
    model = neighbors.KNeighborsRegressor()
    resultados_t06 = resultados_t06.append(returnScoreEvasao(teste, model))
    
    teste = 'T0602'
    model = neighbors.KNeighborsRegressor(n_neighbors=3)
    resultados_t06 = resultados_t06.append(returnScoreEvasao(teste, model))
    
    teste = 'T0603'
    model = neighbors.KNeighborsRegressor(n_neighbors=7)
    resultados_t06 = resultados_t06.append(returnScoreEvasao(teste, model))
    
    teste = 'T0604'
    model = neighbors.KNeighborsRegressor(weights='distance')
    resultados_t06 = resultados_t06.append(returnScoreEvasao(teste, model))
    
    
    
    plotComparativo(resultados_t06)
    
    print('KNN Regressor')
    resultados_t06
    
def testNaiveBayesGaussianNB():
     # Teste para Naive Bayes GaussianNB
    
    global resultados_t07
    
    teste = 'T0701'
    model = naive_bayes.GaussianNB()
    resultados_t07 = resultados_t07.append(returnScoreEvasao(teste, model))
    
    plotComparativo(resultados_t07)
    
    print('Naive Bayes GaussianNB')
    resultados_t07
    
    
def testNaiveBayesBernoulliNB():
     # Teste para Naive Bayes BernoulliNB
    
    global resultados_t08
    
    teste = 'T0801'
    model = naive_bayes.BernoulliNB()
    resultados_t08 = resultados_t08.append(returnScoreEvasao(teste, model))
    
    plotComparativo(resultados_t08)
    
    print('Naive Bayes BernoulliNB')
    resultados_t08

testLogisticRegression()
testSvmSVC()
testSvmSVR()
testKNNClassifier()
testKNNRegressor()
testNaiveBayesGaussianNB()
testNaiveBayesBernoulliNB()

todos_testes = resultados_t01
todos_testes = todos_testes.append(resultados_t02)
todos_testes = todos_testes.append(resultados_t04)
todos_testes = todos_testes.append(resultados_t05)
todos_testes = todos_testes.append(resultados_t06)
todos_testes = todos_testes.append(resultados_t07)
todos_testes = todos_testes.append(resultados_t08)

print ('Todos os testes: \n', todos_testes)

plotComparativo(todos_testes)

todos_testes.to_csv('dados_comparativos_tecnicas_eca_evasao.csv', index=False)