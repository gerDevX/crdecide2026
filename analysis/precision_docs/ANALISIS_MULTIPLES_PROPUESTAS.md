# Análisis: Sistema de Múltiples Propuestas

## Situación Actual

### Sistema Actual (v6)
- **Extracción**: Identifica todas las propuestas por pilar
- **Selección**: Solo usa la **mejor propuesta** por pilar (mayor score D1-D4)
- **Resultado**: 1 propuesta por pilar por candidato (máximo 10 propuestas)

### Análisis de Datos Actuales

**Propuestas reales identificadas**: 174 propuestas
**Propuestas usadas**: ~180 (10 por candidato × 18 candidatos con propuestas)

**Distribución de dimensiones**:
- E solo: 5.2% (propuestas básicas)
- E+H+F: 47.1% (propuestas con cómo y financiamiento)
- E+W+H+F: 2.9% (propuestas completas con todas las dimensiones)

---

## Problema Identificado

### Limitaciones del Sistema Actual

1. **Pérdida de información**: Se descartan propuestas válidas que podrían ser complementarias
2. **No premia profundidad**: Un candidato con 3 propuestas bien estructuradas en un pilar recibe el mismo score que uno con 1
3. **No valora cobertura**: Múltiples propuestas pueden cubrir diferentes aspectos del mismo pilar

### Ejemplo

**Candidato A** (P3 - Seguridad):
- Propuesta 1: Score 4/4 (E+W+H+F) - "Reforzar policía"
- Propuesta 2: Score 3/4 (E+H+F) - "Mejorar cárceles"
- Propuesta 3: Score 3/4 (E+H+F) - "Combate al narcotráfico"

**Sistema actual**: Solo usa Propuesta 1 → Score: 4/4

**Sistema propuesto**: Usa las 3 → Score mejorado por cobertura

---

## Propuesta: Sistema de Premios (No Penalizaciones)

### Principios

1. ✅ **Premiar, no penalizar**: Bonos por múltiples propuestas
2. ✅ **Neutralidad**: No sesgo ideológico
3. ✅ **Calidad sobre cantidad**: Las propuestas deben cumplir dimensiones mínimas
4. ✅ **Cobertura**: Múltiples propuestas pueden cubrir diferentes aspectos

---

## Sistema Propuesto: Bonos por Múltiples Propuestas

### Criterios de Elegibilidad

**Propuesta válida para bono**:
- ✅ Dimensión E (Existencia) = 1 (obligatorio)
- ✅ Al menos una dimensión adicional (W, H o F) = 1
- ✅ Score mínimo: 2/4

**Propuesta no válida**:
- ❌ Solo E (sin W, H, F)
- ❌ Score < 2/4

### Sistema de Bonos

#### Bono por Múltiples Propuestas en un Pilar

| Número de Propuestas Válidas | Bono Adicional | Justificación |
|------------------------------|----------------|---------------|
| 1 propuesta | 0 (baseline) | Sin bono |
| 2 propuestas | +0.5 puntos | Cobertura complementaria |
| 3+ propuestas | +1.0 puntos | Cobertura amplia y detallada |

**Límite**: Máximo 3 propuestas por pilar para evitar spam

#### Bono por Calidad de Dimensiones

**Propuesta completa** (E+W+H+F = 4/4):
- Bono: +0.25 puntos adicionales por propuesta completa

**Propuesta con financiamiento** (E+...F):
- Bono: +0.1 puntos (indica seriedad)

### Fórmula de Cálculo

```
Score por Pilar = 
  (Mejor propuesta score / 4) × peso_pilar
  + (Bono múltiples propuestas)
  + (Bono calidad dimensiones)
  - (Penalizaciones fiscales/omisiones)
```

**Ejemplo**:
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas: +0.5
- 1 propuesta completa (4/4): +0.25
- **Score efectivo**: 4.75/4 (normalizado a 1.0 máximo)

---

## Implementación Propuesta

### Cambios en `extract_best_proposal_per_pillar()`

**Actual**:
```python
best_by_pillar[pillar_id] = proposals[0]  # Solo la mejor
```

**Propuesto**:
```python
# Seleccionar hasta 3 mejores propuestas válidas
valid_proposals = [p for p in proposals if p["raw_score"] >= 2]
valid_proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)
best_by_pillar[pillar_id] = valid_proposals[:3]  # Hasta 3 propuestas
```

### Cambios en `create_proposals_json()`

**Actual**: Crea 1 propuesta por pilar

**Propuesto**: Crea hasta 3 propuestas por pilar (si hay disponibles)

### Cambios en `calculate_candidate_score()`

**Actual**: Usa solo la mejor propuesta

