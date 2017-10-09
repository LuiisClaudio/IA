import numpy as np
from random import shuffle, randint
import time

def readingTsp (filename):
    file = open(filename, 'r')
    file.readline()
    file.readline()
    file.readline()
    file.read(11)
    ncidade = file.readline()
    file.close
    lst_matriz = str.split(file.read())
    #print lst_matriz
    del lst_matriz[0:5]
    del lst_matriz[-1]
    return int(ncidade), lst_matriz


def fill_matriz(size_matrix, lst_matrix):
    matrix = np.zeros(shape=(size_matrix,size_matrix))
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

def escreveArquivo(nome_arquivo, custo, solucao):
    escrita = open(nome_arquivo[:-4]+'.txt','w')
    escrita.write(str(custo))
    escrita.write('\n')        
    for i in solucao:
        escrita.write(str(i))
        escrita.write(' ')

def funcao_custo(solucao, matrizcusto):
    n = len(solucao)  # pega o tamanho do vet
    custo = 0
    for i in range(n - 1):
        custo = custo + matrizcusto[solucao[i]][solucao[i + 1]]
    custo = custo + matrizcusto[solucao[-1]][solucao[0]]
    return custo
        
def gera_solucao(n):
    solucao = []
    for i in range(n):
        solucao.append(i)
        shuffle(solucao)
    return solucao

def relaciona_vizinhos(vizinhos, matrix):
    lst_custo = []
    for i in range(len(vizinhos)):
        lst_custo.append([funcao_custo(vizinhos[i], matrix), i])
        lst_custo.sort()
    return lst_custo

def busca_outra_solucao(solucao):
    n = len(solucao)
    #print(solucao)
    x=[]
    index1 = randint(0, n-1)
    index2 = randint(0, n-1)
    
    while index1 == index2:
        index1 = randint(0, n-1)
        index2 = randint(0, n-1)
    x=solucao.copy()
    temp = x[index1]
    x[index1] = x[index2]
    x[index2] = temp
    #print(x)
    return x
    
def hill_climbing(matriz, lst_param):
    
    n = len(matriz)
    
    solucao = gera_solucao(n)
    custo = funcao_custo(solucao, matriz)
    vezes_teste_derivada_0 = lst_param[0]
    cont_vezes_teste_derivada_0 = 0
    vezes_nao_melhora = lst_param[1]
    cont_vezes_nao_melhora = 0
    vizinhos = [solucao]
    qtd_vizinhos = lst_param[2]
    temporariocount=0
    time_ini = time.clock()
    while(True):
        temporariocount =temporariocount +1
        for i in range(qtd_vizinhos):
            x = []
            x= busca_outra_solucao(solucao)
            #print('mudou algo:  ', x)
            vizinhos.append(x)
 
        '''for v in vizinhos:
            print(v)
            print '\n'''
        #for viz in vizinhos:
            #print (viz)
        #print(temporariocount)
        lst_avaliacao_vizinhos = relaciona_vizinhos(vizinhos, matriz)
    
        #print('Vizinhos em ordem:',lst_avaliacao_vizinhos)
        solucao_nova = vizinhos[ lst_avaliacao_vizinhos[0][1] ]
        #print(solucao_nova, '   ', solucao, ' nao melhora: ', cont_vezes_nao_melhora, '   deriv-0', cont_vezes_teste_derivada_0)
        custo_novo = funcao_custo(solucao_nova, matriz)
        vizinhos = []
        
        if custo_novo < custo:
            solucao = solucao_nova
            custo = custo_novo
            cont_vezes_teste_derivada_0 = 0
            cont_vezes_nao_melhora = 0
        elif custo_novo == custo:
            cont_vezes_teste_derivada_0 = cont_vezes_teste_derivada_0 + 1
            if cont_vezes_teste_derivada_0 == vezes_teste_derivada_0:
                break
        else:
            cont_vezes_nao_melhora = cont_vezes_nao_melhora + 1
            if cont_vezes_nao_melhora == vezes_nao_melhora:
                break
    time_end = time.clock() 
    print('Tempo: ', time_end-time_ini)
    return custo, solucao
    
def main():
    lst_arquivos = ['gr17.tsp', 'gr21.tsp']
    lst_param = [[6000, 1000, 20], [7000, 1000, 300]]
    i_param = 0
    for nome_arquivo in lst_arquivos:
        num, lst_matrix = readingTsp(nome_arquivo)
        matrix = fill_matriz(num, lst_matrix)
        custo, solucao = hill_climbing(matrix, lst_param[i_param])
        print (custo)
        print (solucao)
        print ()
        for nome_arquivo in lst_arquivos:
            escreveArquivo(nome_arquivo, custo, solucao)
        i_param = i_param + 1
main()