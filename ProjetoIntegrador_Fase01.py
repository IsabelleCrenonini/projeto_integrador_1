#entrada de dados
print('Entrada de Dados')
cp = int(input('Código do produto: '))
nome = input('Nome do produto: ')
descricao = input('Descrição do produto: ')
ca = float(input('Custo do produto: '))
cf = float(input('Custo fixo: '))
cv = float(input('Comissão de vendas: '))
iv = float(input('Impostos: '))
ml = float(input('Rentabilidade: '))


#cálculo preço de venda
pv = ca/(1-((cf+cv+iv+ml)/(100)))

#um porcento

#cálculo receita bruta
rb = pv-ca

#cálculo de lucro
mc = ((cf+cv+iv+ml)/pv)-100

#valor sobre o preço final
valor_imposto=(iv/100)*pv
valor_comissao=(cv/100)*pv
valor_custofixo=(cf/100)*pv

#cálculo outros custos e rentabilidade
oc = valor_imposto+valor_comissao+valor_custofixo
rentabilidade=rb-oc
rentabilidadePorcem= (rentabilidade/pv)*100



#saída
from tabulate import tabulate #para importar usamos o terminal e colocamos o comando: pip install tabulate
data = [[ 'A. Preço de Venda', f'{pv:.2f}', f'{((pv/pv)*100):.0f}%'],
['B. Custo de Aquisição (Fornecedor)',  f'{ca:.2f}', f'{((ca/pv)*100):.0f}%'],
['C. Receita Bruta', f'{rb:.2f}', f'{((rb/pv)*100):.0f}%'],
['D. Custo Fixo/Administrativo', f'{valor_custofixo:.2f}', f'{((valor_custofixo/pv)*100):.0f}%'],
['E. Comissão de Vendas', f'{valor_comissao:.2f}', f'{((valor_comissao/pv)*100):.0f}%'],
['F. Impostos', f'{valor_imposto:.2f}', f'{((valor_imposto/pv)*100):.0f}%'],
['G. Outros Custos (D+E+F)', f'{oc:.2f}', f'{((oc/pv)*100):.0f}%'],
['H. Rentabilidade (C-G)', f'{rentabilidade:.2f}', f'{((rentabilidade/pv)*100):.0f}%\n']]
print (tabulate(data, headers=["Descrição", "Valor", "%"], floatfmt=".2f"))

#data = dados que vão aparecer na tabela, hearders = cabeçario

if(ml > 0):
    if(ml <= 10):
        print("Lucro Baixo")
    if(ml > 10 and ml <=20):
        print("Lucro médio")
    else:
        print("Lucro Alto")

else:
    if(ml == 0):
        print("Equilíbrio")
    else:
        print("Prejuízo")