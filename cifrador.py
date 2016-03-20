 # -*- coding: utf-8 -*-

'''
# Introdução #

Este codigo visa apresentar o uso da criptografia, atraves da linguagem Python.
Comentei o codigo para tornar o entendimento mais facil, mas qualquer duvida, pode mandar um email que tento responder: dnl31337@gmail.com.
Logo abaixo, fiz um pequeno texto explicando alguns pontos conceituais importantes, que vai facilitar o entendimento do modo como a criptografia esta agindo.
Criticas, ofensas, sugestões, etc... Tudo sera bem vindo...
Um abraço, espero que seja util..


1) Algoritmo usado, AES:

O algoritmo AES é um algoritmo simetrico (mesma chave para cifrar é a mesma usada para decifrar), que utiliza cifras de blocos com o tamanho minimo de 16 bytes. 
Sua chave de cifração pode ser de 128, 192 ou 256 bits.
O modo de cifração de blocos utilizado na aplicação sera o modo CBC. O modo CBC foi inventado pela IBM 1976. 
Para o seu funcionamento é necessario um vetor de inicialização como um parametro inicial fundamental, que sera explicado abaixo.. 
    
1.1) IV:

Todo bloco do texto claro(plain text) faz uma operação XOR (o 'ou exclusivo') com o bloco anterior. No caso o primeiro bloco de texto claro, nao existe um bloco anterior a ele, desta forma utiliza-se o IV (initialization vector, ou vetor de inicializacao) para poder realizar a primeira operação do XOR. E em seguida produz-se o primeiro bloco de texto cifrado, que sera utilizado posteriormente na operação do segundo bloco, e assim sucessivamente.

No processo de cifração, um unico IV deve ser utilizado para criptografar um arquivo. Neste caso, o programa utiliza um IV randomico, ou seja, para cada arquivo cifrado, a aplicação utilizara um novo IV para ser utilizado na cifração. Com esta caracteristica, o bloco cifrado sera diferente para cada cifração, mesmo que use a mesma chave sempre.

1.2) Chave:

O processo para gerar a chave de cifração sera atraves de uma função hash, no caso da aplicação, utilizamos o SHA256. O usuario ira digitar sua chave, e independente de quantos caracteres, ira gerar uma saida de 16 bytes, que correspondem aos 128 bits exigidos pelo AES, correspondente ao tamanho da chave..

1 byte -> 8 bits
16 bytes ->  x 
x = 16*8
x = 128 

:P

1.3) Função Padding:

A função de padding é utilizada para ajustar o tamanho do ultimo bloco para o tamanho determinado, que o modo de cifra de bloco necessita para funionar.
No caso da aplicação, que utiliza o modo CBC, é necessario que os blocos sejam de 16 bytes.. Entao quando chega no ultimo bloco, e por acaso este não tenha os 16 bytes necessarios, é adicionado caracteres nulos, ate atingir os 16 bytes, tamanho exigido pelo modo CBC...


Tentei explicar da forma que eu entendi, a fonte q utilizei foi: en.wikipedia.org/wiki/Block_cipher_mode_of_operation


Um abraco a todos..

Daniel.
'''

import os
import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def cifrar (key, filename):
    chunksize = 64*1024 # Tamanho do bloco que vamos tirar do arquivo a ser cifrado
    outputFile = "dnl_"+filename # Arquivo de saida
    filesize = str(os.path.getsize(filename)).zfill(16) # Tamanho total do arquivo, se for menor que 16, completa com 0 ate ficar 16 bytes.
    iv = ''

    # Gerando o IV randomico...
    for i in range(16):
        iv += chr(random.randint(0, 0xFF))

    # Gerando o cifrador, escolhendo o algoritmo, o modo cifrador de bloco CBC e o iv
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    # Abrindo arquivo de origem, modo leitura
    with open(filename,'rb') as infile:

        # Abrindo arquivo destino, modo escrita
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize) # Escrevendo o tamanho do arq original, q sera usado qdo for truncar o arquvivo na decifração..
            outfile.write(iv) # Escrevendo o IV, que vai ser usado no momento de decifrar o arquivo..

            while True:
                chunk = infile.read(chunksize) # Pega o bloco do arquivo de origem
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0: # função de padding..
                    chunk += ' ' * (16 - (len(chunk) % 16)) # add ' ' ate o bloco ficar do tamanho de 16 bytes..

                outfile.write(encryptor.encrypt(chunk)) # escreve o bloco cifrado no arquivo de saida..

def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[4:]

    with open(filename, 'rb') as infile:
        filesize = long(infile.read(16))
        iv = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def Main():
    escolha = raw_input('[C]ifrar , [D]ecifrar: ')
    if escolha == 'C':
        filename = raw_input('Caminho para o arquivo a ser cifrado: ')
        password = raw_input('Chave: ')
        cifrar(getKey(password),filename)
        print 'Feito...'
    elif escolha == 'D':
        filename = raw_input('Caminho para o arquivo a ser decifrado: ')
        password = raw_input('Chave: ')
        decrypt(getKey(password),filename)
        print 'Feito...'
    else:
        print 'Opcao invalida... fechando...'

if __name__ == '__main__':
    Main()