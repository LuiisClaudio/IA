# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle, randint
import time

''' Essa funcao recebe a lista custo das cidades e passa para a matriz
	Ela retorna matriz preenchida
'''
def fill_matriz(size_matrix, lst_matrix):
    # lst_matrix.reverse()
    matrix = np.zeros(shape=(size_matrix, size_matrix))
    i = 0
    j = 0
    for k in range(len(lst_matrix)):
        matrix[i][j] = int(lst_matrix[k])
        j = j + 1
        if int(lst_matrix[k]) == 0 and i + 1 < size_matrix:
            i = i + 1
            j = 0
    matrix = matrix + np.transpose(matrix)
    return matrix 

def fill_matriz_175(size_matrix, lst_matrix):
 
    matrix = np.zeros(shape=(size_matrix, size_matrix))
    i = 0
    j = 0
    
    for k in range(len(lst_matrix) - 1):
        if int(lst_matrix[k]) == 0 and i < size_matrix - 1 and k > 0:
            i = i + 1
            j =  i - 1
        matrix[i][j] = int(lst_matrix[k]) 
        '''if i < 2:
            print i, j, lst_matrix[k]'''
        if j < size_matrix - 1:
            j = j + 1
    matrix = matrix + np.transpose(matrix)
    return matrix 
 
'''Essa funcao recebe qual arquivo deve ler 
	Ela retorna a quantidade a dimensao da matriz e sua lista custo
'''
def readingTsp(filename):
    if filename == 'si175.tsp':
        file = open(filename, 'r')
        file.readline()
        file.readline()
        file.read(11)
        ncidade = file.readline()
    
        lst_matriz = str.split(file.read())
        file.close
        
        del lst_matriz[0:7]
        del lst_matriz[-1]
        return int(ncidade), lst_matriz
    
    
    file = open(filename, 'r')
    file.readline()
    file.readline()
    file.readline()
    file.read(11)
    ncidade = file.readline()

    lst_matriz = str.split(file.read())
    file.close
    # print lst_matriz
    del lst_matriz[0:5]
    del lst_matriz[-1]
    return int(ncidade), lst_matriz

'''Essa funcao gera os simbolos de cada cidade de acordo com a dimensao recebida do arquivo lido'''
def generate_genes(qtd_genes):
    genes_lst = []
    for i in range(qtd_genes):
        genes_lst.append(i)
    return genes_lst

'''Essa funcao gera a populacao inicial e retorna uma lista de lista'''
def generate_first_population(genes, population_size):
    population = []
    while len(population) < population_size:
        shuffle(genes)
        population.append(list(genes))
    return population


'''Essa funcao eh uma auxiliar do crossover_mapeado_parcialmente on insere no gene o corte selecionado de um pai'''
def botaRecorte(p, limite1, limite2, p_ret):
    for i in range(limite1, limite2):
        p_ret[i] = p[i]
    return p_ret


# ret = botaRecorte(p_t, 2, 6, p_r)
# print ret

'''Essa funcao eh uma auxiliar que confere se um alelo esta pesente do gene'''
def presente_no_gene(elem, gene):
    for i in gene:
        if elem == i:
            return 1
    return 0

'''Essa funcao acha onde um alelo esta exatamente presente no gene'''
def index_do_alelo(elem, gene):
    for i in range(len(gene)):
        if elem == gene[i]:
            return i
    return -1

'''Essa funcao eh uma auxiliar do crossover_mapeado_parcialmente onde aleatóriamente define o quao deve se mater o corte de um pai'''
def define_tamanho_corte(n):
    limite1 = randint(0, n)
    limite2 = limite1
    while limite2 == limite1:
        limite2 = randint(0, n)
    if limite1 > limite2:
        aux = limite1
        limite1 = limite2
        limite2 = aux
    return limite1, limite2

