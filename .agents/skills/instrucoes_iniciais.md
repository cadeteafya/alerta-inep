Manual de Operações: Protocolo de Desenvolvimento Antigravity Kit

O Antigravity Kit (AG Kit) não é apenas uma ferramenta de auxílio; é uma infraestrutura de engenharia de software de alta escala projetada para automatizar fluxos de trabalho e maximizar a eficiência operacional através de agentes inteligentes. Como Arquiteto Principal, a implementação deste protocolo é mandatória para garantir a consistência técnica, eliminar a dívida técnica precoce e sustentar uma cultura de excelência em todo o ciclo de vida do software.

1. Fundamentos e Infraestrutura do Sistema

A base do AG Kit reside na padronização. O sistema opera a partir da pasta .agent/, que centraliza personas, módulos de conhecimento e automações. A configuração comportamental do workspace é regida pelo arquivo rules/GEMINI.md, que estabelece as diretrizes globais de codificação e as restrições operacionais que os agentes devem obedecer.

Inicialização e Gestão via CLI

A forma mais eficiente de instanciar o ecossistema é via npx ag-kit init, garantindo o uso imediato dos templates mais recentes sem overhead de instalação global.

Comando	Operação Técnica	Impacto na Estrutura .agent/
ag-kit init	Inicialização do ambiente.	Instala a pasta .agent/, bibliotecas e o core GEMINI.md.
ag-kit update	Atualização de infraestrutura.	Destrutivo: Substitui a pasta .agent/. Requer backup de customizações.
ag-kit status	Diagnóstico de integridade.	Valida versões e contagem de 20+ agentes, 37+ skills e workflows.

Arquitetura de Conhecimento e Intelligent Routing

O AG Kit utiliza uma arquitetura triádica (Agents, Skills, Workflows) otimizada para performance de contexto:

* Skills & YAML Frontmatter: As habilidades não são apenas prompts, mas módulos carregados via frontmatter YAML. Isso permite que o sistema utilize Selective Reading, lendo apenas as seções necessárias da documentação da skill para otimizar o uso do context window da IA.
* Intelligent Routing: O roteamento automático elimina a necessidade de ativação manual, detectando o contexto da tarefa para invocar o especialista correto (ex: backend-specialist para rotas de API).

Esta infraestrutura instalada é o pré-requisito absoluto para o ciclo de descoberta estruturada.


--------------------------------------------------------------------------------


2. Fase 1: Descoberta Estruturada e Planejamento

Arquitetos de alto nível separam a concepção da execução. No AG Kit, codificar sem um blueprint validado é considerado um desvio de protocolo.

Workflow /brainstorm: Socratic Discovery

O comando /brainstorm ativa o protocolo de Socratic Discovery. O sistema é impedido de sugerir soluções triviais, sendo obrigado a:

1. Apresentar no mínimo 3 abordagens arquiteturais distintas.
2. Analisar rigorosamente prós, contras e nível de esforço (LoE).
3. Utilizar questionamentos socráticos para identificar restrições ocultas antes da primeira linha de código.

Workflow /plan: O Protocolo Rígido "NO CODE"

O comando /plan aplica uma política de zero produção de código. O objetivo é a delimitação de escopo através do agente project-planner.

* Output: Geração do arquivo docs/PLAN-{slug}.md.
* Blueprint: Este documento torna-se a única fonte de verdade para a execução.
* Dica Pro: Utilize a annotation // turbo em workflows confiáveis para permitir a execução automática de comandos de leitura ou criação de arquivos, ignorando aprovações manuais repetitivas e acelerando o fluxo de planejamento.


--------------------------------------------------------------------------------


3. Fase 2: Execução e Orquestração de Especialistas

A transição para a construção é gerida pelo AG Kit como um maestro de múltiplos agentes especialistas, garantindo paralelismo e especialização.

Scaffolding de Alta Escala com /create

O comando /create atua como um wizard de scaffolding. Ele coordena simultaneamente o database-architect, o backend-specialist e o frontend-specialist para erguer aplicações completas a partir do plano aprovado, definindo tech stacks e estruturas de arquivos de forma automatizada.

Orquestração e Agentes Especializados

Para projetos complexos, o workflow /orchestrate delega ao agente orchestrator a função de Project Manager. Ele decompõe o PLAN.md e distribui tarefas para especialistas específicos:

* code-archaeologist: Invocado para análise e refatoração de código legado.
* explorer-agent: Utilizado para exploração profunda de codebases desconhecidas.
* security-auditor: Monitora a implementação de fluxos de autenticação.

UI/UX de Alta Fidelidade

O sub-workflow /ui-ux-pro-max integra-se diretamente ao nextlevelbuilder.io. A execução deve ser baseada em style prompts específicos, permitindo a aplicação instantânea de estéticas como glassmorphism ou claymorphism, garantindo interfaces profissionais com acessibilidade e SEO integrados.


--------------------------------------------------------------------------------


4. Fase 3: Iteração, Validação e Debugging

A manutenção da qualidade em sistemas de alta escala exige ferramentas cirúrgicas para modificações incrementais.

Desenvolvimento Cirúrgico com /enhance

O comando /enhance foca em vertical slices, adicionando funcionalidades sem degradar o sistema existente.

* Obrigatoriedade: O uso do script checklist.py é mandatório para monitorar dependências e prevenir o inchaço do bundle (bundle bloat) ao adicionar novas bibliotecas.

Protocolos de Diagnóstico e Testes

* /debug (Protocolo de 4 Fases): Nenhuma correção é aplicada sem evidência. O fluxo exige:
  1. Discovery (Logs e fatos); 2. Hypothesis (Causas prováveis); 3. Verification (Teste da hipótese); 4. Resolution (Fix + teste de regressão).
* /test (Operações de QA): O comando deve ser utilizado com sub-parâmetros específicos para cobertura total:
  * run: Execução da suíte atual.
  * generate: Criação automatizada de testes para novos arquivos.
  * coverage: Auditoria de lacunas de teste.
  * watch: Modo de desenvolvimento reativo.

O comando /status atua como o dashboard operacional, reportando o progresso dos agentes e a saúde do projeto em tempo real.


--------------------------------------------------------------------------------


5. Fase 4: Governança, Audit e Deployment

A última milha do desenvolvimento no AG Kit é regida pelo rigor da segurança e estabilidade operacional.

Gestão de Preview

O comando /preview automatiza a detecção de frameworks (Next.js, Vite, etc.) e resolve conflitos de porta de forma inteligente, garantindo que o ambiente local de validação seja sempre consistente com o estado atual do código.

Fluxo /deploy: O Audit & Release Conductor

O comando /deploy não é um simples transporte de arquivos, mas um pipeline de auditoria.

* Dry-run Obrigatório: O comando /deploy check deve ser executado para validar a saúde do projeto sem realizar o deploy físico.
* Critérios de Interrupção (Stop-on-Fail): O deploy será bloqueado se o sistema detectar:
  * [ ] Vulnerabilidades de segurança (via security-auditor).
  * [ ] Erros de linting ou violações de estilo.
  * [ ] Tipos TypeScript inválidos ou inconsistentes.
  * [ ] Falhas em suítes de testes críticos.

Salvaguardas Operacionais

Em caso de anomalias pós-release, o comando /deploy rollback deve ser acionado para restauração imediata da última versão estável. A adoção irrestrita deste protocolo garante não apenas a velocidade de entrega, mas a sustentabilidade técnica e a segurança de software em escala industrial através do Antigravity Kit.
