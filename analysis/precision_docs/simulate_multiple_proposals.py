#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación: Sistema de Bonos por Múltiples Propuestas
Compara el sistema actual (1 propuesta) vs sistema propuesto (2-3 propuestas con bonos)
"""

import json
import os
from collections import defaultdict
from typing import Dict, List

# Cargar datos actuales (desde el directorio padre)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_data():
    """Carga los datos actuales."""
    with open(os.path.join(DATA_DIR, "proposals.json"), 'r', encoding='utf-8') as f:
        proposals = json.load(f)
    with open(os.path.join(DATA_DIR, "candidate_scores.json"), 'r', encoding='utf-8') as f:
        scores = json.load(f)
    with open(os.path.join(DATA_DIR, "ranking.json"), 'r', encoding='utf-8') as f:
        ranking = json.load(f)
    return proposals, scores, ranking


def extract_all_proposals_by_pillar(proposals: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
    """Extrae todas las propuestas agrupadas por candidato y pilar."""
    result = defaultdict(lambda: defaultdict(list))
    
    for prop in proposals:
        if prop.get('dimensions', {}).get('existence', 0) > 0:
            cid = prop.get('candidate_id', '')
            pid = prop.get('pillar_id', '')
            result[cid][pid].append(prop)
    
    return result


def calculate_score_with_bonus(
    candidate_proposals: List[Dict],
    pillar_id: str,
    pillar_weight: float
) -> Dict:
    """
    Calcula score con sistema de bonos simplificado.
    
    Bonos:
    - Solo 3+ propuestas válidas: +1.0
    - Propuesta completa (4/4): +0.25
    - Propuesta con financiamiento (3+): +0.1
    
    Criterio: Solo premia si tiene exactamente 3 o más propuestas válidas (score >= 2)
    """
    # Filtrar propuestas válidas (score >= 2, E=1 obligatorio)
    valid_proposals = [
        p for p in candidate_proposals
        if p.get('pillar_id') == pillar_id and
        p.get('dimensions', {}).get('existence', 0) == 1 and
        sum(p.get('dimensions', {}).values()) >= 2
    ]
    
    if not valid_proposals:
        return {
            "base_score": 0,
            "bonus_multiple": 0,
            "bonus_quality": 0,
            "effective_score": 0,
            "normalized": 0,
            "weighted": 0,
            "num_proposals": 0
        }
    
    # Mejor propuesta (score base)
    best_prop = max(valid_proposals, key=lambda p: sum(p['dimensions'].values()))
    base_score = sum(best_prop['dimensions'].values())
    
    # Bono por múltiples propuestas: SOLO si tiene 3 o más
    num_valid = len(valid_proposals)
    if num_valid >= 3:
        bonus_multiple = 1.0
    else:
        bonus_multiple = 0.0  # No bono para 1 o 2 propuestas
    
    # Bono por calidad
    complete_count = len([
        p for p in valid_proposals 
        if sum(p['dimensions'].values()) == 4
    ])
    funding_count = len([
        p for p in valid_proposals 
        if p['dimensions'].get('funding', 0) == 1 and sum(p['dimensions'].values()) >= 3
    ])
    
    bonus_quality = (complete_count * 0.25) + (funding_count * 0.1)
    
    # Score efectivo (máximo 4.0)
    effective_score = min(4.0, base_score + bonus_multiple + bonus_quality)
    normalized = effective_score / 4.0
    weighted = normalized * pillar_weight
    
    return {
        "base_score": base_score,
        "bonus_multiple": bonus_multiple,
        "bonus_quality": round(bonus_quality, 2),
        "effective_score": round(effective_score, 2),
        "normalized": round(normalized, 4),
        "weighted": round(weighted, 4),
        "num_proposals": num_valid
    }


def simulate_new_scoring(proposals: List[Dict], scores: List[Dict]) -> Dict:
    """Simula el nuevo sistema de scoring con bonos."""
    
    # Peso de pilares (del sistema actual)
    PILLAR_WEIGHTS = {
        "P1": 0.14, "P2": 0.11, "P3": 0.18, "P4": 0.16, "P5": 0.10,
        "P6": 0.03, "P7": 0.12, "P8": 0.05, "P9": 0.02, "P10": 0.09
    }
    
    # Agrupar propuestas por candidato y pilar
    all_proposals_by_candidate = extract_all_proposals_by_pillar(proposals)
    
    new_scores = []
    
    for old_score in scores:
        candidate_id = old_score.get('candidate_id', '')
        candidate_proposals = []
        
        # Obtener todas las propuestas del candidato
        for pid in PILLAR_WEIGHTS.keys():
            candidate_proposals.extend(
                all_proposals_by_candidate[candidate_id][pid]
            )
        
        # Calcular scores por pilar con bonos
        pillar_scores_new = []
        total_weighted = 0
        
        for pid, weight in PILLAR_WEIGHTS.items():
            pillar_proposals = [
                p for p in candidate_proposals 
                if p.get('pillar_id') == pid
            ]
            
            score_data = calculate_score_with_bonus(
                pillar_proposals, pid, weight
            )
            
            pillar_scores_new.append({
                "pillar_id": pid,
                "base_score": score_data["base_score"],
                "bonus_multiple": score_data["bonus_multiple"],
                "bonus_quality": score_data["bonus_quality"],
                "effective_score": score_data["effective_score"],
                "normalized": score_data["normalized"],
                "weighted": score_data["weighted"],
                "num_proposals": score_data["num_proposals"]
            })
            
            total_weighted += score_data["weighted"]
        
        new_scores.append({
            "candidate_id": candidate_id,
            "weighted_sum": round(total_weighted, 4),
            "pillar_scores": pillar_scores_new
        })
    
    return new_scores


def compare_rankings(old_scores: List[Dict], new_scores: List[Dict]):
    """Compara rankings antes y después."""
    
    # Ranking actual
    old_ranking = sorted(
        [(s['candidate_id'], s['overall']['weighted_sum']) for s in old_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Ranking nuevo
    new_ranking = sorted(
        [(s['candidate_id'], s['weighted_sum']) for s in new_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    print("=" * 80)
    print("COMPARACIÓN DE RANKINGS")
    print("=" * 80)
    print()
    
    print(f"{'#':<3} {'Candidato':<30} {'Score Actual':<12} {'Score Nuevo':<12} {'Cambio':<10} {'Posición':<10}")
    print("-" * 80)
    
    for i, (cid, new_score) in enumerate(new_ranking[:20], 1):
        old_entry = next((e for e in old_ranking if e[0] == cid), None)
        old_score = old_entry[1] if old_entry else 0
        old_pos = old_ranking.index((cid, old_score)) + 1 if old_entry else 999
        
        change = new_score - old_score
        change_pct = (change / old_score * 100) if old_score > 0 else 0
        pos_change = old_pos - i
        
        change_str = f"{change:+.1%}" if change != 0 else "0%"
        pos_str = f"{old_pos}→{i}" if pos_change != 0 else str(i)
        
        print(f"{i:<3} {cid[:28]:<30} {old_score:<12.1%} {new_score:<12.1%} {change_str:<10} {pos_str:<10}")
    
    print()
    print("=" * 80)


def analyze_impact(proposals: List[Dict], old_scores: List[Dict], new_scores: List[Dict]):
    """Analiza el impacto del nuevo sistema."""
    
    print("=" * 80)
    print("ANÁLISIS DE IMPACTO")
    print("=" * 80)
    print()
    
    # Candidatos que más se benefician
    improvements = []
    for old_score in old_scores:
        cid = old_score['candidate_id']
        old_ws = old_score['overall']['weighted_sum']
        new_entry = next((s for s in new_scores if s['candidate_id'] == cid), None)
        
        if new_entry:
            new_ws = new_entry['weighted_sum']
            improvement = new_ws - old_ws
            improvements.append((cid, improvement, old_ws, new_ws))
    
    improvements.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 10 candidatos que más se benefician:")
    print("-" * 80)
    for cid, improvement, old_ws, new_ws in improvements[:10]:
        print(f"  {cid[:30]:<30} {old_ws:.1%} → {new_ws:.1%} (+{improvement:.1%})")
    
    print()
    
    # Estadísticas de propuestas
    all_proposals_by_candidate = extract_all_proposals_by_pillar(proposals)
    
    print("Estadísticas de propuestas por candidato:")
    print("-" * 80)
    
    stats = []
    for cid, pillars in all_proposals_by_candidate.items():
        total_props = sum(len(props) for props in pillars.values())
        valid_props = sum(
            len([p for p in props if sum(p.get('dimensions', {}).values()) >= 2])
            for props in pillars.values()
        )
        pillars_with_multiple = sum(
            1 for props in pillars.values()
            if len([p for p in props if sum(p.get('dimensions', {}).values()) >= 2]) > 1
        )
        stats.append((cid, total_props, valid_props, pillars_with_multiple))
    
    stats.sort(key=lambda x: x[2], reverse=True)
    
    print(f"{'Candidato':<30} {'Total':<8} {'Válidas':<8} {'Pilares múltiples':<15}")
    print("-" * 80)
    for cid, total, valid, multiple in stats[:10]:
        print(f"{cid[:28]:<30} {total:<8} {valid:<8} {multiple:<15}")


def main():
    print("=" * 80)
    print("SIMULACIÓN: Sistema de Bonos por Múltiples Propuestas")
    print("=" * 80)
    print()
    
    # Cargar datos
    print("📊 Cargando datos...")
    proposals, scores, ranking = load_data()
    print(f"   ✅ {len(proposals)} propuestas cargadas")
    print(f"   ✅ {len(scores)} candidatos con scores")
    print()
    
    # Simular nuevo scoring
    print("🔄 Simulando nuevo sistema de scoring...")
    new_scores = simulate_new_scoring(proposals, scores)
    print(f"   ✅ Scores recalculados para {len(new_scores)} candidatos")
    print()
    
    # Comparar rankings
    compare_rankings(scores, new_scores)
    
    # Análisis de impacto
    analyze_impact(proposals, scores, new_scores)
    
    # Guardar resultados
    output_file = os.path.join(DATA_DIR, "simulation_multiple_proposals.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "simulation_date": "2026-01-11",
            "system": "bonos_multiples_propuestas",
            "new_scores": new_scores
        }, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"💾 Resultados guardados en: {output_file}")
    print()
    print("=" * 80)
    print("✅ SIMULACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == "__main__":
    main()
