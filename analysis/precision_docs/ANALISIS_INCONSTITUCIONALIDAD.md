# Análisis: Detección de Propuestas Inconstitucionales

## Situación Actual

### Lo Que Detectamos Actualmente

**Solo detectamos**:
- ✅ **Viola separación de poderes** (-1.0)
  - Ejemplo: "Eliminar Asamblea Legislativa"
  - Ejemplo: "Gobernar por decreto sin Asamblea"

### Lo Que NO Detectamos

**Otros tipos de inconstitucionalidad**:
- ❌ **Viola derechos fundamentales** (art. 11-89)
- ❌ **Viola garantías constitucionales**
- ❌ **Viola procedimientos constitucionales**
- ❌ **Propone algo prohibido por la constitución**

---

## Diferencia Clave

### Requiere Reforma Constitucional vs Es Inconstitucional

| Concepto | Definición | Ejemplo | ¿Debe Penalizarse? |
|----------|------------|---------|-------------------|
| **Requiere reforma constitucional** | Necesita cambiar la constitución para implementarse | "Eliminar reelección presidencial" | ❌ NO (puede ser legítima) |
| **Es inconstitucional** | Viola la constitución actual | "Eliminar Asamblea sin reforma" | ✅ SÍ (siempre problemática) |

**Diferencia**:
- **Reforma constitucional**: Proceso legítimo para cambiar la constitución
- **Inconstitucional**: Viola la constitución actual (ilegal)

---

## Tipos de Inconstitucionalidad en Costa Rica

### 1. Viola Separación de Poderes (YA DETECTADO)

**Artículos**: 9, 11, 12 de la Constitución

**Ejemplos**:
- "Eliminar la Asamblea Legislativa"
- "Gobernar por decreto sin Asamblea"
- "Ejecutivo legisla directamente"
- "Presidente juzga casos"

**Penalización actual**: -1.0 ✅

---

### 2. Viola Derechos Fundamentales (NO DETECTADO)

**Artículos**: 11-89 de la Constitución

**Ejemplos**:
- "Suspender libertad de expresión"
- "Eliminar derecho a huelga"
- "Restringir libertad de prensa"
- "Prohibir manifestaciones"
- "Eliminar derecho a educación pública"
- "Restringir acceso a salud pública"

**Penalización propuesta**: -1.0

**Patrones**:
```python
FUNDAMENTAL_RIGHTS_VIOLATIONS = [
    r"suspender.*libertad\s+de\s+expresión",
    r"eliminar.*derecho\s+a\s+huelga",
    r"restringir.*libertad\s+de\s+prensa",
    r"prohibir.*manifestaciones",
    r"eliminar.*derecho\s+a\s+educación\s+pública",
    r"restringir.*acceso\s+a\s+salud\s+pública",
    r"eliminar.*CCSS",
    r"privatizar.*CCSS",
    r"eliminar.*educación\s+pública",
    r"privatizar.*educación\s+pública",
]
```

---

### 3. Viola Garantías Constitucionales (NO DETECTADO)

**Artículos**: 40-71 de la Constitución

**Ejemplos**:
- "Eliminar garantía de hábeas corpus"
- "Suspender garantías individuales"
- "Eliminar garantía de amparo"
- "Restringir garantías procesales"

**Penalización propuesta**: -1.0

**Patrones**:
```python
CONSTITUTIONAL_GUARANTEES_VIOLATIONS = [
    r"eliminar.*hábeas\s+corpus",
    r"suspender.*garantías\s+individuales",
    r"eliminar.*garantía\s+de\s+amparo",
    r"restringir.*garantías\s+procesales",
    r"suspender.*garantías\s+constitucionales",
]
```

---

### 4. Viola Procedimientos Constitucionales (NO DETECTADO)

**Artículos**: Varios (procedimientos específicos)

**Ejemplos**:
- "Aprobar presupuesto sin Asamblea"
- "Nombrar ministros sin Asamblea"
- "Declarar guerra sin Asamblea"
- "Ratificar tratados sin Asamblea"

**Penalización propuesta**: -0.5