'''Essa funcao eh um dos crossovers'''
def crossover_mapeado_parcialmente(g1, g2):
    n = len(g1)
    lim1, lim2 = define_tamanho_corte(n)
    tamanho_corte = lim2 - lim1

    while tamanho_corte <= 2 and tamanho_corte >= n - 2:
        lim1, lim2 = define_tamanho_corte(n)
        tamanho_corte = lim2 - lim1
    # lim1 = 3
    # lim2 = 7
    # print 'Fatiamento: ', g1[lim1:lim2]
    g = [-1] * n

    g = botaRecorte(g1, lim1, lim2, g)

    ''' Parte do algoritmo no intervalo de corte'''
    for i in range(lim1, lim2):
        # print '*****************************'
        # print 'Index: %s' %i
        pivor = g2[i]
        elem = g1[i]
        for j in range(n):
            # print elem, 'Elemento de g1'
            # print g2[i], 'Elemento de g2'
            posicao = index_do_alelo(elem, g2)
            # print 'Posicao de g2 retornada %s e g2[posicao] == %s' %(posicao, g2[posicao])
            if posicao >= 0:
                # print 'presente_no_gene', presente_no_gene(g2[i], g1[lim1:lim2])
                if (posicao < lim1 or posicao >= lim2) and presente_no_gene(pivor,
                                                                            g1[lim1:lim2]) == 0 and presente_no_gene(
                        g2[i], g) == 0:
                    # print 'g[%s] recebe:::::::::::::::::::::' %posicao, pivor
                    g[posicao] = pivor
                    # print g
                    # print ''
                    # print '-------->'
                    break
                else:
                    elem = g1[posicao]

                    # print ''
                    # print '#########'
    '''Antes do intervalo de corte'''
    for i in range(lim1):
        pivor = g1[i]
        elem = pivor
        # print pivor
        for j in range(n):
            if presente_no_gene(pivor, g) != 0:
                break
            posicao = index_do_alelo(elem, g2)
            # print ''
            # print 'g1[%s] = %s' %(elem)
            # print 'g2[%s] == %s' %(posicao, g2[posicao])
            # print ''
            if (posicao < lim1 or posicao >= lim2) and presente_no_gene(pivor, g) == 0:
                # print 'g[%s] recebe:::::::::::::::::::::' %posicao, pivor
                g[posicao] = pivor
                # print g
                # print ''
                # print '-------->'
                break
            else:
                elem = g1[posicao]

    '''Depois do intervalo de corte'''
    for i in range(lim2, n):
        pivor = g1[i]
        elem = pivor
        for j in range(n):
            if presente_no_gene(pivor, g) != 0:
                break
            posicao = index_do_alelo(elem, g2)
            # print ''
            # print 'g1[%s] = %s' %(elem)
            # print 'g2[%s] == %s' %(posicao, g2[posicao])
            # print ''
            if (posicao < lim1 or posicao >= lim2) and presente_no_gene(pivor, g) == 0:
                # print 'g[%s] recebe:::::::::::::::::::::' %posicao, pivor
                g[posicao] = pivor
                # print g
                # print ''
                # print '-------->'
                break
            else:
                elem = g1[posicao]
    return g

'''Essa funcao aleatoriamente troca dois alelos de lugar um com outro'''
def mutation(gene):
    n = len(gene)
    index1 = randint(0, n-1)
    index2 = randint(0, n-1)
    while index1 == index2:
        index1 = randint(0, n-1)
        index2 = randint(0, n-1)
    temp = gene[index1]
    gene[index1] = gene[index2]
    gene[index2] = temp
    return gene

'''Essa funcao avalia o quao o gene gerado eh bom'''
def FuncaoFitness(caminho, matrizcusto):
    n = len(caminho)  # pega o tamanho do vet
    custo = 0
    for i in range(n - 1):
        custo = custo + matrizcusto[caminho[i]][caminho[i + 1]]  # pega o custo de ir da cidade i para a i+1(próxima)
    custo = custo + matrizcusto[caminho[-1]][caminho[0]]  # soma o caminho da ultima para a primeira pq é um ciclo euclidiano
    return custo

'''Essa funcao seleciona o cruzamento apenas das melhores genes'''
def metodo_elitista(populacao, lst_custos):
    n = len(populacao)
    filho_lst = []
    for i in range(0, n, 2):
        # print 'index: ', lst_custos[i][1], lst_custos[i+1][1]
        filho_lst.append(crossover_mapeado_parcialmente(populacao[lst_custos[i][1]], populacao[lst_custos[i + 1][1]]))
        # print filho_lst
    return filho_lst


'''Dentre os genes ja avaliados seleciona o melhor de todos'''
def seleciona_melhor_genetica(arvore_custo):
    melhor = arvore_custo[0][-1]
    x = -1
    y = 0
    # print melhor
    for i in range(len(arvore_custo)):
        #print('Geracao[%s]' % i)
        for j in range(len(arvore_custo[i])):
            #print(arvore_custo[i][j][0], melhor[0])
            if arvore_custo[i][j][0] < melhor[0]:
                #print('\t Entrei', arvore_custo[i][j][0], melhor[0])
                melhor = arvore_custo[i][j]
                x = i
                y = j
        #print
    #print(x, y)
    return x, y, melhor