**Propuesto**:
```python
# Calcular score base (mejor propuesta)
base_score = mejor_propuesta_score

# Bono por múltiples propuestas
num_valid_proposals = len([p for p in propuestas_pilar if p["raw_score"] >= 2])
if num_valid_proposals >= 3:
    bonus = 1.0
elif num_valid_proposals >= 2:
    bonus = 0.5
else:
    bonus = 0.0

# Bono por calidad
complete_proposals = len([p for p in propuestas_pilar if p["raw_score"] == 4])
quality_bonus = complete_proposals * 0.25

# Score final
effective_score = min(4.0, base_score + bonus + quality_bonus)
```

---

## Ventajas del Sistema Propuesto

### 1. Premia Profundidad
- Candidatos con múltiples propuestas bien estructuradas reciben reconocimiento
- Incentiva planes de gobierno más detallados

### 2. Mantiene Neutralidad
- No penaliza posiciones ideológicas
- Solo premia estructura y completitud
- Basado en dimensiones objetivas (D1-D4)

### 3. Mejora Cobertura
- Múltiples propuestas pueden cubrir diferentes aspectos del mismo pilar
- Ejemplo: Seguridad puede incluir policía, cárceles, prevención

### 4. Calidad sobre Cantidad
- Requiere score mínimo (2/4) para ser válida
- Premia propuestas completas (4/4)
- Límite de 3 propuestas evita spam

---

## Análisis de Impacto Esperado

### Candidatos que se Beneficiarían

**Candidatos con planes detallados**:
- Múltiples propuestas bien estructuradas por pilar
- Cobertura amplia de temas
- Propuestas completas (E+W+H+F)

**Candidatos con planes básicos**:
- Una propuesta por pilar
- Sin cambio en su score (sin bono, sin penalización)

### Impacto en Rankings

**Estimación**:
- Candidatos con planes detallados: +5-10% en score
- Candidatos con planes básicos: Sin cambio
- Mejora diferenciación entre planes detallados y básicos

---

## Recomendaciones de Implementación

### Fase 1: Análisis y Validación (Recomendado)

1. **Analizar propuestas disponibles**:
   - Contar cuántas propuestas válidas hay realmente por candidato/pilar
   - Identificar candidatos que se beneficiarían

2. **Simular impacto**:
   - Calcular scores con sistema propuesto
   - Comparar con sistema actual
   - Verificar que no introduce sesgos

### Fase 2: Implementación Gradual

1. **Modificar extracción**:
   - Extraer hasta 3 propuestas por pilar
   - Mantener criterios de calidad (score >= 2)

2. **Implementar bonos**:
   - Bono por múltiples propuestas
   - Bono por calidad de dimensiones
   - Mantener penalizaciones existentes

3. **Validar resultados**:
   - Comparar rankings antes/después
   - Verificar que premia calidad, no cantidad

### Fase 3: Ajustes y Optimización

1. **Ajustar umbrales**:
   - Score mínimo para propuesta válida (actual: 2/4)
   - Bonos (actual: +0.5, +1.0)
   - Límite de propuestas (actual: 3)

2. **Documentar cambios**:
   - Actualizar metodología
   - Explicar sistema de bonos

---

## Consideraciones de Neutralidad

### ✅ Mantiene Neutralidad

1. **No premia contenido ideológico**: Solo estructura (D1-D4)
2. **No premia cantidad sin calidad**: Requiere score mínimo
3. **Premia completitud objetiva**: E+W+H+F es objetivo
4. **No discrimina por tema**: Aplica igual a todos los pilares

### ⚠️ Riesgos a Evitar

1. **No premiar propuestas repetitivas**: Verificar diversidad
2. **No premiar propuestas vagas**: Mantener criterios estrictos
3. **No crear incentivos perversos**: Límite de 3 propuestas

---

## Propuesta de Umbrales

### Propuesta Válida (Elegible para Bono)
- ✅ E = 1 (obligatorio)
- ✅ Al menos una de: W=1, H=1, F=1
- ✅ Score mínimo: 2/4

### Bono por Múltiples Propuestas
- 2 propuestas válidas: +0.5 puntos
- 3+ propuestas válidas: +1.0 puntos
- Límite: Máximo 3 propuestas por pilar

### Bono por Calidad
- Propuesta completa (4/4): +0.25 puntos
- Propuesta con financiamiento (E+...F): +0.1 puntos

---

## Próximos Pasos Recomendados

1. ✅ **Analizar datos actuales** (completado)
2. 🔄 **Simular impacto** del sistema propuesto
3. 🔄 **Implementar extracción de múltiples propuestas**
4. 🔄 **Implementar sistema de bonos**
5. 🔄 **Validar y ajustar umbrales**

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, listo para implementación
