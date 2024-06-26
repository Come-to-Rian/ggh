import sys, os, json;

sys.path.append("../"); # estamos em /form, 

from PySide6.QtGui import QAction;
from PySide6.QtWidgets import  QCheckBox, QTextEdit, QLineEdit, QApplication, QDialog, QLineEdit, QPushButton, QMdiArea, QMainWindow, QFormLayout, QLabel, QMessageBox;
from PySide6 import QtWidgets;

from form.form_ip_info import FormIPInfo

from classes.conexao.xmpp_client import XMPPCliente;
from classes.conexao.sessao import Sessao;
from classes.singleton.configuracao import Configuracao;

class FormLogin(QDialog):
    def __init__(self, parent=None):
        super(FormLogin, self).__init__(parent)
        #self.setStyleSheet("border: 1px solid rgba(0, 0, 0, 0.15);")
        self.setWindowTitle("Grupo")
        self.setGeometry(400, 400, 800, 500)

        self.form_main = parent;
        self.jid_grupo = QLineEdit('', self);
        self.jid_pessoa = QLineEdit('', self);
        self.password = QLineEdit('', self);
        self.chave_criptografia = QLineEdit('', self);
        
        self.check = QCheckBox("Usar PROXY")
        self.check.setChecked(True);
        self.check.toggled.connect( self.check_connect);
        self.protocolo_proxy = QLineEdit('http', self);
        self.servidor_proxy = QLineEdit('127.0.0.1', self);
        self.porta_proxy = QLineEdit('9051', self);

        if os.path.exists(os.path.expanduser("~/.ggh_client.json")):
            buffer_config = json.loads( open(os.path.expanduser("~/.ggh_client.json"), 'r').read() );
            self.jid_grupo.setText( buffer_config["jid_grupo"] );
            self.jid_pessoa.setText( buffer_config["jid_pessoa"] );
            self.chave_criptografia.setText( buffer_config["chave_criptografia"] );
            self.password.setText( buffer_config["password"] );
            buffer_config = None;


        self.chave_criptografia.setEchoMode(QLineEdit.Password)
        self.password.setEchoMode(QLineEdit.Password)

        self.pushButton = QPushButton("Entrar"); 
        self.pushButton.clicked.connect(self.action_btn_entrar) 

        layout = QFormLayout();
        layout.addRow(QLabel("XMPP do grupo"), self.jid_grupo);
        layout.addRow(QLabel("XMPP do participante"), self.jid_pessoa);
        layout.addRow(QLabel("Senha do XMPP do participante"), self.password);
        layout.addRow(QLabel("Chave de criptografia"), self.chave_criptografia);

        layout.addRow(QLabel(""), self.check );
        layout.addRow(QLabel("Protocolo proxy"), self.protocolo_proxy);
        layout.addRow(QLabel("IP do proxy"), self.servidor_proxy);
        layout.addRow(QLabel("Porta do Proxy"), self.porta_proxy);

        layout.addRow(self.pushButton);
        self.setLayout(layout);
    def check_connect(self):
        if self.check.isChecked():
            self.protocolo_proxy.setReadOnly(False);
            self.servidor_proxy.setReadOnly(False);
            self.porta_proxy.setReadOnly(False);
        else:
            self.protocolo_proxy.setReadOnly(True);
            self.servidor_proxy.setReadOnly(True);
            self.porta_proxy.setReadOnly(True);

    def action_btn_entrar(self):
        proxy_ip = "";
        proxy_protocolo = "";
        proxy_porta = "";
        if self.check.isChecked():
            proxy_ip = self.servidor_proxy.text();
            proxy_protocolo = self.protocolo_proxy.text();
            proxy_porta = self.porta_proxy.text();
        self.pushButton.setDisabled( False );
        xmpp_var = XMPPCliente(self.jid_pessoa.text(), self.password.text(), self.jid_grupo.text(), self.chave_criptografia.text() );
        if xmpp_var.proxy( proxy_protocolo , proxy_ip,  proxy_porta):
            f = FormIPInfo();
            f.exec();
            if not f.continuar:
                return;
            if xmpp_var.conectar():
                self.form_main.callback_login( xmpp_var );
                self.close();
            else:
                self.pushButton.setDisabled( True );
                QMessageBox.information(self, "Falha de autenticação", "Não foi possível autenticar no serviço XMPP do participante, confirme que seu usuário XMPP está correto e que a senha também esteja correta.", QMessageBox.StandardButton.Ok);
        else:
            QMessageBox.information(self, "Proxy não existe", "O proxy não funcionou, veja o manual.", QMessageBox.StandardButton.Ok);