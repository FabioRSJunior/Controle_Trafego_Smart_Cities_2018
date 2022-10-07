# -*- coding: cp1252 -*-
'''Programa de iniciaçao cientifica: Smart cities
@Autor: Fabio Romero de Souza Junior data: 02/2019
'''
import numpy as np
import cv2
import os
import serial

# responsavel pela comunicacao com Arduino 
porta = ("COM3");                                           
velocidade = 9600;                                        
conexao = serial.Serial(porta, velocidade);
print("arduino conectado")

global x1 ; #variavel semaforo 1 arduino
global y2 ; #variavel semaforo 2 arduino

# funcao responsavel pela logica do Arduino
# os prints sao utilizados para auxilios e testes 
def funcaoArduino(x1,y2):
    
    if( (x1 ==0) and (y2 == 0) ):
        conexao.write(b'10');        
        print("funcionamento normal");
    else:
        if((x1 == 100) or (y2 == 100)): 
            if(x1 == 100):
                conexao.write(b'1')
                print("semaforo 1 prioritario")
            else:
                conexao.write(b'0')
                print("semaforo 2 prioritario")
        else:
            if(x1 >= y2):
                conexao.write(b'1')
                print("semaforo 1 tem mais carros")
            else:
                conexao.write(b'0')
                print("semaforo 2 tem mais carros")
    print('x1:'); 
    print(str(x1));
    print('y2');
    print(str(y2));
    
    #cria um arquivo com o caminho da imagem, com o nome da pasta data
    #o nome da imgem e o rotulo ou label das imagens, por exemplo:
    # data\01\189.png;0 faz isso para todas as imagens da pasta e 
    # grava em um arquivo de nome TRAIN (somente os caminhos)   
def criaArquivoDeRotulo(pasta):
    
    label = 0
    f = open("TRAIN", "w+")
    for dirPrincipal, nomeDirs, nomeArqs in os.walk(pasta):
        for subDir in nomeDirs:
            caminhoPasta = os.path.join(dirPrincipal, subDir)
            for filename in os.listdir(caminhoPasta):
                caminhoAbs = caminhoPasta + "\\" + filename
                f.write(caminhoAbs + ";" + str(label) + "\n")
            label = label + 1
    f.close()
    
    #recebe como parametro o caminho das imagens que foram gerados pela funcao
    #criarArquivoDeRotulo, que está no arquivo fPoint. Essa funcao abre as informacoes
    #dos caminhos recebidos e os armazenam em um arquivo, utilizando dos labels ou 
    #marcadores
def criaDicionarioDeImagens(fPoint):
    lines = fPoint.readlines()
    dicionarioDeFotos = {}
    for line in lines:
        filename, label = line.rstrip().split(';')
        if int(label) in dicionarioDeFotos.keys():
            dicionarioDeFotos.get(int(label)).append(cv2.imread(filename, 0))
        else:
            dicionarioDeFotos[int(label)] = [cv2.imread(filename, 0)]
    return dicionarioDeFotos

# Recebe como dados as imagens dos carros, organizadas
# e aqui que acontece a diferenciacao entre os veiculos
# aplicacao do metodo do LBPH separando um para cada marcador
# retona o modelo para ser feito a comparacao o super vetor
# com a informaçao de cada imagem e o label    
    
def treinaModelo(dicionarioDeCarros):  
    model = cv2.face.LBPHFaceRecognizer_create()
    listkey = []
    listvalue = []
    for key in dicionarioDeCarros.keys():
        for value in dicionarioDeCarros[key]:
            listkey.append(key)
            listvalue.append(value)

    model.train(np.array(listvalue), np.array(listkey))
    return model

# o codigo principal, e aqui que acontece a maior parte da identificacao e 
# reconhecimento. Ele recebe o modelo treinado pelos algoritmos anteriores
# e faz as comparacoes.    
    
