# Implementación: Verificación de Viabilidad Legal - Fase 1

## Implementación Completada

### Cambios Realizados en `process_plans_v7.py`

#### 1. Nueva Función: `check_viability()`

**Ubicación**: Líneas 648-720

**Funcionalidad**:
- Verifica si una propuesta requiere reforma constitucional (-0.5)
- Verifica si una propuesta viola separación de poderes (-1.0)
- Retorna penalizaciones y flags de viabilidad

**Patrones de Detección**:

**Reforma Constitucional**:
- "reforma constitucional"
- "modificar la constitución"
- "eliminar asamblea legislativa"
- "eliminar poder judicial"
- "disolver asamblea"
- etc.

**Separación de Poderes**:
- "gobernar por decreto sin asamblea"
- "ejecutivo legisla"
- "presidente juzga"
- "concentración de poderes"
- etc.

#### 2. Integración en `calculate_candidate_score()`

**Ubicación**: Líneas 1000-1010

**Cambios**:
- Se aplica verificación de viabilidad a la mejor propuesta de cada pilar
- Las penalizaciones de viabilidad se agregan a `pillar_penalties`
- Se incluyen en el cálculo del `effective_score`
- Se guardan flags y penalización en `pillar_scores`

**Código agregado**:
```python
# v7 Fase 1: Verificación de viabilidad legal
viability_analysis = check_viability(best_prop_text, pillar_id)
viability_penalty = viability_analysis["total_penalty"]
viability_flags = viability_analysis["flags"]
pillar_penalties.extend(viability_analysis["penalties"])
```

#### 3. Actualización de Estructura de Datos

**En `pillar_scores`**:
- `viability_penalty`: Penalización total por viabilidad
- `viability_flags`: Flags de viabilidad detectados
- `penalties`: Incluye ahora penalizaciones de viabilidad

#### 4. Actualización de Mensajes

**Header del script**: Actualizado a "v7 NEUTRAL + ESTRICTO + BONOS + VIABILIDAD LEGAL"

**Mensajes de salida**: Incluyen información sobre verificación de viabilidad

**Versión en JSON**: `v7_neutral_strict_bonus_viability`

---

## Pruebas Realizadas

### Test 1: Reforma Constitucional
**Input**: "Eliminar la Asamblea Legislativa y gobernar por decreto"
**Resultado**: ✅ Penalización -0.5 (requiere reforma constitucional)

### Test 2: Separación de Poderes
**Input**: "Gobernar por decreto sin la Asamblea Legislativa"
**Resultado**: ✅ Penalización -1.0 (viola separación de poderes)

### Test 3: Propuesta Normal
**Input**: "Crear programa de empleo juvenil mediante reforma a Ley de Zonas Francas"
**Resultado**: ✅ Penalización 0 (sin problemas de viabilidad)

### Test 4: Procesamiento Completo
**Resultado**: ✅ Sistema procesa todos los PDFs correctamente
**Detectado**: 1 candidato con penalización de viabilidad (`luis-amadorjimenez` en P1)

---

## Resultados de la Prueba

### Penalizaciones Detectadas

**Candidato**: `luis-amadorjimenez`
**Pilar**: P1 (Responsabilidad Fiscal)
**Problema**: Requiere reforma constitucional
**Penalización**: -0.5
**Score Base**: 3/4
**Score Efectivo**: Ajustado con penalización

---

## Impacto en Scoring

### Fórmula Actualizada

```
Score Base = D1 + D2 + D3 + D4 (0-4)
Bono Múltiples = +1.0 (si tiene 3+ propuestas)
Bono Calidad = +0.25 (completas) + +0.1 (con financiamiento)
Penalización Viabilidad = -0.5 (reforma constitucional) o -1.0 (separación de poderes)
Otras Penalizaciones = Fiscal, omisiones, etc.

Score Efectivo = max(0, min(4.0, Score Base + Bonos + Penalizaciones))
```

### Ejemplo de Cálculo

**Propuesta con reforma constitucional**:
- Score Base: 3/4
- Bono Múltiples: 0
- Bono Calidad: 0
- Penalización Viabilidad: -0.5
- **Score Efectivo: 2.5/4**

**Propuesta que viola separación de poderes**:
- Score Base: 4/4
- Bono Múltiples: 0
- Bono Calidad: 0
- Penalización Viabilidad: -1.0
- **Score Efectivo: 3.0/4**

---

## Ventajas de la Implementación

### 1. Mantiene Neutralidad
- ✅ No penaliza contenido ideológico
- ✅ Solo penaliza inviabilidad legal/constitucional
- ✅ Criterios objetivos basados en constitución

### 2. Mejora Calidad
- ✅ Distingue propuestas viables de inviables
- ✅ Penaliza propuestas inconstitucionales
- ✅ Ajusta scores a la realidad legal

### 3. Transparente
- ✅ Criterios claros y documentados
- ✅ Flags visibles en JSON
- ✅ Evidencia guardada en penalizaciones

---

## Próximos Pasos (Fase 2)

### Verificaciones Adicionales a Implementar

1. **Realismo Fiscal** (-0.5)
   - Detectar financiamiento irrealista
   - Verificar violación de regla fiscal

2. **Factibilidad Temporal** (-0.3)
   - Detectar plazos irrealistas para reformas constitucionales
   - Verificar factibilidad según complejidad

3. **Contexto Nacional** (-0.3)
   - Detectar desconexión con realidad del país
   - Verificar capacidad institucional

---

## Archivos Modificados

1. ✅ `process_plans_v7.py` - Función `check_viability()` agregada
2. ✅ `process_plans_v7.py` - Integración en `calculate_candidate_score()`
3. ✅ `process_plans_v7.py` - Actualización de mensajes y versiones

---

## Validación

### ✅ Funcionalidad Verificada

1. ✅ Función `check_viability()` funciona correctamente
2. ✅ Penalizaciones se aplican al score efectivo
3. ✅ Flags se guardan en estructura de datos
4. ✅ Procesamiento completo funciona sin errores
5. ✅ Penalizaciones detectadas en datos reales

### ✅ Neutralidad Verificada

1. ✅ No penaliza contenido ideológico
2. ✅ Solo penaliza inviabilidad legal/constitucional
3. ✅ Criterios objetivos y documentados

---

## Conclusión

### ✅ Fase 1 Implementada Exitosamente

**Implementación completada**:
- ✅ Verificación de reforma constitucional
- ✅ Verificación de separación de poderes
- ✅ Integración en sistema de scoring
- ✅ Pruebas realizadas y validadas

**Resultado**:
- Sistema detecta propuestas inviables legalmente
- Penalizaciones se aplican correctamente
- Neutralidad mantenida
- Calidad mejorada

---

**Fecha**: 2026-01-11  
**Estado**: Fase 1 implementada y validada, lista para Fase 2
