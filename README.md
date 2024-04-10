# Portfólio BI 
Portfólio de projetos de BI, criados com o objetivo de estudo e aprendizado. 

## Dashboard vendas com PowerBI
Aqui construí um dashboard de vendas para analisar os principais insights que podem ser gerados com os dados da planilha de vendas utilizada (Link: https://www.hashtagtreinamentos.com/modelos-power-bi / Planilha "Vendas" anexada).

Você pode conferir o pbix, juntamente com a planilha utilizada, aqui: [dashboard_vendas](https://github.com/Caiquesgoulart/portfolio-bi/tree/main/dashboard_vendas)

### Visual e dados
- Aqui optei por um visual simples com cores destacando as marcas, KPIs com os principais insights sumarizados (como não existem dados de metas na planilha o KPI funciona apenas como exemplo visual). 
- Contei com a inserção de filtros para diversificar as análises realizadas, trazendo mais praticidade para o relatório. 
- Também temos visuais mostrando o faturamento líquido e quantidade vendida tanto por marca quanto por tipo de produto, assim oferecendo respostas rápidas para as principais dúvidas. 
- Mais abaixo temos um gráfico de linhas que nos apresenta o faturamento líquido por mês para cada um dos anos presentes nos dados da planilha, essa visão é especialmente interessante pois nos permite, de prontidão, comparar um ano com o outro. 

![image](https://github.com/Caiquesgoulart/portfolio-bi/assets/70335792/38bdb351-d1ff-4cce-982b-07cbdb1ca805)

### Observações 
- Os visuais aqui seguem o contexto dos dados contidos na planilha, sendo assim, algumas análises são específicas para esses contextos, por exemplo:
  - O gráfico de pizza utilizado funciona bem pois temos apenas três marcas, o que deixa visualmente atrativo e de fácil visualização.
  - O gráfico de linhas também funciona bem pois temos apenas dois anos para analisar.
 

## Projeto ETL de compras + Dashboard no Looker
Esse é um projeto para estudar ETLs com Python, alguns desafios desse projeto.

- Carregar uma planilha com quatro abas para o BigQuery
- Iterar com todas as aba para subir cada uma para sua respectiva tabela no BigQuery
- Aprender a trabalhar com Python + BigQuery, integrar os dois
- Desenvolver habilidades com o Looker Studio
- Fazer conexão do BigQuery com o Looker

### O código: 
O código completo pode ser encontrado pelo link: [main.py](https://github.com/Caiquesgoulart/portfolio-bi/blob/main/etl_compras/main.py) na pasta "etl_compras". O código possuí comentários explicando todos os passos que realizei. 

### O dashboard: 

#### Clique para seguir o link para o dashboard, você pode testar os filtros e outras funcionalidades por lá.
[![Dashboard](https://github.com/Caiquesgoulart/portfolio-bi/assets/70335792/1f220a93-00da-4952-9822-ca04ee5b1e18)
)](https://lookerstudio.google.com/s/iclcIvS9is4)


Esse dashboard visa apresentar insights sobre as vendas de uma empresa X, dentre os principais insight temos: 
- Cards:
  - Qtde de pedidos: apresenta a quantidade total de pedidos realizados.
  - Qtde pedidos atrasados: apresenta o total de pedidos entregues com atraso.
  - Qtde pedidos no prazo: apresenta o total de pedidos entregues no prazo.
  - % pedidos atrasados: visa mostrar o quão bem ou mal estão as entregas, aqui existe uma regra para, caso o valor for menor que 30% as cores ficam verdes indicando que está dentro do limite aceitável de pedidos atrasados, caso fique maior que 30% as cores ficam vermelhas.
 
- Gráficos:
    - % de pedidos por fornecedor: mostra os fornecedores com mais pedidos de forma percentual.
    - Qtde de pedidos por comprados: mostra os compradores com mais pedidos.
    - Materias primas mais vendidas
    - Crescimento das vendas mês a mês: mostra uma visão que apresenta o crescimentos das vendas a cada ano e a cada mês.
    - Detalhamento dos pedidos : uma visão mais detalhada dos pedidos para outros tipos de análises.






