#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Turma: CC3BN.

Integrantes: Claudia Thifany dos Santos (RA: 1903247);
             Gilberto Ramos de Oliveira (RA: 1903991);
             Leandro Epifanio Silva Costa (RA: 1902516);
             Rodrigo Monastero (RA: 1904247).

'''
from prato_macarao import Prato, QUANTIDADE_DE_MACARAO, QUANTIDADE_DE_MACARAO_COMIDO_POR_TALHER;
from filosofo import Filosofo;
from threading import *;

QUANTIDADE_DE_LUGARES_NA_MESA = 5;

# Chaves dos garfos
FILOSOFO_UTILIZANDO = "filosofoUtilizando";
FILOSOFO_DONO = "filosofoDono";
ESTA_SENDO_UTILIZADO = "estaSendoUtilizado";

# Define a posição de cada filosofo e o garfo que os pertence
class Mesa:
    # controlador começando aberto
    def __init__(self):
        print(" + MESA: Quantidade de Macarrão por prato %0.0f" % QUANTIDADE_DE_MACARAO)
        print(" + MESA: Quantidade de Macarrão comido com 2 garfos %0.0f" % (QUANTIDADE_DE_MACARAO_COMIDO_POR_TALHER * 2) )
        self.controle = Semaphore(1);
        # Vetores que mapeiam os lugares e talheres na mesa!
        self.lugares_a_mesa = [0] * QUANTIDADE_DE_LUGARES_NA_MESA;
        # Criando Vetor dos garfos e Registando um filosofo "Ninguem" para evitar
        # erros de referencia!!!
        filosofo_padrao = Filosofo("Ninguem", self);
        self.garfos = [{    ESTA_SENDO_UTILIZADO : False,
                            FILOSOFO_DONO:filosofo_padrao,
                            FILOSOFO_UTILIZANDO:filosofo_padrao }] * QUANTIDADE_DE_LUGARES_NA_MESA ;

        # Ajuda a mapear o nome dos filosofos para as
        # posições no vetor lugares_a_mesa
        self.lugares_filosofos = {};
        self.lugares_ocupados = 0;

    def getPosicaoFilosofo(self, filosofo):
        return self.lugares_filosofos[filosofo.nome];

    # chamado quando um filosofo quer se sentar na mesa
    def sentar_na_mesa(self, filosofo):
        if self.lugares_ocupados > QUANTIDADE_DE_LUGARES_NA_MESA:
            return False;
        print(" + MESA: %s aceito na mesa!!!\n" % filosofo.nome);
        # Colocando um lugar a mesa
        self.lugares_filosofos[filosofo.nome] = self.lugares_ocupados;
        self.lugares_a_mesa[self.lugares_ocupados] = filosofo;
        # Criando um garfo para o filosofo
        self.garfos[self.lugares_ocupados] = {
                ESTA_SENDO_UTILIZADO: False,
                FILOSOFO_DONO:filosofo,
                FILOSOFO_UTILIZANDO:filosofo,
        };

        # Colocando um prato
        filosofo.setPrato(Prato());
        
        self.lugares_ocupados+=1;
        if self.lugares_ocupados == QUANTIDADE_DE_LUGARES_NA_MESA:
            self.mostrar_estado();

    def mostrar_estado(self):
        texto = "ESTADO DA MESA:\n";
        texto += " Ocupantes: %.0i \n" % self.lugares_ocupados ;

        for nome_filosofo, index in self.lugares_filosofos.items():
            garfo    = self.garfos[index];
            filosofo = self.lugares_a_mesa[index];
            
            texto += "\t Filosofo: "+ nome_filosofo +"\n";

            texto += "\t  Quantidade ja comida: %.0f%%\n" % filosofo.getPrato().getPercentualComido();            
            texto += "\t  Garfo a Direita sendo utilizado por: %s \n" % garfo[FILOSOFO_UTILIZANDO].nome;
            texto += "\t  Garfo a Esquerda sendo utilizado por: %s \n" %  self.garfos[index-1][FILOSOFO_UTILIZANDO].nome;
            texto += "\n";

        print(texto);

    # Chamado quando um filosofo requisita os dois garfos
    # !!!! Região CRITICA !!!!
    def pegar_garfos(self, filosofo):
        self.controle.acquire();
        index           = self.getPosicaoFilosofo(filosofo);
        # Saber se o garfo a direita(O garfo do proprio filosofo) esta livre
        garfo_direito   = self.garfos[index];
        # Saber se existe garfo a esquerda do filosofo 
        garfo_esquerdo  = self.garfos[index - 1];
        texto = "\n";
        texto += (" + MESA: %s tentando pegar garfos!!!\n" % filosofo.nome);
        
        texto += (" + MESA:\t %s GARFO DIREITO:\n" % filosofo.nome);
        texto += ("\t\t Sendo utilizado? %s \n" % garfo_direito[ESTA_SENDO_UTILIZADO]);
        texto += ("\t\t Quem utiliza? %s \n" % garfo_direito[FILOSOFO_UTILIZANDO]);
        texto += ("\t\t Esta ha Direita de quem? %s \n" % garfo_direito[FILOSOFO_DONO]);

        texto += (" + MESA:\t %s GARFO ESQUERDO:\n" % filosofo.nome);
        texto += ("\t\t Sendo utilizado? %s \n" % garfo_esquerdo[ESTA_SENDO_UTILIZADO]);
        texto += ("\t\t Quem utiliza? %s \n" % garfo_esquerdo[FILOSOFO_UTILIZANDO]);
        texto += ("\t\t Esta ha Direita de quem? %s \n" % garfo_esquerdo[FILOSOFO_DONO]);

        print(texto);
        # !!!! Região CRITICA !!!!
        pode_levar_os_dois_garfos = (not garfo_direito[ESTA_SENDO_UTILIZADO] and not garfo_esquerdo[ESTA_SENDO_UTILIZADO]);
        if pode_levar_os_dois_garfos:
            # Bloquear o uso desses 2 garfos    
            garfo_direito[ESTA_SENDO_UTILIZADO] = True;
            garfo_esquerdo[ESTA_SENDO_UTILIZADO] = True;

            garfo_direito[FILOSOFO_UTILIZANDO] = filosofo;
            garfo_esquerdo[FILOSOFO_UTILIZANDO] = filosofo;

        self.controle.release();
        return pode_levar_os_dois_garfos;

    # !!!! Região CRITICA !!!!
    def liberar_garfos(self, filosofo):
        self.controle.acquire();

        index           = self.getPosicaoFilosofo(filosofo);
        garfo_direito   = self.garfos[index];
        garfo_esquerdo  = self.garfos[index - 1];
        
        # Liberando o uso desses 2 garfos    
        garfo_direito[ESTA_SENDO_UTILIZADO] = False;
        garfo_esquerdo[ESTA_SENDO_UTILIZADO] = False;

        self.controle.release();
    

minha_mesa = Mesa();

Esopo =  Filosofo("Esopo",minha_mesa);
Socrates =  Filosofo("Socrates",minha_mesa);
Platao =  Filosofo("Platao",minha_mesa);
Aristoteles =  Filosofo("Aristoteles",minha_mesa);
Confucio =  Filosofo("Confucio",minha_mesa);


filosofo1 = Thread(target = Esopo.iniciarFilosofo );
filosofo2 = Thread(target = Socrates.iniciarFilosofo);
filosofo3 = Thread(target = Platao.iniciarFilosofo );
filosofo4 = Thread(target = Aristoteles.iniciarFilosofo);
filosofo5 = Thread(target = Confucio.iniciarFilosofo);

filosofo1.start();
filosofo2.start();
filosofo3.start();
filosofo4.start();
filosofo5.start();
