# 📦 ARQUIVO DE CONTEXTO DO PROJETO

## 1. Visão Geral do Projeto

* Nome: Alerta INEP-Revalida
* Descrição: Sistema de monitoramento automático de portais governamentais e instituições associadas para detectar e notificar novos documentos e notícias sobre o processo Revalida.
* Objetivo principal: Capturar novos editais, portarias, retificações e notícias do processo Revalida e notificar os interessados via Microsoft Teams, sem custos operacionais de servidor.
* Status atual: Em produção (Implementado com fontes do INEP e ABMES).

## 2. Contexto de Negócio / Produto

* Problema que resolve: Acompanhamento manual exaustivo e risco de perda de prazos de novos editais ou retificações relacionadas ao Revalida.
* Público-alvo: Equipe educacional/administrativa que acompanha o Revalida.
* Proposta de valor: Entrega imediata de alertas estruturados via Teams, eliminando ruídos e focando apenas em conteúdo novo e relevante, utilizando automação serverless com zero custo.

## 3. Stack Técnica

* Linguagens: Python 3
* Frameworks: N/A (Scripts nativos)
* Bibliotecas: `requests`, `beautifulsoup4`
* Infraestrutura: GitHub Actions (Cron Scheduler) e Repositório Privado no GitHub
* APIs/Serviços externos: Webhook do Microsoft Teams (via Power Automate)

## 4. Arquitetura

* Desenho geral: Uma pipeline rodando no GitHub Actions aciona periodicamente scripts de web scraping em Python. Os scripts comparam os itens obtidos com um estado armazenado localmente. Itens novos são formatados em "Adaptive Cards" e enviados via requisição HTTP para o webhook do Teams. O estado é então atualizado e salvo no repositório.
* Padrões utilizados: Scrapers separados por fonte, Card Builders modulares e estado persistido em arquivo JSON.
* Decisões importantes: Uso de GitHub Actions para viabilizar execução gratuita. Eliminação do uso inicial planejado de Inteligência Artificial (Gemini) em favor de scraping direto de sub-páginas específicas que já são filtradas nativamente.
* Fluxo de dados (passo a passo):
  1. GitHub Actions dispara a rotina (`monitor.yml`).
  2. Executa os scrapers sequencialmente (Editais INEP, Notícias INEP, Editais ABMES).
  3. Compara os resultados encontrados no web scraping com `data/last_seen.json`.
  4. Formata o card e dispara via HTTP/POST ao webhook do Teams para novidades.
  5. Salva novo estado consolidado no arquivo `last_seen.json`.
  6. Realiza o commit e push do novo JSON de volta ao GitHub Actions (para a próxima execução).

## 5. Código & Estrutura

* Estrutura do projeto:
  * `.github/workflows/`: Contém `monitor.yml` com as regras de agendamento.
  * `data/`: Contém `last_seen.json` (banco de dados/estado leve).
  * `src/`: Core da aplicação.
    * `scraper_editais.py`, `scraper_noticias.py`, `scraper_abmes.py`: Scripts de extração de dados.
    * `notifier.py`: Lida com envio dos pacotes (Adaptive Cards) via requisições ao Webhook do Teams.
    * `cards/`: Diretório modular com arquivos de formatação visual (`card_edital.py`, `card_noticia.py`, `card_abmes.py`).
* Principais módulos/componentes: Scrapers (extratores HTML) e geradores de Adaptive Cards (formatadores visuais JSON).
* Convenções de nomenclatura: `snake_case` (padrão Python), modularização por tipo de responsabilidade.
* Padrões de código: Scripts focados na manipulação robusta de dados em HTML estático (BeautifulSoup), sem bibliotecas desnecessárias.

## 6. Funcionalidades

### ✅ Concluídas

* [Monitoramento INEP Editais] - Scraping da URL de conteúdos de legislação `/revalida/2026`.
* [Monitoramento INEP Notícias] - Scraping da central focada em notícias do Revalida.
* [Monitoramento ABMES] - Busca de "EDITAL INEP" na ABMES, extraindo o resumo/texto descritivo das atualizações e retificações.
* [Integração Microsoft Teams] - Envio contínuo e responsivo via Adaptive Cards para o Webhook configurado.
* [Persistência de Estado] - Arquivo `last_seen.json` que registra as últimas ocorrências e previne disparos duplicados.
* [Automação de Agendamento] - Cron job configurado para rodar a cada 30min (Seg a Sex, 07:00 às 18:30 BRT) e uma vez aos fins de semana.

### 🚧 Em andamento

* (Nenhuma feature crítica em andamento)

### 📌 Planejadas

* (Nenhuma funcionalidade especificamente listada pendente)

## 7. Registro de Decisões (CRÍTICO)

* Decisão: Remoção da filtragem por IA (Gemini) no scraper de notícias do INEP.
  * Contexto: O plano inicial era consumir a API do Gemini para ler cards misturados no site principal do governo.
  * Escolha feita: Utilizar uma URL secundária específica (`/noticias/revalida`) que filtra a origem automaticamente.
  * Motivo: Elimina custos com API de LLM e torna o scraper 100% determinístico e rápido.

