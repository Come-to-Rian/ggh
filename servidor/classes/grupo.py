import sys, os, hashlib;

from classes.mysqlhelp import MysqlHelp

def criar_diretorio_se_nao_existe(diretorio):
    if not os.path.exists( diretorio ):
        os.makedirs( diretorio );

class Grupo:
    def __init__(self, jid_grupo):
        # iniciar diretórios
        self.jid = jid_grupo;
        self.id = hashlib.md5( self.jid.encode() ).hexdigest() ;
        print("Grupo iniciado:", self.id );
        self.path_home = os.path.expanduser("~/ggh_servidor/")
        self.path_grupo = self.path_home + "/" + hashlib.md5( jid_grupo.encode() ).hexdigest();
        self.path_grupo_html = self.path_grupo + "/html";
        self.path_grupo_public_key = self.path_grupo + "/public_key";
        self.path_grupo_apelidos = self.path_grupo + "/apelidos";
        
        criar_diretorio_se_nao_existe(self.path_home);
        criar_diretorio_se_nao_existe(self.path_grupo);
        criar_diretorio_se_nao_existe(self.path_grupo_html);
        
        criar_diretorio_se_nao_existe(self.path_grupo + "/clientes/" );
        os.environ['PATH_GRUPO'] = self.path_grupo;
        self.clientes = {};
    def clientes_nick(self):
        my = MysqlHelp();
        datatable = my.datatable("select cl.apelido from grupo_cliente as gc inner join cliente as cl on gc.id_cliente = cl.id where gc.id_grupo = %s", [ self.id ]);
        return { "lista" : datatable };
    def niveis(self):
        my = MysqlHelp();
        buffer =  my.datatable("select * from nivel as ni where ni.id_grupo = %s", [ self.id ]);
        return buffer; 
    def tags(self):
        my = MysqlHelp();
        return my.datatable("select * from tag as ta where ta.id_grupo = %s", [ self.id ]);
    
    def registrar_chave_publica(self, cliente, semente=""):
        chave_simetrica =  str( uuid.uuid5(uuid.NAMESPACE_URL, semente + cliente ) )[0:16];
        self.clientes[ cliente ] = chave_simetrica; 
        return chave_simetrica;
        


