# 🏛️ Alerta INEP - Revalida

Sistema de monitoramento automático do portal do INEP para detectar novos **editais**, **portarias** e **notícias** relacionados ao processo **Revalida** (Exame Nacional de Revalidação de Diplomas Médicos).

## Como funciona

O bot roda automaticamente via GitHub Actions e monitora duas fontes:

| Fonte | Estratégia | Card Teams |
|---|---|---|
| Página de Editais | Determinístico — qualquer novo link é alerta | 🏛️ Azul |
| Página Principal | Filtro por IA (Gemini) — só Revalida | 📰 Verde |

### Frequência de execução
- **Seg a Sex:** a cada hora, das 07h às 18h (horário de Brasília)
- **Sáb e Dom:** uma vez ao dia às 12h (horário de Brasília)

## Fontes monitoradas

- **Editais/Portarias:** https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida
- **Notícias:** https://www.gov.br/inep/pt-br

## Configuração

### 1. Secrets do GitHub (Settings → Secrets → Actions)

| Secret | Descrição |
|---|---|
| `TEAMS_WEBHOOK_URL` | URL do webhook do Microsoft Teams (Power Automate) |
| `GEMINI_API_KEY` | Chave da API do Google AI Studio (gratuita) |

### 2. Permissões do Actions

Em **Settings → Actions → General → Workflow permissions**: marcar **"Read and write permissions"**.

### 3. Configurar webhook no Teams

1. No Teams, abra o app **Workflows** (Fluxos de Trabalho)
2. Escolha o modelo *"Postar em um chat quando uma solicitação de webhook for recebida"*
3. **IMPORTANTE:** Altere o campo **"Postar como"** de `Flow bot` para `Usuário`
4. Selecione o chat/grupo de destino
5. No campo do Cartão Adaptável, use a expressão: `first(variables('Attachments'))?['content']`
6. Copie a URL do webhook e adicione como secret `TEAMS_WEBHOOK_URL`

## Estrutura

```
alerta-inep/
├── .github/workflows/monitor.yml   # Automação GitHub Actions
├── src/
│   ├── scraper_editais.py          # Scraper de editais (determinístico)
│   ├── scraper_noticias.py         # Scraper de notícias (filtro IA)
│   ├── ai_filter.py                # Módulo Gemini 2.5 Flash-Lite
│   ├── notifier.py                 # Envio para Teams
│   └── cards/
│       ├── card_edital.py          # Card azul — documentos oficiais
│       └── card_noticia.py         # Card verde — notícias/informativos
├── data/last_seen.json             # Estado persistido (banco gratuito)
└── requirements.txt
```

## Tecnologias (custo zero)

- **Python + BeautifulSoup** — scraping
- **Gemini 2.5 Flash-Lite** — filtro por IA (1.000 req/dia grátis)
- **GitHub Actions** — automação (2.000 min/mês grátis)
- **Power Automate + Teams** — entrega das notificações
