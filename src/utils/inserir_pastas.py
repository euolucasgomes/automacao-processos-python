from banco_dados import BancoDeDados

# Inicializa o banco de dados
banco = BancoDeDados()

# Lista de pastas a serem inseridas
pastas = [
    "00147 - ADVOCACIA MURILLO DE ARAGÃO",
    "00200 - CLIENTE XYZ",
    "00350 - EMPRESA ABC",
    "00400 - CLIENTE TESTE",
    "00500 - OUTRO CLIENTE",
]

# Insere as pastas no banco de dados
banco.inserir_pastas(pastas)

# Lista todas as pastas para confirmar a inserção
todas_pastas = banco.listar_todas_pastas()
print("Pastas no banco de dados:")
for pasta in todas_pastas:
    print(pasta)

# Fecha a conexão com o banco
banco.fechar_conexao()
