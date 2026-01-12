# Propuesta: Dimensiones Mejoradas con Viabilidad Legal y Realista

## Resumen Ejecutivo

### Problema Actual
Las dimensiones D1-D4 solo evalúan **estructura** (qué, cuándo, cómo, con qué), pero **no evalúan viabilidad**:
- ❌ No verifican si es legalmente posible
- ❌ No verifican si es constitucional
- ❌ No verifican si es realista según el contexto del país

### Solución Propuesta
**Mantener D1-D4** (evaluación de estructura) + **Agregar capa de verificación de viabilidad** que ajusta el score.

---

## Sistema Propuesto: D1-D4 + Verificación de Viabilidad

### Dimensiones Estructurales (Mantener)

| Dimensión | Evaluación | Propósito |
|-----------|------------|-----------|
| **D1** | ¿Es acción concreta? | Verificar que no sea solo aspiracional |
| **D2** | ¿Tiene plazo verificable? | Verificar que tenga temporalidad |
| **D3** | ¿Describe mecanismo? | Verificar que explique cómo |
| **D4** | ¿Indica financiamiento? | Verificar que explique con qué |

**Score Base = D1 + D2 + D3 + D4 (0-4)**

### Nueva Capa: Verificación de Viabilidad

**Penalizaciones por inviabilidad**:

| Tipo de Inviabilidad | Penalización | Justificación |
|----------------------|--------------|---------------|
| Requiere reforma constitucional | **-0.5** | Requiere 2 períodos legislativos mínimo |
| Viola separación de poderes | **-1.0** | Viola principios constitucionales fundamentales |
| Financiamiento irrealista | **-0.5** | No es factible según capacidad fiscal |
| Plazo irrealista | **-0.3** | No es posible en el tiempo propuesto |
| Desconectado de realidad | **-0.3** | No considera contexto actual del país |

**Score Efectivo = max(0, Score Base + Penalizaciones Viabilidad)**

---

## Criterios de Verificación

### 1. Requiere Reforma Constitucional (-0.5)

**Indicadores**:
- Menciona "reforma constitucional"
- Propone modificar la constitución
- Propone eliminar instituciones constitucionales (Asamblea, Poder Judicial)
- Propone cambios que requieren mayoría calificada (2/3) sin mencionarlo

**Ejemplo**:
- ❌ "Eliminar la Asamblea Legislativa" → Requiere reforma constitucional
- ✅ "Reformar la Ley de Presupuesto" → No requiere reforma constitucional

### 2. Viola Separación de Poderes (-1.0)

**Indicadores**:
- Propone que el Ejecutivo legisle sin Asamblea
- Propone que el Ejecutivo juzgue
- Propone eliminar o disolver poderes del Estado
- Propone "gobierno por decreto" permanente

**Ejemplo**:
- ❌ "Gobernar por decreto sin Asamblea" → Viola separación de poderes
- ✅ "Usar decretos de emergencia temporal" → No viola (si es temporal y legal)

### 3. Financiamiento Irrealista (-0.5)

**Indicadores**:
- Propone gasto sin fuente clara
- Propone gasto que excede capacidad fiscal
- Propone "financiar con ahorros" sin especificar de dónde
- Propone "sin costo adicional" para gastos grandes

**Ejemplo**:
- ❌ "Invertir 10% del PIB sin aumentar impuestos ni deuda" → Irrealista
- ✅ "Invertir 1% del PIB con reasignación presupuestaria" → Realista

### 4. Plazo Irrealista (-0.3)

**Indicadores**:
- Propone reforma constitucional en "primer año" (imposible)
- Propone cambios estructurales complejos en "primeros 100 días"
- Propone implementación inmediata de procesos que requieren años

**Ejemplo**:
- ❌ "Reforma constitucional en primer año" → Irrealista (requiere 2 períodos)
- ✅ "Reforma constitucional en cuatrienio" → Realista (si se inicia temprano)

### 5. Desconectado de Realidad (-0.3)

**Indicadores**:
- Propone soluciones que ignoran crisis actuales
- Propone cambios que requieren recursos inexistentes
- Propone reformas que no consideran capacidad institucional

**Ejemplo**:
- ❌ "Construir 100 hospitales en primer año" → Desconectado de realidad
- ✅ "Construir 5 hospitales en cuatrienio" → Conectado con realidad

---

## Implementación Técnica

### Nueva Función: `check_viability()`

