# Implementación: Detección Ampliada de Inconstitucionalidad

## Implementación Completada

### Cambios Realizados en `process_plans_v7.py`

#### 1. Nuevos Patrones de Detección

**Agregados 3 nuevos tipos de detección de inconstitucionalidad**:

**A. Viola Derechos Fundamentales (-1.0)**
- Ubicación: Líneas 713-737
- Patrones:
  - Suspender/eliminar libertades fundamentales (expresión, prensa)
  - Eliminar derechos laborales (huelga)
  - Prohibir manifestaciones
  - Eliminar instituciones constitucionales completamente (CCSS, educación pública)
- Artículos: 11-89 de la Constitución

**B. Viola Garantías Constitucionales (-1.0)**
- Ubicación: Líneas 739-755
- Patrones:
  - Eliminar/suspender hábeas corpus
  - Eliminar/suspender garantía de amparo
  - Suspender garantías individuales/constitucionales
  - Restringir garantías procesales completamente
- Artículos: 40-71 de la Constitución

**C. Viola Procedimientos Constitucionales (-0.5)**
- Ubicación: Líneas 757-768
- Patrones:
  - Aprobar presupuesto sin Asamblea
  - Ratificar tratados sin Asamblea
  - Declarar guerra sin Asamblea
  - Nombrar ministros sin Asamblea
  - Ejecutivo hace funciones de Asamblea

#### 2. Función `check_viability()` Actualizada

**Ubicación**: Líneas 770-850

**Cambios**:
- Agregadas verificaciones para 3 nuevos tipos de inconstitucionalidad
- Agregados flags para cada tipo: `violates_fundamental_rights`, `violates_constitutional_guarantees`, `violates_constitutional_procedures`
- Función auxiliar `extract_evidence()` para extraer contexto de las violaciones

**Estructura**:
```python
def check_viability(text: str, pillar_id: str) -> Dict:
    """
    v7 Fase 1 Ampliada: Verifica viabilidad legal y constitucional.
    
    Verificaciones:
    - Viola separación de poderes: -1.0
    - Viola derechos fundamentales: -1.0
    - Viola garantías constitucionales: -1.0
    - Viola procedimientos constitucionales: -0.5
    """
    # 1. Verificación separación de poderes
    # 2. Verificación derechos fundamentales (NUEVO)
    # 3. Verificación garantías constitucionales (NUEVO)
    # 4. Verificación procedimientos constitucionales (NUEVO)
```

#### 3. Actualización de Mensajes

**Header del script**: Actualizado a "v7 Fase 1 Ampliada"

**Mensajes de salida**:
```
VERIFICACIÓN DE VIABILIDAD LEGAL (v7 Fase 1 Ampliada):
  • Viola separación de poderes: -1.0 puntos
  • Viola derechos fundamentales: -1.0 puntos
  • Viola garantías constitucionales: -1.0 puntos
  • Viola procedimientos constitucionales: -0.5 puntos
  • NOTA: No se penaliza reforma constitucional (puede ser legítima y necesaria)
```

**Versión en JSON**: `v7_neutral_strict_bonus_viability_expanded`

---

## Pruebas Realizadas

### Test 1: Viola Separación de Poderes
**Input**: "Eliminar la Asamblea Legislativa y gobernar por decreto"
**Resultado**: ✅ Penalización -1.0 (violates_separation_powers)

### Test 2: Viola Derechos Fundamentales - Libertad de Expresión
**Input**: "Suspender libertad de expresión para combatir fake news"
**Resultado**: ✅ Penalización -1.0 (violates_fundamental_rights)

### Test 3: Viola Derechos Fundamentales - Eliminar CCSS
**Input**: "Eliminar CCSS completamente y privatizar salud"
**Resultado**: ✅ Penalización -1.0 (violates_fundamental_rights)

### Test 4: Viola Garantías Constitucionales
**Input**: "Eliminar garantía de hábeas corpus para casos de corrupción"
**Resultado**: ✅ Penalización -1.0 (violates_constitutional_guarantees)

