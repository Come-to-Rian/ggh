import json, re, base64, requests;

from api.fsseguro import FsSeguro;
from classes.atividade_resposta import AtividadeResposta;

class Atividade:
    def __init__(self):
        self.id = None;
        self.id_cliente = None;
        self.id_nivel = None;
        self.id_grupo = None;
        self.titulo = "";
        self.execucoes = 1;
        self.tentativas = 3;
        self.instrucao_correcao = "";
        self.data_maxima = "2079-12-06";
        self.instrucao = "";
        self.pontos_maximo = 5;
        self.id_status = 0;
        self.respostas = [];
        self.atividade = None;
        self.pontos_correcao_maximo = 1;
        self.operacoes = [];
        self.nome_nivel = None;
        self.posicao_nivel = 0;
    
    def fromJson(self, js ):
        self.id = js["id"];
        self.id_cliente = js["id_cliente"];
        self.id_nivel = js["id_nivel"];
        self.id_grupo = js["id_grupo"];
        self.titulo = js["titulo"];
        self.execucoes = js["execucoes"];
        self.tentativas = js["tentativas"];
        self.instrucao_correcao = js["instrucao_correcao"];
        self.data_maxima = js["data_maxima"];
        self.instrucao = js["instrucao"];
        self.pontos_maximo = js["pontos_maximo"];
        self.id_status = js["id_status"];
        self.atividade = js.get("atividade");
        if js.get("posicao_nivel") != None:
            self.posicao_nivel = js["posicao_nivel"];
        if js.get("nome_nivel") != None:
            self.nome_nivel = js["nome_nivel"];
        if js.get("operacoes") != None:
            self.operacoes = js["operacoes"];
        if js.get("pontos_correcao_maximo") != None:
            self.pontos_correcao_maximo = js["pontos_correcao_maximo"];
        if js.get("respostas") != None:
            for resposta in js["respostas"]:
                buffer = AtividadeResposta();
                buffer.fromJson(resposta);
                self.respostas.append( buffer );
    def getStatus(self):
        if self.id_status == None:
            return "-";
        if self.id_status == 0:
            return "Em edição";
        elif self.id_status == 1:
            return "Cancelado/Pausado";
        elif self.id_status == 2:
            return "Em produção";
    def adicionar_resposta(self,id_cliente, pontos, resposta):
        buffer = AtividadeResposta();
        buffer.pontos = pontos;
        buffer.resposta = resposta;
        buffer.id_cliente = id_cliente;
        buffer.id_atividade = self.id;
        retornar = len(self.respostas);
        self.respostas.append(buffer);
        return retornar;
            
    def toJson(self):
        respostas_buffer = [];
        for resposta in self.respostas:
            respostas_buffer.append( resposta.toJson() );
        return {"id" : self.id, "id_cliente" : self.id_cliente, "id_nivel" : self.id_nivel, "id_grupo" : self.id_grupo, "titulo" : self.titulo,
                "execucoes" : self.execucoes, "tentativas" : self.tentativas, "instrucao_correcao" : self.instrucao_correcao, "data_maxima" : self.data_maxima,
                "instrucao" : self.instrucao, "pontos_maximo" : self.pontos_maximo, "id_status" : self.id_status, "atividade" : self.atividade,
                "respostas" : respostas_buffer , "pontos_correcao_maximo" : self.pontos_correcao_maximo, "operacoes" : self.operacoes };

    def salvar(self, chave, path):
        fs = FsSeguro(chave);
        fs.escrever_json( path + "/" + self.id, self.toJson() );

    def carregar(self, chave, path):
        fs = FsSeguro(chave);
        self.fromJson( fs.ler_json( path ) );
        #self.id = None;
        #self.id_atividade = None;
        #self.id_cliente = None;
        #self.id_avaliador = None;
        #self.data = None;
        #self.data_avaliador = None;
        #self.consideracao_avaliador = None;
