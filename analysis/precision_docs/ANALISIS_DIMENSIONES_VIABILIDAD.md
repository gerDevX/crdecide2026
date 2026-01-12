# Análisis: Dimensiones D1-D4 y Viabilidad Legal/Realista

## Situación Actual

### Dimensiones Actuales (D1-D4)

| Dimensión | Nombre | Evaluación Actual | Limitación |
|-----------|--------|-------------------|------------|
| **D1** | Existencia | ¿Es acción concreta? | Solo verifica verbos de acción |
| **D2** | Cuándo | ¿Tiene plazo verificable? | Solo verifica indicadores de tiempo |
| **D3** | Cómo | ¿Describe mecanismo? | Solo verifica indicadores de mecanismo |
| **D4** | Fondos | ¿Indica financiamiento? | Solo verifica indicadores de financiamiento |

### Problema Identificado

**Las dimensiones actuales solo evalúan estructura, no viabilidad**:
- ❌ No verifican si es legalmente posible
- ❌ No verifican si es constitucional
- ❌ No verifican si es realista según el contexto del país
- ❌ No verifican si es factible en el panorama actual

**Ejemplo de problema**:
- Propuesta: "Eliminar la Asamblea Legislativa y gobernar por decreto"
- Evaluación actual: ✅ D1=1, D2=1, D3=1, D4=1 → Score 4/4
- Evaluación realista: ❌ Inconstitucional, imposible legalmente

---

## Propuesta: Dimensiones Mejoradas con Viabilidad

### Opción 1: Agregar Dimensión D5 (Viabilidad)

**Nueva dimensión D5: Viabilidad Legal y Realista**

| Aspecto | Verificación | Ejemplos |
|---------|--------------|----------|
| **Legal** | ¿Requiere reforma constitucional? | Si requiere reforma → verificar si es realista |
| **Constitucional** | ¿Viola principios constitucionales? | Separación de poderes, derechos fundamentales |
| **Realista** | ¿Es factible en el contexto actual? | Presupuesto, capacidad institucional, contexto político |
| **Temporal** | ¿Es posible en el cuatrienio? | Reformas constitucionales requieren 2 períodos legislativos |

**Criterios de evaluación D5**:
- ✅ **Viabilidad alta**: No requiere reforma, es factible con recursos actuales
- ⚠️ **Viabilidad media**: Requiere reforma legal simple, es factible con ajustes
- ❌ **Viabilidad baja**: Requiere reforma constitucional o es irrealista

### Opción 2: Mejorar Dimensiones Existentes

**Mejorar D3 (Cómo) para incluir viabilidad legal**:

| Aspecto | Verificación Actual | Verificación Mejorada |
|---------|---------------------|----------------------|
| **Mecanismo** | ¿Describe cómo? | ¿Describe cómo Y es legalmente viable? |
| **Instrumento** | ¿Menciona instrumento? | ¿Menciona instrumento Y es el correcto según ley? |
| **Proceso** | ¿Menciona proceso? | ¿Menciona proceso Y respeta separación de poderes? |

**Mejorar D4 (Fondos) para incluir realismo fiscal**:

| Aspecto | Verificación Actual | Verificación Mejorada |
|---------|---------------------|----------------------|
| **Fuente** | ¿Menciona fuente? | ¿Menciona fuente Y es realista según presupuesto? |
| **Monto** | ¿Menciona monto? | ¿Menciona monto Y es factible según capacidad fiscal? |
| **Financiamiento** | ¿Indica financiamiento? | ¿Indica financiamiento Y no viola regla fiscal? |

---

## Propuesta Recomendada: Sistema Híbrido

### Mantener D1-D4 + Agregar Verificaciones de Viabilidad

**D1-D4**: Mantener evaluación de estructura (neutral, objetivo)

**Nueva capa de verificación**: Análisis de viabilidad que ajusta el score

### Sistema de Verificación de Viabilidad

#### 1. Verificación Legal/Constitucional

