
int RED1 = 8; 
int ORA1 = 9;
int GRE1 = 10;

int RED2 = 7; 
int ORA2 = 6;
int GRE2 = 5;

int OPP = 12; //emergencial ativo
int OCC = 13;//FUNCIONAMENTO SMART

int leitura;
int aux = 0;

void OperacaoPython(int leitura){

 digitalWrite(OPP, LOW); // led 12 ativado emergencial
 digitalWrite(OCC, HIGH); // desative o carater python
  

  if(leitura == '1'){
    digitalWrite(RED1, LOW);
    digitalWrite(ORA1, LOW);
    digitalWrite(GRE1, HIGH);
    
    digitalWrite(RED2, HIGH);
    digitalWrite(ORA2, LOW);
    digitalWrite(GRE2, LOW);
                                 }

 if(leitura == '0'){
  
    digitalWrite(RED2, LOW);
    digitalWrite(ORA2, LOW);
    digitalWrite(GRE2, HIGH);
    
    digitalWrite(RED1, HIGH);
    digitalWrite(ORA1, LOW);
    digitalWrite(GRE1, LOW);     }

}

void emergencial(){  
 digitalWrite(OPP, HIGH); // led 12 ativado emergencial
 digitalWrite(OCC, LOW); // desative o carater python
 
 digitalWrite(RED2, HIGH);
 digitalWrite(GRE1, HIGH);
 digitalWrite(RED1, LOW);
 digitalWrite(GRE2, LOW);
 digitalWrite(ORA1, LOW);
 digitalWrite(ORA2, LOW);

 delay(2000);

 digitalWrite(RED1, HIGH);
 digitalWrite(GRE2, HIGH);
 digitalWrite(RED2, LOW);
 digitalWrite(GRE1, LOW);
 digitalWrite(ORA1, LOW);
 digitalWrite(ORA2, LOW);

  delay(2000);}

void setup() {
 
  Serial.begin(9600);
  pinMode(RED1, OUTPUT);
  pinMode(ORA1, OUTPUT);
  pinMode(GRE1, OUTPUT);

  pinMode(RED2, OUTPUT);
  pinMode(ORA2, OUTPUT);
  pinMode(GRE2, OUTPUT);

  pinMode(OPP, OUTPUT);
  pinMode(OCC, OUTPUT);
  
}

void loop() {
     
if (Serial.available()){   //enquanto existir comunicacao com o python 
    char leitura = Serial.read(); //leia do serial
    //deixa o arduino no modo python
    digitalWrite(OPP, LOW);
    digitalWrite(OCC, HIGH);
    OperacaoPython(leitura);
    delay(1000); //leia o serial somente de 1 em 1 segundo 
     if(leitura == 10){
     emergencial();
     }
     }

else{ //se nao existir conexao com o python opere em carater de emergencia
emergencial();
}
}//fecha o loop
  
