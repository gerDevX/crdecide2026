#!/usr/bin/env python3
"""
PROCESADOR DE PLANES v6.0 - NEUTRAL + ESTRICTO

Cambios desde v5:
1. ELIMINADO: Penalización por proponer impuestos (sesgo ideológico)
2. AGREGADO: Penalizaciones por OMISIÓN de urgencias nacionales:
   - ignores_security: -1 (no menciona seguridad operativa)
   - ignores_ccss: -1 (no menciona crisis de la CCSS)
   - ignores_employment: -0.5 (no menciona empleo formal)
   - ignores_organized_crime: -0.5 (no menciona crimen organizado)
   - missing_priority_pillar: -0.5 (por cada pilar prioritario sin propuesta)
3. MANTENIDO: Penalizaciones fiscales objetivas basadas en ley:
   - attacks_fiscal_rule: -2
   - proposes_debt_increase: -1

Este sistema es:
- NEUTRAL: No penaliza posiciones ideológicas legítimas
- ESTRICTO: Penaliza omitir urgencias críticas del país
- OBJETIVO: Basado en ley vigente y necesidades nacionales
"""

import os
import re
import json
import hashlib
import io
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# ====================================================================
# CONFIGURACIÓN OCR (heredada de v5)
# ====================================================================

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyMuPDF no disponible. Instalar: pip install PyMuPDF")

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR no disponible. Instalar: pip install Pillow pytesseract")

# Configuración OCR
RENDER_DPI = 200
TESSERACT_CONFIG = '--psm 1 -l spa'

# Caracteres de fuentes corruptas
CORRUPT_CHARS = set([
    '\uf0b7', '\uf0a7', '\uf0d8', '\uf020', '\uf06c', '\uf06f', '\uf073',
    '\uf061', '\uf065', '\uf06e', '\uf072', '\uf074', '\uf075', '\uf069',
    '\uf064', '\uf063', '\uf06d', '\uf070', '\uf067', '\uf0fc', '\uf0e0',
])
CORRUPT_THRESHOLD = 0.02

# Rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(SCRIPT_DIR, "planes")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# ====================================================================
# PILARES NACIONALES (10 pilares)
# ====================================================================

PILLARS = [
    {"pillar_id": "P1", "name": "Responsabilidad Fiscal", "weight": 0.14},
    {"pillar_id": "P2", "name": "Empleo e Inversión", "weight": 0.11},
    {"pillar_id": "P3", "name": "Seguridad Ciudadana", "weight": 0.18},
    {"pillar_id": "P4", "name": "Salud y CCSS", "weight": 0.16},
    {"pillar_id": "P5", "name": "Educación", "weight": 0.10},
    {"pillar_id": "P6", "name": "Ambiente y Sostenibilidad", "weight": 0.03},
    {"pillar_id": "P7", "name": "Reforma del Estado", "weight": 0.12},
    {"pillar_id": "P8", "name": "Pobreza y Vulnerabilidad", "weight": 0.05},
    {"pillar_id": "P9", "name": "Política Exterior", "weight": 0.02},
    {"pillar_id": "P10", "name": "Infraestructura", "weight": 0.09},
]

PILLAR_WEIGHTS = {p["pillar_id"]: p["weight"] for p in PILLARS}

# Pilares prioritarios (urgencia nacional 2026)
PRIORITY_PILLARS = {"P3", "P4", "P1", "P7"}  # Seguridad, Salud, Fiscal, Reforma

# Pilares críticos (incluye empleo y educación)
CRITICAL_PILLARS = {"P3", "P4", "P1", "P7", "P2", "P5"}

# ====================================================================
# KEYWORDS POR PILAR
# ====================================================================