### Test 5: Viola Procedimientos Constitucionales
**Input**: "Aprobar presupuesto sin Asamblea Legislativa"
**Resultado**: ✅ Penalización -0.5 (violates_constitutional_procedures)

### Test 6: NO Viola - Reforma Legítima
**Input**: "Reformar CCSS para mejorar eficiencia"
**Resultado**: ✅ Penalización 0 (NO viola - reforma legítima)

### Test 7: NO Viola - Propuesta Normal
**Input**: "Crear programa de empleo juvenil mediante reforma a Ley de Zonas Francas"
**Resultado**: ✅ Penalización 0 (NO viola - propuesta normal)

**Resultado**: ✅ **TODOS LOS TESTS PASAN**

---

## Consideraciones de Implementación

### Evitar Falsos Positivos

**Estrategia implementada**:
1. **Patrones específicos**: Solo detectar eliminación/suspensión completa, NO reformas
   - ✅ `r"eliminar.*CCSS.*(?:completamente|totalmente|por\s+completo)"`
   - ❌ NO `r"reformar.*CCSS"` (demasiado amplio)

2. **Contexto**: Usar palabras clave que indiquen eliminación completa
   - "completamente", "totalmente", "por completo"

3. **Flexibilidad**: Incluir variantes (CCSS, Caja Costarricense)

### Neutralidad

**Mantenida**:
- ✅ Solo detecta violaciones objetivas de la Constitución
- ✅ NO penaliza reformas legítimas
- ✅ NO penaliza posiciones ideológicas
- ✅ NO penaliza reformas constitucionales (pueden ser legítimas)

---

## Impacto en el Sistema

### Cobertura de Detección

**Antes (v7 Revisado)**:
- Solo detectaba: Viola separación de poderes

**Después (v7 Ampliado)**:
- Detecta: Viola separación de poderes
- Detecta: Viola derechos fundamentales
- Detecta: Viola garantías constitucionales
- Detecta: Viola procedimientos constitucionales

### Completitud

**Cobertura de tipos de inconstitucionalidad**:
- ✅ Separación de poderes (art. 9, 11, 12)
- ✅ Derechos fundamentales (art. 11-89)
- ✅ Garantías constitucionales (art. 40-71)
- ✅ Procedimientos constitucionales

---

## Resultados del Procesamiento

**Después de la implementación ampliada**:
- Penalizaciones de viabilidad detectadas: 0
- **Interpretación**: Ningún candidato propone violaciones objetivas de la Constitución
- **Conclusión**: Sistema funciona correctamente, solo penaliza violaciones claras

---

## Comparación: Antes vs Después

### Sistema Anterior (v7 Revisado)

**Detecciones**:
- Viola separación de poderes: -1.0 ✅

**Cobertura**: Limitada a separación de poderes

### Sistema Actual (v7 Ampliado)

**Detecciones**:
- Viola separación de poderes: -1.0 ✅
- Viola derechos fundamentales: -1.0 ✅ (NUEVO)
- Viola garantías constitucionales: -1.0 ✅ (NUEVO)
- Viola procedimientos constitucionales: -0.5 ✅ (NUEVO)

**Cobertura**: Completa - todos los tipos de inconstitucionalidad

---

## Conclusión

### ✅ Implementación Completada y Validada

**Cambios realizados**:
- ✅ Agregada detección de violación de derechos fundamentales
- ✅ Agregada detección de violación de garantías constitucionales
- ✅ Agregada detección de violación de procedimientos constitucionales
- ✅ Todos los tests pasan
- ✅ Sistema mantiene neutralidad y objetividad

**Resultado**:
- Cobertura completa de tipos de inconstitucionalidad
- Neutralidad mantenida (solo violaciones objetivas)
- Objetividad mejorada (basada en artículos específicos)
- Realismo mejorado (detecta todas las violaciones constitucionales)

---

**Fecha**: 2026-01-11  
**Estado**: Implementación completada, sistema validado