def reconheceVideo(modelo, arquivo):
    
    face_cascade = cv2.CascadeClassifier('cas1.xml')
    #carrega o arquivo de cascatas para identificacao dos veiculos
    
    cap = cv2.VideoCapture(int(arquivo))  # inicia captura da câmera 1
    cap2 = cv2.VideoCapture(1)            # inicia camera 2
    
    while (True):  #enquanto voce nao pressionar 'q' ou nao tiver erros    
        # inicia as variaveis que controla o arduino 
        x1 = 0; 
        y2 = 0;     
        #recebe os quadros da webcam
        
        ret, img = cap.read()
        ret2,img2 = cap2.read()
        # frame não pode ser obtido? entao saia
        if (ret == False):
            cap.release()
            return
        
        if (ret2 == False):    
            cap2.release()
            return  
        #transforma os frames em tons de cinza que e o padrao do 
        #haar cascate       
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 =cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        #detecta os veiculos apartir do frame junto a analise das
        #cascatas       
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces2= face_cascade.detectMultiScale(gray2, 1.3, 5)
        
        #inicia as variais de vetores          
        carro = []
        carro2 = []  
        # achou um carro? recorte ele (crop)  
        #para um veiculo identificado na variavel de video em cinza
        for (x, y, w, h) in faces:
            # achou um carro? recorte ele (crop)
            carro = img[y:y + h, x:x + w]  
            
            # esse carro é grande o suficiente?
            # e apenas um tratamento dos erros
            if  w > 50 and  h > 50 :
                
                #conta ao arduino a quantidade de carros no quadro
                x1 =(len(faces)) 
                
                # modifica o tamanho dele pra se ajustar ao comparador
                carro = cv2.resize(carro, (255, 255))
                carro = cv2.cvtColor(carro, cv2.COLOR_BGR2GRAY)

                #aqui é feito o reconhecimento, se o carro foi identificado
                #ele é recortado e mandado para o comparador. se o comparador
                #acusa que o carro é um AMB ou um PM
                #aqui o algoritmo prediz se apartir do modelo
                #o carro2 é um dos veiculos com prioridade
                #e recebe o marcador do veiculo
                
                label = modelo.predict(carro)
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                
                if (label[0] == 0): #e a POLICIA?
                    # então escreva um texto em cima da caixa
                    cv2.putText(img, 'PM', (x - 20, y + h + 60), font, 3, (255, 0, 0), 5, cv2.LINE_AA)
                    # (imagem, texto, posicao, fonte, tamanho da  fonte, cor, expessura, antialiasing)
                    # pinte um retângulo ao redor do carro da policia
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    x1 = 100; #avise o arduino. pois e preferencial
                    
                if (label[0] == 1):  # é a AMBULANCIA?
                    # então bota um texto em cima da caixa
                    cv2.putText(img, 'AMB', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    # pinte um retângulo ao redor do carro da ambulancia
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    x1 = 100; # avise o arduino. pois e preferencial
                    
                 
                # para os demais carros(aqui voce pode colocar marcadores 
                # para outros veiculos)     
                if(label[0] == 2):
                    #cv2.putText(img, 'red', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if(label[0] == 3):
                    #cv2.putText(img, 'blu', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) 
                if(label[0] == 4):
                    #cv2.putText(img, 'yqua', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if(label[0] == 5):   
                    #cv2.putText(img, 'GC', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        #exatamente igual a camera 1:
        #camera2
                
        for (x, y, w, h) in faces2:
            carro2 = img2[y:y + h, x:x + w]
            if w > 50 and h > 50: 
                
                y2 =(len(faces2))
                carro2 = cv2.resize(carro2, (255, 255))
                carro2 = cv2.cvtColor(carro2, cv2.COLOR_BGR2GRAY)
                

                label = modelo.predict(carro2)
                
                
                font = cv2.FONT_HERSHEY_SIMPLEX
             
                if (label[0] == 0): #e a POLICIA?
                    cv2.putText(img2, 'PM', (x - 20, y + h + 60), font, 3, (255, 0, 0), 5, cv2.LINE_AA)
                    img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    y2 = 100; 
                    
                if (label[0] == 1):  # é a AMBULANCIA?
                    cv2.putText(img2, 'AMB', (x - 20, y + h + 60), font, 3, (0, 0, 255), 5, cv2.LINE_AA)
                    img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    y2 = 100;
                 
                if(label[0] == 2):
                   img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                if(label[0] == 3):
                    img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                if(label[0] == 4):
                    img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                   
                if(label[0] == 5):
                    img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                      
        # redimensione só pra ficar bem visivel na tela
        img = cv2.resize(img, (int(0.75 * img.shape[1]), int(0.75 * img.shape[0])))
        img2 = cv2.resize(img2, (int(0.75 * img2.shape[1]), int(0.75 * img2.shape[0])))

        # depois que as variaveis globais foram modificadas no decorrer do programa
        # informe a funcao do arduino que vai devidir qual semaforo será acionado
        funcaoArduino(x1,y2);

        # exiba o reconhecimento e identificaçao na tela
        # aqui e possivel criar janelas para a visualizacao
        
        cv2.imshow("camera 1", img)   #exibe a camera 1
        cv2.imshow("camera 2", img2)  #exibe a camera 2
          
        # quando quiser que o programa seja encerrado:
        # pressione o caracter q
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
    #funcoes de encerramento
    cap.release()
    cap2.release()
    conexao.close() 
    cv2.destroyAllWindows()
    
#funcao principal
def main():
    
    # cria o caminho de cada imagem, organizando
    criaArquivoDeRotulo("data")

    # atribui as informacoes obtidas na funcao anterior
    fPoint = open("TRAIN", "r")

    # constrói um dicionário dos dados lidos no texto
    # recebe como parametro o caminho das imagens e o label 
    dicionarioDeFotos = criaDicionarioDeImagens(fPoint)
    
    # cria o supervetor com o metodo de LBPH
    modelo = treinaModelo(dicionarioDeFotos)

    # chama a funcao onde ocorre o reconhecimento e identificacao
    reconheceVideo(modelo, "0")

# PADRAO PYTHON, DIZ QUE O PROGRAMA TEM UMA FUNCAO PRINCIPAL
# IMPEDE QUE OUTROS PROGRAMAS ACESSEM ESSE PROgRAMA   
if __name__ == "__main__":
    main()
