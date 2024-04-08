
from PySide6.QtGui import QPalette;
from PySide6.QtCore import Qt;
from PySide6 import QtWidgets;
from PySide6.QtWidgets import QGridLayout,QTextEdit, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QHeaderView;


class Utilitario():
    @staticmethod
    def widget_linha(form, layout, controls):
        widget1 = QWidget(form);
        widget1_layout = QHBoxLayout();
        widget1.setLayout(widget1_layout);
        for control in controls:
            widget1_layout.addWidget( control );
        layout.addWidget(widget1);
    def widget_layout(form, controls):
        widget1 = QWidget(form);
        widget1_layout = QHBoxLayout();
        widget1.setLayout(widget1_layout);
        for control in controls:
            widget1_layout.addWidget( control );
        return widget1;
    @staticmethod
    def widget_tab(tab, titulo):
        page = QWidget(tab);
        page_layout=QVBoxLayout()
        page.setLayout(page_layout);
        tab.addTab( page, titulo );
        return page_layout;
    @staticmethod
    def widget_tabela(form, colunas, tamanhos=None, double_click=None):
        table = QTableWidget(form)
        if double_click != None:
            table.doubleClicked.connect( double_click );
        js = {};
        for coluna in colunas:
            js[coluna] = "";
        table.setSelectionBehavior(QAbstractItemView.SelectRows); 
        table.setColumnCount(len(colunas));
        table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        table.setHorizontalHeaderLabels(js.keys());
        if tamanhos != None:
            header = table.horizontalHeader() 
            for i in range(len(tamanhos)):
                header.setSectionResizeMode(i, tamanhos[i]);
        table.setRowCount(0)
        return table;

