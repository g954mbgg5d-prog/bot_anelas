# BOT_ANELAS

BOT_ANELAS é um bot desenvolvido em Python que gera e publica tweets automaticamente no X.

O conteúdo é construído proceduralmente a partir de dados armazenados em uma planilha do Google Sheets. Os tweets são gerados por meio de templates, publicados utilizando a API oficial do X e armazenados em um banco SQLite.

A versão 2.0 do projeto introduz uma nova arquitetura de geração sob demanda, sistema persistente de cooldown por categoria, scheduler com curva exponencial de publicação e uma suíte de ferramentas para validação e testes.

---

# Arquitetura

O fluxo principal do BOT_ANELAS é:

```text
Google Sheets
      ↓
    sheets.py
      ↓
   generator.py
      ↓
selection_manager.py
      ↓
 queue_manager.py
      ↓
    SQLite
      ↓
  scheduler.py
      ↓
  publisher.py
      ↓
   API do X
```

O bot roda continuamente em uma VPS Ubuntu através do `systemd`.

---

# Tecnologias

O projeto utiliza:

- Python 3.12
- SQLite
- Pandas
- Tweepy
- Google Sheets
- python-dotenv
- systemd

---

# Estrutura do projeto

```text
bot_anelas/
│
├── data/
│   └── tweets.db
│
├── logs/
│   └── bot.log
│
├── tools/
│   ├── analyze_distribution.py
│   ├── content_check.py
│   ├── diagnostics.py
│   ├── pre_release_check.py
│   ├── stress_test.py
│   └── validate_templates.py
│
├── config.py
├── database.py
├── generator.py
├── main.py
├── manual_post.py
├── publisher.py
├── queue_manager.py
├── scheduler.py
├── selection_manager.py
├── sheets.py
├── requirements.txt
└── README.md
```

---

# Funcionamento

## 1. Google Sheets

O conteúdo utilizado pelo bot fica armazenado em diferentes abas de uma planilha do Google Sheets.

Atualmente são utilizadas as seguintes abas:

```text
substantivos
adjetivos
verbos
frases
chamada
templates
lugares
coisas
comidas
```

Cada aba possui um GID configurado no arquivo:

```text
config.py
```

As planilhas são carregadas através do módulo:

```text
sheets.py
```

Os dados ficam armazenados em cache na memória.

A sincronização ocorre automaticamente em intervalos definidos através de:

```python
SHEETS_SYNC_INTERVAL_MINUTES
```

O cache somente é substituído quando todas as abas são carregadas com sucesso.

Isso evita que uma falha temporária durante a sincronização deixe o bot com dados incompletos.

---

# Generator

O módulo:

```text
generator.py
```

é responsável pela construção dos tweets.

O generator:

1. seleciona um template;
2. identifica os placeholders utilizados;
3. seleciona apenas os dados necessários;
4. substitui os placeholders;
5. normaliza o texto;
6. retorna o tweet e o `SelectionManager`.

Diferentemente da arquitetura anterior, o generator não sorteia dados que não serão utilizados pelo template.

Por exemplo, se um template utiliza:

```text
{substantivo}
{substantivo2}
{presente}
```

somente esses elementos serão selecionados.

Isso reduz processamento desnecessário e torna o sistema de cooldown mais preciso.

---

# Templates

Os templates ficam armazenados na aba:

```text
templates
```

Exemplo:

```text
na moral? ninguém tem coragem de falar, mas {substantivo} é mesmo de {infinitivo}
```

O generator utiliza:

```python
str.format()
```

para realizar as substituições.

Templates inválidos são automaticamente ignorados.

O generator tenta selecionar outro template até atingir o limite máximo de tentativas configurado internamente.

Isso impede que um único template inválido interrompa o ciclo principal do bot.

---

# Placeholders

## Substantivos

A aba `substantivos` contém informações relacionadas à mesma palavra.

Exemplo conceitual:

```text
palavra
artigo
de
em
```

Placeholders disponíveis:

```text
{substantivo}
{artigo}
{de}
{em}
```

Também são suportadas versões numeradas:

```text
{substantivo2}
{substantivo3}
{substantivo4}
{substantivo5}
```

O mesmo vale para os demais campos:

```text
{artigo2}
{de2}
{em2}
```

Todos os valores pertencentes ao mesmo grupo são obtidos da mesma linha da planilha.

---

## Adjetivos

Placeholders:

```text
{adjetivo}
```

e versões numeradas:

```text
{adjetivo2}
{adjetivo3}
{adjetivo4}
{adjetivo5}
```