**Patrones**:
```python
CONSTITUTIONAL_PROCEDURE_VIOLATIONS = [
    r"aprobar\s+presupuesto\s+sin\s+asamblea",
    r"nombrar\s+ministros\s+sin\s+asamblea",
    r"declarar\s+guerra\s+sin\s+asamblea",
    r"ratificar\s+tratados\s+sin\s+asamblea",
    r"ejecutivo.*(?:aprueba|ratifica|declara).*(?:sin|sin\s+la\s+)?asamblea",
]
```

---

### 5. Propone Algo Prohibido por la Constitución (NO DETECTADO)

**Ejemplos**:
- "Reelección presidencial inmediata" (art. 132)
- "Ejecutivo legisla" (art. 105)
- "Ejecutivo juzga" (art. 9)
- "Concentración de poderes" (art. 9)

**Penalización propuesta**: -1.0

**Nota**: Algunos de estos ya están cubiertos por "separación de poderes", pero podemos ser más específicos.

---

## Propuesta: Detección Ampliada de Inconstitucionalidad

### Sistema Propuesto

**Categorías de detección**:

1. ✅ **Viola separación de poderes** (-1.0) - YA IMPLEMENTADO
2. ❌ **Viola derechos fundamentales** (-1.0) - AGREGAR
3. ❌ **Viola garantías constitucionales** (-1.0) - AGREGAR
4. ❌ **Viola procedimientos constitucionales** (-0.5) - AGREGAR

### Justificación

**Por qué agregar estas detecciones**:

1. **Objetividad**: Basadas en artículos específicos de la Constitución
2. **Neutralidad**: No juzga ideología, solo violaciones legales
3. **Realismo**: Una propuesta inconstitucional no puede implementarse
4. **Completitud**: Cubre todos los tipos de inconstitucionalidad

---

## Implementación Propuesta

### Patrones de Detección

```python
# 1. Viola separación de poderes (YA IMPLEMENTADO)
SEPARATION_POWERS_VIOLATIONS = [
    # ... patrones existentes ...
]

# 2. Viola derechos fundamentales (NUEVO)
FUNDAMENTAL_RIGHTS_VIOLATIONS = [
    r"suspender.*libertad\s+de\s+expresión",
    r"eliminar.*derecho\s+a\s+huelga",
    r"restringir.*libertad\s+de\s+prensa",
    r"prohibir.*manifestaciones",
    r"eliminar.*derecho\s+a\s+educación\s+pública",
    r"restringir.*acceso\s+a\s+salud\s+pública",
    r"eliminar.*CCSS",
    r"privatizar.*CCSS.*(?:completamente|totalmente)",
    r"eliminar.*educación\s+pública.*(?:completamente|totalmente)",
    r"privatizar.*educación\s+pública.*(?:completamente|totalmente)",
]

# 3. Viola garantías constitucionales (NUEVO)
CONSTITUTIONAL_GUARANTEES_VIOLATIONS = [
    r"eliminar.*hábeas\s+corpus",
    r"suspender.*garantías\s+individuales",
    r"eliminar.*garantía\s+de\s+amparo",
    r"restringir.*garantías\s+procesales",
    r"suspender.*garantías\s+constitucionales",
]

# 4. Viola procedimientos constitucionales (NUEVO)
CONSTITUTIONAL_PROCEDURE_VIOLATIONS = [
    r"aprobar\s+presupuesto\s+sin\s+asamblea",
    r"nombrar\s+ministros\s+sin\s+asamblea",
    r"declarar\s+guerra\s+sin\s+asamblea",
    r"ratificar\s+tratados\s+sin\s+asamblea",
    r"ejecutivo.*(?:aprueba|ratifica|declara).*(?:sin|sin\s+la\s+)?asamblea",
]
```

