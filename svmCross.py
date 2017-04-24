import csv
from svmutil import *

entradasT = []
salidasT = []

with open('Mammographic.csv','r') as archivo:
    reader = csv.reader(archivo)          
    for row in reader:
        try:
            #Intenta encontrar el indice de un atributo faltante
            row.index("?")
        except ValueError:
            #Al no faltar atributos faltantes entra aqui
            fila = []
            for valor in row:
                #Se agregan los valores como float porque se necesitan asi en svm_problem
                fila.append(float(valor))
            #Se borra el atributo edad que esta en la posicion 1
            del fila[1]
            entradasT.append(fila)
            salidasT.append(float(row[5]))

cantPartes = 10
cantPorParte = len(salidasT)/cantPartes
precisiones = []
                   
for posPrueba in range(cantPartes):
    posInicioPrueba = posPrueba*cantPorParte
    posFinPrueba = posInicioPrueba+cantPorParte
    #Datos para prueba
    entradasPrueba = entradasT[posInicioPrueba:posFinPrueba]
    salidasPrueba = salidasT[posInicioPrueba:posFinPrueba]
    #Datos de entrenamiento
    entradasEntre = entradasT[:]
    salidasEntre = salidasT[:]
    #Se borran los datos que se encuentran en los indices de pruebas actuales
    del entradasEntre[posInicioPrueba:posFinPrueba]
    del salidasEntre[posInicioPrueba:posFinPrueba]

    prob = svm_problem(salidasEntre,entradasEntre)
    m = svm_train(prob, '-t 0 -s 1')   
    p_label, p_acc, p_val = svm_predict(salidasPrueba, entradasPrueba, m)
    precisiones.append(p_acc[0])

precisionFinal = sum(precisiones)/len(precisiones)
print "Precision Final: " + str(precisionFinal)
prob = svm_problem(salidasT,entradasT)
m = svm_train(prob, '-v 140')   
