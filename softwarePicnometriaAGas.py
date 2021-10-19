"""
#UNIVERSIDADE TECNOLÓGICA FEDERAL DO PARANÁ

#ANO: 2021

#ALUNO: PAULO GASPAR
#ORIENTADOR: RICARDO SCHNEIDER
#COORIENTADOR: FELIPE PFRIMER

#SOFTWARE UTILIZADO PARA A ANÁLISE DE DADOS DE MEDIÇÕES DE PRESSÃO OBTIDAS NO PROCESSO DE PICNOMETRIA A GÁS

#Este software permite o usuário importar um arquivo CSV com valores de pressão...
#gerados pelo SPARKvue e realizar o cálculo de volume, selecionando manualmente...
#na interface gráfica os valores de pressão inicial, intermediária e final.

"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
import math

#leitura de arquivo CSV
with open('esf7K.csv', newline='') as csvfile:
 
    #para csv gerado no SPARKvue
    #-----
    #faz a leitura do arquivo CSV gerado pelo SPARKvue
    auxReader = csv.reader(csvfile, delimiter=';', quotechar='|')
    #-----
    
    #converte objeto para uma lista de lista com três strings 
    testData = list(auxReader)

#Manipulação de dados
#Para CSV gerado no SPARKvue
#-----
    
#exclui o primeiro item da lista, pois é referente ao título das colunas    
del testData[0]         
#transforma testData em um vetor numpy 
testData = np.asarray(testData)
#mantém apenas a coluna de número 2, referente aos valores de pressão 
testData = testData[:,2]

#um for percorrendo a lista testData
for i in range(len(testData)):
    #troca a vírgula, por ponto, então converte a string em um float e multiplica por mil, transformando de kPA para PA
    testData[i] = np.float64(testData[i].replace(',','.'))*1000

#transforma testData de uma matriz de strings em uma matriz de floats, 
testData = testData.astype(np.float)

#-----

#y recebe os valores de pressão
y = testData
#x recebe série de valores de 0 até o número total de amostras em y
x = np.asarray(range(len(y)))

#cria um subplot
fig, ax = plt.subplots()
#ajusta a posição do plot criado
plt.subplots_adjust(right=0.8)
#habilita iteratividade no matplotlib
plt.ion()
# plota os valores de pressão
l, = plt.plot(x,y,lw=2)

#habilita o cursor, para facilitar posicionamento no gráfico
cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                color = 'r', linewidth = 1)

#valores de pressão inicial, média e final recebem -1. 
#Este valor representa que não há um valor valido selecionado
piValue = -1
pmValue = -1
pfValue = -1

#cria lista para argumentos das regiões selecionadas de pressão inicial, média e final
argsPi = []
argsPm = []
argsPf = []

#auxBool é um auxiliar que identifica se foi selecionado o inicio ou o fim...
#do intervalo de medição de uma pressão
#auxBool = False - Está no estágio de seleção do início do intervalo
#auxBool = True - Está no estágio de seleção do fim do estágio
auxBool = False

#auxPress é um auxiliar referente a que pressão está sendo selecionada 
# auxPress = 1 - Está no estágio de selecionar a pressão inicial (pi)
# auxPress = 2 - Está no estágio de selecionar a pressão intermediária (pm)
# auxPress = 3 - Está no estágio de selecionar a pressão final (pf)
# auxPress = 4 - Os valores de pressão já foram selecionados e é calculado o volume
auxPress = 1

#posicionamento dos textos na interface gráfica
axPiTexto = [0, -1]
axPmTexto = [0,-2]
axPfTexto = [0,-3]

#posicionamento dos valores na interface gráfica
axPiValue = [0, -1.5]
axPmValue = [0,-2.5]
axPfValue = [0,-3.5]
axVolume = [0,-4]

#posicionamento do botão de recete na interface gráfica
axReset = plt.axes([0.85, 0.8, 0.1, 0.075])
#axReset = plt.axes([0.85, 0.7, 0.1, 0.075])

#-----
#dados para fazer o cálculo pós calibração. 
# Caso a calibração não foi realizada ainda seguir a observação abaixo 
'''
OBSERVAÇÃO: PARA REALIZAR A CALIBRAÇÃO, INSERIR OS SEGUINTES VALORES NAS VARIÁVEIS:
    minfator = 0; maxVolume = 1; maxFator = 1;
DESTE MODO, OS VALORES EXIBIDOS  NA INTERFACE GRÁFICA SÃO DOS FATORES, QUE PODERÃO SER USADOS NA CALBRAÇÃO.
    
'''

#o fator medido com a câmara vazia
minFator = 0.1590

#o máximo de volume  medido nas calibrações ...
# neste caso o máximo medido foram 7 esferas de raio de 0.25cm - um volume total de 0.459ml.
maxVolume = ((4/3)*math.pi*(0.25**3))*7
#o fator medido com o volume máximo
maxFator = 0.1943

# classe com a função referente ao botão reset    
class Index:
    #ind = 0
    
    #função do botão reset: Limpa os dados e as informações da interface gráfica para ficar como no início
    def reset(self, event):
    
        global piValue, pmValue, pfValue, argsPi, argsPm, argsPf, auxPress, auxBool
        piValue = -1
        pmValue = -1
        pfValue = -1
        argsPi = []
        argsPm = []
        argsPf = []
        auxPress = 1
        auxBool = False;
        
        piValueTexto.set_text(' ')
        pmValueTexto.set_text(' ')
        pfValueTexto.set_text(' ')
        volumeTexto.set_text(' ')
        
        ax.clear()
        ax.plot(x,y,lw=2)
        fig.canvas.draw()
        
        
    
#objeto que é chamado ao pressionar no botão    
callback = Index()

#é criado o botão reset na interface gráfica
bReset = Button(axReset, 'Reset')
#o botão reset recebe o a função reset dentro do objeto callback, que é do tipo index
bReset.on_clicked(callback.reset)

#posiciona os textos e os valores a aparecerem na interface gráfica
piTexto = plt.text(axPiTexto[0],axPiTexto[1], "Pressão Inicial: ")
piValueTexto = plt.text(axPiValue[0],axPiValue[1],' ')
pmTexto = plt.text(axPmTexto[0],axPmTexto[1], "Pressão Intermediaria: ")
pmValueTexto = plt.text(axPmValue[0],axPmValue[1],' ')
pfTexto = plt.text(axPfTexto[0],axPfTexto[1], "Pressão Final: ")
pfValueTexto = plt.text(axPfValue[0],axPfValue[1],' ')
volumeTexto = plt.text(axVolume[0],axVolume[1],' ')

#------------------------------------------------------------------------------
#FUNÇÕES DE SELEÇÃO DE INTERVALOS
#selecaoLivre: permite a selecao livre do intervalo de medidas
#selecaoAutomatica : realiza a selecao automatica do intervalo de medidas

#função que permite a seleção livre do intervalo de medidas
def selecaoLivre(event):
    #chama os objetos definidos fora da função que são necessários para seu funcionamento
    global  x, y, auxBool, auxPress, argsPi, argsPm, argsPf, piValue, pmValue, pfValue
    # xPoint recebe o ponto no eixo x onde ocorreu o clique na interface gráfica
    xPoint = event.xdata
    
    #estágio de seleção da pressão inicial (piValue)
    if auxPress == 1:
        #caso esteja na etapa de seleção do início do intervalo de medidas
        if auxBool == False:    
            #é guardado aorgumento (posição do eixo x)
            argsPi.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='blue')
            #altera auxBool para True, para ir pra etapa de seleção do fim do intervalo
            auxBool = True;
            
        #caso esteja na etapa de seleção do fim do intervalo de medidas    
        else:
            #é guardado aorgumento (posição do eixo x)
            argsPi.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='blue')
            #altera auxBool para False, para ir pra etapa de seleção de início de intervalo
            auxBool = False;
            #auxPress recebe 2, o que significa que no próximo clique... 
            #será selecionada a pressão intermediária
            auxPress = 2
            #piValue recebe a média dos valores de pressão selecionados
            piValue = np.mean(y[ argsPi[0]:argsPi[1]] )
            #exibe na interface gráfica o valor da pressão inicial
            piValueTexto.set_text('{:.2f}'.format(piValue) + ' Pa')
                
    #estágio de seleção da pressão intermediária (pmValue)        
    elif auxPress == 2:
        #caso esteja na etapa de seleção do início do intervalo de medidas
        if auxBool == False:   
            #é guardado aorgumento (posição do eixo x)
            argsPm.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='green')
            #altera auxBool para True, para ir pra etapa de seleção do fim do intervalo
            auxBool = True;
        
        #caso esteja na etapa de seleção do fim do intervalo de medidas  
        else:
            #é guardado aorgumento (posição do eixo x)
            argsPm.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='green')
            #altera auxBool para False, para ir pra etapa de seleção de início de intervalo
            auxBool = False;
            #auxPress recebe 3, o que significa que no próximo clique... 
            #será selecionada a pressão final
            auxPress = 3
            #pmValue recebe a média dos valores de pressão selecionados
            pmValue = np.mean(y[ argsPm[0]:argsPm[1]] )
            #exibe na interface gráfica o valor da pressão intermediária
            pmValueTexto.set_text('{:.2f}'.format(pmValue) + ' Pa')
    
    #estágio de seleção da pressão final (pfValue)  
    elif auxPress == 3:
        #caso esteja na etapa de seleção do início do intervalo de medidas
        if auxBool == False:  
            #é guardado aorgumento (posição do eixo x)
            argsPf.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='red')
            #altera auxBool para True, para ir pra etapa de seleção do fim do intervalo
            auxBool = True;
            
        #caso esteja na etapa de seleção do fim do intervalo de medidas   
        else:
            #é guardado aorgumento (posição do eixo x)
            argsPf.append(int(event.xdata))
            #plota uma linha vertical para marcar o ponto selecionado
            ax.vlines(xPoint,min(y),max(y),color='red')
            #altera auxBool para False
            auxBool = False;
            #auxPress recebe 4, o que significa que o valor de volume será calculado
            auxPress = 4
            #pfValue recebe a média dos valores de pressão selecionados
            pfValue = np.mean(y[ argsPf[0]:argsPf[1]] )
            #exibe na interface gráfica o valor da pressão final
            pfValueTexto.set_text('{:.2f}'.format(pfValue) + ' Pa')
            
    #estágio de calculo de volume        
    if auxPress == 4:
        #é realizado o calculo de volume, com pressões inicial, intermediária e final
        #fatorVolume é o calculo do fator das pressoes medidas
        #volume é o valor do volume em ml após os cálculos
        fatorVolume = (1 - ((pfValue - pmValue)/(piValue - pfValue)))
        volume = (fatorVolume - minFator)/(maxFator - minFator) * maxVolume
        #exibe na interface gráfica o valor do volume
        volumeTexto.set_text("Volume = {:.2f} ml".format(volume))
        #auxPress recebe 0, significando para o sistema que o processo foi concluido
        auxPress = 0
    
    #após o clique, a interface gráfica é atualizada
    fig.canvas.draw() 
 

#função que faz a seleção automática do intervalo de medidas
def selecaoAutomatica(event):
    #chama os objetos definidos fora da função que são necessários para seu funcionamento
    global  x, y, auxPress, argsPi, argsPm, argsPf, piValue, pmValue, pfValue
    # xPoint recebe o ponto no eixo x onde ocorreu o clique na interface gráfica
    xPoint = event.xdata   
    #estágio de seleção da pressão inicial (piValue)
    if auxPress == 1:
        #é guardado os argumentos dos intervalor a serem calculados
        argsPi.append(int(event.xdata))
        argsPi.append(int(event.xdata)+20)
        #plota uma linha vertical para marcar o ponto selecionado
        ax.vlines(xPoint,min(y),max(y),color='blue')
        #auxPress recebe 2, o que indica para o sistema que no próximo clique...
        #será selecionado a pressão intermediária
        auxPress=2
        #piValue recebe a média dos valores de pressão selecionados
        piValue = np.mean(y[ argsPi[0]:argsPi[1]] )
        #exibe na interface gráfica o valor da pressão inicial
        piValueTexto.set_text('{:.2f}'.format(piValue) + ' Pa')
        
    #estágio de seleção da pressão intermediária (pmValue)        
    elif auxPress == 2:
        
        #é guardado aorgumento (posição do eixo x)
        argsPm.append(int(event.xdata)-20)
        argsPm.append(int(event.xdata))
        argsPf.append(int(event.xdata)+30)
        argsPf.append(int(event.xdata)+50)
        #plota uma linha vertical para marcar o ponto selecionado
        ax.vlines(xPoint,min(y),max(y),color='green')
        ax.vlines(xPoint+30,min(y),max(y),color='red')
        #será selecionada a pressão final
        auxPress = 3
        #pmValue recebe a média dos valores de pressão selecionados
        pmValue = np.mean(y[ argsPm[0]:argsPm[1]] )
        pfValue = np.mean(y[ argsPf[0]:argsPf[1]] )
        #exibe na interface gráfica o valor da pressão intermediária
        pmValueTexto.set_text('{:.2f}'.format(pmValue) + ' Pa')
        pfValueTexto.set_text('{:.2f}'.format(pfValue) + ' Pa')
            
    #estágio de calculo de volume        
    if auxPress == 3:
        #é realizado o calculo de volume, com pressões inicial, intermediária e final

        fatorVolume = (1 - ((pfValue - pmValue)/(piValue - pfValue)))
        #fatorVolume é o calculo do fator das pressoes medidas
        #volume é o valor do volume em ml após os cálculos
        volume = (fatorVolume - minFator)/(maxFator - minFator) * maxVolume
        #exibe na interface gráfica o valor do volume
        volumeTexto.set_text("Volume = {:.2f} ml".format(volume))
        #auxPress recebe 0, significando para o sistema que o processo foi concluido
        auxPress = 0
    
    #após o clique, a interface gráfica é atualizada
    fig.canvas.draw() 

#------------------------------------------------------------------------------
#ESCOLHA DO MODO DE SELEÇÃO E INVOCAÇÃO DE FUNÇÃO
 
#faz o sistema iniciar uma função, toda vez que a interface gráfica for clicada
#para permitir seleção de intervalos livres, inserir função "selecaoLivre"
#para utilizar seleção automática, inserir função "selecaoAutomatica"    
fig.canvas.mpl_connect('button_press_event', selecaoLivre)

#exibe a interface gráfica
plt.show()    
    