PILLAR_KEYWORDS = {
    "P1": [
        "fiscal", "presupuesto", "deuda", "déficit", "regla fiscal", "gasto público",
        "Hacienda", "finanzas", "tributario", "austeridad", "eficiencia",
        "racionalización", "consolidación fiscal", "sostenibilidad", "reforma tributaria"
    ],
    "P2": [
        "empleo", "trabajo", "desempleo", "informalidad", "PYME", "inversión extranjera",
        "zona franca", "nearshoring", "competitividad", "IED", "exportación",
        "productividad", "capacitación laboral", "salario", "formalización"
    ],
    "P3": [
        "seguridad", "crimen", "narcotráfico", "policía", "fuerza pública", "OIJ",
        "violencia", "homicidio", "robo", "hurto", "extorsión", "sicariato",
        "cárcel", "prisión", "delito", "penitenciario", "vigilancia", "inteligencia"
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
    r"reasignación",
    r"ahorro\s*(?:fiscal|público)",
    r"eficiencia\s*en\s*el\s*gasto",
    r"cooperación\s*internacional",
    r"APP\b",
    r"alianza\s*público[-\s]?privada",
    r"concesión",
    r"\d+(?:\.\d+)?\s*(?:millones?|billones?)",
    r"\d+(?:[.,]\d+)?%\s*del\s*(?:PIB|presupuesto)",
]

# ====================================================================
# PENALIZACIONES v6 - NEUTRAL + ESTRICTO
# ====================================================================

# PENALIZACIÓN FISCAL SEVERA: Flexibilizar regla fiscal (-2)
# Objetivo: basado en Ley 9635 vigente
FISCAL_RULE_ATTACK_PATTERNS = [
    r"(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender)",
    r"(?:limita|impide|obstaculiza).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:limita|impide|obstaculiza)",
    r"(?:revisión|revisar).*(?:crítica|profunda).*regla\s*fiscal",
]

# PENALIZACIÓN FISCAL: Proponer aumento de deuda (-1)
DEBT_INCREASE_PATTERNS = [
    r"(?:aumentar|incrementar|ampliar|expandir)\s*(?:la\s*)?(?:deuda|endeudamiento)",
    r"(?:nuevo|nueva|más)\s*(?:deuda|endeudamiento|crédito\s*público)",
    r"(?:emitir|emisión)\s*(?:de\s*)?(?:bonos?|deuda)",
    r"financiar.*(?:mediante|con)\s*(?:deuda|endeudamiento)",
]

# NOTA v6: ELIMINADO - proponer impuestos NO se penaliza (es posición ideológica legítima)
# TAX_INCREASE_PATTERNS = [...]  # REMOVIDO

# INDICADORES POSITIVOS (mitigan riesgo)
FISCAL_RESPONSIBILITY_INDICATORS = [
    r"sostenibilidad\s*fiscal",
    r"responsabilidad\s*fiscal",
    r"equilibrio\s*fiscal",
    r"reducir\s*(?:el\s*)?(?:déficit|gasto)",
    r"eficiencia\s*(?:del\s*)?gasto",
    r"austeridad",
    r"respetar.*regla\s*fiscal",
    r"cumplir.*regla\s*fiscal",
    r"mantener.*regla\s*fiscal",
]

# ====================================================================
# URGENCIAS NACIONALES v6 - CRITERIOS DE OMISIÓN
# ====================================================================

# Términos que indican que el candidato aborda la urgencia
URGENCY_TERMS = {
    "security_operations": {
        "terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "patrullaje", 
                  "operativo", "vigilancia", "control territorial"],
        "description": "Seguridad operativa",
        "penalty": -1
    },
    "ccss_crisis": {
        "terms": ["CCSS", "Caja Costarricense", "déficit actuarial", "listas de espera", 
                  "IVM", "régimen de pensiones", "sostenibilidad CCSS"],
        "description": "Crisis de la CCSS",
        "penalty": -1
    },
    "formal_employment": {
        "terms": ["empleo formal", "formalización", "informalidad laboral", "trabajo decente",
                  "cotizante", "seguro social obligatorio"],
        "description": "Empleo formal",
        "penalty": -0.5
    },
    "organized_crime": {
        "terms": ["crimen organizado", "narcotráfico", "sicariato", "extorsión",
                  "lavado de dinero", "cartel", "banda criminal"],
        "description": "Crimen organizado",
        "penalty": -0.5
    }
}

