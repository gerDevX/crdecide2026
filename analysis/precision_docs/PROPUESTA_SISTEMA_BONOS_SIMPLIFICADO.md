# Propuesta: Sistema de Bonos Simplificado (Solo 3 Propuestas)

## Sistema Simplificado

### Cambio Principal

**Sistema anterior**: Premia 2 propuestas (+0.5) y 3+ propuestas (+1.0)  
**Sistema nuevo**: **Solo premia 3+ propuestas válidas (+1.0)**

### Justificación

1. **Más estricto**: Solo premia planes realmente detallados
2. **Más simple**: Un solo umbral (3 propuestas)
3. **Más claro**: Fácil de entender y comunicar
4. **Mantiene neutralidad**: Solo estructura, no contenido

---

## Sistema de Bonos Simplificado

### Bono por Múltiples Propuestas

| Número de Propuestas Válidas | Bono | Justificación |
|------------------------------|------|---------------|
| 1-2 propuestas | **0** | Sin bono (baseline) |
| **3+ propuestas** | **+1.0** | Plan detallado con cobertura amplia |

**Criterio de elegibilidad**:
- ✅ E = 1 (obligatorio)
- ✅ Score >= 2/4 (E + al menos una dimensión más)
- ✅ Mínimo 3 propuestas válidas para obtener bono

### Bonos por Calidad (Mantiene)

| Calidad | Bono | Justificación |
|---------|------|---------------|
| Propuesta completa (E+W+H+F = 4/4) | **+0.25** | Máxima completitud |
| Propuesta con financiamiento (E+...F, score >= 3) | **+0.1** | Indica seriedad |

**Nota**: Bonos de calidad se aplican independientemente del número de propuestas.

### Fórmula Simplificada

```
Score Base = Mejor propuesta score (0-4)
Bono Múltiples = 
  - 3+ propuestas válidas: +1.0
  - Menos de 3: 0
Bono Calidad = 
  - (Número de propuestas completas × 0.25)
  - (Número de propuestas con financiamiento × 0.1)

Score Efectivo = min(4.0, Score Base + Bono Múltiples + Bono Calidad)
Score Normalizado = Score Efectivo / 4.0
Score Ponderado = Score Normalizado × peso_pilar
```

---

## Ejemplos

### Ejemplo 1: Candidato con 1 propuesta
- Propuesta: 4/4 (E+W+H+F)
- Bono múltiples: 0 (solo 1 propuesta)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 4.25/4 → normalizado a 1.0 (máximo)

### Ejemplo 2: Candidato con 2 propuestas
- Mejor propuesta: 4/4
- 1 propuesta adicional válida (score 3/4)
- Bono múltiples: 0 (solo 2 propuestas, no alcanza 3)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 4.25/4 → normalizado a 1.0 (máximo)

### Ejemplo 3: Candidato con 3 propuestas
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas (scores 3/4, 3/4)
- Bono múltiples: +1.0 (tiene 3 propuestas)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 5.25/4 → normalizado a 1.0 (máximo)

### Ejemplo 4: Candidato con 3 propuestas (todas completas)
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas (scores 4/4, 4/4)
- Bono múltiples: +1.0 (tiene 3 propuestas)
- Bono calidad: +0.75 (3 completas × 0.25)
- **Score efectivo**: 5.75/4 → normalizado a 1.0 (máximo)

---

## Ventajas del Sistema Simplificado

### 1. Más Estricto
- ✅ Solo premia planes realmente detallados (3+ propuestas)
- ✅ No premia planes básicos (1-2 propuestas)
- ✅ Mejor diferenciación entre planes detallados y básicos

### 2. Más Simple
- ✅ Un solo umbral (3 propuestas)
- ✅ Fácil de entender y comunicar
- ✅ Menos confusión sobre cuándo se aplica el bono

