"""
def verifica_par(x):
    if (x % 2 == 0):
        return True
    return False
x = int(input("Digite um valor inteiro"))
if (verifica_par):
    print(f"O {x} é par")
else:
    print(f"O n{x} não é par")
    """

def calcDesconto(precos, p):
    for i in range(0, len(precos)):
        desconto = precos[i] * (p/100)
        valorFinal = precos[i] - desconto
        precos[i] = valorFinal
    return precos    

indiceProd = 0
produtos = [""] * 10
precos = []    

    
opc = 0
while(opc != 4):
    print("1- Cadastrar produto")
    print("2- Listar produtos")
    print("3- Aplicar desconto")
    print("4- Sair do programa")

    opc = int(input("Digite um valor:"))
    if(opc == 1):
        print("1- Cadastrar produto")
        nome = str(input("Digite o nome do produto: "))
        preco = float(input("Informe o valor do produto: "))
        produtos[indiceProd] = nome 
        indiceProd += 1 
        precos.append(preco)

       

    elif(opc == 2):
        print("2- Listar produtos")
        for i in range(0, len(precos)):
            print(produtos[i], "-", precos[i])

    elif(opc == 3):
        print("3- Aplicar desconto")
        desconto = int(input("Digite a porcentagem de desconto"))
        precoFinal = calcDesconto(precos,desconto)
        for i in range(0, len(precos)):
            print(produtos[i], "-", precoFinal[i])
        

    elif(opc == 4):
        print("4- Sair do programa")
        
    else: 
        print("Opção inválida")


