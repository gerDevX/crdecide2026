# Propuesta: Sistema de Bonos por Múltiples Propuestas

## Análisis de la Situación Actual

### Sistema Actual (v6)
- **Extracción**: Identifica todas las propuestas por pilar
- **Selección**: Solo guarda la **mejor propuesta** por pilar
- **Scoring**: Usa solo 1 propuesta por pilar
- **Resultado**: Máximo 10 propuestas por candidato

### Limitaciones Identificadas

1. **Pérdida de información**: Se descartan propuestas válidas complementarias
2. **No premia profundidad**: Un candidato con 3 propuestas bien estructuradas recibe el mismo score que uno con 1
3. **No valora cobertura**: Múltiples propuestas pueden cubrir diferentes aspectos del mismo pilar

---

## Propuesta: Sistema de Bonos (No Penalizaciones)

### Principios Fundamentales

1. ✅ **Premiar, no penalizar**: Bonos adicionales por múltiples propuestas
2. ✅ **Neutralidad total**: Solo premia estructura (D1-D4), no contenido ideológico
3. ✅ **Calidad sobre cantidad**: Requiere dimensiones mínimas
4. ✅ **Cobertura amplia**: Múltiples propuestas pueden cubrir diferentes aspectos

---

## Sistema de Bonos Propuesto

### Criterios de Elegibilidad

**Propuesta válida para bono**:
- ✅ Dimensión E (Existencia) = 1 (obligatorio)
- ✅ Al menos una dimensión adicional (W, H o F) = 1
- ✅ Score mínimo: **2/4** (E + al menos una más)

**Propuesta no válida**:
- ❌ Solo E (sin W, H, F) → Score 1/4
- ❌ Score < 2/4

### Bonos por Múltiples Propuestas

| Número de Propuestas Válidas | Bono Adicional | Justificación |
|------------------------------|----------------|---------------|
| 1 propuesta | 0 (baseline) | Sin bono adicional |
| 2 propuestas | **+0.5 puntos** | Cobertura complementaria |
| 3+ propuestas | **+1.0 puntos** | Cobertura amplia y detallada |

**Límite**: Máximo 3 propuestas por pilar (evita spam)

### Bonos por Calidad de Dimensiones

**Propuesta completa** (E+W+H+F = 4/4):
- Bono: **+0.25 puntos** por cada propuesta completa

**Propuesta con financiamiento** (E+...F, score >= 3):
- Bono: **+0.1 puntos** (indica seriedad y viabilidad)

### Fórmula de Cálculo

```
Score Base = Mejor propuesta score (0-4)
Bono Múltiples = 
  - 2 propuestas válidas: +0.5
  - 3+ propuestas válidas: +1.0
Bono Calidad = 
  - Propuesta completa (4/4): +0.25
  - Propuesta con financiamiento (3+): +0.1

Score Efectivo = min(4.0, Score Base + Bono Múltiples + Bono Calidad)
Score Normalizado = Score Efectivo / 4.0
Score Ponderado = Score Normalizado × peso_pilar
```

**Ejemplo 1 - Candidato con 1 propuesta**:
- Propuesta: 4/4 (E+W+H+F)
- Bono múltiples: 0
- Bono calidad: +0.25
- **Score efectivo**: 4.25/4 → normalizado a 1.0 (máximo)

**Ejemplo 2 - Candidato con 3 propuestas**:
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas (scores 3/4, 3/4)
- Bono múltiples: +1.0
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 5.25/4 → normalizado a 1.0 (máximo)

**Ejemplo 3 - Candidato con 2 propuestas**:
- Mejor propuesta: 3/4 (E+H+F)
- 1 propuesta adicional válida (score 3/4)
- Bono múltiples: +0.5
- Bono calidad: +0.1 (con financiamiento)
- **Score efectivo**: 3.6/4 → normalizado a 0.9

---

## Implementación Técnica

### Cambio 1: Extracción de Múltiples Propuestas

**Archivo**: `process_plans_v6.py`  
**Función**: `extract_best_proposal_per_pillar()`

**Actual**:
```python
best_by_pillar[pillar_id] = proposals[0]  # Solo la mejor
```

**Propuesto**:
```python
# Filtrar propuestas válidas (score >= 2)
valid_proposals = [p for p in proposals if p["raw_score"] >= 2]
valid_proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)

# Guardar hasta 3 mejores propuestas
best_by_pillar[pillar_id] = valid_proposals[:3] if valid_proposals else []
```

### Cambio 2: Crear JSON con Múltiples Propuestas

**Archivo**: `process_plans_v6.py`  
**Función**: `create_proposals_json()`

**Actual**: Crea 1 propuesta por pilar

**Propuesto**: Crea hasta 3 propuestas por pilar (si hay disponibles)

```python
if pillar_id in best_by_pillar:
    proposals_list = best_by_pillar[pillar_id]  # Ahora es una lista
    for p in proposals_list[:3]:  # Máximo 3
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
        proposals.append(proposal)
```

### Cambio 3: Cálculo de Score con Bonos

**Archivo**: `process_plans_v6.py`  
**Función**: `calculate_candidate_score()`

