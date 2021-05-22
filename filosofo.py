# -*- coding: utf-8 -*-

from prato_macarao import Prato;
from threading import *;
import time;

class Filosofo:
    def __init__(self, nome, mesa):
        self.nome = nome;
        self.mesa = mesa;

    # inicia o ciclo de vida do filosofo
    def iniciarFilosofo(self):
        # Registrando filosofo na mesa
        print("\t @%s: Estou tentando sentar na mesa!\n" % self.nome);
        self.mesa.sentar_na_mesa(self);
        while True:
            time.sleep(1);
            print("\t @%s: Estou tentando pegar 2 garfos na mesa!\n" % self.nome);
            # !!!! Região CRITICA !!!!
            conseguiu_pegar_os_garfos = self.mesa.pegar_garfos(self);
            quantidade_garfos = 2 if conseguiu_pegar_os_garfos else 1;
            
            consegui_comer = self.getPrato().comer(quantidade_garfos);

            if consegui_comer:
                print("\t @%s: Consegui comer %0.1f%%!\n" % (self.nome, self.getPrato().getPercentualComido()));
                print("\t @%s: liberando 2 garfos na mesa e voltando a Pensar!!!\n" % self.nome);
                self.mesa.liberar_garfos(self);
            else:
                print(" + MESA: %s não conseguiu comer e ficou Pensando!!!\n" % self.nome);

            if not self.getPrato().existeMacarao():
                # Terminou de comer 
                print("\t @%s: Terminei de Comer!!\n" % self.nome);
                print("\t @%s: estou Pensando!!!\n" % self.nome);
                self.mesa.mostrar_estado();
                return;# FINALIZA O CICLO DE VIDA DO FILOSOFO!!!!!

            time.sleep(3);

    def pensar(self):
        print("\t @%s: estou pensando!" % self.nome );
    def setPrato(self, prato):
        print("\t @%s: Recebi um prato!!!!\n" % self.nome);
        self.prato = prato;
    def getPrato(self):
        return self.prato;

    def __str__(self):
      return self.nome;
    def __unicode__(self):
        return self.nome;
    def __repr__(self):
        return self.nome;