# Controle_Trafego_Smart_Cities
Pibic 2018 - Cefet - Araxá 

Pesquisas indicam que cerca de 50% dos tempos de viagem nas grandes cidades e 30% do consumo de gasolina são gastos nos semáforos, esperando que o sinal passe do período de vermelho para o verde (DENATRAN, 1979). Desta forma, controlar o tráfego de veículos de maneira eficiente deixou de ser mero conforto e se tornou uma grande necessidade em decorrência do aumento substancial da frota de veículos, sendo assim, um semáforo controlado por câmeras evidencia uma opção eficiente e ecologicamente contributiva no panorama social.

O objetivo do projeto é Controlar um cruzamento constituído de duas vias e dois semáforos utilizando de abordagens simples de visão computacional. Otimizar o fluxo de veículos, reduzindo o tempo de espera e parada. Reconhecer veículos automotores que possuem prioridades em cada via.

![alt text](https://github.com/FabioRSJunior/Controle_Trafego_Smart_Cities_2018/blob/main/images_projeto/Funcionando_reconhecendo.png)

As tecnologias propostas foram desenvolvidas a partir da combinação de duas soluções principais, sendo o método Viola-Jones para detectar em um frame a existência de um veiculo e a ferramenta de Histogramas de Padrões Binários Locais (LBPH) que permite o reconhecimento de padrões na região contendo o veiculo, sendo este o responsável por indicar os carros que possuem prioridade. O processo de validação da proposta foi feito mediante a experimentação através de testes em ambiente controlado. 

O protótipo foi capaz de identificar e reconhecer os veículos em tempo real, sendo capaz de decidir de forma inteligente qual das vias deveria ter a livre passagem. Desta forma, teve êxito quanto a diminuição do tempo de parada dos veículos e como consequência a diminuição da emissão de gases poluentes. O sistema se mostra sensível quanto a variação de luminosidade na etapa de reconhecimento de veículos prioritários.

Departamento nacional de trânsito (DENATRAN). Manual do semáforo. Ministério da justiça, serviços de Engenharia ,1979.

Paul Viola and Michael J. Jones. Rapid Object Detection using a Boosted Cascade of Simple Features. IEEE CVPR, 2001.

Ahonen, Timo, Abdenour Hadid, and Matti Pietikainen. “Face description with local binary patterns: Application to face recognition.”IEEE, 2006.
