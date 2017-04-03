import pandas as pd


eca = pd.read_csv('eca_clean.csv')

eca = eca.loc[eca['APROVADO']==0]

eca.drop('SIT_MATRICULA',axis=1, inplace=True)
eca.drop('NOTAS',axis=1, inplace=True)
eca.drop('N_FALTAS',axis=1, inplace=True)
eca.drop('COD_DISCIPLINA',axis=1, inplace=True)
eca.drop('APROVADO',axis=1, inplace=True)


eca.to_csv('temp.csv', index=False)


from weka.clusterers import Clusterer
import weka.core.jvm as jvm
import weka.core.serialization as serialization

jvm.start()

# executar a tecnica variando de 1 a 9 clusters 
for i in range(1,10):
    print '**************Numero de clusters: ' + str(i)
    clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", str(i)])
    clusterer.build_clusterer(eca)
    print(clusterer)

clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "4"])
clusterer.build_clusterer(eca)
print(clusterer)
serialization.write("model/kmeans_eca_reprovacao.model", clusterer)


# ler model
'''objects = serialization.read_all("cluster.model")
clusterer = Clusterer(jobject=objects[0])

data_aluno = loader.load_file("aluno_temp.csv")
for instancia in data_aluno:
    resultado = clusterer.cluster_instance(instancia) 
    print ('O aluno pertence ao cluster: ' + str(resultado))'''


"""
for inst in data:
    cl = clusterer.cluster_instance(inst)  # 0-based cluster index
    dist = clusterer.distribution_for_instance(inst)   # cluster membership distribution

    print("cluster=" + str(cl) + ", distribution=" + str(dist))


# Ler modelo de cluster salvo e realizar classificação
import weka.core.serialization as serialization
from weka.classifiers import Classifier
objects = serialization.read_all("cluster.model")
clusterer = Clusterer(jobject=objects[0])

predict = clusterer.cluster_instance(aluno)
print(clusterer)"""



jvm.stop()
