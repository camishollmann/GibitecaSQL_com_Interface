from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
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


# Interface Gráfica com PyQt5
class GibiApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRUD Gibis")
        self.setGeometry(100, 100, 400, 400)  # Aumentando a altura para caber os novos campos
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos para o Gibi
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

        form_layout.addRow(self.title_label, self.title_input)
        form_layout.addRow(self.year_label, self.year_input)
        form_layout.addRow(self.editora_label, self.editora_input)
        form_layout.addRow(self.autor_label, self.autor_input)
        form_layout.addRow(self.categoria_label, self.categoria_input)

        # Campos para Editora
        self.editora_nome_label = QLabel("Nome da Editora:")
        self.editora_nome_input = QLineEdit()

        self.editora_cidade_label = QLabel("Cidade da Editora:")
        self.editora_cidade_input = QLineEdit()

        form_layout.addRow(self.editora_nome_label, self.editora_nome_input)
        form_layout.addRow(self.editora_cidade_label, self.editora_cidade_input)

        # Campos para Autor
        self.autor_nome_label = QLabel("Nome do Autor:")
        self.autor_nome_input = QLineEdit()

        self.autor_pais_label = QLabel("País de Origem:")
        self.autor_pais_input = QLineEdit()

        form_layout.addRow(self.autor_nome_label, self.autor_nome_input)
        form_layout.addRow(self.autor_pais_label, self.autor_pais_input)

        # Campos para Categoria
        self.categoria_nome_label = QLabel("Nome da Categoria:")
        self.categoria_nome_input = QLineEdit()

        form_layout.addRow(self.categoria_nome_label, self.categoria_nome_input)

        layout.addLayout(form_layout)

        # Botões de CRUD para Gibi
        self.add_btn = QPushButton("Adicionar Gibi")
        self.add_btn.clicked.connect(self.add_gibi)

        self.search_btn = QPushButton("Buscar Gibi")
        self.search_btn.clicked.connect(self.search_gibi)

        self.update_btn = QPushButton("Atualizar Gibi")
        self.update_btn.clicked.connect(self.update_gibi)

        self.delete_btn = QPushButton("Deletar Gibi")
        self.delete_btn.clicked.connect(self.delete_gibi)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)

        # Botões para adicionar Editora, Autor e Categoria
        self.add_editora_btn = QPushButton("Adicionar Editora")
        self.add_editora_btn.clicked.connect(self.add_editora)

        self.add_autor_btn = QPushButton("Adicionar Autor")
        self.add_autor_btn.clicked.connect(self.add_autor)

        self.add_categoria_btn = QPushButton("Adicionar Categoria")
        self.add_categoria_btn.clicked.connect(self.add_categoria)

        layout.addWidget(self.add_editora_btn)
        layout.addWidget(self.add_autor_btn)
        layout.addWidget(self.add_categoria_btn)

        self.setLayout(layout)

    def add_gibi(self):
        try:
            titulo = self.title_input.text()
            ano = int(self.year_input.text())
            editora_id = int(self.editora_input.text())
            autor_id = int(self.autor_input.text())
            categoria_id = int(self.categoria_input.text())
            add_gibi(titulo, ano, editora_id, autor_id, categoria_id)
            QMessageBox.information(self, "Sucesso", "Gibi adicionado com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro nos dados inseridos: {e}")

    def add_editora(self):
        try:
            nome = self.editora_nome_input.text()
            cidade = self.editora_cidade_input.text()
            add_editora(nome, cidade)
            QMessageBox.information(self, "Sucesso", "Editora adicionada com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro nos dados inseridos: {e}")

    def add_autor(self):
        try:
            nome = self.autor_nome_input.text()
            pais_origem = self.autor_pais_input.text()
            add_autor(nome, pais_origem)
            QMessageBox.information(self, "Sucesso", "Autor adicionado com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro nos dados inseridos: {e}")

    def add_categoria(self):
        try:
            nome = self.categoria_nome_input.text()
            add_categoria(nome)
            QMessageBox.information(self, "Sucesso", "Categoria adicionada com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro nos dados inseridos: {e}")

    def search_gibi(self):
        titulo = self.title_input.text()
        gibi = get_gibi(titulo)
        if gibi:
            QMessageBox.information(self, "Gibi Encontrado", f"Título: {gibi.titulo}\nAno: {gibi.ano}")
        else:
            QMessageBox.warning(self, "Erro", "Gibi não encontrado.")

    def update_gibi(self):
        try:
            gibi_id = int(self.title_input.text())
            novo_titulo = self.year_input.text()
            update_gibi(gibi_id, novo_titulo)
            QMessageBox.information(self, "Sucesso", "Gibi atualizado com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar: {e}")

    def delete_gibi(self):
        try:
            gibi_id = int(self.title_input.text())
            delete_gibi(gibi_id)
            QMessageBox.information(self, "Sucesso", "Gibi deletado com sucesso!")
        except ValueError as e:
            QMessageBox.warning(self, "Erro", f"Erro ao deletar: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = GibiApp()
    window.show()
    app.exec_()