'''Avalia o fitnnes da gene e atribui a ele uma hierarquia do melhor'''
def relaciona_fitness(alelos, matrix):
    lst_custo = []
    for i in range(len(alelos)):
        lst_custo.append([FuncaoFitness(alelos[i], matrix), i])
        lst_custo.sort()
    return lst_custo

'''Um metodo de crossover e dois genes. Retorna dois filhos '''
def crossoverCiclo(papi, mami):
    n = len(papi)
    m = len(mami)
    if (n != m):
        print('zuou o negocio')
        return 0
    lista_ciclos_index = []
    # procura por ciclos
    num_ciclos = 1
    for i in range(n):
        if i not in (lista_ciclos_index):
            ini_ciclo_pai = papi[i]
            lista_ciclos_index.append(i)
            temp_mae = mami[i]
            # print('pai:')
            # print(ini_ciclo_pai)
            while (temp_mae != ini_ciclo_pai):
                index_pai = papi.index(temp_mae)

                lista_ciclos_index.append(
                    index_pai)  # isso aqui é dos alelos que passaram NO PAI (o ciclo vai ser igual na mae entao tanto faz)
                #print(index_pai)
                temp_mae = mami[index_pai]
            #print('-' * 10 + 'acabou ciclo' + '-' * 10)
            num_ciclos = num_ciclos + 1
            lista_ciclos_index.append(-1)

    # cria os filhos
    filho1 = [-1] * m
    filho2 = [-1] * m
    #print(filho1)
    flag = 0
    #print(lista_ciclos_index)
    #print(len(lista_ciclos_index))
    for k in range(len(lista_ciclos_index)):
        if lista_ciclos_index[k] != -1:
            if flag != 1:
                filho1[lista_ciclos_index[k]] = papi[lista_ciclos_index[k]]
                filho2[lista_ciclos_index[k]] = mami[lista_ciclos_index[k]]
                #print(filho1, ' /// ', filho2, '///', flag)
            else:
                filho1[lista_ciclos_index[k]] = mami[lista_ciclos_index[k]]
                filho2[lista_ciclos_index[k]] = papi[lista_ciclos_index[k]]
                #print(filho1, ' /// ', filho2, '///', flag)
        else:
            if flag == 0:
                flag = 1
                #print('mudança de flag')
            else:
                flag = 0
                #print('mudança de flag pra 0')
    #print(mami, '//mae ')
    #print(papi, 'compara cos pais')
    #print(filho1, '//filho um vamo ve')
    #print(filho2, '//filho 2 e ai')
    return filho1, filho2


#g1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#g2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
#g1, g2 = crossoverCiclo(g1, g2)
#print(g1, g2)
#print('----' * 20)
#print()
#print()

''' não usada
def roleta(lst_custo):
    n = len(lst_custo)
    soma = 0
    for i in range(n):
        soma = soma + lst_custo[i][0]
    sorteado = randint(0, n)
'''

'''Escolhe o pai a ser usado no crossover '''
def escolhe_pais(lst_custo):
    #escolhe entre dois aleatórios o de menor custo para virar um pai
    n = len(lst_custo)
    indexrand1 = randint(0,n-1)
    indexrand2 = randint(0,n-1)
    valor1 = lst_custo[indexrand1][0]
    valor2 = lst_custo[indexrand2][0]
    if(valor1<valor2):
        return indexrand1
    else:
        return indexrand2
        
'''funcao que escreve no arquivo '''
def escreveArquivo(nome_arquivo, elem_custo, gene):
    escrita = open(nome_arquivo[:-4]+'sol.txt','w')
    escrita.write(str(elem_custo))
    escrita.write('\n')        
    for i in gene:
        escrita.write(str(i))
        escrita.write(' ')
                        
