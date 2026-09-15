import datetime
from peewee import *

# Configuração do Banco
db = SqliteDatabase("agenda.db")


class BaseModel(Model):

  class Meta:
    database = db


class Contato(BaseModel):
  nome = CharField()
  telefone = CharField(unique=True)
  data_cadastro = DateTimeField(default=datetime.datetime.now)

  def __str__(self):
    return (
        f"ID: {self.id} | Nome: {self.nome} | Tel: {self.telefone} | Cadastrado"
        f" em: {self.data_cadastro.strftime('%d/%m/%Y %H:%M')}"
    )


# Inicializa banco
db.connect()
db.create_tables([Contato])

# Loop do Menu
while True:
  print("\n=== AGENDA DE CONTATOS ===")
  print("1 - Cadastrar contato")
  print("2 - Ver todos os contatos")
  print("3 - Buscar pelo nome")
  print("4 - Editar pelo ID")
  print("5 - Excluir pelo ID")
  print("6 - Sair")

  opcao = input("Escolha uma opção: ")

  if opcao == "1":
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    try:
      Contato.create(nome=nome, telefone=telefone)
      print("Contato cadastrado com sucesso!")
    except IntegrityError:
      print("Erro: Este telefone já está cadastrado.")

  elif opcao == "2":
    print("\n--- LISTA ---")
    contatos = Contato.select()
    if not contatos:
      print("Nenhum contato cadastrado.")
    for c in contatos:
      print(c)

  elif opcao == "3":
    termo = input("Nome para buscar: ")
    resultados = Contato.select().where(Contato.nome.icontains(termo))
    for c in resultados:
      print(c)

  elif opcao == "4":
    id_txt = input("ID do contato para editar: ")
    if id_txt.isdigit():
      c = Contato.get_or_none(Contato.id == int(id_txt))
      if c:
        c.nome = input(f"Novo nome [{c.nome}]: ") or c.nome
        c.telefone = input(f"Novo telefone [{c.telefone}]: ") or c.telefone
        c.save()
        print("Atualizado com sucesso!")
      else:
        print("ID não encontrado.")
    else:
      print("ID inválido.")

  elif opcao == "5":
    id_txt = input("ID do contato para excluir: ")
    if id_txt.isdigit():
      c = Contato.get_or_none(Contato.id == int(id_txt))
      if c:
        c.delete_instance()
        print("Excluído com sucesso!")
      else:
        print("ID não encontrado.")
    else:
      print("ID inválido.")

  elif opcao == "6":
    print("Saindo...")
    db.close()
    break
  else:
    print("Opção inválida!")