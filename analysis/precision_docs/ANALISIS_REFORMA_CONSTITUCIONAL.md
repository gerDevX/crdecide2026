# Análisis: ¿Cuándo Realmente Requiere Reforma Constitucional?

## Problema Identificado

### Situación Actual
El sistema detecta "reforma constitucional" como palabra clave, pero **no analiza si realmente se propone un cambio que requiera reforma constitucional**.

### Ejemplo del Problema

**Propuesta detectada**:
> "Reforma constitucional y fiscal: • Reafirmar el carácter público, solidario y universal de la CCSS (art. 21 y 73). • Saldar la deuda estatal. • Establecer impuestos progresivos."

**Análisis**:
- ❌ **Detección actual**: Penaliza porque menciona "reforma constitucional"
- ✅ **Análisis real**: 
  - "Reafirmar" CCSS (art. 21 y 73) → Ya está en la constitución, solo reafirma
  - "Saldar deuda estatal" → No requiere reforma constitucional (puede hacerse por ley)
  - "Establecer impuestos" → No requiere reforma constitucional (puede hacerse por ley)

**Conclusión**: La propuesta menciona "reforma constitucional" pero **no propone cambios que realmente requieran reforma constitucional**.

---

## ¿Qué Requiere Reforma Constitucional?

### Según Artículos 195-196 de la Constitución

**Reforma constitucional se requiere para**:
1. **Cambios a estructura fundamental del Estado**:
   - Eliminar/modificar poderes del Estado (Asamblea, Poder Judicial, etc.)
   - Cambiar sistema de gobierno
   - Modificar separación de poderes

2. **Cambios a derechos y deberes fundamentales**:
   - Modificar derechos fundamentales (art. 11-89)
   - Cambiar deberes constitucionales
   - Modificar garantías constitucionales

3. **Cambios a instituciones constitucionales**:
   - Modificar funciones de instituciones constitucionales
   - Cambiar estructura de poderes
   - Modificar procedimientos constitucionales

### NO Requiere Reforma Constitucional

**Puede hacerse por ley ordinaria**:
1. **Políticas públicas**:
   - Crear programas
   - Establecer políticas
   - Modificar leyes existentes

2. **Aspectos fiscales**:
   - Establecer impuestos (ya está permitido en constitución)
   - Modificar presupuesto
   - Saldar deudas

3. **Reafirmar derechos existentes**:
   - "Reafirmar" derechos ya constitucionales
   - "Garantizar" derechos existentes
   - "Fortalecer" instituciones existentes

---

## Criterios Mejorados para Detección

### Indicadores de Reforma Constitucional REAL

**Alta confianza** (requiere reforma constitucional):
- "Eliminar [institución constitucional]"
- "Modificar [artículo constitucional específico]"
- "Cambiar [estructura fundamental del Estado]"
- "Reformar constitución para [cambio estructural]"

**Baja confianza** (probablemente NO requiere):
- "Reforma constitucional y [política]" (mención genérica)
- "Reafirmar [derecho constitucional existente]"
- "Garantizar [derecho constitucional existente]"
- "Fortalecer [institución constitucional existente]"

### Patrones Mejorados

**Patrón 1: Eliminar/Modificar Instituciones Constitucionales**
```python
REAL_CONSTITUTIONAL_REFORM = [
    r"eliminar\s+(?:la\s+)?asamblea\s+legislativa",
    r"eliminar\s+(?:el\s+)?poder\s+judicial",
    r"modificar\s+art\.?\s*\d+.*constitución",
    r"cambiar\s+(?:la\s+)?estructura\s+del\s+estado",
    r"reformar\s+constitución\s+para\s+(?:eliminar|modificar|cambiar)",
]
```

**Patrón 2: Menciones Genéricas (NO penalizar)**
```python
GENERIC_CONSTITUTIONAL_MENTIONS = [
    r"reforma\s+constitucional\s+y\s+[a-z]+",  # "reforma constitucional y fiscal"
    r"reafirmar.*constitución",
    r"garantizar.*constitución",
    r"fortalecer.*constitución",
]
```

---

## Propuesta: Detección Mejorada

### Sistema de Dos Niveles

**Nivel 1: Detección de Menciones**
- Detecta si menciona "reforma constitucional"

**Nivel 2: Análisis de Contexto**
- Analiza si realmente propone cambios que requieran reforma constitucional
- Verifica si es solo mención genérica o propuesta real

### Lógica Propuesta

```python
def requires_real_constitutional_reform(text: str) -> bool:
    """
    Verifica si realmente propone cambios que requieran reforma constitucional.
    """
    text_lower = text.lower()
    
    # Indicadores de alta confianza (realmente requiere)
    high_confidence_patterns = [
        r"eliminar\s+(?:la\s+)?asamblea",
        r"eliminar\s+(?:el\s+)?poder\s+judicial",
        r"modificar\s+art\.?\s*\d+.*constitución",
        r"cambiar\s+estructura\s+del\s+estado",
        r"reformar\s+constitución\s+para\s+(?:eliminar|modificar|cambiar)",
    ]
    
    # Indicadores de baja confianza (solo mención)
    low_confidence_patterns = [
        r"reforma\s+constitucional\s+y\s+[a-z]+",  # "reforma constitucional y X"
        r"reafirmar.*(?:art\.?\s*\d+|constitución)",
        r"garantizar.*(?:art\.?\s*\d+|constitución)",
        r"fortalecer.*(?:art\.?\s*\d+|constitución)",
    ]
    
    # Si tiene patrones de alta confianza → requiere reforma
    for pattern in high_confidence_patterns:
        if re.search(pattern, text_lower):
            return True
    
    # Si tiene patrones de baja confianza → NO requiere reforma
    for pattern in low_confidence_patterns:
        if re.search(pattern, text_lower):
            return False
    
    # Si solo menciona "reforma constitucional" sin contexto específico
    if re.search(r"reforma\s+constitucional", text_lower):
        # Verificar si hay contexto que indique cambio real
        # Por ahora, ser conservador: si menciona, asumir que requiere
        # (pero esto puede mejorarse con más análisis)
        return True
    
    return False
```

---

## Recomendación

### Opción 1: Ser Más Específico (Recomendado)

**Solo penalizar si realmente propone cambios estructurales**:
- Eliminar instituciones constitucionales
- Modificar artículos constitucionales específicos
- Cambiar estructura del Estado

**NO penalizar**:
- Menciones genéricas de "reforma constitucional"
- "Reafirmar" derechos existentes
- "Garantizar" derechos existentes

### Opción 2: Mantener Actual pero Mejorar

**Mantener detección actual pero agregar contexto**:
- Si menciona "reforma constitucional" → verificar contexto
- Si es solo mención genérica → NO penalizar
- Si propone cambios reales → penalizar

---

## Próximos Pasos

1. ✅ **Análisis completado** - Problema identificado
2. 🔄 **Mejorar detección** - Agregar análisis de contexto
3. 🔄 **Probar con datos** - Verificar que no genera falsos positivos
4. 🔄 **Ajustar umbrales** - Si es necesario

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, listo para mejorar detección
