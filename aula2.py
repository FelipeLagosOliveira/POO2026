print("Programação Orientada a Objetos")
nome = input("Nome: ")
idade = input("Idade: ")
salario = float(input("Salário: "))

print("Olá", nome, "você tem", idade, "anos.")
# str formatada
print(f"Olá {nome}. Você tem {idade} anos.")


if(salario < 10000):
    print(f"Você ganha muito mal: {salario:.2f}")
elif(salario > 10000 and salario <2000):
    print(f"Você ganha bem: {salario:.2f}")
else: 
    print(f"Você ganha muito bem: {salario:.2f}")