# Penalización por pilar prioritario sin propuesta concreta
MISSING_PRIORITY_PILLAR_PENALTY = -0.5

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
# EXTRACCIÓN DE PDF CON SOPORTE OCR (heredado de v5)
# ====================================================================

def detect_corrupt_text(text: str) -> Tuple[bool, float]:
    """Detecta si un texto tiene caracteres de fuentes corruptas."""
    if not text:
        return False, 0.0
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in CORRUPT_CHARS)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    return corrupt_ratio > CORRUPT_THRESHOLD, corrupt_ratio


def extract_page_with_ocr(page, dpi: int = RENDER_DPI) -> str:
    """Extrae texto de una página usando OCR."""
    if not OCR_AVAILABLE:
        return ""
    try:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
        return text
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""


def extract_text_from_pdf(pdf_path: str) -> Tuple[List[Tuple[int, str]], str]:
    """
    Extrae texto de un PDF, retorna páginas y texto completo.
    Detecta automáticamente texto corrupto y usa OCR cuando es necesario.
    """
    pages = []
    full_text = ""
    ocr_pages = 0
    doc = None
    
    try:
        doc = fitz.open(pdf_path)
        pdf_name = os.path.basename(pdf_path)
        num_pages = len(doc)
        
        # Primera pasada: detectar si hay texto corrupto (muestra de primeras 10 páginas)
        sample_text = ""
        for page_num in range(min(10, num_pages)):
            sample_text += doc[page_num].get_text()
        
        is_corrupt, ratio = detect_corrupt_text(sample_text)
        use_ocr = is_corrupt and OCR_AVAILABLE
        
        if is_corrupt:
            if OCR_AVAILABLE:
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%), usando OCR...")
            else:
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%) pero OCR no disponible")
        
        # Segunda pasada: extraer texto
        for page_num in range(num_pages):
            page = doc[page_num]
            
            if use_ocr:
                # Usar OCR para esta página
                text = extract_page_with_ocr(page)
                ocr_pages += 1
            else:
                # Extracción directa
                text = page.get_text()
                # Verificar si esta página específica tiene problemas
                page_corrupt, _ = detect_corrupt_text(text)
                if page_corrupt and OCR_AVAILABLE:
                    text = extract_page_with_ocr(page)
                    ocr_pages += 1
            
            normalized = normalize_text(text)
            if normalized:
                pages.append((page_num + 1, normalized))
                full_text += " " + normalized
        
        if ocr_pages > 0:
            print(f"  ✅ OCR completado: {ocr_pages}/{num_pages} páginas procesadas")
            
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
    finally:
        if doc:
            doc.close()
    
    return pages, full_text

def extract_candidate_info(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, str]:
    """Extrae información del candidato."""
    first_pages_text = " ".join([text for _, text in pages[:5]])
    
    candidate_name = "no_especificado"
    party_name = "no_especificado"
    
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
# ANÁLISIS FISCAL v6 (neutral - sin penalización por impuestos)
# ====================================================================