---

## Verbos

A aba `verbos` suporta:

```text
{infinitivo}
{presente}
{passado}
{gerundio}
```

Também são suportadas versões numeradas até 5.

Exemplo:

```text
{infinitivo2}
{presente3}
{passado4}
{gerundio5}
```

---

## Frases

Placeholder:

```text
{frase}
```

Com versões numeradas até 5.

---

## Chamadas

Placeholder:

```text
{chamada}
```

Com versões numeradas até 5.

---

## Lugares

A aba `lugares` possui:

```text
lugar
de_lugar
em_lugar
pra_lugar
```

Placeholders:

```text
{lugar}
{de_lugar}
{em_lugar}
{pra_lugar}
```

Exemplo conceitual:

```text
Rio de Janeiro
do Rio de Janeiro
no Rio de Janeiro
pro Rio de Janeiro
```

Todos os valores são obtidos da mesma linha.

Também são suportadas versões numeradas até 5.

---

## Coisas

A aba `coisas` possui:

```text
coisa
artigo_coisa
um_coisa
```

Placeholders:

```text
{coisa}
{artigo_coisa}
{um_coisa}
```

Também são suportadas versões numeradas até 5.

---

## Comidas

A aba `comidas` possui:

```text
comida
um_comida
```

Placeholders:

```text
{comida}
{um_comida}
```

Também são suportadas versões numeradas até 5.

---

# SelectionManager

O módulo:

```text
selection_manager.py
```

centraliza a seleção dos elementos utilizados na geração.

Suas principais responsabilidades são:

- selecionar linhas aleatórias;
- respeitar os cooldowns configurados;
- manter consistência entre os valores da mesma linha;
- sanitizar valores importados das planilhas;
- registrar os índices utilizados na geração.

A sanitização impede que valores vazios do Pandas sejam transformados em texto.

Valores como:

```text
NaN
None
```

são convertidos para strings vazias quando necessário.

Isso permite que campos opcionais, como artigos, permaneçam vazios sem gerar textos contendo `nan`.

---

# Sistema de cooldown

A versão 2.0 introduziu um sistema persistente de cooldown.

O objetivo é impedir que os mesmos elementos sejam reutilizados com muita frequência.

Os cooldowns são configurados no:

```text
config.py
```

Exemplo:

```python
COOLDOWNS = {
    "templates": 30,
    "substantivos": 30,
    "adjetivos": 15,
    "verbos": 15,
    "frases": 10,
    "chamada": 5,
    "lugares": 8,
    "coisas": 5,
    "comidas": 7,
}
```

O cooldown funciona por elementos utilizados, e não necessariamente por tweets publicados.

Por exemplo, se um único tweet utilizar:

```text
{substantivo}
{substantivo2}
{substantivo3}
```

três índices da categoria `substantivos` serão registrados.

Os dados são persistidos no SQLite, portanto o histórico de cooldown não é perdido quando:

- o bot reinicia;
- a VPS reinicia;
- o serviço é reiniciado.

---

# Banco de dados

O projeto utiliza SQLite.

O banco fica armazenado em:

```text
data/tweets.db
```

---

## Tabela tweets

Armazena os tweets gerados e publicados.

Campos:

```text
id
texto
hash
status
criado_em
publicado_em
```

O hash é gerado utilizando SHA256.

A coluna possui restrição de unicidade, impedindo a inserção de tweets duplicados.

---

## Tabela metadata

Armazena informações internas do bot no formato chave/valor.

Campos:

```text
chave
valor
```

---

## Tabela recent_items

Armazena os elementos utilizados recentemente pelo sistema de cooldown.

Campos:

```text
id
categoria
indice
usado_em
```

Essa tabela permite que o `SelectionManager` descubra quais elementos devem permanecer temporariamente bloqueados.

---

# Geração sob demanda

A arquitetura anterior mantinha uma fila de tweets pendentes.

Essa fila foi removida na versão 2.0.

Agora o fluxo funciona da seguinte forma:

```text
Scheduler decide publicar
        ↓
Tweet é gerado
        ↓
Hash é verificado
        ↓
Tweet é publicado
        ↓
Tweet é salvo no banco
        ↓
Cooldowns são registrados
```

Isso evita:

- geração antecipada de conteúdo;
- manutenção desnecessária de uma fila;
- tweets antigos aguardando publicação;
- processamento de elementos que podem nunca ser utilizados.

---

# Queue Manager

Apesar do nome histórico, o módulo:

```text
queue_manager.py
```

não mantém mais uma fila.

