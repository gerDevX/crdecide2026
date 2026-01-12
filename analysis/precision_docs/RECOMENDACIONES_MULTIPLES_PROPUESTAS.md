# Recomendaciones: Sistema de Múltiples Propuestas

## Análisis de la Situación

### Hallazgos Clave

1. **Hay múltiples propuestas disponibles**: 
   - Análisis de PPSO muestra: P3 tiene 15 propuestas totales, 13 válidas
   - P10 tiene 11 propuestas totales, 10 válidas
   - Muchos pilares tienen 3+ propuestas válidas disponibles

2. **Sistema actual solo usa 1 propuesta**:
   - Línea 852: `best_by_pillar[pillar_id] = proposals[0]`
   - Se descartan propuestas complementarias válidas

3. **Impacto de la simulación**:
   - Cambios significativos en rankings (+5-15% en algunos candidatos)
   - Candidatos con planes detallados se benefician más

---

## Recomendaciones Estratégicas

### ✅ Recomendación 1: Implementar Sistema de Bonos (NO Penalizaciones)

**Justificación**:
- Premia planes detallados sin penalizar planes básicos
- Mantiene neutralidad (solo estructura, no contenido)
- Mejora diferenciación entre planes detallados y básicos

**Sistema propuesto**:
- **Bono por múltiples propuestas**: 2 propuestas = +0.5, 3+ = +1.0
- **Bono por calidad**: Completa (4/4) = +0.25, Con financiamiento = +0.1
- **Límite**: Máximo 3 propuestas por pilar

### ✅ Recomendación 2: Criterios de Elegibilidad Estrictos

**Propuesta válida para bono**:
- ✅ E = 1 (obligatorio - debe ser propuesta concreta)
- ✅ Score >= 2/4 (E + al menos una dimensión más)
- ✅ No propuestas repetitivas (verificar diversidad)

**Propuesta no válida**:
- ❌ Solo E (sin W, H, F) → Score 1/4
- ❌ Score < 2/4
- ❌ Propuestas muy similares (duplicados)

### ✅ Recomendación 3: Implementación Gradual

**Fase 1: Análisis y Validación** (Recomendado primero)
1. ✅ Analizar propuestas disponibles (completado)
2. ✅ Simular impacto (completado)
3. 🔄 Validar que no introduce sesgos
4. 🔄 Ajustar umbrales si es necesario

**Fase 2: Implementación**
1. Modificar `extract_best_proposal_per_pillar()` para extraer hasta 3
2. Modificar `create_proposals_json()` para guardar múltiples
3. Modificar `calculate_candidate_score()` para aplicar bonos

**Fase 3: Validación**
1. Comparar rankings antes/después
2. Verificar neutralidad
3. Documentar cambios

---

## Sistema de Bonos Detallado

### Bonos por Múltiples Propuestas

| Escenario | Bono | Justificación |
|-----------|------|---------------|
| 1 propuesta válida | 0 | Baseline (sin bono) |
| 2 propuestas válidas | +0.5 | Cobertura complementaria |
| 3+ propuestas válidas | +1.0 | Cobertura amplia y detallada |

**Límite**: Máximo 3 propuestas por pilar (evita spam)

### Bonos por Calidad

| Calidad | Bono | Justificación |
|---------|------|---------------|
| Propuesta completa (E+W+H+F = 4/4) | +0.25 | Máxima completitud |
| Propuesta con financiamiento (E+...F, score >= 3) | +0.1 | Indica seriedad y viabilidad |

**Límite**: Bonos de calidad se aplican por propuesta (máximo 3)

### Fórmula Final

```
Score Base = Mejor propuesta score (0-4)
Bono Múltiples = 
  - 2 propuestas válidas: +0.5
  - 3+ propuestas válidas: +1.0
Bono Calidad = 
  - (Número de propuestas completas × 0.25)
  - (Número de propuestas con financiamiento × 0.1)

Score Efectivo = min(4.0, Score Base + Bono Múltiples + Bono Calidad)
Score Normalizado = Score Efectivo / 4.0
Score Ponderado = Score Normalizado × peso_pilar
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

3. **Bonos fijos**: No dependen del contenido
   - Mismo bono para todos los pilares
   - No discrimina por tema

4. **Límite de propuestas**: Evita abusos
   - Máximo 3 propuestas por pilar
   - Evita spam de propuestas repetitivas

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

## Impacto Esperado (Basado en Simulación)

### Candidatos que se Benefician Más

**Candidatos con planes detallados**:
- Múltiples propuestas bien estructuradas
- Propuestas completas (E+W+H+F)
- Cobertura amplia de temas
- **Mejora estimada**: +8-15% en score

**Candidatos con planes básicos**:
- Una propuesta por pilar
- Sin cambio en su score (sin bono, sin penalización)
- **Mejora estimada**: 0-2%

### Cambios en Rankings

**Basado en simulación**:
- Cambios moderados en posiciones (1-5 posiciones)
- Candidatos con planes detallados suben
- Candidatos con planes básicos se mantienen o bajan ligeramente
- **Mejora diferenciación**: Planes detallados vs básicos

---

## Consideraciones Importantes

### ⚠️ Riesgos a Evitar

1. **Propuestas repetitivas**:
   - Verificar diversidad de contenido
   - No premiar propuestas muy similares

2. **Propuestas vagas**:
   - Mantener criterios estrictos (score >= 2)
   - Requerir al menos una dimensión adicional

3. **Incentivos perversos**:
   - Límite de 3 propuestas evita spam
   - Score mínimo evita propuestas vacías

### ✅ Ventajas del Sistema

1. **Premia profundidad sin sesgo**:
   - Basado en estructura objetiva
   - No discrimina por contenido

2. **Mantiene neutralidad**:
   - Solo premia completitud
   - No premia posiciones ideológicas

3. **Mejora cobertura**:
   - Múltiples propuestas cubren diferentes aspectos
   - Mejor representación del plan completo

---

## Pasos Recomendados

### Paso 1: Validar Simulación (Recomendado)

1. Revisar resultados de simulación
2. Verificar que cambios son razonables
3. Ajustar umbrales si es necesario

### Paso 2: Implementar Extracción Múltiple

1. Modificar `extract_best_proposal_per_pillar()`:
   - Extraer hasta 3 propuestas válidas
   - Filtrar por score >= 2

2. Modificar `create_proposals_json()`:
   - Guardar hasta 3 propuestas por pilar
   - Mantener estructura actual

### Paso 3: Implementar Sistema de Bonos

1. Modificar `calculate_candidate_score()`:
   - Calcular bonos por múltiples propuestas
   - Calcular bonos por calidad
   - Aplicar a score efectivo

2. Validar resultados:
   - Comparar rankings
   - Verificar neutralidad

### Paso 4: Documentar y Publicar

1. Actualizar metodología
2. Explicar sistema de bonos
3. Publicar cambios

---

## Umbrales Propuestos (Ajustables)

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

## Conclusión

### ✅ Sistema Recomendado

**Implementar sistema de bonos por múltiples propuestas** porque:

1. ✅ Premia planes detallados sin penalizar básicos
2. ✅ Mantiene neutralidad total (solo estructura)
3. ✅ Mejora diferenciación entre planes
4. ✅ Basado en criterios objetivos (D1-D4)

### Próximos Pasos

1. ✅ **Análisis completado**
2. ✅ **Simulación completada**
3. 🔄 **Validar resultados de simulación**
4. 🔄 **Implementar si validación es positiva**

---

**Fecha**: 2026-01-11  
**Estado**: Recomendaciones listas para implementación