**Indicadores de problemas legales**:
- Requiere reforma constitucional (artículos 195-196)
- Viola separación de poderes (artículos 9, 11, 12)
- Requiere mayoría calificada (2/3) sin mencionarlo
- Propone eliminar instituciones constitucionales

**Penalización**: -0.5 a -1.0 puntos según gravedad

#### 2. Verificación de Realismo Fiscal

**Indicadores de irrealismo fiscal**:
- Propone gasto sin fuente de financiamiento clara
- Propone gasto que excede capacidad fiscal actual
- Propone gasto que viola regla fiscal (Ley 9635)
- Propone financiamiento irrealista (ej: "con ahorros")

**Penalización**: -0.5 puntos

#### 3. Verificación de Factibilidad Temporal

**Indicadores de irrealismo temporal**:
- Propone reforma constitucional en "primer año" (imposible)
- Propone cambios estructurales sin tiempo suficiente
- Propone implementación inmediata de procesos complejos

**Penalización**: -0.3 puntos

#### 4. Verificación de Contexto Nacional

**Indicadores de desconexión con realidad**:
- Propone soluciones que ignoran crisis actuales
- Propone cambios que requieren recursos inexistentes
- Propone reformas que no consideran capacidad institucional

**Penalización**: -0.3 puntos

---

## Implementación Propuesta

### Nueva Función: `check_viability()`

```python
def check_viability(text: str, pillar_id: str) -> Dict:
    """
    Verifica viabilidad legal, constitucional y realista de una propuesta.
    Retorna penalizaciones por inviabilidad.
    """
    penalties = []
    flags = {
        "requires_constitutional_reform": False,
        "violates_separation_powers": False,
        "unrealistic_funding": False,
        "unrealistic_timeline": False,
        "disconnected_from_reality": False
    }
    
    text_lower = text.lower()
    
    # 1. Verificación legal/constitucional
    if requires_constitutional_reform(text_lower):
        flags["requires_constitutional_reform"] = True
        penalties.append({
            "type": "requires_constitutional_reform",
            "value": -0.5,
            "reason": "Requiere reforma constitucional (2 períodos legislativos mínimo)"
        })
    
    if violates_separation_powers(text_lower):
        flags["violates_separation_powers"] = True
        penalties.append({
            "type": "violates_separation_powers",
            "value": -1.0,
            "reason": "Viola separación de poderes (artículos 9, 11, 12)"
        })
    
    # 2. Verificación realismo fiscal
    if unrealistic_funding(text_lower, pillar_id):
        flags["unrealistic_funding"] = True
        penalties.append({
            "type": "unrealistic_funding",
            "value": -0.5,
            "reason": "Financiamiento irrealista según capacidad fiscal"
        })
    
    # 3. Verificación factibilidad temporal
    if unrealistic_timeline(text_lower):
        flags["unrealistic_timeline"] = True
        penalties.append({
            "type": "unrealistic_timeline",
            "value": -0.3,
            "reason": "Plazo irrealista para la complejidad de la propuesta"
        })
    
    # 4. Verificación contexto nacional
    if disconnected_from_reality(text_lower, pillar_id):
        flags["disconnected_from_reality"] = True
        penalties.append({
            "type": "disconnected_from_reality",
            "value": -0.3,
            "reason": "No considera contexto actual del país"
        })
    
    return {
        "flags": flags,
        "penalties": penalties,
        "total_penalty": sum(p["value"] for p in penalties),
        "viability_score": max(0, 1.0 + sum(p["value"] for p in penalties))  # 0.0-1.0
    }
```

### Patrones de Detección

#### Requiere Reforma Constitucional

```python
CONSTITUTIONAL_REFORM_INDICATORS = [
    r"reforma\s+constitucional",
    r"modificar\s+la\s+constitución",
    r"cambiar\s+la\s+constitución",
    r"eliminar\s+(?:la\s+)?asamblea\s+legislativa",
    r"eliminar\s+(?:el\s+)?poder\s+judicial",
    r"gobierno\s+por\s+decreto",
    r"poderes\s+extraordinarios",
]
```

#### Viola Separación de Poderes