def analyze_fiscal_responsibility(full_text: str) -> Dict:
    """
    Analiza la posición fiscal del candidato.
    v6: Elimina penalización por impuestos (posición ideológica legítima).
    """
    text_lower = full_text.lower()
    
    analysis = {
        "penalties": [],
        "flags": {
            "attacks_fiscal_rule": False,
            "proposes_debt_increase": False,
            "shows_fiscal_responsibility": False,
        },
        "evidence": [],
        "total_penalty": 0
    }
    
    # Verificar indicadores de responsabilidad fiscal
    for pattern in FISCAL_RESPONSIBILITY_INDICATORS:
        if re.search(pattern, text_lower):
            analysis["flags"]["shows_fiscal_responsibility"] = True
            break
    
    # PENALIZACIÓN SEVERA: Atacar regla fiscal (-2)
    for pattern in FISCAL_RULE_ATTACK_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["attacks_fiscal_rule"] = True
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "attacks_fiscal_rule",
                "value": -2,
                "reason": "Propone flexibilizar/reformar la regla fiscal (Ley 9635)",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
    # PENALIZACIÓN: Proponer aumento de deuda (-1)
    for pattern in DEBT_INCREASE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["proposes_debt_increase"] = True
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "proposes_debt_increase",
                "value": -1,
                "reason": "Propone aumentar deuda pública sin plan de sostenibilidad",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
    # NOTA v6: NO se penaliza proponer impuestos
    # Es una posición ideológica legítima, no irresponsabilidad fiscal
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

# ====================================================================
# ANÁLISIS DE OMISIONES v6 - URGENCIAS NACIONALES
# ====================================================================

def analyze_urgency_omissions(full_text: str) -> Dict:
    """
    Analiza si el candidato omite urgencias nacionales críticas.
    v6: Nueva función para penalizar omisiones.
    """
    text_lower = full_text.lower()
    
    analysis = {
        "penalties": [],
        "coverage": {},
        "total_penalty": 0
    }
    
    for urgency_key, urgency_data in URGENCY_TERMS.items():
        found_terms = []
        for term in urgency_data["terms"]:
            if term.lower() in text_lower:
                found_terms.append(term)
        
        is_covered = len(found_terms) > 0
        analysis["coverage"][urgency_key] = {
            "covered": is_covered,
            "terms_found": found_terms,
            "description": urgency_data["description"]
        }
        
        # Si no cubre la urgencia, aplicar penalización
        if not is_covered:
            analysis["penalties"].append({
                "type": f"ignores_{urgency_key}",
                "value": urgency_data["penalty"],
                "reason": f"No aborda: {urgency_data['description']}",
                "evidence": "Término no encontrado en el documento"
            })
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

def analyze_pillar_omissions(proposals: List[Dict], candidate_id: str) -> Dict:
    """
    Analiza si faltan propuestas en pilares prioritarios.
    v6: Penalización por cada pilar prioritario sin propuesta.
    """
    analysis = {
        "penalties": [],
        "missing_pillars": [],
        "total_penalty": 0
    }
    
    candidate_proposals = [p for p in proposals if p["candidate_id"] == candidate_id]
    
    for pillar_id in PRIORITY_PILLARS:
        prop = next((p for p in candidate_proposals if p["pillar_id"] == pillar_id), None)
        
        # Si no hay propuesta o es placeholder
        if not prop or prop["dimensions"]["existence"] == 0:
            analysis["missing_pillars"].append(pillar_id)
            analysis["penalties"].append({
                "type": "missing_priority_pillar",
                "value": MISSING_PRIORITY_PILLAR_PENALTY,
                "reason": f"Sin propuesta concreta en pilar prioritario {pillar_id}",
                "pillar_id": pillar_id
            })
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

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
# SCORING v6 - CON TODAS LAS PENALIZACIONES
# ====================================================================

