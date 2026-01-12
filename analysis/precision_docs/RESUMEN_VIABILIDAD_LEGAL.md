# Resumen: Viabilidad Legal y Realista en Dimensiones

## Problema Identificado

### Situación Actual
Las dimensiones D1-D4 solo evalúan **estructura** (qué, cuándo, cómo, con qué), pero **no evalúan viabilidad**:
- ❌ No verifican si es legalmente posible
- ❌ No verifican si es constitucional
- ❌ No verifican si es realista según el contexto de Costa Rica

### Ejemplo del Problema

**Propuesta**: "Eliminar la Asamblea Legislativa y gobernar por decreto en primer año"

**Evaluación actual**:
- D1=1 (acción concreta) ✅
- D2=1 (tiene plazo) ✅
- D3=1 (describe mecanismo) ✅
- D4=1 (no requiere financiamiento) ✅
- **Score = 4/4** ❌ (INCORRECTO - es inconstitucional)

**Evaluación realista**:
- Requiere reforma constitucional ❌
- Viola separación de poderes ❌
- Plazo irrealista ❌
- **Score = 2.7/4** ✅ (CORRECTO)

---

## Solución Propuesta

### Mantener D1-D4 + Agregar Verificación de Viabilidad

**D1-D4**: Siguen evaluando estructura (neutral, objetivo)

**Nueva capa**: Verificación de viabilidad que ajusta el score

### Penalizaciones por Inviabilidad

| Tipo | Penalización | Ejemplo Costa Rica |
|------|--------------|-------------------|
| **Reforma constitucional** | -0.5 | "Eliminar Asamblea" requiere reforma (art. 195-196) |
| **Separación de poderes** | -1.0 | "Gobernar por decreto" viola art. 9, 11, 12 |
| **Financiamiento irrealista** | -0.5 | "10% PIB sin impuestos ni deuda" viola regla fiscal |
| **Plazo irrealista** | -0.3 | "Reforma constitucional en primer año" (requiere 2 períodos) |
| **Desconectado de realidad** | -0.3 | "100 hospitales en primer año" (capacidad limitada) |

---

## Ejemplos Específicos de Costa Rica

### Ejemplo 1: Inconstitucional

**Propuesta**: "Eliminar la Asamblea Legislativa y gobernar por decreto"

**Problemas**:
- ❌ Viola art. 9 (separación de poderes)
- ❌ Viola art. 105 (Asamblea es poder legislativo)
- ❌ Requiere reforma constitucional (art. 195-196)

**Penalización**: -1.0 (separación de poderes) + -0.5 (reforma constitucional) = **-1.5**

### Ejemplo 2: Irrealista Fiscalmente

**Propuesta**: "Invertir 10% del PIB en infraestructura sin aumentar impuestos ni deuda"

**Problemas**:
- ❌ 10% del PIB ≈ $6,000 millones (presupuesto total ≈ $20,000 millones)
- ❌ Violaría regla fiscal (Ley 9635)
- ❌ No es factible sin aumentar impuestos o deuda

**Penalización**: -0.5 (financiamiento irrealista)

### Ejemplo 3: Plazo Irrealista

**Propuesta**: "Reforma constitucional para eliminar reelección en primer año"

**Problemas**:
- ❌ Reforma constitucional requiere 2 períodos legislativos (art. 195)
- ❌ Mínimo 2 años (no es posible en "primer año")
- ❌ Requiere mayoría calificada (2/3) en 2 períodos

**Penalización**: -0.5 (reforma constitucional) + -0.3 (plazo irrealista) = **-0.8**

### Ejemplo 4: Desconectado de Realidad

**Propuesta**: "Construir 100 hospitales nuevos en primer año"

**Problemas**:
- ❌ Costa Rica tiene ~30 hospitales públicos actualmente
- ❌ Construir 100 en un año es físicamente imposible
- ❌ No considera capacidad de construcción, recursos humanos, etc.

**Penalización**: -0.3 (desconectado de realidad)

---

## Marco Legal de Referencia

### Constitución Política de Costa Rica

**Artículos relevantes**:
- **Art. 9**: Separación de poderes
- **Art. 11**: Prohibición de poderes extraordinarios
- **Art. 105**: Asamblea Legislativa es poder legislativo
- **Art. 195-196**: Reforma constitucional requiere 2 períodos legislativos

### Leyes Relevantes

**Ley 9635 (Regla Fiscal)**:
- Limita crecimiento del gasto público
- Requiere equilibrio fiscal
- Penalización si se propone violar: -2 puntos (ya implementado)

**Ley de Presupuesto**:
- Requiere aprobación de Asamblea
- No puede el Ejecutivo gastar sin aprobación legislativa

---

## Implementación Propuesta

### Fase 1: Verificación Básica (Recomendado Primero)

1. **Reforma constitucional** (-0.5)
   - Detectar: "reforma constitucional", "modificar constitución", "eliminar asamblea"
   
2. **Separación de poderes** (-1.0)
   - Detectar: "gobernar por decreto", "eliminar asamblea", "ejecutivo legisla"

### Fase 2: Verificación Avanzada

3. **Realismo fiscal** (-0.5)
   - Detectar: gastos grandes sin fuente, violación de regla fiscal

4. **Factibilidad temporal** (-0.3)
   - Detectar: reformas constitucionales en plazos cortos

### Fase 3: Refinamiento

5. **Ajustar umbrales** según resultados
6. **Validar con expertos** en derecho constitucional

---

## Impacto Esperado

### Propuestas que se Benefician

**Propuestas viables y realistas**:
- No reciben penalizaciones
- Mantienen su score alto
- Se distinguen de propuestas inviables

### Propuestas que se Penalizan

**Propuestas inviables**:
- Reciben penalizaciones por inviabilidad
- Score ajustado a la realidad
- Se distinguen de propuestas viables

### Mejora en Calidad

- ✅ Distingue propuestas viables de inviables
- ✅ Premia propuestas realistas
- ✅ Penaliza propuestas irrealistas
- ✅ Mantiene neutralidad (solo viabilidad, no contenido)

---

## Recomendación Final

### ✅ Implementar Verificación de Viabilidad

**Razones**:
1. ✅ **Mejora calidad**: Distingue propuestas viables de inviables
2. ✅ **Mantiene neutralidad**: Solo penaliza inviabilidad, no contenido
3. ✅ **Basado en ley**: Criterios objetivos (constitución, leyes)
4. ✅ **Transparente**: Criterios claros y documentados

### Próximo Paso

**Implementar Fase 1** (reforma constitucional + separación de poderes) y probar con datos reales.

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, listo para implementación
