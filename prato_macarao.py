# -*- coding: utf-8 -*-

QUANTIDADE_DE_MACARAO = 40;
QUANTIDADE_DE_MACARAO_COMIDO_POR_TALHER = 4;

class Prato:

    def __init__(self):
        self.macarao = QUANTIDADE_DE_MACARAO;

    def comer(self,quantidade_talheres):
        if not self.existeMacarao():
            return False;
        # Bloquea que um filosofo coma com somente 1 garfo
        if quantidade_talheres < 2:
            return False;
        else:
            self.macarao = self.macarao - (QUANTIDADE_DE_MACARAO_COMIDO_POR_TALHER * quantidade_talheres);
            return True;
    def getPercentualComido(self):
        return (QUANTIDADE_DE_MACARAO - float(self.macarao)) / QUANTIDADE_DE_MACARAO * 100;
    def existeMacarao(self):
        return self.macarao > 0;