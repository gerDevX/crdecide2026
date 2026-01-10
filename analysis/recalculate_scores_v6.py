#!/usr/bin/env python3
"""
Recalculate candidate scores with the new penalty system v6.

Changes from previous version:
1. REMOVED proposes_tax_increase penalty (was ideological bias)
2. ADDED omission penalties for ignoring national urgencies:
   - ignores_security: -1 (not mentioning security operations)
   - ignores_ccss: -1 (not mentioning CCSS crisis)
   - ignores_employment: -0.5 (not mentioning employment)
   - ignores_organized_crime: -0.5 (not mentioning organized crime)
   - missing_priority_pillar: -0.5 (per missing priority pillar P1,P3,P4,P7)
3. KEPT fiscal penalties (objective - based on law):
   - attacks_fiscal_rule: -2
   - proposes_debt_increase: -1
"""

import json
from pathlib import Path
from typing import Any

# Paths
DATA_DIR = Path(__file__).parent / "data"

# ============================================
# PENALTY CONFIGURATION (v6 - Neutral + Strict)
# ============================================

# Fiscal penalties (objective - based on current law)
FISCAL_PENALTIES = {
    "attacks_fiscal_rule": -2,      # Attacks the current fiscal rule
    "proposes_debt_increase": -1,   # More debt without sustainability plan
}

# Omission penalties (based on Costa Rica's national urgencies)
OMISSION_PENALTIES = {
    "ignores_security": -1,           # Doesn't mention security operations
    "ignores_ccss": -1,               # Doesn't mention CCSS crisis  
    "ignores_employment": -0.5,       # Doesn't mention employment
    "ignores_organized_crime": -0.5,  # Doesn't mention organized crime
    "missing_priority_pillar": -0.5,  # Per missing priority pillar
}

# Priority pillars (P3: Security, P4: Health, P1: Fiscal, P7: State Reform)
PRIORITY_PILLARS = ["P3", "P4", "P1", "P7"]

# Critical pillars (add P2: Employment, P5: Education)
CRITICAL_PILLARS = ["P3", "P4", "P1", "P7", "P2", "P5"]

# Pillar weights
PILLAR_WEIGHTS = {
    "P1": 0.14,
    "P2": 0.11,
    "P3": 0.18,
    "P4": 0.16,
    "P5": 0.10,
    "P6": 0.03,
    "P7": 0.12,
    "P8": 0.05,
    "P9": 0.02,
    "P10": 0.09,
}


def load_json(filename: str) -> Any:
    """Load a JSON file from the data directory."""
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data: Any) -> None:
    """Save data to a JSON file in the data directory."""
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved: {filename}")


def analyze_omissions(detailed: dict) -> dict:
    """
    Analyze what urgencies a candidate ignores.
    Returns omission analysis dict.
    """
    urgency = detailed.get("urgency_coverage", {})
    
    omission = {
        "ignores_security": not urgency.get("seguridad_operativa", {}).get("covered", True),
        "ignores_ccss": not urgency.get("salud_ccss", {}).get("covered", True),
        "ignores_employment": not urgency.get("empleo", {}).get("covered", True),
        "ignores_organized_crime": not urgency.get("crimen_organizado", {}).get("covered", True),
        "missing_priority_pillars": [],
        "total_penalty": 0,
        "details": [],
    }
    
    # Calculate penalty
    penalty = 0
    details = []
    
    if omission["ignores_security"]:
        penalty += OMISSION_PENALTIES["ignores_security"]
        details.append("🚨 No menciona seguridad operativa")
    
    if omission["ignores_ccss"]:
        penalty += OMISSION_PENALTIES["ignores_ccss"]
        details.append("🏥 No menciona crisis de CCSS")
    
    if omission["ignores_employment"]:
        penalty += OMISSION_PENALTIES["ignores_employment"]
        details.append("💼 No menciona empleo/desempleo")
    
    if omission["ignores_organized_crime"]:
        penalty += OMISSION_PENALTIES["ignores_organized_crime"]
        details.append("🔫 No menciona crimen organizado")
    
    omission["total_penalty"] = penalty
    omission["details"] = details
    
    return omission


def check_missing_priority_pillars(pillar_scores: list) -> list:
    """
    Check which priority pillars are missing (score 0 or very low).
    Returns list of missing pillar IDs.
    """
    missing = []
    for pillar_id in PRIORITY_PILLARS:
        # Find this pillar's score
        ps = next((p for p in pillar_scores if p["pillar_id"] == pillar_id), None)
        if ps is None or ps.get("raw_score", 0) <= 1:
            missing.append(pillar_id)
    return missing


