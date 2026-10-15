# TaskAnalyzer — Módulo de Processamento e Métricas de Tarefas

> **Bootcamp III** — Disciplina Virtual (EAD)  
> **Aluno:** Eduardo Fleming Diniz  
> **Curso:** Ciência de Dados e Machine Learning (Turma A)  
> **Fase 2:** Implementação Assistida por IA, Test Harness e Versionamento no GitHub  

---

## 📌 Visão Geral do Projeto
O **TaskAnalyzer** é um módulo Python desenvolvido sob a metodologia **SDD (Spec-Driven Development)** para processamento de lotes de tarefas, cálculo de métricas de produtividade (tempo médio de execução) e identificação de taxas de atraso.

A solução foi implementada utilizando assistentes de Inteligência Artificial Generativa sob rigorosa governança de contexto (`CONTEXT_RULES.md`) e validada de forma automatizada via suíte de testes com `pytest`.

---

## 🛠️ Estrutura do Repositório
sdd-task-analyzer/
├── README.md                 # Documentação geral e instruções de execução
├── CONTEXT_RULES.md          # Regras de governança e restrições para a IA
├── .gitignore                # Arquivos ignorados pelo Git (__pycache__, etc.)
├── requirements.txt          # Dependências do projeto (pytest)
├── specs/
│   └── task_analyzer_spec.md # Especificação do contrato técnico SDD
├── tests/
│   └── test_harness.py       # Suíte de testes automatizados (Pytest)
└── src/
    └── task_analyzer.py      # Código-fonte principal homologado

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
* Python 3.11 ou superior
* Git instalado

### 2. Clonar o Repositório
git clone https://github.com/EduFleming/sdd-task-analyzer.git
cd sdd-task-analyzer

### 3. Instalar Dependências
python -m pip install -r requirements.txt

### 4. Executar os Testes Automatizados (Test Harness)
Para validar o comportamento do sistema contra os cenários de aceite definidos na especificação, execute:
python -m pytest

---

## 🧪 Cobertura do Test Harness (Pytest)
A suíte em `tests/test_harness.py` valida:
* **Cenário 1 (Sucesso):** Cálculo correto de totais, tempos médios em horas e taxa de atraso percentual por prioridade e geral.
* **Cenário 2 (Exceções):** Disparo de `TaskValidationError` para tarefas com `data_conclusao` anterior à `data_criacao`.
* **Casos de Borda:** Prevenção de divisão por zero retornando `0.0` para métricas sem tarefas concluídas na amostra.

---

## 🛡️ Governança e IA (CONTEXT_RULES)
O código em `src/task_analyzer.py` foi gerado via IA e homologado manualmente garantindo:
* 100% de **Type Hints** em funções e parâmetros.
* Conformidade total com **PEP 8** e uso de **bibliotecas nativas** (`datetime`, `logging`, `typing`).
* Prevenção de alucinações e tratamentos específicos de exceção.
