# Portfólio de Dados: Health Analytics – Gestão de Custos e Perfil da Carteira

**Autor:** Adriano Parente Machado  
**Área de Atuação:** Análise de Dados e Business Intelligence  

## 1. Visão Geral do Projeto
Este projeto apresenta uma solução analítica de ponta a ponta voltada para o setor de saúde suplementar e recursos humanos. O objetivo principal foi diagnosticar os direcionadores de custo (sinistralidade) de uma carteira de plano de saúde corporativo e entregar uma ferramenta tática para a tomada de decisão gerencial. A solução foi dividida em duas fases: a exploração estatística em Python e a construção de um painel executivo interativo no Power BI.

## 2. Conjunto de Dados e Qualidade
* **Fonte dos Dados:** Este conjunto de dados foi originalmente disponibilizado pela plataforma educacional **Preditiva** para fins de estudo e desenvolvimento de portfólio.
* **Volume:** 1.337 registros de colaboradores.
* **Integridade:** Base de dados consistente, sem valores ausentes (missing values). Um registro duplicado foi identificado e tratado durante a etapa de limpeza.
* **Variáveis Analisadas:** Idade, Sexo, Índice de Massa Corporal (IMC), Quantidade de Filhos, Status de Tabagismo, Região e Custo de Saúde (Variável-alvo).

## 3. Stack Tecnológico e Ferramentas
* **Python:** Utilizado para manipulação de dados e Análise Exploratória (EDA). Bibliotecas: Pandas, Matplotlib e Seaborn.
* **Power BI:** Utilizado para a camada de visualização e Business Intelligence.
* **Linguagem DAX:** Modelagem de métricas de negócio e indicadores de performance (KPIs).
* **Design:** Desenvolvimento de interface com UX focado em *Dark Theme* corporativo para destaque de dados críticos.

## 4. Principais Descobertas (Insights de Negócio)
A etapa de exploração estatística revelou comportamentos vitais para a gestão financeira da carteira:
* **A Ilusão da Média Financeira:** A média de gastos (1.327 reais) não reflete a realidade da maior parte da empresa, sendo distorcida por eventos médicos extremos (outliers). A métrica ideal adotada para o negócio foi a **Mediana** (938 reais).
* **O Peso do Tabagismo e da Obesidade:** O status de fumante demonstrou ser o maior fator de alavancagem de custos. Quando analisado em conjunto com as faixas de Obesidade (especialmente graus II e III), o custo mediano chega a quadruplicar em relação ao perfil de peso normal e não fumante.
* **Fatores de Baixo Impacto Isolado:** Variáveis como Região, Gênero Biológico e Número de Dependentes apresentaram baixa correlação direta com os picos de sinistralidade.

## 5. Arquitetura do Dashboard (Power BI)
<img width="1322" height="742" alt="image" src="https://github.com/user-attachments/assets/f767d6c9-9447-42ef-91d9-bff92d7e6482" />

O painel foi estruturado com foco em usabilidade executiva, seguindo o padrão de leitura em "Z":
1. **Menu de Contexto:** Filtros suspensos (Dropdown) para simulação de cenários segmentados por Região, Sexo e Dependentes.
2. **Indicadores-Chave (KPIs):** Cartões de leitura rápida apontando Volume de Vidas, Custo Mediano e Alertas Comportamentais (% Fumantes e % Obesidade).
3. **Detalhamento Causal:** Gráficos de contraste destacando o impacto financeiro do tabagismo e a progressão dos custos através das categorias do IMC.
4. **Matriz de Risco Combinado:** Um mapa de calor tático cruzando Tabagismo vs. IMC, formatado condicionalmente para evidenciar imediatamente o quadrante de maior sangramento financeiro da carteira.

## 6. Próximos Passos (Evolução do Produto)
A próxima iteração deste projeto envolverá a modelagem preditiva utilizando **Machine Learning (Regressão Linear Múltipla)** em Python. O objetivo será criar um algoritmo capaz de prever o custo exato em reais de um novo colaborador com base no seu perfil demográfico e clínico, permitindo provisionamentos orçamentários mais precisos por parte da área de Recursos Humanos.