Atualmente ele é responsável por:

- solicitar a geração de um novo tweet;
- verificar se o tweet já existe no banco;
- tentar novamente em caso de duplicação;
- salvar tweets publicados.

O generator pode realizar múltiplas tentativas para encontrar um tweet inédito antes de retornar um erro.

---

# Scheduler

O módulo:

```text
scheduler.py
```

controla quando o bot deve publicar.

A estratégia atual utiliza uma curva de crescimento exponencial.

## Regras

```text
0–59 minutos
0% de chance
```

A partir de 60 minutos, a probabilidade começa a crescer.

```text
60 minutos
0%
```

Entre 60 e 120 minutos:

```text
crescimento exponencial da probabilidade
```

Em:

```text
120 minutos
100%
```

a publicação é garantida.

Exemplo aproximado da curva:

```text
0 min      0%
30 min     0%
59 min     0%
60 min     0%
70 min     3%
80 min    11%
90 min    25%
100 min   44%
110 min   69%
120 min  100%
```

O loop principal é executado em intervalos definidos por:

```python
LOOP_INTERVAL_SECONDS
```

---

# Publicação

A publicação é realizada pelo módulo:

```text
publisher.py
```

O projeto utiliza:

- Tweepy;
- API oficial do X;
- OAuth 1.0a.

O cliente do Tweepy é criado uma única vez durante a inicialização do módulo.

A função de publicação retorna sucesso ou falha para o fluxo principal.

Os cooldowns somente são registrados depois que a publicação ocorre com sucesso.

---

# Variáveis de ambiente

As credenciais da API do X devem ficar armazenadas em um arquivo:

```text
.env
```

Exemplo:

```text
X_CONSUMER_KEY=
X_CONSUMER_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
```

O arquivo `.env` não deve ser enviado ao GitHub.

Certifique-se de adicioná-lo ao:

```text
.gitignore
```

---

# Execução manual

Para gerar e publicar imediatamente um tweet:

```bash
python manual_post.py
```

A publicação manual ignora o scheduler.

O fluxo é:

```text
Sincronizar planilhas
        ↓
Gerar tweet
        ↓
Publicar no X
```

Esse script é útil para:

- testes;
- publicações manuais;
- validação da API.

---

# Execução do bot

Para executar diretamente:

```bash
python main.py
```

Em produção, o projeto utiliza `systemd`.

---

# systemd

O serviço utilizado é:

```text
bot-anelas.service
```

## Iniciar

```bash
sudo systemctl start bot-anelas
```

## Parar

```bash
sudo systemctl stop bot-anelas
```

## Reiniciar

```bash
sudo systemctl restart bot-anelas
```

## Verificar status

```bash
sudo systemctl status bot-anelas
```

## Acompanhar logs

```bash
journalctl -u bot-anelas -f
```

Também é possível acompanhar o arquivo de log:

```bash
tail -f logs/bot.log
```

O serviço:

- inicia automaticamente após reboot;
- reinicia em caso de falha;
- mantém o bot rodando continuamente.

---

# Ferramentas de desenvolvimento

A pasta:

```text
tools/
```

contém utilitários para testes, validação e diagnóstico.

---

## validate_templates.py

Executa múltiplas gerações para verificar se existem erros fatais relacionados aos templates.

Executar:

```bash
python tools/validate_templates.py
```

---

## content_check.py

Realiza uma análise automática da qualidade do conteúdo gerado.

Atualmente verifica:

- ocorrência de `nan`;
- ocorrência de `None`;
- placeholders não substituídos;
- tweets vazios;
- tweets maiores que 280 caracteres;
- espaços duplos;
- quebras de linha;
- tabulações;
- espaços no início;
- espaços no final.

Executar:

```bash
python tools/content_check.py
```

---

## stress_test.py

Executa milhares de gerações para validar estabilidade e desempenho.

O relatório inclui:

- total de tweets gerados;
- tempo total;
- tempo médio de geração.

Executar:

```bash
python tools/stress_test.py
```

---

## analyze_distribution.py

Analisa estatisticamente a geração de conteúdo.

O relatório inclui:

- tweets gerados;
- tweets únicos;
- colisões;
- utilização por categoria;
- templates mais utilizados;
- templates menos utilizados;
- desempenho da geração.

Executar:

```bash
python tools/analyze_distribution.py
```

---

## diagnostics.py

Exibe informações gerais sobre a saúde do bot.

O relatório inclui dados como:

- planilhas carregadas;
- última publicação;
- chance atual do scheduler;
- quantidade de tweets;
- estado dos cooldowns.

