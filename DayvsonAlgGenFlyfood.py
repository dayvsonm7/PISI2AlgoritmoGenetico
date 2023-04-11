# algoritmo genético para calcular o problema do TSP1
#este exato código com aproximadamente 9000 gerações encontrou um caminho de distância apriximada 38000. Ao
#finalizar, encontrou [1,2,3,4,5,7,9,13,14,17,16,20,21,18,19,22,26,25,24,27,28,29,23,15,11,10,12,8,6]
#de distância 37329. Esse valor excede em 9726 o caminho encontrado em https://www.math.uwaterloo.ca/tsp/world/witour.html
#Western Sahara WI29

# imports
import matplotlib.pyplot as plt  # biblioteca para gerar gráficos
import random  # biblioteca para gerar números aleatórios
import tsplib95  # biblioteca para trabalhar com arquivos do tipo TSP

# leitura do arquivo tsp
problem = tsplib95.load('wi29.tsp')  # carrega o arquivo TSP com o nome 'wi29.tsp'
quantpontos = int(problem.dimension)  # quantidade de pontos do arquivo TSP
distances = [[problem.get_weight(i, j) for j in range(1, problem.dimension + 1)] for i in range(1, problem.dimension + 1)]  # matriz de distâncias entre os pontos
# atributos
letrasdospontos = list(range(1, quantpontos + 1))  # lista com os números dos pontos



# FUNÇÕES

# função para gerar a população inicial
def gerarpopulacao(numpoints, pointsletters):
    paths = []
    for l in range(10):  # para cada ponto
        if l < numpoints:
            caminho = []  # inicia um novo caminho
            elementos_restantes = pointsletters  # agora trabalhamos com uma lista temporária
            caminho.append(elementos_restantes[l])  # anexa o primeiro ponto do caminho
            elementos_restantes = elementos_restantes[:l] + elementos_restantes[l + 1:]  # retira o ponto da lista
            for ll in range(numpoints - 1):
                if ll == numpoints - 2:  # se tiver na última volta
                    caminho.append(elementos_restantes[0])  # anexa o que restou
                    paths.append(caminho)  # e anexa o caminho finalmente na lista de paths
                else:
                    i = random.randint(0, len(elementos_restantes) - 1)  # sorteia um índice da lista
                    caminho.append(elementos_restantes[i])  # anexa o ponto sorteado
                    elementos_restantes = elementos_restantes[:i] + elementos_restantes[i + 1:]
    return paths




# função para calcular o fitness de cada indivíduo da população
def calculodofitness(pathslist, numpoints, matrix): #Npontos*Ncaminhos
    listadosfitness = []
    # Calculando os fitness
    for z in range(len(pathslist)):  # para cada caminho #Ncaminhos
        distt = 0  # inicializa a distância percorrida
        for v in range(numpoints): #Npontos
            if (v == 0):
                # se for a primeira cidade, adiciona a distância até a próxima cidade
                cidade1 = pathslist[z][v]
                cidade2 = pathslist[z][v + 1]
                distt += matrix[cidade1 - 1][cidade2 - 1]
            elif (v < numpoints - 1):
                # para as demais cidades, adiciona a distância até a próxima cidade
                cidade1 = pathslist[z][v]
                cidade2 = pathslist[z][v + 1]
                distt += matrix[cidade1 - 1][cidade2 - 1]
            if v == numpoints-1:
                cidade1 = pathslist[z][v]
                cidade2 = pathslist[z][0]
                distt += matrix[cidade1-1][cidade2-1]
                
                listadosfitness.append(distt)
    
    return listadosfitness




#Seleção por torneio
def torneio_ (listaaa): #recebe a populacao inicial
    listatemporaria = []
    for l in range (len(listaaa)):
        listatemporaria.append(listaaa[l])
    pais = []
    
    torneio = random.sample (listaaa, 2)
    indicedofuturopai = listaaa.index(max(torneio)) #seleciona o caminho com maior aptidao
    pais.append (indicedofuturopai)

    listatemporaria = listatemporaria[:indicedofuturopai]+listatemporaria[indicedofuturopai+1:]

    torneio = random.sample (listatemporaria, 2)
    indicedofuturopai = listatemporaria.index(max(torneio)) #seleciona o caminho com maior aptidao
    if indicedofuturopai<pais[0]:
                pais.append(indicedofuturopai)
    else:
                pais.append(indicedofuturopai+1)


    return pais[0], pais[1]



#Cálculo de aptidão para roleta
def aptidao (dronometros):
    soma = sum(dronometros)
    aptidoes = [0]*len(dronometros)

    for l, ind in enumerate (dronometros): #Ncaminhos
        aptidon = soma/ind
        aptidoes[l]=aptidon
    return aptidoes




def roleta(aptidoes):
    indices = []
    aptidoestemporarias = []
    for l in range (len(aptidoes)):
        aptidoestemporarias.append(aptidoes[l])
    soma_roleta = sum(aptidoes)
    n_sorteado = random.random() * soma_roleta
    soma_atual = 0
    for i, apt in enumerate(aptidoes):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            indices.append(i)
            aptidoestemporarias = aptidoestemporarias[:i]+aptidoestemporarias[i+1:]


    #escolhendo 2º pai
    soma_roleta = sum(aptidoestemporarias)
    n_sorteado = random.random() *soma_roleta
    soma_atual = 0
    for i, apt in enumerate (aptidoestemporarias):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            if i<indices[0]:
                indices.append(i)
            else:
                indices.append(i+1)
    return indices[0], indices[1]
    