**Nuevo código**:
```python
# Obtener todas las propuestas del candidato para este pilar
candidate_proposals_pillar = [
    p for p in proposals 
    if p["candidate_id"] == candidate_id and p["pillar_id"] == pillar_id
]

# Filtrar propuestas válidas (score >= 2)
valid_proposals = [
    p for p in candidate_proposals_pillar
    if p["dimensions"]["existence"] == 1 and sum(p["dimensions"].values()) >= 2
]

# Mejor propuesta (score base)
if valid_proposals:
    best_prop = max(valid_proposals, key=lambda p: sum(p["dimensions"].values()))
    base_score = sum(best_prop["dimensions"].values())
else:
    base_score = 0

# Bono por múltiples propuestas
num_valid = len(valid_proposals)
if num_valid >= 3:
    bonus_multiple = 1.0
elif num_valid >= 2:
    bonus_multiple = 0.5
else:
    bonus_multiple = 0.0

# Bono por calidad
complete_count = len([p for p in valid_proposals if sum(p["dimensions"].values()) == 4])
funding_count = len([p for p in valid_proposals if p["dimensions"]["funding"] == 1 and sum(p["dimensions"].values()) >= 3])

bonus_quality = (complete_count * 0.25) + (funding_count * 0.1)

# Score efectivo (máximo 4.0)
effective_score = min(4.0, base_score + bonus_multiple + bonus_quality)
```

---

## Ventajas del Sistema

### 1. Premia Profundidad sin Sesgo
- ✅ Candidatos con planes detallados reciben reconocimiento
- ✅ Basado en estructura objetiva (D1-D4), no contenido
- ✅ No discrimina por posición ideológica

### 2. Mantiene Neutralidad
- ✅ No premia contenido específico
- ✅ Solo premia completitud y estructura
- ✅ Aplica igual a todos los pilares

### 3. Mejora Cobertura
- ✅ Múltiples propuestas pueden cubrir diferentes aspectos
- ✅ Ejemplo: Seguridad puede incluir policía, cárceles, prevención
- ✅ Mejor representación del plan completo

### 4. Calidad sobre Cantidad
- ✅ Requiere score mínimo (2/4) para ser válida
- ✅ Premia propuestas completas (4/4)
- ✅ Límite de 3 propuestas evita spam

---

## Impacto Esperado

### Candidatos que se Beneficiarían

**Candidatos con planes detallados**:
- Múltiples propuestas bien estructuradas por pilar
- Propuestas completas (E+W+H+F)
- Cobertura amplia de temas
- **Mejora estimada**: +5-10% en score

**Candidatos con planes básicos**:
- Una propuesta por pilar
- Sin cambio en su score (sin bono, sin penalización)
- **Mejora estimada**: 0%

### Impacto en Rankings

- **Mejora diferenciación**: Planes detallados vs básicos
- **Mantiene equilibrio**: No cambia rankings de forma drástica
- **Premia calidad**: Incentiva propuestas completas

---

## Validación de Neutralidad

### ✅ Criterios Objetivos

1. **Dimensiones D1-D4**: Objetivas y verificables
2. **Score mínimo**: Requisito claro (2/4)
3. **Bonos fijos**: No dependen del contenido
4. **Límite de propuestas**: Evita abusos

### ✅ No Introduce Sesgos

1. **No premia contenido ideológico**: Solo estructura
2. **No discrimina por tema**: Aplica igual a todos los pilares
3. **No favorece partidos**: Criterios objetivos para todos

---

## Recomendaciones de Implementación

### Fase 1: Análisis y Simulación (Recomendado Primero)

1. **Analizar propuestas disponibles**:
   - Contar cuántas propuestas válidas hay realmente
   - Identificar candidatos que se beneficiarían

2. **Simular impacto**:
   - Calcular scores con sistema propuesto
   - Comparar rankings antes/después
   - Verificar que no introduce sesgos

### Fase 2: Implementación

1. **Modificar extracción**: Extraer hasta 3 propuestas por pilar
2. **Implementar bonos**: Sistema de bonos en cálculo de scores
3. **Actualizar JSON**: Guardar múltiples propuestas

### Fase 3: Validación

1. **Comparar resultados**: Rankings antes/después
2. **Ajustar umbrales**: Si es necesario
3. **Documentar cambios**: Actualizar metodología

---

## Umbrales Propuestos

### Propuesta Válida
- ✅ E = 1 (obligatorio)
- ✅ Score >= 2/4 (E + al menos una dimensión más)

### Bonos
- **Múltiples**: 2 propuestas = +0.5, 3+ = +1.0
- **Calidad**: Completa (4/4) = +0.25, Con financiamiento (3+) = +0.1

### Límites
- Máximo 3 propuestas por pilar
- Score efectivo máximo: 4.0 (normalizado a 1.0)

---

## Próximos Pasos

1. ✅ **Análisis completado** - Documento creado
2. 🔄 **Simular impacto** - Calcular scores con sistema propuesto
3. 🔄 **Implementar cambios** - Si la simulación es positiva
4. 🔄 **Validar resultados** - Comparar rankings

---

**Fecha**: 2026-01-11  
**Estado**: Propuesta lista para revisión e implementación
