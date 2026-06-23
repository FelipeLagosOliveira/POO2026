import os

print("✉️ Configurando email...")
email = input("Informe o email ou deixe vazio: ")
if (len(email) < 3 ):
    email = "20241PVAI0030007@estudantes.ifpr.edu.br"
    print ("Usando o email padrão")
comando_email = f"git config user.email {email}"
os.system(comando_email)

print("🆕 Adicionando modificações...")
comando1 = "git add *"
os.system(comando1)

mensagem = input("🔤 Informe a mensagem do commit: ")
while (len(mensagem) < 5):
    print("⚠️ Mensagem muito pequena, detalhe mais...")

print("✅ Registrando alterações...")
comando2 = f"git commit -m \"{mensagem}\" "
os.system(comando2)

print ("🛜 Enviando projeto ao GitHub")
comando3 = "git push"
os.system(comando3)