```python
def check_viability(text: str, pillar_id: str) -> Dict:
    """
    Verifica viabilidad legal, constitucional y realista.
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
    
    # Verificaciones...
    
    return {
        "flags": flags,
        "penalties": penalties,
        "total_penalty": sum(p["value"] for p in penalties),
        "viability_score": max(0, 1.0 + sum(p["value"] for p in penalties))
    }
```

### Integración en Scoring

```python
# En calculate_candidate_score()
viability_analysis = check_viability(prop["text"], pillar_id)
viability_penalty = viability_analysis["total_penalty"]

# Score efectivo con penalización de viabilidad
effective_score = max(0, min(4.0, base_score + bonus_multiple + bonus_quality + viability_penalty))
```

---

## Ejemplos de Impacto

### Ejemplo 1: Propuesta Inviable

**Propuesta**: "Eliminar la Asamblea Legislativa y gobernar por decreto en primer año"

**Evaluación actual (D1-D4)**:
- D1=1 (acción concreta)
- D2=1 (tiene plazo: "primer año")
- D3=1 (describe mecanismo: "gobernar por decreto")
- D4=1 (no requiere financiamiento adicional)
- **Score Base = 4/4**

**Evaluación con viabilidad**:
- Penalización: -1.0 (viola separación de poderes) + -0.3 (plazo irrealista)
- **Score Efectivo = 2.7/4**

### Ejemplo 2: Propuesta Viable

**Propuesta**: "Crear programa de empleo juvenil mediante reforma a Ley de Zonas Francas, financiado con reasignación presupuestaria, en primer año"

**Evaluación actual (D1-D4)**:
- D1=1, D2=1, D3=1, D4=1
- **Score Base = 4/4**

**Evaluación con viabilidad**:
- No requiere reforma constitucional ✅
- No viola separación de poderes ✅
- Financiamiento realista ✅
- Plazo realista ✅
- **Score Efectivo = 4/4** (sin penalizaciones)

---

## Ventajas del Sistema

### 1. Mantiene Neutralidad
- ✅ No penaliza contenido ideológico
- ✅ Solo penaliza inviabilidad legal/realista
- ✅ Criterios objetivos basados en constitución y leyes

### 2. Mejora Calidad
- ✅ Distingue propuestas viables de inviables
- ✅ Premia propuestas realistas
- ✅ Penaliza propuestas irrealistas

### 3. Transparente
- ✅ Criterios claros y documentados
- ✅ Basado en constitución y leyes vigentes
- ✅ Aplicable a todos por igual

---

## Consideraciones Importantes

### ⚠️ No Ser Demasiado Estricto

**Evitar**:
- Penalizar propuestas ambiciosas pero viables
- Penalizar innovación que requiere reformas legales
- Penalizar complejidad (reformas complejas pueden ser viables)

**Enfoque**:
- Penalizar solo inviabilidad clara (violación constitucional, irrealismo fiscal extremo)
- Permitir propuestas ambiciosas si son legalmente viables

### ✅ Mantener Neutralidad

**No penalizar**:
- Posiciones ideológicas (aunque sean ambiciosas)
- Propuestas que requieren reformas legales (si son viables)
- Propuestas innovadoras (si son legalmente posibles)

**Solo penalizar**:
- Violaciones constitucionales claras
- Irrealismo fiscal extremo
- Plazos imposibles para reformas constitucionales

---

## Próximos Pasos Recomendados

### Fase 1: Implementación Básica (Recomendado Primero)

1. **Agregar verificación de reforma constitucional** (-0.5)
2. **Agregar verificación de separación de poderes** (-1.0)
3. **Probar con datos reales** y ajustar umbrales

### Fase 2: Implementación Avanzada

4. **Agregar verificación de realismo fiscal** (-0.5)
5. **Agregar verificación de factibilidad temporal** (-0.3)
6. **Validar con expertos** en derecho constitucional

### Fase 3: Refinamiento

7. **Ajustar umbrales** según resultados
8. **Documentar criterios** para transparencia
9. **Publicar metodología** actualizada

---

## Conclusión

### ✅ Sistema Recomendado

**Implementar verificación de viabilidad** porque:

1. ✅ **Mejora calidad**: Distingue propuestas viables de inviables
2. ✅ **Mantiene neutralidad**: Solo penaliza inviabilidad, no contenido
3. ✅ **Basado en ley**: Criterios objetivos (constitución, leyes)
4. ✅ **Transparente**: Criterios claros y documentados

### Próximo Paso Inmediato

**Implementar verificación básica** (reforma constitucional + separación de poderes) y probar con datos reales.

---

**Fecha**: 2026-01-11  
**Estado**: Propuesta lista para implementación