* Decisão: Correção de URL (Target específico para o ano do Revalida).
  * Contexto: O HTML da página padrão do INEP carregava a lista de editais via requisições assíncronas (AJAX), ocultando os dados do BeautifulSoup.
  * Escolha feita: Apontar diretamente para a subpágina server-rendered (`/revalida/2026`).
  * Motivo: Estabilidade e simplicidade na captura dos dados via pacote genérico (`requests`), fugindo de scrapers pesados em headless (como Playwright).

* Decisão: Ajustes e simplificação no formato do Adaptive Card de Editais.
  * Contexto: O Teams descartava silenciosamente os cartões gerados pelos alertas iniciais.
  * Escolha feita: Remoção do atributo `backgroundImage` configurado erroneamente como vazio.
  * Motivo: Webhooks do Teams recusam payloads ligeiramente mal formatados (como URLs de imagens vazias) sem retornar logs de erro na API.

* Decisão: Scraping sequencial na página da ABMES validado pelo JSON (`last_seen.json`).
  * Contexto: Necessidade de alertar no caso de editais ou retificações ocorrerem várias vezes num mesmo dia.
  * Escolha feita: Comparar todo o pacote extraído de volta com o banco JSON (e não puramente com a data do dia).
  * Motivo: Garante alertas paralelos no mesmo dia individualizados e sem repetições caso o workflow rode inúmeras vezes.

* Decisão: Cron executado a cada 30 minutos em dias úteis.
  * Contexto: A necessidade de rapidez contrapunha-se à cota free do GitHub (2.000 minutos/mês).
  * Escolha feita: Rodar de 30 em 30 min durante horários comerciais estratégicos.
  * Motivo: O consumo estimado (~500 mins/mês) acomoda agilidade, não gera bloqueios por excesso de taxa no portal do Governo, e respeita folgadamente os limites gratuitos do Actions.

## 8. Restrições e Regras

* Restrições técnicas: Scripts focados em HTML estático (`requests` + `BeautifulSoup`); dependência do tempo limite gratuito do GitHub Actions; formatação estrita dos Adaptive Cards do Teams.
* Restrições de negócio: Processamento restrito apenas à informações de Revalidação do INEP.
* Requisitos de performance/segurança: Webhook injetado seguramente pelo GitHub Secrets (`TEAMS_WEBHOOK_URL`). Os artefatos do repositório devem ser limpos (`.gitignore` para logs e `__pycache__`).

## 9. Problemas Conhecidos / Limitações

* [Dependência da Estrutura HTML/DOM Governista] - A coleta irá quebrar instantaneamente se as classes ou ids das marcações alvo (ex.: `#content-core` ou `.conteudo`) do portal do Governo ou da ABMES sofrerem alterações de layout em alguma atualização de design.

## 10. Próximos Passos (PRIORIZADO)

1. [Manutenção de Ano-Base (Suposição)] Atualizar a URL fixa dos editais no scraper para referenciar `/revalida/2027` quando ocorrer a virada ou quando a página oficial for migrada.
2. [Teste Periódico] Acompanhar rejeições silenciosas no Teams (Microsoft constantemente atualiza schemas de webhooks e templates).

## 11. Dúvidas em Aberto

* O sistema passará a ser acionado em múltiplos instantes em anos subsequentes? Deverá ser automatizada a identificação de abas de anos correntes e migração progressiva da URL do Revalida?

## 12. Como Continuar Este Projeto

* Em que focar: Caso seja necessário adicionar novas entidades governamentais/associadas, continuar a padronização e abstração (`scraper_*.py` interligado ao construtor da visualização `card_*.py`), atrelando as novas lógicas comparando sempre contra o `last_seen.json`.
* O que evitar:
  * Evitar incorporar scraping baseado em inteligência artificial (LLM) a menos que as páginas não apresentem segmentação base, para preservar rapidez e custo nulo.
  * Evitar chaves mal formuladas e nulas nos metadados enviados no Adaptive Card (causa silenciamento e rejeição na pipeline do Teams).
* Contexto crítico que deve ser respeitado: É fundamental preservar o bloco do GitHub Actions responsável por realizar o `git push` atualizando o estado do arquivo local (`last_seen.json`) após a validação de webhooks no Teams, prevenindo looping reincidente dos mesmos alertas a cada meia hora.

## 13. Resumo Rápido (TL;DR)

* Aplicação Serverless de notificações ativas sobre editais e notícias do Exame Revalida do INEP.
* Tecnologias principais: Python (Web Scraping puro), GitHub Actions, Microsoft Teams Adaptive Cards.
* Totalmente isento de custos de hospedagem/operação (aproveita Action runners e extração determinística).
* Vigia três fontes de dados separadas: Legislação Revalida INEP, Notícias Revalida INEP e atualizações indexadas na ABMES.
* Arquitetura em jobs cíclicos de 30 minutos em dias úteis (07:00 às 18:30 BRT), gravando rastros de envio no repositório.
* Preparado contra alertas duplos (estado salvo em JSON local) e suporta detecção contínua de publicações no mesmo dia (como retificações frequentes).