def crossover (pai1, pai2): #Npontos + Npontos-1
    taxacrossover = random.randint (0,99)
    filho1 = []
    filho2 = []
    for i in range (len(pai1)): #Npontos/cidades
        filho1.append(pai1[i])
        filho2.append(pai2[i])
    
    if taxacrossover <80:

        i = random.randint (1,len(pai1)-1) #define um ponto de corte aleatório
        
        
        for l in range (i): #exemplo abaixo #Npontos-1
            indice=filho1.index(pai2[l])
            filho1[l], filho1[indice] = filho1[indice], filho1[l]

            indice=filho2.index(pai1[l])
            filho2[l], filho2[indice] = filho2[indice], filho2[l]
            


        
        return filho1, filho2
    return filho1, filho2


def mutacao (filho1):
    for l in range (len(filho1)): #Npontos
        taxamutacao = random.randint (0,99)
        
        if taxamutacao<2:
            genemutado = random.randint(0,len(filho1)-1)
            filho1[l],filho1[genemutado]=filho1[genemutado], filho1[l]
    return filho1
    

def escolherfilhoindividual (filho1, filho2, matrix):
    listacomosfilhos = []
    listacomosfilhos.append (filho1)
    listacomosfilhos.append (filho2)
    dronometrosdeles = calculodofitness(listacomosfilhos, len(filho1), matrix) #Npontos*Ncaminhos
    aptidoesdeles = aptidao(dronometrosdeles)
    if aptidoesdeles[0]>aptidoesdeles[1]:
        return filho1
    else:
        return filho2
    

    
def calcdistanciaindividual (filho, matrix):
    listacomele = []
    listacomele.append(filho)
    dronometrodele = calculodofitness(listacomele, len(filho), matrix)
    return dronometrodele[0]


def escolherfilho5050 (filho1, filho2): #UNICA NAO UTILIZADA
    filhoquevai = []
    if random.random() < 0.5:
        filhoquevai = filho1
    else:
        filhoquevai = filho2
    return filhoquevai






caminhos = []  # lista vazia para armazenar os caminhos
dronometros = []  # lista vazia para armazenar os fitness


numgeracoes = 10000

caminhos=gerarpopulacao(quantpontos, letrasdospontos)

dronometros=calculodofitness(caminhos, quantpontos, distances)

aptidoes = aptidao(dronometros)

listafinal = list(zip(caminhos, dronometros))


melhorindividuoeverglobal = []
melhorindividuoeverglobal.append (min(listafinal)[0])
melhorindividuotamanhopercursoglobal = []
melhorindividuotamanhopercursoglobal.append (min(listafinal)[1])





for geracao in range(numgeracoes): #Ngerações
    dronestemporarios = [] 
    print(f'Geração {geracao}: ', end='') 
    melhorindividuolocal = []
    melhorindividuolocal.append (min(listafinal)[0])
    melhorindividuotamanhopercursolocal = []
    melhorindividuotamanhopercursolocal.append (min(listafinal)[1])

    if melhorindividuotamanhopercursolocal[0]<melhorindividuotamanhopercursoglobal[0]:
        melhorindividuotamanhopercursoglobal=[]
        melhorindividuotamanhopercursoglobal.append (melhorindividuotamanhopercursolocal[0])
        melhorindividuoeverglobal = []
        melhorindividuoeverglobal.append(melhorindividuolocal[0])

    

    if geracao<numgeracoes-1:
        print (melhorindividuotamanhopercursoglobal[0])
    else:
        print (melhorindividuoeverglobal[0])
        print (melhorindividuotamanhopercursoglobal[0])

    

    # Seleção dos pais e reprodução
    torneioaleatorio = random.randint(0,99)
    torneioroleta = True #true para roleta

    if aptidoes[aptidoes.index(max(aptidoes))] < 1.025 * (sum(aptidoes)/len(aptidoes)): #AQUI FAZ POR TORNEIO
        torneioroleta = False

    if torneioaleatorio<1: 
        torneioroleta = False

    nova_populacao = []

    while len(nova_populacao)<(10): #LOOP CRIAÇÃO NOVA POPULACAO #Ncaminhos

        if torneioroleta:
            indicepai1, indicepai2 =roleta(aptidoes) #Ncaminhos
        else:
            indicepai1, indicepai2 =torneio_(aptidoes)
        pai1 = caminhos[indicepai1] 
        pai2 = caminhos[indicepai2]
        filho1, filho2 = crossover(pai1, pai2) #Npontos
        filho1 = mutacao(filho1) #Npontos
        filho2 = mutacao(filho2)

        if len(nova_populacao)==(10)-1: #SE FOR CRIAR O ULTIMO FILHO
                
                

                filhoescolhido = escolherfilhoindividual (filho1, filho2, distances) #Npontos*Ncaminhos
                filhoescolhidodist = calcdistanciaindividual (filhoescolhido, distances) 
                if filhoescolhidodist not in dronestemporarios:
                    nova_populacao.append(filhoescolhido)
                
        else: #CRIANDO OS PRIMEIROS FILHOS
                
                

                filho1dist = calcdistanciaindividual(filho1, distances)
                filho2dist = calcdistanciaindividual (filho2, distances)
                if filho1dist not in dronestemporarios:
                    nova_populacao.append(filho1)
                    dronestemporarios.append (filho1dist)
                if filho2dist not in dronestemporarios:
                    nova_populacao.append(filho2)
                    dronestemporarios.append(filho2dist)

    
    

                

    caminhos = nova_populacao
    dronometros=calculodofitness(caminhos, quantpontos, distances)
    if melhorindividuotamanhopercursoglobal[0] not in dronometros:
        indicedopior = dronometros.index(max(dronometros))
        caminhos[indicedopior]=melhorindividuoeverglobal[0]
        dronometros[indicedopior]=melhorindividuotamanhopercursoglobal[0]

    aptidoes = aptidao(dronometros)
    listafinal = list(zip(caminhos, dronometros))

        