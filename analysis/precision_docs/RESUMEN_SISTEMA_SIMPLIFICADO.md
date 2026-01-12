# Resumen: Sistema de Bonos Simplificado (Solo 3 Propuestas)

## Sistema Final Propuesto

### Regla Principal

**Solo se premia a candidatos que tienen 3 o más propuestas válidas por pilar**

### Criterios de Elegibilidad

**Propuesta válida**:
- ✅ E = 1 (obligatorio - debe ser propuesta concreta)
- ✅ Score >= 2/4 (E + al menos una dimensión más: W, H o F)

**Propuesta no válida**:
- ❌ Solo E (sin W, H, F) → Score 1/4
- ❌ Score < 2/4

---

## Sistema de Bonos

### Bono por Múltiples Propuestas

| Escenario | Bono | Condición |
|-----------|------|-----------|
| 1-2 propuestas válidas | **0** | Sin bono |
| **3+ propuestas válidas** | **+1.0** | Plan detallado |

### Bonos por Calidad (Adicionales)

| Calidad | Bono | Condición |
|---------|------|-----------|
| Propuesta completa (E+W+H+F = 4/4) | **+0.25** | Por cada propuesta completa |
| Propuesta con financiamiento (E+...F, score >= 3) | **+0.1** | Por cada propuesta con financiamiento |

**Nota**: Los bonos de calidad se aplican independientemente del número de propuestas.

---

## Fórmula de Cálculo

```
Score Base = Mejor propuesta score (0-4)

Bono Múltiples = 
  - Si tiene 3+ propuestas válidas: +1.0
  - Si tiene menos de 3: 0

Bono Calidad = 
  - (Número de propuestas completas × 0.25)
  - (Número de propuestas con financiamiento × 0.1)

Score Efectivo = min(4.0, Score Base + Bono Múltiples + Bono Calidad)
Score Normalizado = Score Efectivo / 4.0
Score Ponderado = Score Normalizado × peso_pilar
```

---

## Ejemplos Prácticos

### Ejemplo 1: Candidato con 1 propuesta
- Propuesta: 4/4 (E+W+H+F)
- Bono múltiples: **0** (solo 1 propuesta)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 4.25/4 → normalizado a **1.0** (máximo)

### Ejemplo 2: Candidato con 2 propuestas
- Mejor propuesta: 4/4
- 1 propuesta adicional válida (score 3/4)
- Bono múltiples: **0** (solo 2 propuestas, no alcanza 3)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 4.25/4 → normalizado a **1.0** (máximo)

### Ejemplo 3: Candidato con 3 propuestas ✅
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas (scores 3/4, 3/4)
- Bono múltiples: **+1.0** (tiene 3 propuestas)
- Bono calidad: +0.25 (1 completa)
- **Score efectivo**: 5.25/4 → normalizado a **1.0** (máximo)

### Ejemplo 4: Candidato con 3 propuestas completas ✅
- Mejor propuesta: 4/4
- 2 propuestas adicionales válidas (scores 4/4, 4/4)
- Bono múltiples: **+1.0** (tiene 3 propuestas)
- Bono calidad: +0.75 (3 completas × 0.25)
- **Score efectivo**: 5.75/4 → normalizado a **1.0** (máximo)

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

### Cambios Necesarios

#### 1. Modificar `extract_best_proposal_per_pillar()`

**Actual**:
```python
best_by_pillar[pillar_id] = proposals[0]  # Solo la mejor
```

**Nuevo**:
```python
# Filtrar propuestas válidas (score >= 2)
valid_proposals = [p for p in proposals if p["raw_score"] >= 2]
valid_proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)

# Guardar hasta 3 mejores propuestas válidas
best_by_pillar[pillar_id] = valid_proposals[:3] if valid_proposals else []
```

#### 2. Modificar `create_proposals_json()`

**Actual**: Crea 1 propuesta por pilar

**Nuevo**: Crea hasta 3 propuestas por pilar (si hay disponibles)

#### 3. Modificar `calculate_candidate_score()`

```python
# Obtener todas las propuestas válidas del candidato para este pilar
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

# Bono por calidad
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

## Validación de Neutralidad

### ✅ Criterios Objetivos

1. **Dimensiones D1-D4**: Objetivas y verificables
   - E: ¿Es propuesta concreta? (Sí/No)
   - W: ¿Tiene plazo? (Sí/No)
   - H: ¿Explica mecanismo? (Sí/No)
   - F: ¿Indica financiamiento? (Sí/No)

2. **Score mínimo**: Requisito claro (2/4)
   - No premia propuestas vagas
   - Requiere al menos estructura básica

3. **Umbral único**: 3 propuestas (claro y objetivo)
   - Fácil de entender
   - Fácil de comunicar

4. **Bonos fijos**: No dependen del contenido
   - Mismo bono para todos los pilares
   - No discrimina por tema

### ✅ No Introduce Sesgos

1. **No premia contenido ideológico**:
   - Solo estructura (D1-D4)
   - No importa si propone impuestos o recortes
   - No importa el tema específico

2. **No discrimina por tema**:
   - Aplica igual a todos los pilares
   - Mismo sistema para P1 (Fiscal) y P6 (Ambiente)

3. **No favorece partidos**:
   - Criterios objetivos para todos
   - Basado en estructura, no contenido

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

- **Planes detallados**: Reciben reconocimiento claro (+1.0 bono)
- **Planes básicos**: No se benefician (sin penalización)
- **Mejor diferenciación**: Gap más claro entre planes detallados y básicos

---

## Comparación: Sistema Anterior vs Simplificado

| Aspecto | Sistema Anterior | Sistema Simplificado |
|---------|------------------|----------------------|
| Bono 2 propuestas | +0.5 | **0** (sin bono) |
| Bono 3+ propuestas | +1.0 | **+1.0** (igual) |
| Umbrales | 2 y 3 | **Solo 3** |
| Complejidad | Media | **Baja** |
| Estrictez | Media | **Alta** |

---

## Próximos Pasos

### Paso 1: Validar Disponibilidad de Propuestas
- [ ] Verificar que hay múltiples propuestas disponibles en el texto
- [ ] Confirmar que el sistema actual solo está guardando 1 por pilar

### Paso 2: Implementar Extracción Múltiple
- [ ] Modificar `extract_best_proposal_per_pillar()` para extraer hasta 3
- [ ] Modificar `create_proposals_json()` para guardar múltiples

### Paso 3: Implementar Sistema de Bonos
- [ ] Modificar `calculate_candidate_score()` para aplicar bonos
- [ ] Solo premia si tiene 3+ propuestas válidas

### Paso 4: Probar y Validar
- [ ] Ejecutar procesamiento completo
- [ ] Comparar rankings antes/después
- [ ] Verificar neutralidad

---

## Conclusión

### ✅ Sistema Recomendado

**Implementar sistema simplificado** porque:

1. ✅ **Más estricto**: Solo premia planes realmente detallados
2. ✅ **Más simple**: Un solo umbral fácil de entender
3. ✅ **Mantiene neutralidad**: Solo estructura, no contenido
4. ✅ **Mejor diferenciación**: Gap claro entre planes detallados y básicos

---

**Fecha**: 2026-01-11  
**Estado**: Sistema simplificado definido, listo para implementación