def recalculate_candidate_score(
    old_score: dict, 
    detailed: dict,
    proposals: list
) -> dict:
    """
    Recalculate a candidate's score with the new penalty system.
    """
    candidate_id = old_score["candidate_id"]
    pillar_scores = old_score["pillar_scores"]
    
    # Get fiscal flags (remove proposes_tax_increase from consideration)
    old_fiscal = old_score.get("fiscal_analysis", {}).get("flags", {})
    fiscal_flags = {
        "attacks_fiscal_rule": old_fiscal.get("attacks_fiscal_rule", False),
        "proposes_debt_increase": old_fiscal.get("proposes_debt_increase", False),
        "shows_fiscal_responsibility": old_fiscal.get("shows_fiscal_responsibility", False),
    }
    
    # Calculate fiscal penalty (only objective penalties)
    fiscal_penalty = 0
    fiscal_evidence = old_score.get("fiscal_analysis", {}).get("evidence", [])
    
    if fiscal_flags["attacks_fiscal_rule"]:
        fiscal_penalty += FISCAL_PENALTIES["attacks_fiscal_rule"]
    if fiscal_flags["proposes_debt_increase"]:
        fiscal_penalty += FISCAL_PENALTIES["proposes_debt_increase"]
    
    # Analyze omissions
    omission_analysis = analyze_omissions(detailed)
    
    # Check missing priority pillars
    missing_priority = check_missing_priority_pillars(pillar_scores)
    omission_analysis["missing_priority_pillars"] = missing_priority
    
    # Add penalty for missing priority pillars
    for pillar_id in missing_priority:
        omission_analysis["total_penalty"] += OMISSION_PENALTIES["missing_priority_pillar"]
        omission_analysis["details"].append(f"📋 Falta propuesta concreta en {pillar_id}")
    
    omission_penalty = omission_analysis["total_penalty"]
    total_penalty = fiscal_penalty + omission_penalty
    
    # Recalculate pillar scores (remove old tax penalty if any)
    new_pillar_scores = []
    for ps in pillar_scores:
        new_ps = {
            "pillar_id": ps["pillar_id"],
            "raw_score": ps["raw_score"],
            "effective_score": ps["raw_score"],  # Start fresh
            "normalized": 0.0,
            "weighted": 0.0,
            "penalties": [],
        }
        
        # Apply fiscal penalties only to P1
        if ps["pillar_id"] == "P1":
            if fiscal_flags["attacks_fiscal_rule"]:
                new_ps["penalties"].append({
                    "type": "attacks_fiscal_rule",
                    "value": FISCAL_PENALTIES["attacks_fiscal_rule"],
                    "reason": "Propone flexibilizar/reformar la regla fiscal",
                    "evidence": fiscal_evidence[0] if fiscal_evidence else ""
                })
                new_ps["effective_score"] = max(0, new_ps["effective_score"] + FISCAL_PENALTIES["attacks_fiscal_rule"])
            
            if fiscal_flags["proposes_debt_increase"]:
                new_ps["penalties"].append({
                    "type": "proposes_debt_increase",
                    "value": FISCAL_PENALTIES["proposes_debt_increase"],
                    "reason": "Propone aumentar deuda pública",
                    "evidence": fiscal_evidence[1] if len(fiscal_evidence) > 1 else ""
                })
                new_ps["effective_score"] = max(0, new_ps["effective_score"] + FISCAL_PENALTIES["proposes_debt_increase"])
        
        # Calculate normalized and weighted
        new_ps["normalized"] = new_ps["effective_score"] / 4.0
        weight = PILLAR_WEIGHTS.get(ps["pillar_id"], 0)
        new_ps["weighted"] = round(new_ps["normalized"] * weight, 4)
        
        new_pillar_scores.append(new_ps)
    
    # Calculate overall sums
    raw_sum = sum(ps["raw_score"] for ps in new_pillar_scores)
    effective_sum = sum(ps["effective_score"] for ps in new_pillar_scores)
    weighted_sum = round(sum(ps["weighted"] for ps in new_pillar_scores), 4)
    
    # Priority weighted sum (P3, P4, P1, P7)
    priority_weighted = sum(
        ps["weighted"] for ps in new_pillar_scores 
        if ps["pillar_id"] in PRIORITY_PILLARS
    )
    
    # Critical weighted sum (P3, P4, P1, P7, P2, P5)
    critical_weighted = sum(
        ps["weighted"] for ps in new_pillar_scores 
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Build notes
    notes_parts = []
    if fiscal_flags["attacks_fiscal_rule"]:
        notes_parts.append(f"⚠️ ATACA REGLA FISCAL ({FISCAL_PENALTIES['attacks_fiscal_rule']})")
    if fiscal_flags["proposes_debt_increase"]:
        notes_parts.append(f"💰 Propone más deuda ({FISCAL_PENALTIES['proposes_debt_increase']})")
    if fiscal_flags["shows_fiscal_responsibility"]:
        notes_parts.append("✅ Muestra responsabilidad fiscal")
    
    # Add omission notes
    for detail in omission_analysis["details"]:
        notes_parts.append(detail)
    
    # Check for missing pillars (non-priority)
    missing_non_priority = [
        ps["pillar_id"] for ps in new_pillar_scores 
        if ps["raw_score"] == 0 and ps["pillar_id"] not in PRIORITY_PILLARS
    ]
    if missing_non_priority:
        notes_parts.append(f"Sin propuestas: {', '.join(missing_non_priority)}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": new_pillar_scores,
        "fiscal_analysis": {
            "flags": fiscal_flags,
            "total_penalty": fiscal_penalty,
            "evidence": fiscal_evidence,
        },
        "omission_analysis": omission_analysis,
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": weighted_sum,
            "priority_weighted_sum": round(priority_weighted, 4),
            "critical_weighted_sum": round(critical_weighted, 4),
            "fiscal_penalty_applied": fiscal_penalty,
            "omission_penalty_applied": omission_penalty,
            "total_penalty_applied": total_penalty,
            "notes": " | ".join(notes_parts) if notes_parts else "",
        },
    }


