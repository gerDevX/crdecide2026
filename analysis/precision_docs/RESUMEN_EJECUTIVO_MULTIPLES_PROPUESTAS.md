# Resumen Ejecutivo: Sistema de Múltiples Propuestas

## Situación Actual vs Propuesta

### ❌ Sistema Actual
- **Extracción**: Identifica todas las propuestas
- **Selección**: Solo guarda la **mejor** propuesta por pilar
- **Scoring**: Usa 1 propuesta por pilar
- **Resultado**: Máximo 10 propuestas por candidato

### ✅ Sistema Propuesto
- **Extracción**: Identifica todas las propuestas
- **Selección**: Guarda hasta **3 mejores** propuestas válidas por pilar
- **Scoring**: Usa múltiples propuestas con **sistema de bonos**
- **Resultado**: Hasta 30 propuestas por candidato (3 × 10 pilares)

---

## Hallazgos del Análisis

### Propuestas Disponibles (Ejemplo: PPSO)

| Pilar | Total | Válidas (score >= 2) | Actualmente Usadas |
|-------|-------|----------------------|-------------------|
| P3 (Seguridad) | 15 | 13 | 1 |
| P10 (Infraestructura) | 11 | 10 | 1 |
| P2 (Empleo) | 7 | 7 | 1 |
| P5 (Educación) | 11 | 10 | 1 |

**Conclusión**: Hay **múltiples propuestas válidas disponibles** que no se están usando.

### Impacto de la Simulación

**Cambios en rankings**:
- Candidatos con planes detallados: +8-15% en score
- Candidatos con planes básicos: 0-2% (sin cambio significativo)
- Mejora diferenciación entre planes detallados y básicos

---

## Sistema de Bonos Propuesto

### Bonos por Múltiples Propuestas

| Propuestas Válidas | Bono | Ejemplo |
|---------------------|------|---------|
| 1 propuesta | 0 | Baseline |
| 2 propuestas | **+0.5** | Cobertura complementaria |
| 3+ propuestas | **+1.0** | Cobertura amplia |

### Bonos por Calidad

| Calidad | Bono | Ejemplo |
|---------|------|---------|
| Completa (E+W+H+F = 4/4) | **+0.25** | Propuesta con todas las dimensiones |
| Con financiamiento (E+...F, score >= 3) | **+0.1** | Indica seriedad |

### Criterios de Elegibilidad

**Propuesta válida para bono**:
- ✅ E = 1 (obligatorio)
- ✅ Score >= 2/4 (E + al menos una dimensión más)

**Propuesta no válida**:
- ❌ Solo E (score 1/4)
- ❌ Score < 2/4

---

## Ventajas del Sistema

### 1. Premia Profundidad sin Sesgo
- ✅ Candidatos con planes detallados reciben reconocimiento
- ✅ Basado en estructura objetiva (D1-D4), no contenido
- ✅ No discrimina por posición ideológica

### 2. Mantiene Neutralidad Total
- ✅ Solo premia estructura, no contenido
- ✅ No premia posiciones ideológicas específicas
- ✅ Aplica igual a todos los pilares

### 3. Mejora Cobertura
- ✅ Múltiples propuestas cubren diferentes aspectos
- ✅ Ejemplo: Seguridad puede incluir policía, cárceles, prevención
- ✅ Mejor representación del plan completo

### 4. Calidad sobre Cantidad
- ✅ Requiere score mínimo (2/4)
- ✅ Premia propuestas completas (4/4)
- ✅ Límite de 3 propuestas evita spam

---

## Recomendaciones Finales

### ✅ Recomendación Principal: IMPLEMENTAR

**Razones**:
1. Hay múltiples propuestas disponibles que no se están usando
2. El sistema premia calidad sin penalizar planes básicos
3. Mantiene neutralidad total (solo estructura)
4. Mejora diferenciación entre planes detallados y básicos

### Pasos Concretos

#### Paso 1: Validar Simulación (1-2 horas)
- [ ] Revisar resultados de `simulate_multiple_proposals.py`
- [ ] Verificar que cambios son razonables
- [ ] Ajustar umbrales si es necesario

#### Paso 2: Implementar Extracción Múltiple (2-3 horas)
- [ ] Modificar `extract_best_proposal_per_pillar()`:
  - Cambiar `proposals[0]` a `proposals[:3]`
  - Filtrar por score >= 2
- [ ] Modificar `create_proposals_json()`:
  - Guardar hasta 3 propuestas por pilar
  - Mantener estructura actual

#### Paso 3: Implementar Sistema de Bonos (3-4 horas)
- [ ] Modificar `calculate_candidate_score()`:
  - Calcular bonos por múltiples propuestas
  - Calcular bonos por calidad
  - Aplicar a score efectivo
- [ ] Validar que no rompe código existente

#### Paso 4: Probar y Validar (2-3 horas)
- [ ] Ejecutar procesamiento completo
- [ ] Comparar rankings antes/después
- [ ] Verificar neutralidad
- [ ] Ajustar umbrales si es necesario

#### Paso 5: Documentar (1 hora)
- [ ] Actualizar metodología
- [ ] Explicar sistema de bonos
- [ ] Publicar cambios

**Tiempo total estimado**: 9-13 horas

---

## Umbrales Propuestos (Ajustables)

### Propuesta Válida
- ✅ E = 1 (obligatorio)
- ✅ Score >= 2/4

### Bonos
- **Múltiples**: 2 propuestas = +0.5, 3+ = +1.0
- **Calidad**: Completa (4/4) = +0.25, Con financiamiento (3+) = +0.1

### Límites
- Máximo 3 propuestas por pilar
- Score efectivo máximo: 4.0

---

## Consideraciones de Neutralidad

### ✅ Mantiene Neutralidad

1. **Criterios objetivos**: Solo estructura (D1-D4)
2. **No premia contenido**: No importa qué propone, solo cómo está estructurado
3. **Aplica igual**: Mismo sistema para todos los pilares y candidatos
4. **No discrimina**: No favorece ninguna posición ideológica

### ⚠️ Riesgos Mitigados

1. **Propuestas repetitivas**: Límite de 3 y verificación de diversidad
2. **Propuestas vagas**: Score mínimo de 2/4
3. **Incentivos perversos**: Límites claros y criterios estrictos

---

## Conclusión

### ✅ Sistema Recomendado para Implementación

**Implementar sistema de bonos por múltiples propuestas** porque:

1. ✅ **Premia planes detallados** sin penalizar básicos
2. ✅ **Mantiene neutralidad** total (solo estructura)
3. ✅ **Mejora diferenciación** entre planes
4. ✅ **Basado en criterios objetivos** (D1-D4)
5. ✅ **Hay propuestas disponibles** que no se están usando

### Próximo Paso Inmediato

**Validar simulación** y luego implementar si los resultados son positivos.

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completo, listo para decisión de implementación
