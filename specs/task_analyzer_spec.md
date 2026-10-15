# ESPECIFICAÇÃO TÉCNICA E CONTRATO DE NEGÓCIO - TASKANALYZER

## 1. VISÃO GERAL E CONTRATO DE NEGÓCIO (SDD)

### 1.1 Identificação
* **Nome:** Eduardo Fleming Diniz
* **Curso:** Ciência de Dados e Machine Learning (Turma A)
* **E-mail:** eduardo.fleming@sempreceub.com

---

### 1.2 Propósito do Módulo TaskAnalyzer
O módulo `TaskAnalyzer` é um componente de software projetado para processar dados de execução de tarefas e gerar métricas de produtividade e desempenho[cite: 1]. Seu propósito principal é permitir a análise rigorosa de tempos de execução e o monitoramento de prazos, fornecendo indicadores detalhados para tomada de decisão e melhoria contínua de processos[cite: 1].

**Principais Responsabilidades do Módulo:**
* Calcular o tempo médio de conclusão de tarefas[cite: 1].
* Identificar e mensurar a taxa de atraso (tarefas finalizadas após a data prevista de término)[cite: 1].
* Agrupar e apresentar indicadores consolidados por nível de prioridade (`"baixa"`, `"media"`, `"alta"`)[cite: 1].

---

### 1.3 Contrato Executável de Interface
O contrato a seguir especifica estritamente as entradas, saídas, tipos de dados e restrições de negócio que deverão ser seguidos pela implementação do sistema[cite: 1].

#### 1.3.1 Entradas (Inputs)
A função principal receberá uma estrutura de dados (lista de dicionários) contendo tarefas com os seguintes campos[cite: 1]:

| Campo | Tipo de Dado | Obrigatório | Descrição / Formato |
| :--- | :--- | :---: | :--- |
| `id` | `int` ou `str` | Sim | Identificador único da tarefa[cite: 1]. |
| `titulo` | `str` | Sim | Nome ou descrição resumida da tarefa[cite: 1]. |
| `prioridade` | `str` | Sim | Nível de prioridade (`"baixa"`, `"media"`, `"alta"`)[cite: 1]. |
| `data_criacao` | `str` | Sim | Data e hora de criação no formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)[cite: 1]. |
| `data_conclusao` | `str` / `None` | Não | Data e hora de término (`YYYY-MM-DDTHH:MM:SS`) ou `None` se pendente[cite: 1]. |
| `data_prazo` | `str` | Sim | Data limite prevista para conclusão (`YYYY-MM-DDTHH:MM:SS`)[cite: 1]. |
| `status` | `str` | Sim | Estado da tarefa (`"concluida"`, `"pendente"`, `"cancelada"`)[cite: 1]. |

#### 1.3.2 Saídas (Outputs)
O módulo deverá retornar um dicionário estruturado com as seguintes métricas calculadas[cite: 1]:

| Campo / Métrica | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `total_tarefas` | `int` | Quantidade total de tarefas recebidas no lote[cite: 1]. |
| `total_concluidas` | `int` | Quantidade total de tarefas com status `"concluida"`[cite: 1]. |
| `tempo_medio_conclusao_horas` | `float` | Média do tempo decorrido entre criação e conclusão (em horas)[cite: 1]. |
| `taxa_atraso_percentual` | `float` | Porcentagem de tarefas concluídas após a `data_prazo` (ex: `15.5` para 15,5%)[cite: 1]. |
| `metricas_por_prioridade` | `dict` | Objeto contendo contagem, tempo médio e taxa de atraso divididos por prioridade (`baixa`, `media`, `alta`)[cite: 1]. |

#### 1.3.3 Regras de Negócio e Restrições
1. **Filtro de Processamento:** Apenas tarefas com `status == "concluida"` e que possuam `data_conclusao` preenchida devem ser consideradas nos cálculos de tempo e atraso[cite: 1].
2. **Consistência Temporal:** A `data_conclusao` deve ser estritamente igual ou posterior à `data_criacao`[cite: 1]. Caso seja anterior, uma exceção de validação de dados (`TaskValidationError`) deve ser lançada[cite: 1].
3. **Prevenção de Erros Aritméticos:** Se não houver tarefas concluídas na amostra (ou em uma prioridade específica), o sistema não deve realizar divisão por zero[cite: 1]. O valor atribuído ao tempo médio e à taxa de atraso nesses casos deve ser obrigatoriamente `0.0`[cite: 1].
4. **Cálculo de Atraso:** Uma tarefa é considerada em atraso se `data_conclusao > data_prazo`[cite: 1].

---

## 2. ESPECIFICAÇÃO DE CENÁRIOS DE ACEITE E TEST HARNESS

### 2.1 Cenários de Aceite (Dado-Quando-Então)