### 3. Mantiene Neutralidad
- ✅ Solo premia estructura (D1-D4)
- ✅ No premia contenido ideológico
- ✅ Criterios objetivos para todos

### 4. Incentiva Planes Detallados
- ✅ Motiva a candidatos a desarrollar planes más completos
- ✅ Premia cobertura amplia de temas
- ✅ Valora profundidad en cada pilar

---

## Implementación Técnica

### Cambio en `calculate_candidate_score()`

```python
# Filtrar propuestas válidas (score >= 2, E=1)
valid_proposals = [
    p for p in candidate_proposals_pillar
    if p["dimensions"]["existence"] == 1 and 
    sum(p["dimensions"].values()) >= 2
]

# Mejor propuesta (score base)
if valid_proposals:
    best_prop = max(valid_proposals, key=lambda p: sum(p["dimensions"].values()))
    base_score = sum(best_prop["dimensions"].values())
else:
    base_score = 0

# Bono por múltiples propuestas: SOLO si tiene 3+
num_valid = len(valid_proposals)
if num_valid >= 3:
    bonus_multiple = 1.0
else:
    bonus_multiple = 0.0  # No bono para 1 o 2 propuestas

# Bono por calidad (mantiene)
complete_count = len([p for p in valid_proposals if sum(p["dimensions"].values()) == 4])
funding_count = len([
    p for p in valid_proposals 
    if p["dimensions"]["funding"] == 1 and sum(p["dimensions"].values()) >= 3
])

bonus_quality = (complete_count * 0.25) + (funding_count * 0.1)

# Score efectivo (máximo 4.0)
effective_score = min(4.0, base_score + bonus_multiple + bonus_quality)
```

---

## Impacto Esperado

### Candidatos que se Benefician

**Candidatos con planes muy detallados**:
- 3+ propuestas válidas por pilar
- Propuestas completas (E+W+H+F)
- **Mejora estimada**: +10-15% en score

**Candidatos con planes básicos**:
- 1-2 propuestas por pilar
- Sin cambio en su score (sin bono)
- **Mejora estimada**: 0%

### Diferenciación Mejorada

- **Planes detallados**: Reciben reconocimiento claro
- **Planes básicos**: No se benefician (sin penalización)
- **Mejor diferenciación**: Gap más claro entre planes detallados y básicos

---

## Validación de Neutralidad

### ✅ Criterios Objetivos

1. **Dimensiones D1-D4**: Objetivas y verificables
2. **Score mínimo**: Requisito claro (2/4)
3. **Umbral único**: 3 propuestas (claro y objetivo)
4. **Bonos fijos**: No dependen del contenido

### ✅ No Introduce Sesgos

1. **No premia contenido ideológico**: Solo estructura
2. **No discrimina por tema**: Aplica igual a todos los pilares
3. **No favorece partidos**: Criterios objetivos para todos

---

## Comparación: Sistema Anterior vs Simplificado

| Aspecto | Sistema Anterior | Sistema Simplificado |
|---------|------------------|----------------------|
| Bono 2 propuestas | +0.5 | 0 (sin bono) |
| Bono 3+ propuestas | +1.0 | +1.0 (igual) |
| Umbrales | 2 y 3 | Solo 3 |
| Complejidad | Media | Baja |
| Estrictez | Media | Alta |

---

## Recomendación Final

### ✅ Implementar Sistema Simplificado

**Razones**:
1. ✅ Más estricto: Solo premia planes realmente detallados
2. ✅ Más simple: Un solo umbral fácil de entender
3. ✅ Mantiene neutralidad: Solo estructura, no contenido
4. ✅ Mejor diferenciación: Gap claro entre planes detallados y básicos

### Próximos Pasos

1. ✅ Actualizar simulación con sistema simplificado
2. 🔄 Validar resultados
3. 🔄 Implementar si validación es positiva

---

**Fecha**: 2026-01-11  
**Estado**: Sistema simplificado propuesto, listo para validación
