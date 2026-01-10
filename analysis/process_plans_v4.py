#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Planes de Gobierno - Costa Rica 2026-2030
Versión 4.0 - Con penalizaciones D5 y 10 pilares ajustados a realidad CR

Modelo estricto:
- 10 pilares (incluye Infraestructura)
- Pesos ajustados a urgencias nacionales
- Penalizaciones D5 por incoherencia fiscal y omisión de urgencias
"""

import fitz
import json
import os
import re
import hashlib
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(BASE_DIR, "planes")
DATA_DIR = os.path.join(BASE_DIR, "data")

# ====================================================================
# 10 PILARES NACIONALES - PESOS AJUSTADOS A REALIDAD CR 2026
# ====================================================================

PILLARS = [
    {"pillar_id": "P1", "pillar_name": "Sostenibilidad fiscal y finanzas públicas", "weight": 0.15},
    {"pillar_id": "P2", "pillar_name": "Empleo, competitividad e inversión extranjera", "weight": 0.15},
    {"pillar_id": "P3", "pillar_name": "Seguridad ciudadana y justicia", "weight": 0.18},  # MAYOR PESO
    {"pillar_id": "P4", "pillar_name": "Salud pública y seguridad social (CCSS)", "weight": 0.10},
    {"pillar_id": "P5", "pillar_name": "Educación y talento humano", "weight": 0.12},
    {"pillar_id": "P6", "pillar_name": "Ambiente y desarrollo sostenible", "weight": 0.04},
    {"pillar_id": "P7", "pillar_name": "Reforma del Estado y lucha contra la corrupción", "weight": 0.08},
    {"pillar_id": "P8", "pillar_name": "Política social focalizada", "weight": 0.06},
    {"pillar_id": "P9", "pillar_name": "Política exterior y comercio internacional", "weight": 0.02},
    {"pillar_id": "P10", "pillar_name": "Infraestructura y obra pública", "weight": 0.10},  # NUEVO
]

PILLAR_WEIGHTS = {p["pillar_id"]: p["weight"] for p in PILLARS}
CRITICAL_PILLARS = {"P1", "P2", "P3", "P5", "P10"}  # 70% del peso total

# ====================================================================
# PALABRAS CLAVE POR PILAR
# ====================================================================

PILLAR_KEYWORDS = {
    "P1": [
        "fiscal", "tributar", "impuesto", "presupuest", "déficit", "deuda", "hacienda",
        "recaudación", "gasto público", "austeridad", "PIB", "regla fiscal",
        "finanzas públicas", "equilibrio fiscal", "reforma tributaria", "FMI",
        "sostenibilidad", "banco central", "inflación", "estabilidad monetaria"
    ],
    "P2": [
        "empleo", "trabajo", "desempleo", "competitividad", "PYME", "mipyme", "empresa",
        "emprendimiento", "innovación", "productividad", "exportación", "zona franca",
        "inversión extranjera", "IED", "nearshoring", "multinacional", "atracción",
        "salario", "informalidad", "capacitación laboral", "mercado laboral"
    ],
    "P3": [
        "seguridad", "policía", "crimen", "delincuencia", "narcotráfico", "drogas",
        "violencia", "homicidio", "robo", "extorsión", "sicariato", "pandillas",
        "cárcel", "prisión", "justicia", "OIJ", "fuerza pública", "criminalidad",
        "crimen organizado", "lavado de dinero", "armas", "inteligencia policial"
    ],
    "P4": [
        "salud", "CCSS", "Caja Costarricense", "hospital", "clínica", "médic",
        "EBAIS", "lista de espera", "seguridad social", "pensión", "jubilación",
        "IVM", "déficit actuarial", "cotizante", "asegurado", "farmacia"
    ],
    "P5": [
        "educación", "escuela", "colegio", "universidad", "docente", "MEP",
        "deserción escolar", "aprendizaje", "PISA", "educación técnica", "INA",
        "beca", "infraestructura educativa", "calidad educativa", "8% PIB"
    ],
    "P6": [
        "ambiente", "ambiental", "cambio climático", "carbono", "emisiones",
        "renovable", "agua", "bosque", "biodiversidad", "conservación",
        "contaminación", "reciclaje", "residuos", "SINAC", "MINAE"
    ],
    "P7": [
        "reforma del estado", "modernización", "digitalización", "gobierno digital",
        "simplificación", "corrupción", "transparencia", "contraloría", "auditoría",
        "ética", "servidor público", "eficiencia", "burocracia", "trámite"
    ],
    "P8": [
        "pobreza", "vulnerable", "desigualdad", "bono", "subsidio", "IMAS",
        "FODESAF", "programa social", "niñez", "adulto mayor", "discapacidad",
        "vivienda social", "BANHVI", "focalización"
    ],
    "P9": [
        "política exterior", "diplomacia", "comercio internacional", "TLC",
        "exportación", "cooperación internacional", "ONU", "OEA", "SICA",
        "bilateral", "multilateral", "Estados Unidos", "China"
    ],
    "P10": [
        "infraestructura", "carretera", "ruta", "puente", "puerto", "aeropuerto",
        "obra pública", "concesión", "APP", "alianza público-privada", "CONAVI",
        "MOPT", "transporte", "ferrocarril", "tren", "vial", "construcción"
    ]
}

# ====================================================================
# INDICADORES PARA DIMENSIONES D1-D4
# ====================================================================

TIME_INDICATORS_VALID = [
    r"primer(?:o|a)?\s*(?:año|mes|semestre|trimestre)",
    r"primeros?\s*100\s*días",
    r"primeros?\s*\d+\s*(?:años?|meses?|días?)",
    r"20\d{2}[-–]20\d{2}",
    r"cuatrienio",
    r"durante\s*el\s*(?:gobierno|período|cuatrienio)",
    r"al\s*(?:inicio|final)\s*del?\s*gobierno",
]

HOW_INDICATORS = [
    r"mediante\s+(?:la|el|un|una)\s+\w+",
    r"a\s*través\s*de",
    r"proyecto\s*de\s*ley",
    r"decreto\s*ejecutivo",
    r"programa\s+(?:de|para|nacional)",
    r"plan\s*(?:de\s*)?(?:acción|nacional)",
    r"reforma\s+(?:a|de|del|al)",
    r"crear(?:á|emos)?\s+(?:una?|el|la)",
    r"establecer(?:á|emos)?",
    r"implementar(?:á|emos)?",
]

FUNDING_INDICATORS = [
    r"financ(?:iar|iamiento|iado)",
    r"presupuest(?:o|ar|ario)",
    r"recursos?\s*(?:públicos?|del\s+Estado)",
    r"fondos?\s*(?:públicos?|del\s+Estado)",
    r"impuesto",
    r"tribut",
    r"deuda\s*(?:pública|interna|externa)",
    r"crédito\s+(?:internacional|BID|Banco\s+Mundial)",
    r"cooperación\s*internacional",
    r"APP\b",
    r"alianza\s*público[-\s]?privada",
    r"concesión",
    r"reasignación",
    r"\d+(?:\.\d+)?\s*(?:millones?|billones?)",
    r"\d+(?:[.,]\d+)?%\s*del\s*(?:PIB|presupuesto)",
]

# ====================================================================
# PATRONES DE PENALIZACIÓN D5
# ====================================================================

# D5.1: Incoherencia fiscal
FISCAL_INCOHERENCE_PATTERNS = [
    (r"(?:flexibilizar|reformar|eliminar|excluir).*regla\s*fiscal", "Propone flexibilizar regla fiscal"),
    (r"(?:aumentar|incrementar|duplicar).*gasto.*(?!financiad|mediante|con\s+fondos)", "Propone aumentar gasto sin financiamiento"),
    (r"(?:eliminar|reducir).*impuesto.*(?!compensar|alternativ)", "Propone reducir impuestos sin compensación"),
    (r"subsidio\s+universal", "Propone subsidio universal en contexto de déficit"),
]

# D5.2: Omisión de urgencias nacionales
URGENCY_REQUIREMENTS = {
    "P3": {  # Seguridad
        "required_terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "operativ"],
        "penalty_reason": "No propone medidas operativas de seguridad"
    },
    "P2": {  # Empleo/IED
        "required_terms": ["inversión extranjera", "zona franca", "IED", "nearshoring", "multinacional"],
        "penalty_reason": "No menciona inversión extranjera como generador de empleo"
    },
    "P1": {  # Fiscal
        "required_terms": ["sostenibilidad", "equilibrio", "responsabilidad fiscal", "déficit"],
        "penalty_reason": "No aborda sostenibilidad fiscal"
    },
    "P10": {  # Infraestructura
        "required_terms": ["APP", "concesión", "alianza público", "inversión privada"],
        "penalty_reason": "No propone mecanismos de financiamiento de infraestructura"
    }
}

# ====================================================================
# FUNCIONES UTILITARIAS
# ====================================================================

def normalize_text(text: str) -> str:
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_proposal_id(pdf_id: str, text: str) -> str:
    hash_input = f"{pdf_id}:{text[:100]}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    return f"{pdf_id.lower()}-{short_hash}"

def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

# ====================================================================
# EXTRACCIÓN DE PDF
# ====================================================================

def extract_text_from_pdf(pdf_path: str) -> Tuple[List[Tuple[int, str]], str]:
    """Extrae texto de un PDF, retorna páginas y texto completo."""
    pages = []
    full_text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            normalized = normalize_text(text)
            if normalized:
                pages.append((page_num + 1, normalized))
                full_text += " " + normalized
        doc.close()
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
    return pages, full_text

def extract_candidate_info(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, str]:
    """Extrae información del candidato."""
    first_pages_text = " ".join([text for _, text in pages[:5]])
    
    candidate_name = "no_especificado"
    party_name = "no_especificado"
    
    # Buscar nombre del candidato
    patterns = [
        r"candidat[oa].*?presidencia[:\s]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+(?:para\s+)?[Pp]residente",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, first_pages_text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 5 and len(name.split()) >= 2:
                candidate_name = name
                break
    
    # Buscar partido
    party_patterns = [
        r"[Pp]artido\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
        r"[Cc]oalición\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
        r"[Ff]rente\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
    ]
    
    for pattern in party_patterns:
        match = re.search(pattern, first_pages_text)
        if match:
            party = match.group(0).strip()[:60]
            party_name = party
            break
    
    return {"candidate_name": candidate_name, "party_name": party_name}

# ====================================================================
# EVALUACIÓN DE DIMENSIONES
# ====================================================================

def identify_primary_pillar(text: str) -> Optional[str]:
    text_lower = text.lower()
    scores = {}
    
    for pillar_id, keywords in PILLAR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score >= 2:
            scores[pillar_id] = score
    
    if not scores:
        return None
    return max(scores, key=scores.get)

def check_existence(text: str) -> bool:
    patterns = [
        r"(?:crear|establecer|implementar|desarrollar|reformar|construir|ampliar)(?:á|emos)?",
        r"(?:programa|proyecto|plan|estrategia|política)\s+(?:de|para|nacional)",
        r"(?:ley|decreto|reglamento)",
        r"(?:invertir|destinar|asignar)\s+(?:recursos?|fondos?)",
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_when(text: str) -> Tuple[bool, str]:
    for pattern in TIME_INDICATORS_VALID:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return True, match.group(0).strip()
    return False, "no_especificado"

def check_how(text: str) -> Tuple[bool, str]:
    for pattern in HOW_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            return True, text[start:end].strip()[:100]
    return False, "no_especificado"

def check_funding(text: str) -> Tuple[bool, str]:
    for pattern in FUNDING_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            return True, text[start:end].strip()[:100]
    return False, "no_especificado"

# ====================================================================
# PENALIZACIONES D5
# ====================================================================

def check_fiscal_incoherence(full_text: str) -> List[Dict]:
    """Detecta incoherencias fiscales en el documento completo."""
    penalties = []
    text_lower = full_text.lower()
    
    for pattern, reason in FISCAL_INCOHERENCE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            penalties.append({
                "type": "fiscal_incoherence",
                "value": -1,
                "reason": reason
            })
            break  # Solo una penalización fiscal por documento
    
    return penalties

def check_urgency_omission(full_text: str, pillar_id: str) -> List[Dict]:
    """Verifica si omite urgencias nacionales para un pilar específico."""
    penalties = []
    
    if pillar_id not in URGENCY_REQUIREMENTS:
        return penalties
    
    req = URGENCY_REQUIREMENTS[pillar_id]
    text_lower = full_text.lower()
    
    found = any(term.lower() in text_lower for term in req["required_terms"])
    
    if not found:
        penalties.append({
            "type": "urgency_omission",
            "value": -1,
            "reason": req["penalty_reason"]
        })
    
    return penalties

# ====================================================================
# EXTRACCIÓN DE PROPUESTAS
# ====================================================================

def extract_best_proposal_per_pillar(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, Dict]:
    candidates_by_pillar = defaultdict(list)
    
    for page_num, text in pages:
        paragraphs = re.split(r'\n\s*\n|\.\s+(?=[A-ZÁÉÍÓÚÑ])', text)
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) < 50:
                continue
            
            pillar_id = identify_primary_pillar(paragraph)
            if not pillar_id:
                continue
            
            is_concrete = check_existence(paragraph)
            if not is_concrete:
                continue
            
            has_when, when_text = check_when(paragraph)
            has_how, how_text = check_how(paragraph)
            has_funding, funding_text = check_funding(paragraph)
            
            dimensions = {
                "existence": 1,
                "when": 1 if has_when else 0,
                "how": 1 if has_how else 0,
                "funding": 1 if has_funding else 0
            }
            
            raw_score = sum(dimensions.values())
            snippet = paragraph[:237] + "…" if len(paragraph) > 240 else paragraph
            title = paragraph[:57] + "…" if len(paragraph) > 60 else paragraph[:60]
            
            proposal = {
                "pillar_id": pillar_id,
                "page_num": page_num,
                "text": paragraph[:500],
                "title": title,
                "dimensions": dimensions,
                "raw_score": raw_score,
                "extracted_fields": {
                    "when_text": when_text,
                    "how_text": how_text,
                    "funding_text": funding_text
                },
                "snippet": snippet
            }
            
            candidates_by_pillar[pillar_id].append(proposal)
    
    best_by_pillar = {}
    for pillar_id, proposals in candidates_by_pillar.items():
        proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)
        best_by_pillar[pillar_id] = proposals[0]
    
    return best_by_pillar

def create_proposals_json(best_by_pillar: Dict[str, Dict], candidate_id: str, pdf_id: str) -> List[Dict]:
    proposals = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        
        if pillar_id in best_by_pillar:
            p = best_by_pillar[pillar_id]
            proposal = {
                "proposal_id": generate_proposal_id(pdf_id, p["text"]),
                "candidate_id": candidate_id,
                "pillar_id": pillar_id,
                "proposal_title": p["title"],
                "proposal_text": p["text"],
                "dimensions": p["dimensions"],
                "extracted_fields": p["extracted_fields"],
                "evidence": {
                    "pdf_id": pdf_id,
                    "page": p["page_num"],
                    "snippet": p["snippet"]
                }
            }
        else:
            proposal = {
                "proposal_id": generate_proposal_id(pdf_id, f"placeholder_{pillar_id}"),
                "candidate_id": candidate_id,
                "pillar_id": pillar_id,
                "proposal_title": "Sin propuesta identificada para este pilar",
                "proposal_text": "El documento no contiene propuestas concretas para este pilar.",
                "dimensions": {"existence": 0, "when": 0, "how": 0, "funding": 0},
                "extracted_fields": {
                    "when_text": "no_especificado",
                    "how_text": "no_especificado",
                    "funding_text": "no_especificado"
                },
                "evidence": {"pdf_id": pdf_id, "page": 1, "snippet": "Sin contenido para este pilar."}
            }
        
        proposals.append(proposal)
    
    return proposals

# ====================================================================
# SCORING CON PENALIZACIONES
# ====================================================================

def calculate_candidate_score(proposals: List[Dict], candidate_id: str, full_text: str) -> Dict:
    """Calcula scores con penalizaciones D5."""
    
    proposal_by_pillar = {p["pillar_id"]: p for p in proposals if p["candidate_id"] == candidate_id}
    
    # Penalizaciones a nivel documento
    global_penalties = check_fiscal_incoherence(full_text)
    
    pillar_scores = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        weight = pillar["weight"]
        
        prop = proposal_by_pillar.get(pillar_id)
        
        if prop:
            dims = prop["dimensions"]
            raw_score = dims["existence"] + dims["when"] + dims["how"] + dims["funding"]
        else:
            raw_score = 0
        
        # Penalizaciones específicas del pilar
        pillar_penalties = check_urgency_omission(full_text, pillar_id)
        
        # Aplicar penalización fiscal global solo a P1
        if pillar_id == "P1" and global_penalties:
            pillar_penalties.extend(global_penalties)
        
        # Calcular effective_score (mínimo 0)
        total_penalty = sum(p["value"] for p in pillar_penalties)
        effective_score = max(0, raw_score + total_penalty)
        
        normalized = effective_score / 4.0
        weighted = normalized * weight
        
        pillar_scores.append({
            "pillar_id": pillar_id,
            "raw_score": raw_score,
            "effective_score": effective_score,
            "normalized": round(normalized, 4),
            "weighted": round(weighted, 4),
            "penalties": pillar_penalties
        })
    
    # Totales
    raw_sum = sum(ps["raw_score"] for ps in pillar_scores)
    effective_sum = sum(ps["effective_score"] for ps in pillar_scores)
    weighted_sum = sum(ps["weighted"] for ps in pillar_scores)
    
    coverage_critical = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Notas
    notes = []
    penalized = [ps["pillar_id"] for ps in pillar_scores if ps["penalties"]]
    if penalized:
        notes.append(f"Penalizados: {', '.join(penalized)}")
    
    empty = [ps["pillar_id"] for ps in pillar_scores if ps["raw_score"] == 0]
    if empty:
        notes.append(f"Sin propuestas: {', '.join(empty)}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": round(weighted_sum, 4),
            "coverage_critical_weighted_sum": round(coverage_critical, 4),
            "notes": " | ".join(notes) if notes else ""
        }
    }

# ====================================================================
# ANÁLISIS DETALLADO POR CANDIDATO
# ====================================================================

def analyze_candidate_detailed(pages: List[Tuple[int, str]], full_text: str, pdf_id: str) -> Dict:
    """Genera análisis detallado de coherencia."""
    
    text_lower = full_text.lower()
    
    analysis = {
        "pdf_id": pdf_id,
        "total_pages": len(pages),
        "urgency_coverage": {},
        "fiscal_analysis": {},
        "strengths": [],
        "weaknesses": []
    }
    
    # Análisis de cobertura de urgencias
    urgencies = {
        "seguridad_operativa": {
            "terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "patrullaje", "operativo"],
            "found": []
        },
        "inversion_extranjera": {
            "terms": ["inversión extranjera", "zona franca", "IED", "nearshoring", "multinacional"],
            "found": []
        },
        "sostenibilidad_fiscal": {
            "terms": ["sostenibilidad fiscal", "equilibrio fiscal", "regla fiscal", "déficit"],
            "found": []
        },
        "infraestructura_APP": {
            "terms": ["APP", "alianza público-privada", "concesión", "inversión privada"],
            "found": []
        },
        "crimen_organizado": {
            "terms": ["crimen organizado", "narcotráfico", "sicariato", "extorsión", "lavado"],
            "found": []
        }
    }
    
    for key, data in urgencies.items():
        for term in data["terms"]:
            count = text_lower.count(term.lower())
            if count > 0:
                data["found"].append(f"{term} ({count})")
        
        analysis["urgency_coverage"][key] = {
            "covered": len(data["found"]) > 0,
            "mentions": data["found"]
        }
    
    # Análisis fiscal
    fiscal_flags = {
        "critica_regla_fiscal": bool(re.search(r"(?:reformar|flexibilizar|eliminar).*regla\s*fiscal", text_lower)),
        "propone_gasto_sin_fuente": bool(re.search(r"(?:aumentar|crear).*(?:programa|subsidio|gasto).*(?!financiad|mediante)", text_lower)),
        "menciona_deficit": "déficit" in text_lower,
        "menciona_FMI": "fmi" in text_lower or "fondo monetario" in text_lower,
    }
    analysis["fiscal_analysis"] = fiscal_flags
    
    # Fortalezas y debilidades
    if analysis["urgency_coverage"]["seguridad_operativa"]["covered"]:
        analysis["strengths"].append("Aborda seguridad con enfoque operativo")
    else:
        analysis["weaknesses"].append("No propone medidas operativas de seguridad")
    
    if analysis["urgency_coverage"]["inversion_extranjera"]["covered"]:
        analysis["strengths"].append("Considera inversión extranjera para empleo")
    else:
        analysis["weaknesses"].append("Omite inversión extranjera como motor de empleo")
    
    if analysis["urgency_coverage"]["infraestructura_APP"]["covered"]:
        analysis["strengths"].append("Propone APP para infraestructura")
    else:
        analysis["weaknesses"].append("No propone mecanismos privados para infraestructura")
    
    if fiscal_flags["critica_regla_fiscal"]:
        analysis["weaknesses"].append("Propone flexibilizar regla fiscal sin alternativa clara")
    
    if not fiscal_flags["menciona_deficit"]:
        analysis["weaknesses"].append("No aborda explícitamente el déficit fiscal")
    
    return analysis

# ====================================================================
# RANKING
# ====================================================================

def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    ranking_overall = sorted(
        [(cs["candidate_id"], cs["overall"]["weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    ranking_critical = sorted(
        [(cs["candidate_id"], cs["overall"]["coverage_critical_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "method_version": "v4_strict",
        "weights": PILLAR_WEIGHTS,
        "critical_pillars": list(CRITICAL_PILLARS),
        "ranking_overall_weighted": [
            {"rank": i + 1, "candidate_id": cid, "weighted_sum": ws}
            for i, (cid, ws) in enumerate(ranking_overall)
        ],
        "ranking_critical_weighted": [
            {"rank": i + 1, "candidate_id": cid, "coverage_critical_weighted_sum": ccws}
            for i, (cid, ccws) in enumerate(ranking_critical)
        ]
    }

# ====================================================================
# PROCESAMIENTO PRINCIPAL
# ====================================================================

def process_all_pdfs():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    all_scores = []
    all_analysis = []
    
    print(f"Procesando {len(pdf_files)} planes de gobierno...")
    print("Modelo: v4 ESTRICTO (10 pilares + penalizaciones D5)")
    print("=" * 70)
    
    for pdf_file in sorted(pdf_files):
        pdf_id = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(PLANES_DIR, pdf_file)
        
        print(f"\n📄 {pdf_id}...")
        
        pages, full_text = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print(f"   ⚠️ No se pudo extraer texto")
            continue
        
        info = extract_candidate_info(pages, pdf_id)
        
        if info["candidate_name"] != "no_especificado":
            candidate_id = slugify(info["candidate_name"])
        else:
            candidate_id = pdf_id.lower()
        
        candidate = {
            "candidate_id": candidate_id,
            "candidate_name": info["candidate_name"],
            "party_name": info["party_name"],
            "pdf_id": pdf_id,
            "pdf_title": f"Plan de Gobierno {pdf_id} 2026-2030",
            "pdf_url": "no_especificado"
        }
        all_candidates.append(candidate)
        
        # Extraer propuestas
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        all_proposals.extend(proposals)
        
        # Calcular scores con penalizaciones
        scores = calculate_candidate_score(proposals, candidate_id, full_text)
        all_scores.append(scores)
        
        # Análisis detallado
        analysis = analyze_candidate_detailed(pages, full_text, pdf_id)
        analysis["candidate_id"] = candidate_id
        all_analysis.append(analysis)
        
        # Resumen
        penalized_count = sum(1 for ps in scores["pillar_scores"] if ps["penalties"])
        print(f"   → Págs: {len(pages)} | Pilares: {len(best_by_pillar)}/10 | Penalizados: {penalized_count}")
        print(f"   → Score: {scores['overall']['weighted_sum']:.1%} (raw: {scores['overall']['raw_sum']}/40)")
        
        if scores["overall"]["notes"]:
            print(f"   → Notas: {scores['overall']['notes'][:60]}...")
    
    # Generar ranking
    ranking = generate_ranking(all_scores)
    
    print("\n" + "=" * 70)
    print("📊 TOP 5 RANKING (v4 ESTRICTO)")
    print("=" * 70)
    for entry in ranking["ranking_overall_weighted"][:5]:
        print(f"   {entry['rank']}. {entry['candidate_id']}: {entry['weighted_sum']:.1%}")
    
    # Guardar archivos
    print("\n📁 Guardando archivos...")
    
    outputs = {
        "candidates.json": all_candidates,
        "pillars.json": PILLARS,
        "proposals.json": all_proposals,
        "candidate_scores.json": all_scores,
        "ranking.json": ranking,
        "detailed_analysis.json": all_analysis
    }
    
    for filename, data in outputs.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ {filename}")
    
    return outputs

if __name__ == "__main__":
    print("=" * 70)
    print("PROCESADOR DE PLANES v4.0 - MODELO ESTRICTO")
    print("10 pilares | Penalizaciones D5 | Pesos ajustados a CR")
    print("=" * 70)
    result = process_all_pdfs()
    print("\n✅ PROCESO COMPLETADO")