```python
SEPARATION_POWERS_VIOLATIONS = [
    r"asamblea\s+legislativa.*(?:eliminar|disolver|cerrar)",
    r"poder\s+judicial.*(?:eliminar|disolver|cerrar)",
    r"gobierno\s+por\s+decreto\s+(?:sin|sin\s+la\s+)?asamblea",
    r"ejecutivo.*(?:legislar|juzgar)",
    r"presidente.*(?:legislar|juzgar)",
]
```

#### Financiamiento Irrealista

```python
UNREALISTIC_FUNDING_PATTERNS = [
    r"financiar.*(?:con\s+)?ahorros",
    r"financiar.*(?:con\s+)?eficiencia",
    r"sin\s+costo\s+adicional",
    r"sin\s+afectar\s+el\s+presupuesto",
    r"\d+\s*(?:millones?|billones?).*(?:sin\s+)?(?:costo|gasto|presupuesto)",
]
```

#### Plazo Irrealista

```python
UNREALISTIC_TIMELINE_PATTERNS = [
    r"(?:primer\s+mes|primer\s+semestre).*reforma\s+constitucional",
    r"(?:primer\s+año).*reforma\s+constitucional",
    r"(?:primeros?\s*100\s*días).*reforma\s+constitucional",
    r"(?:inmediatamente|de\s+inmediato).*reforma\s+constitucional",
]
```

---

## Impacto en Scoring

### Sistema Actual
```
Score = D1 + D2 + D3 + D4 (0-4)
```

### Sistema Propuesto
```
Score Base = D1 + D2 + D3 + D4 (0-4)
Penalización Viabilidad = Suma de penalizaciones por inviabilidad
Score Efectivo = max(0, Score Base + Penalización Viabilidad)
```

**Ejemplo**:
- Propuesta: "Eliminar Asamblea Legislativa en primer año"
- D1=1, D2=1, D3=1, D4=1 → Score Base = 4/4
- Penalización: -1.0 (viola separación de poderes) + -0.3 (plazo irrealista)
- **Score Efectivo = 2.7/4** (en lugar de 4/4)

---

## Consideraciones de Neutralidad

### ✅ Mantiene Neutralidad

1. **No penaliza contenido ideológico**: Solo penaliza inviabilidad legal/realista
2. **Criterios objetivos**: Basados en constitución y leyes vigentes
3. **Aplica igual a todos**: Mismos criterios para todos los candidatos

### ⚠️ Riesgos a Evitar

1. **No ser demasiado estricto**: Algunas propuestas pueden ser ambiciosas pero viables
2. **No penalizar innovación**: Nuevas ideas pueden requerir reformas legales
3. **No sesgar por complejidad**: Reformas complejas no son necesariamente inviables

---

## Recomendaciones

### Fase 1: Implementación Básica

1. **Agregar verificación de reforma constitucional**
   - Penalización: -0.5 si requiere reforma constitucional
   - Justificación: Requiere 2 períodos legislativos mínimo

2. **Agregar verificación de separación de poderes**
   - Penalización: -1.0 si viola separación de poderes
   - Justificación: Viola principios constitucionales fundamentales

### Fase 2: Implementación Avanzada

3. **Agregar verificación de realismo fiscal**
   - Penalización: -0.5 si financiamiento es irrealista
   - Justificación: Basado en capacidad fiscal actual

4. **Agregar verificación de factibilidad temporal**
   - Penalización: -0.3 si plazo es irrealista
   - Justificación: Basado en complejidad de la propuesta

### Fase 3: Refinamiento

5. **Ajustar umbrales** según resultados
6. **Validar con expertos** en derecho constitucional
7. **Documentar criterios** para transparencia

---

## Próximos Pasos

1. ✅ **Análisis completado** - Documento creado
2. 🔄 **Validar criterios** con expertos en derecho constitucional
3. 🔄 **Implementar verificación básica** (reforma constitucional + separación de poderes)
4. 🔄 **Probar con datos reales** y ajustar umbrales
5. 🔄 **Documentar criterios** para transparencia

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, listo para implementación