def calculate_candidate_score(
    proposals: List[Dict], 
    candidate_id: str, 
    full_text: str, 
    fiscal_analysis: Dict,
    urgency_analysis: Dict,
    pillar_analysis: Dict
) -> Dict:
    """Calcula scores con todas las penalizaciones v6."""
    
    proposal_by_pillar = {p["pillar_id"]: p for p in proposals if p["candidate_id"] == candidate_id}
    
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
        
        pillar_penalties = []
        
        # Aplicar penalizaciones fiscales a P1
        if pillar_id == "P1":
            pillar_penalties.extend(fiscal_analysis["penalties"])
        
        # Aplicar penalizaciones de urgencias a pilares relevantes
        if pillar_id == "P3":  # Seguridad
            for p in urgency_analysis["penalties"]:
                if "security" in p["type"] or "organized_crime" in p["type"]:
                    pillar_penalties.append(p)
        
        if pillar_id == "P4":  # Salud
            for p in urgency_analysis["penalties"]:
                if "ccss" in p["type"]:
                    pillar_penalties.append(p)
        
        if pillar_id == "P2":  # Empleo
            for p in urgency_analysis["penalties"]:
                if "employment" in p["type"]:
                    pillar_penalties.append(p)
        
        # Aplicar penalizaciones de pilares prioritarios faltantes
        for p in pillar_analysis["penalties"]:
            if p.get("pillar_id") == pillar_id:
                pillar_penalties.append(p)
        
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
    
    # Coverage de pilares prioritarios
    priority_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in PRIORITY_PILLARS
    )
    
    # Coverage de pilares críticos
    critical_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Calcular penalización total
    all_penalties = (
        fiscal_analysis["penalties"] + 
        urgency_analysis["penalties"] + 
        pillar_analysis["penalties"]
    )
    total_penalties = sum(p["value"] for p in all_penalties)
    
    # Notas
    notes = []
    
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        notes.append("🔴 ATACA REGLA FISCAL (-2)")
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        notes.append("🟠 PROPONE MÁS DEUDA (-1)")
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        notes.append("✅ Responsabilidad fiscal")
    
    # Notas de omisiones
    omitted = [k for k, v in urgency_analysis["coverage"].items() if not v["covered"]]
    if omitted:
        notes.append(f"⚠️ Omite: {', '.join(omitted)}")
    
    if pillar_analysis["missing_pillars"]:
        notes.append(f"❌ Sin propuesta: {', '.join(pillar_analysis['missing_pillars'])}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "fiscal_analysis": {
            "flags": fiscal_analysis["flags"],
            "total_penalty": fiscal_analysis["total_penalty"],
            "evidence": fiscal_analysis["evidence"][:2]
        },
        "omission_analysis": {
            "urgency_coverage": urgency_analysis["coverage"],
            "urgency_penalty": urgency_analysis["total_penalty"],
            "missing_pillars": pillar_analysis["missing_pillars"],
            "pillar_penalty": pillar_analysis["total_penalty"]
        },
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": round(weighted_sum, 4),
            "priority_weighted_sum": round(priority_weighted, 4),
            "critical_weighted_sum": round(critical_weighted, 4),
            "total_penalties_applied": total_penalties,
            "notes": " | ".join(notes) if notes else ""
        }
    }

# ====================================================================
# ANÁLISIS DETALLADO v6
# ====================================================================

def analyze_candidate_detailed(
    pages: List[Tuple[int, str]], 
    full_text: str, 
    pdf_id: str, 
    fiscal_analysis: Dict,
    urgency_analysis: Dict,
    pillar_analysis: Dict
) -> Dict:
    """Genera análisis detallado con nuevo sistema v6."""
    
    analysis = {
        "pdf_id": pdf_id,
        "total_pages": len(pages),
        "version": "v6_neutral_strict",
        "fiscal_flags": fiscal_analysis["flags"],
        "fiscal_evidence": fiscal_analysis["evidence"],
        "urgency_coverage": urgency_analysis["coverage"],
        "missing_priority_pillars": pillar_analysis["missing_pillars"],
        "strengths": [],
        "weaknesses": [],
        "risk_level": "BAJO"
    }
    
    risk_score = 0
    
    # Fortalezas y debilidades por urgencias
    for key, data in urgency_analysis["coverage"].items():
        if data["covered"]:
            analysis["strengths"].append(f"✅ Aborda: {data['description']}")
        else:
            analysis["weaknesses"].append(f"⚠️ No aborda: {data['description']}")
            risk_score += 1
    
    # Riesgo fiscal
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        analysis["weaknesses"].append("🔴 ATACA REGLA FISCAL - Riesgo alto para finanzas públicas")
        risk_score += 3
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        analysis["weaknesses"].append("🟠 Propone aumentar deuda pública")
        risk_score += 2
    
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        analysis["strengths"].append("✅ Demuestra responsabilidad fiscal")
        risk_score -= 1
    
    # Pilares prioritarios faltantes
    for pillar_id in pillar_analysis["missing_pillars"]:
        analysis["weaknesses"].append(f"❌ Sin propuesta en pilar prioritario {pillar_id}")
        risk_score += 1
    
    # Determinar nivel de riesgo
    if risk_score >= 5:
        analysis["risk_level"] = "ALTO"
    elif risk_score >= 2:
        analysis["risk_level"] = "MEDIO"
    else:
        analysis["risk_level"] = "BAJO"
    
    return analysis

