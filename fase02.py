import tabulate
import sys
import oracledb

try:
 conexao = oracledb.connect(
 user="ARTHUR",
 password="Eunasciem",
 dsn="192.168.0.15/XEPDB1")

except Exception as erro:
 print ('Erro em conexão', erro)
else:
 print ("Conectado", conexao.version)

 # Criar Cursor
 cursor= conexao.cursor()

 # Criar Cursor
cursor = conexao.cursor()

'''cursor.execute ("""
CREATE TABLE ESTOQUE (
cod_prod INTEGER PRIMARY KEY,
nome VARCHAR2(50),
descrição VARCHAR2(150),
ca FLOAT,
cf FLOAT,
cv FLOAT,
iv FLOAT,
ml Float
 )""")'''

def mostrar_produtos():
    from tabulate import tabulate

    conexao.commit()
    sql_select_Query = "SELECT * FROM estoque order by cod_prod asc"
    cursor = conexao.cursor()
    cursor.execute(sql_select_Query)
    produtos = cursor.fetchall()

    for row in produtos:

        preco_venda = row[3] / (1 - ((row[4] + row[5] + row[6] + row[7]) / (100)))

        # um porcento

        # cálculo receita bruta
        receita_bruta = preco_venda - row[3]

        # cálculo de lucro
        #mc = ((cf + cv + iv + ml) / pv) - 100

        # valor sobre o preço final
        valor_imposto = (row[6] / 100) * preco_venda
        valor_comissao = (row[5] / 100) * preco_venda
        valor_custofixo = (row[4] / 100) * preco_venda

        # cálculo outros custos e rentabilidade
        oc = valor_imposto + valor_comissao + valor_custofixo
        rentabilidade = receita_bruta - oc


        #valores em porcentagem
        pct_pv=((preco_venda / preco_venda) * 100)
        pct_ca=((row[3] / preco_venda) * 100)
        pct_rb=((receita_bruta / preco_venda) * 100)
        pct_custofix=((valor_custofixo / preco_venda) * 100)
        pct_comissao=((valor_comissao / preco_venda) * 100)
        pct_imp=((valor_imposto / preco_venda) * 100)
        pct_oc=((oc / preco_venda) * 100)
        pct_rent=((rentabilidade / preco_venda) * 100)

        print("\nId:", row[0])
        print("Nome:", row[1])
        print("Descrição:", row[2])   
        #print("\n")
        from tabulate import tabulate #para importar usamos o terminal e colocamos o camando: pip install tabulate
        data = [[ 'A. Preço de Venda', f'{preco_venda:.2f}', f'{pct_pv:.0f}%'],
            ['B. Custo de Aquisição (Fornecedor)',  f'{row[3]:.2f}', f'{pct_ca:.0f}%'],
            ['C. Receita Bruta', f'{receita_bruta:.2f}', f'{pct_rb:.0f}%'],
            ['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{pct_custofix:.0f}%'],
            ['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{pct_comissao:.0f}%'],
            ['F. Impostos', f'{valor_imposto:.2f}', f'{pct_imp:.0f}%'],
            ['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{pct_oc:.0f}%'],
            ['H. Rentabilidade (C-G)', f'{rentabilidade:.2f}', f'{ pct_rent:.0f}%\n']]
        print (tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))
        if (pct_rent > 0):
            if (pct_rent <= 10):
                print("Lucro Baixo")
            if (pct_rent > 10 and pct_rent <= 20):
                print("Lucro médio")
            if (pct_rent > 20):
                print("Lucro Alto")

        else:
            if (pct_rent == 0):
                print("Equilíbrio")
            else:
                print("Prejuízo")
    menu()

def cadastrar_produto():
    print('\nEntrada de Dados')
    validacao = 0
    while True:
        cod_prod = int(input('Código do produto: '))
        # validacao
        validacao = "SELECT * FROM estoque WHERE cod_prod={0}".format(cod_prod)
        cursor.execute(validacao)
        resultado = cursor.fetchall()
        if resultado:
            print("Este produto já foi cadastrado.")
            
        else:
            break  

    nome = input('Nome do produto: ')
    descricao = input('Descrição do produto: ')
    ca = float(input('Custo do produto: '))
    cf = float(input('Custo fixo: '))
    cv = float(input('Comissão de vendas: '))
    iv = float(input('Impostos: '))
    ml = float(input('Rentabilidade: '))


    comando = f"""INSERT INTO ESTOQUE( cod_prod,nome,descrição,ca,cf,cv,iv,ml)
    VALUES
        ( {cod_prod}, '{nome}', '{descricao}',{ca},{cf}, {cv},{iv},{ml})"""

    cursor.execute(comando)
    conexao.commit() 
    print('Produto Cadastrado!')
    print("\n")
    '''from tabulate import tabulate #para importar usamos o terminal e colocamos o camando: pip install tabulate
    data = [[ 'A. Preço de Venda', f'{pv:.2f}', f'{pct_pv:.0f}%'],
    ['B. Custo de Aquisição (Fornecedor)',  f'{ca:.2f}', f'{pct_ca:.0f}%'],
    ['C. Receita Bruta', f'{rb:.2f}', f'{pct_rb:.0f}%'],
    ['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{pct_custofix:.0f}%'],
    ['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{pct_comissao:.0f}%'],
    ['F. Impostos', f'{valor_imposto:.2f}', f'{pct_imp:.0f}%'],
    ['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{pct_oc:.0f}%'],
    ['H. Rentabilidade (C-G)', f'{ml:.2f}', f'{pct_rent:.0f}%\n']]
    print (tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))

    if pct_rent > 20:
        print("Lucro Alto!!")
    elif pct_rent > 10 and pct_rent <= 20:
        print("Lucro médio!")
    elif pct_rent > 0 and pct_rent <=10:
        print("Lucro baixo...")
    elif pct_rent == 0:
        print("Equilíbro.")
    else: 
        print("Prejuízo....")'''
    menu()

def menu():

    print("\n-----MENU-----\n")
    print("DIGITE 1 PARA CADASTRAR UM PRODUTO")
    print("DIGITE 2 PARA VER SEUS PRODUTOS CADASTRADOS")
    print("DIGITE 3 PARA SAIR")
    numero_digitado=int(input(" "))
    if(numero_digitado==1):
        cadastrar_produto()
    if(numero_digitado==2):
        mostrar_produtos()
    if(numero_digitado==3):
        sys.exit()
    else:
        print("Essa opção não existe")
        menu()

menu()