Executar:

```bash
python tools/diagnostics.py
```

---

## pre_release_check.py

Executa automaticamente a suíte de testes antes de um novo release.

Atualmente executa:

```text
validate_templates.py
        ↓
content_check.py
        ↓
stress_test.py
        ↓
analyze_distribution.py
```

Executar:

```bash
python tools/pre_release_check.py
```

Se todos os testes forem aprovados:

```text
BOT APROVADO PARA RELEASE
```

Esse comando deve ser executado antes de alterações importantes serem enviadas para produção.

---

# Fluxo de desenvolvimento recomendado

Antes de iniciar alterações:

```bash
git checkout main
git pull origin main
```

Criar uma nova branch:

```bash
git checkout -b feature/nome-da-feature
```

Realizar as alterações.

Executar a suíte de testes:

```bash
python tools/pre_release_check.py
```

Verificar as alterações:

```bash
git status
git diff
```

Adicionar os arquivos:

```bash
git add .
```

Criar o commit:

```bash
git commit -m "Descrição da alteração"
```

Enviar a branch:

```bash
git push -u origin feature/nome-da-feature
```

Depois:

1. abrir Pull Request;
2. realizar code review;
3. realizar merge na `main`;
4. atualizar a VPS;
5. reiniciar o serviço;
6. acompanhar os logs.

---

# Deploy

Após o merge de uma alteração na `main`:

```bash
git checkout main
git pull origin main
```

Ativar o ambiente virtual, caso necessário:

```bash
source venv/bin/activate
```

Atualizar dependências:

```bash
pip install -r requirements.txt
```

Executar os testes:

```bash
python tools/pre_release_check.py
```

Reiniciar o bot:

```bash
sudo systemctl restart bot-anelas
```

Verificar o status:

```bash
sudo systemctl status bot-anelas
```

Acompanhar os logs:

```bash
journalctl -u bot-anelas -f
```

---

# Testes realizados na versão 2.0

Durante o desenvolvimento da V2 foram realizados:

- testes de geração em massa;
- milhares de tweets gerados sem exceções fatais;
- validação automática de templates;
- validação automática de conteúdo;
- análise de distribuição;
- testes de desempenho;
- testes do scheduler;
- testes de persistência dos cooldowns;
- testes de prevenção de tweets duplicados;
- testes de sincronização das planilhas;
- publicação manual;
- publicação automática;
- publicação utilizando a API oficial do X;
- testes de reinicialização do serviço;
- testes de reboot da VPS.

---

# Histórico de versões

## V1

Primeira versão estável do BOT_ANELAS.

Principais características:

- geração procedural de tweets;
- Google Sheets;
- SQLite;
- publicação automática;
- VPS;
- systemd;
- API oficial do X.

---

## V2.0.0

Grande refatoração da arquitetura.

Principais alterações:

- remoção da fila de tweets;
- geração sob demanda;
- novo generator;
- criação do SelectionManager;
- sistema persistente de cooldown;
- cooldown configurável por categoria;
- geração apenas dos placeholders necessários;
- nova curva exponencial do scheduler;
- tratamento correto de valores NaN;
- melhorias na sanitização dos dados;
- ferramentas de desenvolvimento;
- testes de conteúdo;
- testes de distribuição;
- stress tests;
- diagnósticos;
- suíte automática de pre-release.

---

# Roadmap

Possíveis melhorias futuras:

## V2.x

- melhorias de observabilidade;
- estatísticas de uso;
- relatórios de saúde;
- detecção de templates não utilizados;
- detecção de palavras não utilizadas;
- melhorias nos logs;
- novas categorias de conteúdo;
- novas ferramentas de diagnóstico.

## V3

Possíveis evoluções:

- post-release check;
- métricas avançadas;
- análise de engajamento;
- otimização baseada em desempenho;
- novas formas de geração;
- novas capacidades de publicação.

---

# Objetivo do projeto

O objetivo do BOT_ANELAS é explorar geração procedural de conteúdo através de uma arquitetura simples, configurável e extensível.

A utilização de Google Sheets permite que o conteúdo seja atualizado sem alterações no código.

O sistema de templates permite criar novas estruturas de tweets rapidamente.

O sistema de cooldown reduz repetições.

A persistência em SQLite mantém o histórico do bot.

A suíte de testes permite evoluir o projeto com maior segurança.

A arquitetura da V2 foi projetada para manter o bot simples o suficiente para rodar continuamente em uma VPS, mas organizado o suficiente para permitir novas evoluções no futuro.