# ====================================================================
# RANKING v6
# ====================================================================

def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    ranking_overall = sorted(
        [(cs["candidate_id"], cs["overall"]["weighted_sum"], cs["overall"]["total_penalties_applied"]) 
         for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    ranking_priority = sorted(
        [(cs["candidate_id"], cs["overall"]["priority_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    ranking_critical = sorted(
        [(cs["candidate_id"], cs["overall"]["critical_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "method_version": "v6_neutral_strict",
        "description": "Neutral (sin sesgo ideológico) + Estricto (penaliza omisiones)",
        "weights": PILLAR_WEIGHTS,
        "priority_pillars": list(PRIORITY_PILLARS),
        "critical_pillars": list(CRITICAL_PILLARS),
        "penalties_applied": {
            "fiscal": {
                "attacks_fiscal_rule": -2,
                "proposes_debt_increase": -1,
            },
            "omissions": {
                "ignores_security_operations": -1,
                "ignores_ccss_crisis": -1,
                "ignores_formal_employment": -0.5,
                "ignores_organized_crime": -0.5,
                "missing_priority_pillar": -0.5,
            }
        },
        "ranking_overall_weighted": [
            {
                "rank": i + 1, 
                "candidate_id": cid, 
                "weighted_sum": ws,
                "total_penalties": tp
            }
            for i, (cid, ws, tp) in enumerate(ranking_overall)
        ],
        "ranking_priority_weighted": [
            {"rank": i + 1, "candidate_id": cid, "priority_weighted_sum": pws}
            for i, (cid, pws) in enumerate(ranking_priority)
        ],
        "ranking_critical_weighted": [
            {"rank": i + 1, "candidate_id": cid, "critical_weighted_sum": ccws}
            for i, (cid, ccws) in enumerate(ranking_critical)
        ]
    }

# ====================================================================
# PROCESAMIENTO PRINCIPAL
# ====================================================================

def load_existing_candidates() -> Dict[str, str]:
    """Carga el archivo candidates.json existente."""
    candidates_file = os.path.join(DATA_DIR, "candidates.json")
    if os.path.exists(candidates_file):
        with open(candidates_file, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
            return {c["pdf_id"]: c["candidate_id"] for c in candidates}
    return {}

def process_all_pdfs():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    existing_candidates = load_existing_candidates()
    print(f"📋 Cargados {len(existing_candidates)} candidate_ids del archivo existente")
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    all_scores = []
    all_analysis = []
    
    print(f"Procesando {len(pdf_files)} planes de gobierno...")
    print("=" * 80)
    print("Modelo: v6 NEUTRAL + ESTRICTO")
    print("=" * 80)
    print("PENALIZACIONES FISCALES (objetivas - basadas en ley):")
    print("  • Atacar regla fiscal (Ley 9635): -2 puntos")
    print("  • Proponer más deuda: -1 punto")
    print("-" * 80)
    print("PENALIZACIONES POR OMISIÓN (urgencias nacionales):")
    print("  • No mencionar seguridad operativa: -1 punto")
    print("  • No mencionar crisis CCSS: -1 punto")
    print("  • No mencionar empleo formal: -0.5 puntos")
    print("  • No mencionar crimen organizado: -0.5 puntos")
    print("  • Por cada pilar prioritario sin propuesta: -0.5 puntos")
    print("=" * 80)
    print("NOTA: No se penaliza proponer impuestos (posición ideológica legítima)")
    print("=" * 80)
    
    for pdf_file in sorted(pdf_files):
        pdf_id = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(PLANES_DIR, pdf_file)
        
        print(f"\n📄 {pdf_id}...")
        
        pages, full_text = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print(f"   ⚠️ No se pudo extraer texto")
            continue
        
        info = extract_candidate_info(pages, pdf_id)
        
        if pdf_id in existing_candidates:
            candidate_id = existing_candidates[pdf_id]
        elif info["candidate_name"] != "no_especificado":
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
        
        # Análisis fiscal (v6: sin penalización por impuestos)
        fiscal_analysis = analyze_fiscal_responsibility(full_text)
        
        # Extraer propuestas
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        all_proposals.extend(proposals)
        
        # Análisis de omisiones v6
        urgency_analysis = analyze_urgency_omissions(full_text)
        pillar_analysis = analyze_pillar_omissions(proposals, candidate_id)
        
        # Calcular scores con todas las penalizaciones v6
        scores = calculate_candidate_score(
            proposals, candidate_id, full_text, 
            fiscal_analysis, urgency_analysis, pillar_analysis
        )
        all_scores.append(scores)
        
        # Análisis detallado
        analysis = analyze_candidate_detailed(
            pages, full_text, pdf_id, 
            fiscal_analysis, urgency_analysis, pillar_analysis
        )
        analysis["candidate_id"] = candidate_id
        all_analysis.append(analysis)
        
        # Resumen
        total_penalties = scores["overall"]["total_penalties_applied"]
        risk = analysis["risk_level"]
        risk_emoji = {"ALTO": "🔴", "MEDIO": "🟠", "BAJO": "🟢"}.get(risk, "⚪")
        
        print(f"   → Págs: {len(pages)} | Pilares: {len(best_by_pillar)}/10")
        print(f"   → Score: {scores['overall']['weighted_sum']:.1%} | Penalizaciones: {total_penalties}")
        print(f"   → Riesgo: {risk_emoji} {risk}")
    
    # Generar ranking
    ranking = generate_ranking(all_scores)
    
    print("\n" + "=" * 80)
    print("📊 RANKING FINAL - MODELO v6 NEUTRAL + ESTRICTO")
    print("=" * 80)
    print(f"{'#':<3} {'CANDIDATO':<20} {'SCORE':<10} {'PENALIZACIONES':<15} {'RIESGO'}")
    print("-" * 80)
    
    for entry in ranking["ranking_overall_weighted"]:
        analysis = next((a for a in all_analysis if a["candidate_id"] == entry["candidate_id"]), None)
        risk = analysis["risk_level"] if analysis else "?"
        risk_emoji = {"ALTO": "🔴", "MEDIO": "🟠", "BAJO": "🟢"}.get(risk, "⚪")
        
        print(f"{entry['rank']:<3} {entry['candidate_id']:<20} {entry['weighted_sum']:.1%}      {entry['total_penalties']:<15} {risk_emoji} {risk}")
    
    # Guardar archivos
    print("\n📁 Guardando archivos...")
    print("   ⚠️  candidates.json NO se regenera (mantener datos manuales)")
    
    outputs = {
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
    print("=" * 80)
    print("PROCESADOR DE PLANES v6.0 - NEUTRAL + ESTRICTO")
    print("10 pilares | OCR automático | Penalizaciones por omisión")
    print("=" * 80)
    result = process_all_pdfs()
    print("\n✅ PROCESO COMPLETADO")
