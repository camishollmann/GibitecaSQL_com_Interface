from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Conexão com o banco de dados
DATABASE_URL = "mysql+pymysql://root:@localhost/gibis"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Modelos das Tabelas
class Gibi(Base):
    __tablename__ = 'gibis'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    titulo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    editora_id = Column(Integer, ForeignKey('editoras.id'), nullable=False)
    autor_id = Column(Integer, ForeignKey('autores.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    editora = relationship("Editora", back_populates="gibis")
    autor = relationship("Autor", back_populates="gibis")
    categoria = relationship("Categoria", back_populates="gibis")


class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    pais_origem = Column(String, nullable=False)

    gibis = relationship("Gibi", back_populates="autor")


class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)

    gibis = relationship("Gibi", back_populates="editora")


class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    gibis = relationship("Gibi", back_populates="categoria")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Funções CRUD com validação e tratamento de exceções
def add_editora(nome, cidade):
    try:
        if not nome or not cidade:
            raise ValueError("Nome e cidade são obrigatórios.")
        editora = Editora(nome=nome, cidade=cidade)
        session.add(editora)
        session.commit()
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao adicionar editora: {e}")

def add_autor(nome, pais_origem):
    try:
        if not nome or not pais_origem:
            raise ValueError("Nome e país de origem são obrigatórios.")
        autor = Autor(nome=nome, pais_origem=pais_origem)
        session.add(autor)
        session.commit()
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao adicionar autor: {e}")

def add_categoria(nome):
    try:
        if not nome:
            raise ValueError("Nome da categoria é obrigatório.")
        categoria = Categoria(nome=nome)
        session.add(categoria)
        session.commit()
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao adicionar categoria: {e}")

def add_gibi(titulo, ano, editora_id, autor_id, categoria_id):
    try:
        if not titulo or not ano or not editora_id or not autor_id or not categoria_id:
            raise ValueError("Todos os campos são obrigatórios.")
        gibi = Gibi(titulo=titulo, ano=ano, editora_id=editora_id, autor_id=autor_id, categoria_id=categoria_id)
        session.add(gibi)
        session.commit()
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao adicionar gibi: {e}")

def get_gibi(titulo):
    return session.query(Gibi).filter_by(titulo=titulo).first()

def update_gibi(gibi_id, novo_titulo):
    try:
        if not novo_titulo:
            raise ValueError("O novo título não pode ser vazio.")
        gibi = session.query(Gibi).filter_by(id=gibi_id).first()
        if gibi:
            gibi.titulo = novo_titulo
            session.commit()
        else:
            raise ValueError("Gibi não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao atualizar gibi: {e}")

def delete_gibi(gibi_id):
    try:
        gibi = session.query(Gibi).filter_by(id=gibi_id).first()
        if gibi:
            session.delete(gibi)
            session.commit()
        else:
            raise ValueError("Gibi não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"Erro ao deletar gibi: {e}")

# Funções de listagem
def list_gibis():
    try:
        gibis = session.query(Gibi).all()
        return gibis
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao listar gibis: {e}")

def list_autores():
    try:
        autores = session.query(Autor).all()
        return autores
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao listar autores: {e}")

def list_editoras():
    try:
        editoras = session.query(Editora).all()
        return editoras
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao listar editoras: {e}")

def list_categorias():
    try:
        categorias = session.query(Categoria).all()
        return categorias
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao listar categorias: {e}")

# Interface Gráfica com PyQt5 e Abas
class GibiApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRUD Gibis")
        self.setGeometry(100, 100, 600, 500)

        # Criando o Tab Widget
        self.tabs = QTabWidget()

        # Criando as abas
        self.gibi_tab = QWidget()
        self.editora_tab = QWidget()
        self.autor_tab = QWidget()
        self.categoria_tab = QWidget()

        # Adicionando as abas ao widget
        self.tabs.addTab(self.gibi_tab, "Gibis")
        self.tabs.addTab(self.editora_tab, "Editoras")
        self.tabs.addTab(self.autor_tab, "Autores")
        self.tabs.addTab(self.categoria_tab, "Categorias")

        # Configurando o layout da aba Gibis
        self.gibi_tab_layout = QVBoxLayout()
        form_layout_gibi = QFormLayout()

        self.title_label = QLabel("Título:")
        self.title_input = QLineEdit()

        self.year_label = QLabel("Ano:")
        self.year_input = QLineEdit()

        self.editora_label = QLabel("Editora ID:")
        self.editora_input = QLineEdit()

        self.autor_label = QLabel("Autor ID:")
        self.autor_input = QLineEdit()

        self.categoria_label = QLabel("Categoria ID:")
        self.categoria_input = QLineEdit()

        form_layout_gibi.addRow(self.title_label, self.title_input)
        form_layout_gibi.addRow(self.year_label, self.year_input)
        form_layout_gibi.addRow(self.editora_label, self.editora_input)
        form_layout_gibi.addRow(self.autor_label, self.autor_input)
        form_layout_gibi.addRow(self.categoria_label, self.categoria_input)

        self.add_gibi_btn = QPushButton("Adicionar Gibi")
        self.add_gibi_btn.clicked.connect(self.add_gibi)

        # Tabela e botão de listar Gibis
        self.gibi_table = QTableWidget()
        self.gibi_table.setColumnCount(6)
        self.gibi_table.setHorizontalHeaderLabels(["ID", "Título", "Ano", "Editora", "Autor", "Categoria"])

        self.list_gibis_btn = QPushButton("Listar Gibis")
        self.list_gibis_btn.clicked.connect(self.list_gibis)

        self.gibi_tab_layout.addLayout(form_layout_gibi)
        self.gibi_tab_layout.addWidget(self.add_gibi_btn)
        self.gibi_tab_layout.addWidget(self.gibi_table)
        self.gibi_tab_layout.addWidget(self.list_gibis_btn)

        self.gibi_tab.setLayout(self.gibi_tab_layout)

        # Configurando o layout da aba Editoras
        self.editora_tab_layout = QVBoxLayout()
        form_layout_editora = QFormLayout()

        self.editora_nome_label = QLabel("Nome da Editora:")
        self.editora_nome_input = QLineEdit()

        self.editora_cidade_label = QLabel("Cidade da Editora:")
        self.editora_cidade_input = QLineEdit()

        form_layout_editora.addRow(self.editora_nome_label, self.editora_nome_input)
        form_layout_editora.addRow(self.editora_cidade_label, self.editora_cidade_input)

        self.add_editora_btn = QPushButton("Adicionar Editora")
        self.add_editora_btn.clicked.connect(self.add_editora)

        # Tabela e botão de listar Editoras
        self.editora_table = QTableWidget()
        self.editora_table.setColumnCount(3)
        self.editora_table.setHorizontalHeaderLabels(["ID", "Nome", "Cidade"])

        self.list_editoras_btn = QPushButton("Listar Editoras")
        self.list_editoras_btn.clicked.connect(self.list_editoras)

        self.editora_tab_layout.addLayout(form_layout_editora)
        self.editora_tab_layout.addWidget(self.add_editora_btn)
        self.editora_tab_layout.addWidget(self.editora_table)
        self.editora_tab_layout.addWidget(self.list_editoras_btn)

        self.editora_tab.setLayout(self.editora_tab_layout)

        # Configurando o layout da aba Autores
        self.autor_tab_layout = QVBoxLayout()
        form_layout_autor = QFormLayout()

        self.autor_nome_label = QLabel("Nome do Autor:")
        self.autor_nome_input = QLineEdit()

        self.autor_pais_label = QLabel("País de Origem:")
        self.autor_pais_input = QLineEdit()

        form_layout_autor.addRow(self.autor_nome_label, self.autor_nome_input)
        form_layout_autor.addRow(self.autor_pais_label, self.autor_pais_input)

        self.add_autor_btn = QPushButton("Adicionar Autor")
        self.add_autor_btn.clicked.connect(self.add_autor)

        # Tabela e botão de listar Autores
        self.autor_table = QTableWidget()
        self.autor_table.setColumnCount(3)
        self.autor_table.setHorizontalHeaderLabels(["ID", "Nome", "País"])

        self.list_autores_btn = QPushButton("Listar Autores")
        self.list_autores_btn.clicked.connect(self.list_autores)

        self.autor_tab_layout.addLayout(form_layout_autor)
        self.autor_tab_layout.addWidget(self.add_autor_btn)
        self.autor_tab_layout.addWidget(self.autor_table)
        self.autor_tab_layout.addWidget(self.list_autores_btn)

        self.autor_tab.setLayout(self.autor_tab_layout)

        # Configurando o layout da aba Categorias
        self.categoria_tab_layout = QVBoxLayout()
        form_layout_categoria = QFormLayout()

        self.categoria_nome_label = QLabel("Nome da Categoria:")
        self.categoria_nome_input = QLineEdit()

        form_layout_categoria.addRow(self.categoria_nome_label, self.categoria_nome_input)

        self.add_categoria_btn = QPushButton("Adicionar Categoria")
        self.add_categoria_btn.clicked.connect(self.add_categoria)

        # Tabela e botão de listar Categorias
        self.categoria_table = QTableWidget()
        self.categoria_table.setColumnCount(2)
        self.categoria_table.setHorizontalHeaderLabels(["ID", "Nome"])

        self.list_categorias_btn = QPushButton("Listar Categorias")
        self.list_categorias_btn.clicked.connect(self.list_categorias)

        self.categoria_tab_layout.addLayout(form_layout_categoria)
        self.categoria_tab_layout.addWidget(self.add_categoria_btn)
        self.categoria_tab_layout.addWidget(self.categoria_table)
        self.categoria_tab_layout.addWidget(self.list_categorias_btn)

        self.categoria_tab.setLayout(self.categoria_tab_layout)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

    # Funções de interação com o banco de dados
    def add_gibi(self):
        titulo = self.title_input.text()
        ano = int(self.year_input.text())
        editora_id = int(self.editora_input.text())
        autor_id = int(self.autor_input.text())
        categoria_id = int(self.categoria_input.text())

        try:
            add_gibi(titulo, ano, editora_id, autor_id, categoria_id)
            QMessageBox.information(self, "Sucesso", "Gibi adicionado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def list_gibis(self):
        gibis = list_gibis()
        self.gibi_table.setRowCount(0)

        for gibi in gibis:
            row_position = self.gibi_table.rowCount()
            self.gibi_table.insertRow(row_position)
            self.gibi_table.setItem(row_position, 0, QTableWidgetItem(str(gibi.id)))
            self.gibi_table.setItem(row_position, 1, QTableWidgetItem(gibi.titulo))
            self.gibi_table.setItem(row_position, 2, QTableWidgetItem(str(gibi.ano)))
            self.gibi_table.setItem(row_position, 3, QTableWidgetItem(gibi.editora.nome))
            self.gibi_table.setItem(row_position, 4, QTableWidgetItem(gibi.autor.nome))
            self.gibi_table.setItem(row_position, 5, QTableWidgetItem(gibi.categoria.nome))

    def add_editora(self):
        nome = self.editora_nome_input.text()
        cidade = self.editora_cidade_input.text()

        try:
            add_editora(nome, cidade)
            QMessageBox.information(self, "Sucesso", "Editora adicionada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def list_editoras(self):
        editoras = list_editoras()
        self.editora_table.setRowCount(0)

        for editora in editoras:
            row_position = self.editora_table.rowCount()
            self.editora_table.insertRow(row_position)
            self.editora_table.setItem(row_position, 0, QTableWidgetItem(str(editora.id)))
            self.editora_table.setItem(row_position, 1, QTableWidgetItem(editora.nome))
            self.editora_table.setItem(row_position, 2, QTableWidgetItem(editora.cidade))

    def add_autor(self):
        nome = self.autor_nome_input.text()
        pais_origem = self.autor_pais_input.text()

        try:
            add_autor(nome, pais_origem)
            QMessageBox.information(self, "Sucesso", "Autor adicionado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def list_autores(self):
        autores = list_autores()
        self.autor_table.setRowCount(0)

        for autor in autores:
            row_position = self.autor_table.rowCount()
            self.autor_table.insertRow(row_position)
            self.autor_table.setItem(row_position, 0, QTableWidgetItem(str(autor.id)))
            self.autor_table.setItem(row_position, 1, QTableWidgetItem(autor.nome))
            self.autor_table.setItem(row_position, 2, QTableWidgetItem(autor.pais_origem))

    def add_categoria(self):
        nome = self.categoria_nome_input.text()

        try:
            add_categoria(nome)
            QMessageBox.information(self, "Sucesso", "Categoria adicionada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def list_categorias(self):
        categorias = list_categorias()
        self.categoria_table.setRowCount(0)

        for categoria in categorias:
            row_position = self.categoria_table.rowCount()
            self.categoria_table.insertRow(row_position)
            self.categoria_table.setItem(row_position, 0, QTableWidgetItem(str(categoria.id)))
            self.categoria_table.setItem(row_position, 1, QTableWidgetItem(categoria.nome))


if __name__ == '__main__':
    app = QApplication([])
    window = GibiApp()
    window.show()
    app.exec_()