#### Cenário 1: Sucesso (Processamento e Métricas Corretas)
* **Dado** um conjunto de tarefas válidas contendo diferentes prioridades ("baixa", "media", "alta") e status ("concluida", "pendente")[cite: 1],
* **Quando** o analisador `TaskAnalyzer` for executado[cite: 1],
* **Então** o sistema deve retornar um dicionário com as métricas calculadas corretamente, incluindo[cite: 1]:
  * Tempo médio geral de conclusão em horas preciso[cite: 1].
  * Taxa de atraso geral percentual correta[cite: 1].
  * Contagem total e agrupamento exato de tempo médio e taxa de atraso por cada prioridade[cite: 1].
  * Desconsideração de tarefas pendentes ou canceladas nos cálculos numéricos[cite: 1].

#### Cenário 2: Exceção / Erro (Entradas Inválidas e Tratamento de Bordas)
* **Dado** um conjunto de dados de entrada com inconformidades (ex.: `data_conclusao` anterior à `data_criacao`, datas em formato inválido, ou lote sem nenhuma tarefa concluída)[cite: 1],
* **Quando** o analisador `TaskAnalyzer` for executado[cite: 1],
* **Então** o sistema deve responder com tratamentos específicos[cite: 1]:
  * Disparar uma exceção específica tratada (`TaskValidationError`) com mensagem clara e objetiva caso as datas sejam inconsistentes[cite: 1].
  * Retornar `0.0` para métricas de tempo e atraso caso não existam tarefas concluídas, evitando erros de divisão por zero[cite: 1].

---

### 2.2 Planejamento do Test Harness
O *Test Harness* consistirá em uma suíte de testes automatizados construída com a biblioteca `pytest` na linguagem Python[cite: 1]. A finalidade desta estrutura é atuar como uma barreira de validação objetiva para garantir que qualquer código gerado por assistentes de IA siga estritamente o contrato especificado[cite: 1].

| Componente | Ferramenta / Método | Objetivo do Teste |
| :--- | :--- | :--- |
| **Framework de Teste** | `pytest` | Executar testes unitários e de integração automatizados[cite: 1]. |
| **Massa de Dados (Fixtures)** | `pytest.fixture` | Prover conjuntos de dados sintéticos para testes de sucesso e falha[cite: 1]. |
| **Teste de Sucesso** | `test_calcular_metricas_sucesso()` | Validar os cálculos numéricos do Cenário 1 contra valores esperados[cite: 1]. |
| **Teste de Exceção** | `test_validacao_datas_invalidas()` | Garantir que o sistema lança a exceção correta no Cenário 2 via `pytest.raises`[cite: 1]. |
| **Teste de Borda** | `test_divisao_por_zero()` | Garantir que um lote sem tarefas concluídas retorne `0.0` sem falhar a execução[cite: 1]. |

---

## 3. GOVERNANÇA E REGRAS DE CONTEXTO (CONTEXT_RULES)

Para garantir que a Inteligência Artificial geradora de código opere sob limites estritos durante a próxima fase de implementação, aplicam-se as seguintes diretrizes obrigatórias e proibições rígidas[cite: 1]:

### 3.1 Diretrizes de Qualidade Técnica (Permissões e Obrigatividades)
1. **Padrão PEP 8:** O código Python deve seguir rigorosamente as convenções de estilo PEP 8 (nomes de funções e variáveis em `snake_case`, indentação com 4 espaços, etc.)[cite: 1].
2. **Type Hints Explícitos:** Todas as funções e métodos devem declarar explicitamente as anotações de tipo de dados para parâmetros e retornos (ex.: `def analyze_tasks(tasks: list[dict]) -> dict:`)[cite: 1].
3. **Princípio de Responsabilidade Única (SRP):** Funções e classes devem possuir responsabilidades bem delimitadas (ex.: separar a função de validação/parse de datas da função de cálculo de médias)[cite: 1].
4. **Sistema de Log (Logging):** Utilizar o módulo nativo `logging` de Python para registrar eventos do sistema em níveis adequados (`INFO`, `WARNING`, `ERROR`), evitando o uso de `print()` solto no código[cite: 1].
5. **Tratamento Seguro de Exceções:** Lançar e capturar exceções específicas (`TaskValidationError`), acompanhadas de mensagens descritivas do motivo da falha[cite: 1].

### 3.2 Proibições Rígidas (Restrições)
* ❌ **Proibido o uso de bibliotecas externas não autorizadas:** O processamento deve ser feito preferencialmente com bibliotecas nativas de Python (`datetime`, `logging`, `typing`)[cite: 1]. Uso de dependências pesadas como `pandas` é proibido a menos que expressamente solicitado[cite: 1].
* ❌ **Proibido omitir Type Hints:** Qualquer código gerado pela IA sem anotações de tipo será rejeitado pelo harness de governança[cite: 1].
* ❌ **Proibido realizar alterações fora do escopo do contrato SDD:** A IA não pode adicionar campos não especificados na saída ou alterar os tipos descritos na seção 1.3[cite: 1].
* ❌ **Proibido o uso de blocos `try/except` genéricos:** Proibida a captura silenciosa de exceções genéricas (`except Exception: pass`)[cite: 1].
