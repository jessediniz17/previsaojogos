# ⚽ Previsão de Resultados de Jogos de Futebol

Possuo uma grande paixão por futebol, e decidi que fazer um projeto baseado nessa paixão poderia trazer grandes resultados.
Desenvolvi uma aplicação, **utilizando Python e Streamlit**, que **consome dados do SofaScore para analisar partidas recentes de alguns times de futebol** (todos os times que estavam no Brasileirão Série A de 2025, times da Copa do Brasil 2025 e Libertadores 2025).

O usuário escolhe os dois times que serão analisados e o número de jogos que será analisado. A aplicação **analisa as últimas partidas de cada time, considerando fator casa / fora, gerando um possível resultado para a partida.**

Os resultados, incluindo gols sofridos, gols feitos, partidas sem levar gols, etc. são **exibidos em gráficos detalhados**

O sistema também conta com um **serviço automatizado de notificações via WhatsApp**, que informa diariamente sobre jogos programados em campeonatos específicos.

---

## 🎯 Objetivo do Projeto

* Analisar o desempenho recente de times de futebol
* Gerar previsões simples de placar com base em médias históricas
* Exibir estatísticas avançadas de desempenho
* Visualizar dados de forma clara e interativa
* Enviar alertas automáticos de jogos do dia via WhatsApp


---

## 🧠 Funcionalidades Principais

### 🔮 Previsão de Resultados

* Seleção de **time mandante** e **time visitante**
* Definição da quantidade de jogos analisados (3 a 30)
* Cálculo de um **placar provável** com base em médias de gols pró e contra

### 📊 Análise de Jogos Anteriores

* Exibição dos últimos jogos de cada time
* Informações como:

  * Data
  * Adversário
  * Casa/Fora
  * Gols pró e contra
  * Resultado
  * Campeonato

### 📈 Estatísticas Avançadas

* Aproveitamento como mandante e visitante
* Diferença média de gols
* Percentual de jogos sem sofrer gols
* Percentual de jogos sem marcar gols

### 📉 Visualização de Dados

* Gráficos interativos utilizando **Altair**
* Visualizações claras e responsivas integradas ao Streamlit

### 📲 Notificações via WhatsApp

* Verificação automática de jogos do dia
* Filtro por campeonatos específicos
* Envio de mensagens via **Twilio WhatsApp API**

---

## 🛠️ Tecnologias Utilizadas

### 🐍 Python

Linguagem principal do projeto, responsável por toda a lógica de negócio, integração com APIs e processamento de dados.

Neste projeto, o uso de Python envolve as seguintes **bibliotecas e conceitos**:

* **requests**
  Utilizada para consumo de APIs REST, especificamente para buscar dados de partidas, times e campeonatos a partir da API do SofaScore.

* **pandas**
  Utilizada para manipulação e análise de dados estruturados, incluindo:

  * Criação e transformação de DataFrames
  * Cálculo de médias, percentuais e estatísticas
  * Preparação de dados para visualização

* **altair**
  Biblioteca de visualização declarativa utilizada para criar gráficos interativos e responsivos integrados ao Streamlit.

* **datetime**
  Utilizada para manipulação de datas e horários, conversão de timestamps e formatação de datas exibidas na interface.

* **pytz** e **zoneinfo**
  Utilizadas para tratamento correto de fuso horário (America/Sao_Paulo), garantindo consistência temporal nos dados.

* **os**
  Utilizada para acesso seguro a variáveis de ambiente, evitando a exposição de credenciais sensíveis no código.

* **twilio**
  SDK oficial da Twilio utilizado para integração com a API de envio de mensagens via WhatsApp.

Este conjunto de bibliotecas demonstra experiência prática com **integração de APIs, análise de dados, visualização, automação e boas práticas de segurança** em projetos Python.

---

### 🌐 Streamlit

Framework para criação de aplicações web de dados.

Utilizado para:

* Construção da interface do usuário
* Organização do layout em colunas
* Inputs interativos (selectbox, number_input)
* Exibição de tabelas, mensagens e gráficos

---

### 📡 SofaScore API (não oficial)

API utilizada para obter dados reais de partidas de futebol.

Fornece:

* Resultados de jogos anteriores
* Jogos programados do dia
* Informações de campeonatos, times e placares

---

### 📊 Pandas

Biblioteca fundamental para manipulação de dados.

Utilizada para:

* Estruturação dos dados em DataFrames
* Cálculo de médias, percentuais e estatísticas
* Preparação dos dados para visualização

---

### 📈 Altair

Biblioteca de visualização declarativa baseada em Vega-Lite.

Utilizada para:

* Criação de gráficos de barras
* Visualizações interativas
* Comparação de métricas estatísticas

---

### ☁️ Twilio API (WhatsApp)

Serviço utilizado para envio de mensagens via WhatsApp.

Funções:

* Envio automático de alertas de jogos do dia
* Integração segura via variáveis de ambiente

---

### 🔐 Variáveis de Ambiente (.env)

Utilizadas para proteger informações sensíveis, como:

* Tokens da Twilio
* Números de WhatsApp

---

## 📂 Estrutura do Projeto

```text
previsao-futebol/
├── resultados.py                # Aplicação principal Streamlit
├── .env                  # Variáveis de ambiente (não versionado)
├── .env.example          # Variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
└── requirements.txt      # Dependências do projeto
```

---

## ▶️ Como Executar o Projeto Localmente

1. Clone o repositório:

```bash
git clone https://github.com/jessediniz17/previsaojogos.git
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env`:

```env
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
TWILIO_FROM_WHATSAPP=whatsapp:+14155238886
TWILIO_TO_WHATSAPP=["whatsapp:+55XXXXXXXXX"]
```

5. Execute a aplicação:

```bash
streamlit run resultados.py
```

---

