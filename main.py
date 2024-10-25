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

        self.gibi_id_label = QLabel("ID do Gibi:")
        self.gibi_id_input = QLineEdit()  # Novo campo para o ID do gibi que será atualizado

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

        form_layout_gibi.addRow(self.gibi_id_label, self.gibi_id_input)  # Adiciona o novo campo ao layout
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

        # Botão de atualizar Gibi
        self.update_gibi_btn = QPushButton("Atualizar Gibi")
        self.update_gibi_btn.clicked.connect(self.update_gibi)

        # Botão de deletar Gibi
        self.delete_gibi_btn = QPushButton("Deletar Gibi")
        self.delete_gibi_btn.clicked.connect(self.delete_gibi)

        self.gibi_tab_layout.addLayout(form_layout_gibi)
        self.gibi_tab_layout.addWidget(self.add_gibi_btn)
        self.gibi_tab_layout.addWidget(self.update_gibi_btn)
        self.gibi_tab_layout.addWidget(self.delete_gibi_btn)
        self.gibi_tab_layout.addWidget(self.gibi_table)
        self.gibi_tab_layout.addWidget(self.list_gibis_btn)

        self.gibi_tab.setLayout(self.gibi_tab_layout)

        # Adicionando as abas ao layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def add_gibi(self):
        titulo = self.title_input.text()
        ano = self.year_input.text()
        editora_id = self.editora_input.text()
        autor_id = self.autor_input.text()
        categoria_id = self.categoria_input.text()

        try:
            add_gibi(titulo, int(ano), int(editora_id), int(autor_id), int(categoria_id))
            QMessageBox.information(self, "Sucesso", "Gibi adicionado com sucesso!")
            self.clear_form()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira valores válidos.")

    def list_gibis(self):
        gibis = list_gibis()
        self.gibi_table.setRowCount(len(gibis))
        for row_index, gibi in enumerate(gibis):
            self.gibi_table.setItem(row_index, 0, QTableWidgetItem(str(gibi.id)))
            self.gibi_table.setItem(row_index, 1, QTableWidgetItem(gibi.titulo))
            self.gibi_table.setItem(row_index, 2, QTableWidgetItem(str(gibi.ano)))
            self.gibi_table.setItem(row_index, 3, QTableWidgetItem(str(gibi.editora_id)))
            self.gibi_table.setItem(row_index, 4, QTableWidgetItem(str(gibi.autor_id)))
            self.gibi_table.setItem(row_index, 5, QTableWidgetItem(str(gibi.categoria_id)))

    def update_gibi(self):
        gibi_id_text = self.gibi_id_input.text()  # Obtém o ID do gibi a partir do novo campo
        novo_titulo = self.title_input.text()  # Novo título a ser atualizado

        if not gibi_id_text or not novo_titulo:  # Verifica se os campos estão preenchidos
            QMessageBox.warning(self, "Erro", "Por favor, preencha o ID do gibi e o novo título.")
            return

        try:
            gibi_id = int(gibi_id_text)  # Converte o ID para inteiro
            update_gibi(gibi_id, novo_titulo)  # Chama a função de atualização
            QMessageBox.information(self, "Sucesso", "Gibi atualizado com sucesso!")
        except ValueError:
            QMessageBox.warning(self, "Erro", "ID do gibi deve ser um número inteiro.")

    def delete_gibi(self):
        gibi_id_text = self.gibi_id_input.text()  # Obtém o ID do gibi a ser deletado

        if not gibi_id_text:  # Verifica se o campo do ID está preenchido
            QMessageBox.warning(self, "Erro", "Por favor, preencha o ID do gibi a ser deletado.")
            return

        try:
            gibi_id = int(gibi_id_text)  # Converte o ID para inteiro
            delete_gibi(gibi_id)  # Chama a função de deletar
            QMessageBox.information(self, "Sucesso", "Gibi deletado com sucesso!")
        except ValueError:
            QMessageBox.warning(self, "Erro", "ID do gibi deve ser um número inteiro.")

    def clear_form(self):
        self.title_input.clear()
        self.year_input.clear()
        self.editora_input.clear()
        self.autor_input.clear()
        self.categoria_input.clear()
        self.gibi_id_input.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = GibiApp()
    window.show()
    app.exec_()
