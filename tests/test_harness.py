import pytest
from src.task_analyzer import analyze_tasks, TaskValidationError


@pytest.fixture
def massa_tarefas_cenario_1():
    """Massa de dados sintética válida para validação do Cenário 1."""
    return [
        {
            "id": 101,
            "titulo": "Implementar Login",
            "prioridade": "alta",
            "data_criacao": "2026-03-01T08:00:00",
            "data_conclusao": "2026-03-01T12:00:00",  # 4h de duração
            "data_prazo": "2026-03-01T10:00:00",      # Atrasada
            "status": "concluida"
        },
        {
            "id": 102,
            "titulo": "Corrigir Layout",
            "prioridade": "baixa",
            "data_criacao": "2026-03-01T08:00:00",
            "data_conclusao": "2026-03-01T14:00:00",  # 6h de duração
            "data_prazo": "2026-03-01T18:00:00",      # No prazo
            "status": "concluida"
        },
        {
            "id": 103,
            "titulo": "Atualizar Documentação",
            "prioridade": "media",
            "data_criacao": "2026-03-01T08:00:00",
            "data_conclusao": None,
            "data_prazo": "2026-03-01T12:00:00",
            "status": "pendente"                       # Não entra nas médias
        }
    ]


def test_calcular_metricas_sucesso(massa_tarefas_cenario_1):
    """Valida os cálculos de métricas do Cenário 1."""
    resultado = analyze_tasks(massa_tarefas_cenario_1)

    assert resultado["total_tarefas"] == 3
    assert resultado["total_concluidas"] == 2
    assert resultado["tempo_medio_conclusao_horas"] == 5.0  # (4h + 6h) / 2
    assert resultado["taxa_atraso_percentual"] == 50.0       # 1 em atraso de 2 concluídas

    prio_alta = resultado["metricas_por_prioridade"]["alta"]
    assert prio_alta["total_concluidas"] == 1
    assert prio_alta["tempo_medio_conclusao_horas"] == 4.0
    assert prio_alta["taxa_atraso_percentual"] == 100.0


def test_validacao_datas_invalidas():
    """Garante o disparo de TaskValidationError para data de conclusão anterior à de criação."""
    tarefa_invalida = [{
        "id": 999,
        "titulo": "Tarefa com Viagem no Tempo",
        "prioridade": "alta",
        "data_criacao": "2026-03-01T12:00:00",
        "data_conclusao": "2026-03-01T08:00:00",  # Anterior à criação!
        "data_prazo": "2026-03-01T18:00:00",
        "status": "concluida"
    }]

    with pytest.raises(TaskValidationError) as excinfo:
        analyze_tasks(tarefa_invalida)
    
    assert "Inconsistência temporal" in str(excinfo.value)


def test_divisao_por_zero_lote_vazio():
    """Garante que entradas sem tarefas concluídas retornem 0.0 sem erros de divisão por zero."""
    tarefas_pendentes = [{
        "id": 201,
        "titulo": "Tarefa Pendente",
        "prioridade": "media",
        "data_criacao": "2026-03-01T08:00:00",
        "data_conclusao": None,
        "data_prazo": "2026-03-01T18:00:00",
        "status": "pendente"
    }]

    resultado = analyze_tasks(tarefas_pendentes)

    assert resultado["total_tarefas"] == 1
    assert resultado["total_concluidas"] == 0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0