def update_detailed_analysis(detailed: dict, omission_analysis: dict, fiscal_flags: dict) -> dict:
    """
    Update detailed analysis with new weaknesses based on v6 penalties.
    """
    new_detailed = detailed.copy()
    
    # Update fiscal_responsibility (remove proposes_tax_increase)
    new_detailed["fiscal_responsibility"] = fiscal_flags
    
    # Rebuild weaknesses based on new system
    weaknesses = []
    
    # Fiscal weaknesses
    if fiscal_flags["attacks_fiscal_rule"]:
        weaknesses.append("🔴 ATACA REGLA FISCAL - Riesgo alto para finanzas públicas")
    if fiscal_flags["proposes_debt_increase"]:
        weaknesses.append("🟠 Propone aumentar deuda pública")
    
    # Omission weaknesses
    if omission_analysis["ignores_security"]:
        weaknesses.append("🚨 No aborda la crisis de seguridad")
    if omission_analysis["ignores_ccss"]:
        weaknesses.append("🏥 No aborda la crisis de la CCSS")
    if omission_analysis["ignores_employment"]:
        weaknesses.append("💼 No menciona estrategias de empleo")
    if omission_analysis["ignores_organized_crime"]:
        weaknesses.append("🔫 No menciona crimen organizado")
    
    # Missing priority pillars
    for pillar_id in omission_analysis.get("missing_priority_pillars", []):
        pillar_names = {
            "P1": "Fiscal",
            "P3": "Seguridad", 
            "P4": "Salud",
            "P7": "Reforma Estado",
        }
        weaknesses.append(f"📋 Sin propuesta concreta en {pillar_names.get(pillar_id, pillar_id)}")
    
    # Check for missing APP/infrastructure
    if not detailed.get("urgency_coverage", {}).get("infraestructura_APP", {}).get("covered", True):
        weaknesses.append("No propone mecanismos privados para infraestructura")
    
    new_detailed["weaknesses"] = weaknesses
    
    # Recalculate risk level
    fiscal_penalty = 0
    if fiscal_flags["attacks_fiscal_rule"]:
        fiscal_penalty += abs(FISCAL_PENALTIES["attacks_fiscal_rule"])
    if fiscal_flags["proposes_debt_increase"]:
        fiscal_penalty += abs(FISCAL_PENALTIES["proposes_debt_increase"])
    
    omission_penalty = abs(omission_analysis.get("total_penalty", 0))
    total_penalty = fiscal_penalty + omission_penalty
    
    if fiscal_flags["attacks_fiscal_rule"] or total_penalty >= 3:
        new_detailed["risk_level"] = "ALTO"
    elif total_penalty >= 1.5:
        new_detailed["risk_level"] = "MEDIO"
    else:
        new_detailed["risk_level"] = "BAJO"
    
    return new_detailed


