import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

# Configuração do Logging nativo
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TaskValidationError(ValueError):
    """Exceção customizada lançada quando ocorrem erros de validação ou consistência cronológica."""
    pass


def _parse_iso_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """Auxiliar para conversão de strings no formato ISO 8601 em objetos datetime."""
    if not dt_str:
        return None
    try:
        # Trata formato ISO com sufixo Z ou offsets padrões
        clean_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(clean_str)
    except Exception as exc:
        logger.error(f"Erro ao converter data ISO '{dt_str}': {exc}")
        raise TaskValidationError(f"Formato de data inválido: {dt_str}") from exc


def analyze_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processa uma lista de tarefas e calcula métricas de desempenho e prazos conforme o contrato SDD.
    
    Args:
        tasks: Lista de dicionários representando tarefas.
        
    Returns:
        Dicionário com métricas calculadas e agrupamento por prioridade.
    """
    logger.info(f"Iniciando análise de lote com {len(tasks)} tarefas.")
    
    total_tarefas: int = len(tasks)
    total_concluidas: int = 0
    tempos_conclusao_horas: List[float] = []
    atrasos_count: int = 0
    
    # Estrutura acumuladora por prioridade
    prioridades_validas = ["baixa", "media", "alta"]
    metricas_prio: Dict[str, Dict[str, Any]] = {
        prio: {"total": 0, "concluidas": 0, "tempos_horas": [], "atrasos": 0}
        for prio in prioridades_validas
    }

    for task in tasks:
        prio = str(task.get("prioridade", "")).lower()
        if prio in metricas_prio:
            metricas_prio[prio]["total"] += 1

        status = str(task.get("status", "")).lower()
        if status == "concluida" and task.get("data_conclusao") is not None:
            dt_criacao = _parse_iso_datetime(task.get("data_criacao"))
            dt_conclusao = _parse_iso_datetime(task.get("data_conclusao"))
            dt_prazo = _parse_iso_datetime(task.get("data_prazo"))

            if dt_criacao is None or dt_conclusao is None or dt_prazo is None:
                raise TaskValidationError(f"Campos de data obrigatórios ausentes no ID {task.get('id')}.")

            # Regra de Negócio 2: Consistência Temporal
            if dt_conclusao < dt_criacao:
                msg = f"Inconsistência temporal no ID {task.get('id')}: data_conclusao é anterior à data_criacao."
                logger.error(msg)
                raise TaskValidationError(msg)

            total_concluidas += 1
            if prio in metricas_prio:
                metricas_prio[prio]["concluidas"] += 1

            # Cálculo do tempo em horas
            duracao_segundos = (dt_conclusao - dt_criacao).total_seconds()
            duracao_horas = duracao_segundos / 3600.0
            tempos_conclusao_horas.append(duracao_horas)
            
            if prio in metricas_prio:
                metricas_prio[prio]["tempos_horas"].append(duracao_horas)

            # Regra de Negócio 4: Cálculo de Atraso
            if dt_conclusao > dt_prazo:
                atrasos_count += 1
                if prio in metricas_prio:
                    metricas_prio[prio]["atrasos"] += 1

    # Regra de Negócio 3: Prevenção de Divisão por Zero
    tempo_medio_geral: float = (
        round(sum(tempos_conclusao_horas) / len(tempos_conclusao_horas), 2)
        if tempos_conclusao_horas else 0.0
    )
    
    taxa_atraso_geral: float = (
        round((atrasos_count / total_concluidas) * 100.0, 2)
        if total_concluidas > 0 else 0.0
    )

    # Consolidação por prioridade
    metricas_por_prioridade_output: Dict[str, Dict[str, Any]] = {}
    for prio in prioridades_validas:
        prio_data = metricas_prio[prio]
        prio_concluidas = prio_data["concluidas"]
        prio_tempos = prio_data["tempos_horas"]
        
        prio_tempo_medio = (
            round(sum(prio_tempos) / len(prio_tempos), 2)
            if prio_tempos else 0.0
        )
        prio_taxa_atraso = (
            round((prio_data["atrasos"] / prio_concluidas) * 100.0, 2)
            if prio_concluidas > 0 else 0.0
        )
        
        metricas_por_prioridade_output[prio] = {
            "total_tarefas": prio_data["total"],
            "total_concluidas": prio_concluidas,
            "tempo_medio_conclusao_horas": prio_tempo_medio,
            "taxa_atraso_percentual": prio_taxa_atraso
        }

    logger.info("Análise concluída com sucesso.")
    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "tempo_medio_conclusao_horas": tempo_medio_geral,
        "taxa_atraso_percentual": taxa_atraso_geral,
        "metricas_por_prioridade": metricas_por_prioridade_output
    }