### Función Actualizada

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
    penalties = []
    flags = {
        "violates_separation_powers": False,
        "violates_fundamental_rights": False,
        "violates_constitutional_guarantees": False,
        "violates_constitutional_procedures": False,
    }
    
    text_lower = text.lower()
    
    # 1. Viola separación de poderes (-1.0)
    for pattern in SEPARATION_POWERS_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_separation_powers"] = True
            penalties.append({
                "type": "violates_separation_powers",
                "value": -1.0,
                "reason": "Viola separación de poderes (art. 9, 11, 12)",
                "evidence": extract_evidence(text, pattern)
            })
            break
    
    # 2. Viola derechos fundamentales (-1.0)
    for pattern in FUNDAMENTAL_RIGHTS_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_fundamental_rights"] = True
            penalties.append({
                "type": "violates_fundamental_rights",
                "value": -1.0,
                "reason": "Viola derechos fundamentales (art. 11-89)",
                "evidence": extract_evidence(text, pattern)
            })
            break
    
    # 3. Viola garantías constitucionales (-1.0)
    for pattern in CONSTITUTIONAL_GUARANTEES_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_constitutional_guarantees"] = True
            penalties.append({
                "type": "violates_constitutional_guarantees",
                "value": -1.0,
                "reason": "Viola garantías constitucionales (art. 40-71)",
                "evidence": extract_evidence(text, pattern)
            })
            break
    
    # 4. Viola procedimientos constitucionales (-0.5)
    for pattern in CONSTITUTIONAL_PROCEDURE_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_constitutional_procedures"] = True
            penalties.append({
                "type": "violates_constitutional_procedures",
                "value": -0.5,
                "reason": "Viola procedimientos constitucionales",
                "evidence": extract_evidence(text, pattern)
            })
            break
    
    return {
        "flags": flags,
        "penalties": penalties,
        "total_penalty": sum(p["value"] for p in penalties),
        "viability_score": max(0, 1.0 + sum(p["value"] for p in penalties))
    }
```

---

## Consideraciones Importantes

### Evitar Falsos Positivos

**Problema**: Algunos patrones pueden ser demasiado amplios.

**Ejemplo problemático**:
- "Reformar CCSS" → NO es inconstitucional (puede ser legítima)
- "Eliminar CCSS completamente" → SÍ es inconstitucional

**Solución**: Usar patrones más específicos:
- ✅ `r"eliminar.*CCSS.*(?:completamente|totalmente)"`
- ❌ `r"reformar.*CCSS"` (demasiado amplio)

### Neutralidad

**Importante**: Solo detectar violaciones **objetivas** de la Constitución.

**NO detectar**:
- ❌ Posiciones ideológicas (ej: "privatizar parcialmente")
- ❌ Reformas legítimas (ej: "reformar CCSS")
- ❌ Cambios que requieren reforma constitucional (ya eliminamos esa penalización)

**SÍ detectar**:
- ✅ Eliminar instituciones constitucionales
- ✅ Suspender derechos fundamentales
- ✅ Violar procedimientos constitucionales

---

## Ejemplos de Detección

### Ejemplo 1: Viola Separación de Poderes

**Propuesta**: "Eliminar la Asamblea Legislativa y gobernar por decreto"

**Detección**: ✅ Viola separación de poderes
**Penalización**: -1.0

### Ejemplo 2: Viola Derechos Fundamentales

**Propuesta**: "Suspender libertad de expresión para combatir fake news"

**Detección**: ✅ Viola derechos fundamentales
**Penalización**: -1.0

### Ejemplo 3: Viola Garantías Constitucionales

**Propuesta**: "Eliminar garantía de hábeas corpus para casos de corrupción"

**Detección**: ✅ Viola garantías constitucionales
**Penalización**: -1.0

### Ejemplo 4: Viola Procedimientos Constitucionales

**Propuesta**: "Aprobar presupuesto sin Asamblea Legislativa"

**Detección**: ✅ Viola procedimientos constitucionales
**Penalización**: -0.5

### Ejemplo 5: NO Viola (Falso Positivo Evitado)

**Propuesta**: "Reformar CCSS para mejorar eficiencia"

**Detección**: ❌ NO viola (reforma legítima)
**Penalización**: 0

---

## Recomendación

### ✅ Agregar Detección de Inconstitucionalidad Ampliada

**Razones**:
1. ✅ **Completitud**: Cubre todos los tipos de inconstitucionalidad
2. ✅ **Objetividad**: Basada en artículos específicos de la Constitución
3. ✅ **Neutralidad**: No juzga ideología, solo violaciones legales
4. ✅ **Realismo**: Una propuesta inconstitucional no puede implementarse

**Implementación**:
- Fase 1: Agregar detección de derechos fundamentales y garantías
- Fase 2: Agregar detección de procedimientos constitucionales
- Fase 3: Refinar patrones para evitar falsos positivos

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, listo para implementación