def generate_ranking(scores: list) -> dict:
    """
    Generate ranking from recalculated scores.
    """
    # Sort by weighted_sum descending
    sorted_overall = sorted(
        scores, 
        key=lambda x: x["overall"]["weighted_sum"], 
        reverse=True
    )
    
    sorted_priority = sorted(
        scores,
        key=lambda x: x["overall"]["priority_weighted_sum"],
        reverse=True
    )
    
    sorted_critical = sorted(
        scores,
        key=lambda x: x["overall"]["critical_weighted_sum"],
        reverse=True
    )
    
    ranking = {
        "method_version": "v6_neutral_strict",
        "weights": PILLAR_WEIGHTS,
        "priority_pillars": PRIORITY_PILLARS,
        "critical_pillars": CRITICAL_PILLARS,
        "penalties_applied": {
            "attacks_fiscal_rule": FISCAL_PENALTIES["attacks_fiscal_rule"],
            "proposes_debt_increase": FISCAL_PENALTIES["proposes_debt_increase"],
            "ignores_security": OMISSION_PENALTIES["ignores_security"],
            "ignores_ccss": OMISSION_PENALTIES["ignores_ccss"],
            "ignores_employment": OMISSION_PENALTIES["ignores_employment"],
            "ignores_organized_crime": OMISSION_PENALTIES["ignores_organized_crime"],
            "missing_priority_pillar": OMISSION_PENALTIES["missing_priority_pillar"],
        },
        "ranking_overall_weighted": [],
        "ranking_priority_weighted": [],
        "ranking_critical_weighted": [],
    }
    
    for rank, score in enumerate(sorted_overall, 1):
        ranking["ranking_overall_weighted"].append({
            "rank": rank,
            "candidate_id": score["candidate_id"],
            "weighted_sum": score["overall"]["weighted_sum"],
            "fiscal_penalty": score["overall"]["fiscal_penalty_applied"],
            "omission_penalty": score["overall"]["omission_penalty_applied"],
            "total_penalty": score["overall"]["total_penalty_applied"],
        })
    
    for rank, score in enumerate(sorted_priority, 1):
        ranking["ranking_priority_weighted"].append({
            "rank": rank,
            "candidate_id": score["candidate_id"],
            "priority_weighted_sum": score["overall"]["priority_weighted_sum"],
        })
    
    for rank, score in enumerate(sorted_critical, 1):
        ranking["ranking_critical_weighted"].append({
            "rank": rank,
            "candidate_id": score["candidate_id"],
            "critical_weighted_sum": score["overall"]["critical_weighted_sum"],
        })
    
    return ranking


def main():
    print("=" * 60)
    print("Recalculating scores with v6 penalty system")
    print("=" * 60)
    print("\nChanges:")
    print("  ❌ REMOVED: proposes_tax_increase (ideological bias)")
    print("  ✅ KEPT: attacks_fiscal_rule (-2)")
    print("  ✅ KEPT: proposes_debt_increase (-1)")
    print("  ➕ ADDED: ignores_security (-1)")
    print("  ➕ ADDED: ignores_ccss (-1)")
    print("  ➕ ADDED: ignores_employment (-0.5)")
    print("  ➕ ADDED: ignores_organized_crime (-0.5)")
    print("  ➕ ADDED: missing_priority_pillar (-0.5 each)")
    print()
    
    # Load current data
    print("Loading data...")
    old_scores = load_json("candidate_scores.json")
    detailed_analyses = load_json("detailed_analysis.json")
    proposals = load_json("proposals.json")
    
    # Create lookup for detailed analysis
    detailed_by_id = {d["candidate_id"]: d for d in detailed_analyses}
    
    # Recalculate scores
    print("\nRecalculating scores...")
    new_scores = []
    new_detailed = []
    
    for old_score in old_scores:
        candidate_id = old_score["candidate_id"]
        detailed = detailed_by_id.get(candidate_id, {})
        
        # Recalculate
        new_score = recalculate_candidate_score(old_score, detailed, proposals)
        new_scores.append(new_score)
        
        # Update detailed analysis
        updated_detailed = update_detailed_analysis(
            detailed, 
            new_score["omission_analysis"],
            new_score["fiscal_analysis"]["flags"]
        )
        new_detailed.append(updated_detailed)
        
        # Print summary
        total_penalty = new_score["overall"]["total_penalty_applied"]
        risk = updated_detailed.get("risk_level", "?")
        print(f"  {candidate_id}: weighted_sum={new_score['overall']['weighted_sum']:.3f}, "
              f"penalty={total_penalty}, risk={risk}")
    
    # Generate new ranking
    print("\nGenerating ranking...")
    new_ranking = generate_ranking(new_scores)
    
    # Print top 5
    print("\n🏆 TOP 5 RANKING:")
    for entry in new_ranking["ranking_overall_weighted"][:5]:
        print(f"  {entry['rank']}. {entry['candidate_id']}: {entry['weighted_sum']:.3f} "
              f"(penalty: {entry['total_penalty']})")
    
    # Save files
    print("\nSaving files...")
    save_json("candidate_scores.json", new_scores)
    save_json("detailed_analysis.json", new_detailed)
    save_json("ranking.json", new_ranking)
    
    print("\n✅ Done! Files updated with v6 penalty system.")
    print("\nSummary of changes:")
    print(f"  - {len(new_scores)} candidate scores recalculated")
    print(f"  - {len(new_detailed)} detailed analyses updated")
    print(f"  - Ranking regenerated with {len(new_ranking['ranking_overall_weighted'])} entries")


if __name__ == "__main__":
    main()