'''A funcao main recebe o arquivo e estrutura a evolucao das solucoess'''
def evolucao(nome_arquivo):
    num, lst_matrix = readingTsp(nome_arquivo)
    if num == 175:
        matrix = fill_matriz_175(num, lst_matrix)
    else:
        matrix = fill_matriz(num, lst_matrix)
    gene = generate_genes(num)
    min_populacao = 300
    populacao = generate_first_population(gene, min_populacao)
    #lst_custo = relaciona_fitness(populacao, matrix)
    #for i in populacao:
        #print(i)
    #print('\n\n')
    num_max_geracoes = int(num*3.4)+30
    qtd_max_populacao = 950
    time_ini = time.clock()
    for i in range(num_max_geracoes):
        lst_custo = relaciona_fitness(populacao, matrix)
        #if (num == 175):
            #print(lst_custo[0], 'Geração: ', i)
        #print('Geração:', i, '\t Vai?')
        #flagao = 0
        while (len(populacao) <= (qtd_max_populacao)):
            #if(flagao==0):
                #flagao=1
                #print('entrei geração:', i , '\t Entao foi')
            index1 = escolhe_pais(lst_custo)
            index2 = escolhe_pais(lst_custo)
            if randint(0,1) == 0:
                populacao.append(crossover_mapeado_parcialmente(populacao[index1], populacao[index2]))
            else:
                filho1, filho2 = crossoverCiclo(populacao[index1], populacao[index2])
                populacao.append(mutation(filho1))
                populacao.append(mutation(filho2))
    
        lst_custo = relaciona_fitness(populacao, matrix)
        #------------------------------------------------# começa a matança #------------------------------------------------#
        indexlist = []
        temppopulacao = []
        for j in range(min_populacao+i):
            indexlist.append(lst_custo[j][1])
        for j in range(len(indexlist)):
            temppopulacao.append(populacao[indexlist[j]])

        #conta para os piores 
        num_min = 60
        for ka in range(num_min):
            temppopulacao.append(populacao[-1])
            del populacao[-1]
            #c = randint(int(qtd_max_populacao/20),qtd_max_populacao-1-ka) 
            #temppopulacao.append(populacao[c])
            #del populacao[c]
        del populacao
        populacao = temppopulacao
        del temppopulacao
        del indexlist
        del lst_custo
    lst_custo = relaciona_fitness(populacao, matrix)
    #print(lst_custo)
    #escreveArquivo(nome_arquivo, lst_custo[0][0], populacao[lst_custo[0][1]])
    #escrita.write(populacao[lst_custo[0][1]])
    #print(lst_custo[0], 'geração: ', i)
    time_end = time.clock() 
    print('Tempo: ', time_end-time_ini)
    print(lst_custo[0][0])
    print(populacao[lst_custo[0][1]])
    return populacao[lst_custo[0][1]], lst_custo[0][0]

#evolucao('gr17.txt')

#print(time_end-time_ini)
def main():
    lst_arquivos = ['gr17.tsp', 'gr21.tsp', 'gr24.tsp', 'hk48.tsp', 'si175.tsp']
    vezes_de_teste = [1, 1, 1, 1, 1]
    elem_menor_custo = 10000000
    cont = 0
    melhor_gene = []
    for i in lst_arquivos:
        print(i)
        for j in range(vezes_de_teste[cont]):
            gene, elem_custo = evolucao(i)
            if elem_custo < elem_menor_custo:
                elem_menor_custo = elem_custo
                melhor_gene = gene
        #print(elem_menor_custo)
        #print(melhor_gene)
        cont = cont + 1
        escreveArquivo(i, elem_menor_custo, melhor_gene)
        elem_menor_custo = 10000000
        melhor_gene = []
#time_ini = time.clock()
main()
#time_end = time.clock()    
    
#time_end = time.clock()
#print(time_end-time_ini)

#def testatempo():
   # time_ini = time.clock()
    #populacao = []
   # for i in range(2):
        #populacao.append(main('hk48.tsp'))
        #populacao.append(main('hk48.tsp'))

    #time_end = time.clock()
    #print(populacao)
    #print(float(time_end-time_ini)/(2*i))
    
#testatempo()
    
'''g1 = [1,2,3,4,5,6,7,8,9]
g2 = [9,3,7,8,2,6,5,1,4]
print g1
print 
print g2
print '''

'''num, lst_matrix = readingTsp('gr17.tsp')
matrix = fill_matriz(num, lst_matrix)
genes = generate_genes(num) 
population = generate_first_population(genes, 5)
g1 = population[0]
g2 = population[1]
print g1
print 
print g2
print
g = crossover_mapeado_parcialmente(g1, g2)
print g
custo = FuncaoFitnessDoCostinha(g, matrix)
print 'Custo da solucao %s' %custo
#print matrix
#print population'''
