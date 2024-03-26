import uuid, time;

from classes.atividade import Atividade;

#cliente
class AtividadeComando:    
    def listar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        lista = js["lista"];
        self.salvar_lista( cliente, lista );
       	return True;

    def criar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];

    def salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        a = Atividade();
        a.fromJson( js["atividade"] );
        a.salvar( cliente.chave_local, cliente.path_atividade );
        return js["status"];

    def resposta_adicionar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        return js["status"];
    
    def resposta_salvar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True:
            lista = js["lista"];
            self.salvar_lista( cliente, lista );
        return js["status"];
    
    def resposta_aprovar_reprovar(self, cliente, grupo, mensagem):
        js = mensagem.toJson();
        if js["status"] == True:
            lista = js["lista"];
            self.salvar_lista( cliente, lista );
        return js["status"];

    def salvar_lista(self, cliente, lista):
        for elemento in lista:
            a = Atividade();
            a.fromJson( elemento );
            a.salvar( cliente.chave_local, cliente.path_atividade );