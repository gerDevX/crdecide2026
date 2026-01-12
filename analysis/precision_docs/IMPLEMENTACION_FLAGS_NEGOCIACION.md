# Implementación: Flags de Negociación entre Poderes

## Implementación Completada

### Nueva Funcionalidad Agregada

**Flag informativo**: Detección de propuestas que requieren negociación/coordinación entre poderes del Estado.

**Objetivo**: Informar al ciudadano sobre la complejidad de implementación de propuestas que requieren coordinación entre Ejecutivo y Legislativo.

---

## Cambios Realizados en `process_plans_v7.py`

### 1. Nueva Función: `detect_power_negotiation_requirements()`

**Ubicación**: Líneas 870-970

**Funcionalidad**:
- Detecta propuestas que requieren aprobación de Asamblea Legislativa
- Detecta propuestas que requieren mayoría calificada (2/3)
- Detecta propuestas que requieren coordinación entre poderes
- Retorna flags informativos (NO penalizaciones)

**Patrones detectados**:

#### A. Requiere Aprobación de Asamblea
- "requiere aprobación de la Asamblea"
- "necesita aprobación legislativa"
- "reforma legal que requiere Asamblea"
- "nueva ley que necesita Asamblea"
- "presupuesto que requiere Asamblea"
- "ratificación de tratado que requiere Asamblea"

#### B. Requiere Mayoría Calificada (2/3)
- "mayoría calificada"
- "dos tercios"
- "2/3"
- "mayoría de dos tercios"

#### C. Requiere Coordinación entre Poderes
- "coordinación entre poderes"
- "negociación con la Asamblea"
- "consenso entre poderes"
- "acuerdo con la Asamblea"

### 2. Integración en `analyze_informative_flags()`

**Ubicación**: Líneas 969-1070

**Cambios**:
- Agregado campo `power_negotiation_requirements` a estructura de flags
- Llamada a `detect_power_negotiation_requirements()` al final del análisis
- Flags agregados al resultado final

---

## Estructura de Datos

### Flags de Negociación en JSON

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "power_negotiation_requirements": {
      "requires_assembly_approval": {
        "active": true,
        "severity": "medium",
        "evidence": [
          {
            "pillar_id": "P1",
            "proposal_text": "Reforma fiscal que requiere aprobación de la Asamblea...",
            "matched_patterns": [
              "requiere\\s+aprobación\\s+de\\s+la\\s+asamblea"
            ],
            "detection_method": "pattern_matching"
          }
        ],
        "description": "Requiere aprobación de la Asamblea Legislativa"
      },
      "requires_qualified_majority": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "pillar_id": "P1",
            "proposal_text": "Reforma que requiere mayoría calificada de dos tercios...",
            "matched_patterns": [
              "mayoría\\s+calificada",
              "dos\\s+tercios"
            ],
            "detection_method": "pattern_matching"
          }
        ],
        "description": "Requiere mayoría calificada (2/3) en Asamblea"
      },
      "requires_inter_branch_coordination": {
        "active": false,
        "severity": "medium",
        "evidence": [],
        "description": "Requiere coordinación entre poderes del Estado"
      }
    }
  }
}
```

---

## Pruebas Realizadas

### Test 1: Detección de Aprobación de Asamblea

**Input**:
- "Reforma fiscal que requiere aprobación de la Asamblea Legislativa"
- "Ratificación de tratado internacional que requiere aprobación de la Asamblea"

**Resultado**: ✅ Detectado correctamente (2 propuestas)

### Test 2: Detección de Mayoría Calificada

**Input**:
- "Reforma que requiere mayoría calificada de dos tercios"

**Resultado**: ✅ Detectado correctamente (1 propuesta)

### Test 3: Detección de Coordinación entre Poderes

**Input**:
- "Nueva ley que necesita consenso legislativo y coordinación entre poderes"

**Resultado**: ✅ Detectado correctamente (1 propuesta)

### Test 4: Procesamiento Completo

**Resultado**:
- ✅ 5 candidatos con requisitos de negociación detectados
- ✅ Sistema funcionando correctamente
- ✅ Flags guardados en `candidate_scores.json`

---

## Características de Implementación

### ✅ Neutralidad Mantenida

1. **No penaliza**: Requerir aprobación de Asamblea es legítimo
2. **Solo informa**: Indica complejidad de implementación
3. **Objetivo**: Basado en texto explícito de propuestas
4. **Transparente**: Ciudadano puede verificar evidencia

### ✅ Utilidad para el Ciudadano

**Información valiosa**:
- Propuestas que requieren aprobación legislativa (más complejas)
- Propuestas que requieren mayoría calificada (muy complejas)
- Propuestas que requieren coordinación política (complejidad media)

**Ayuda a entender**:
- Complejidad de implementación
- Necesidad de negociación política
- Factibilidad temporal (más tiempo si requiere Asamblea)

---

## Ejemplos de Uso

### Caso: Candidato con Propuestas que Requieren Asamblea

**Propuestas detectadas**:
- "Reforma fiscal que requiere aprobación de la Asamblea Legislativa"
- "Nueva ley de empleo que necesita consenso legislativo"

**Flags activos**:
- ✅ `requires_assembly_approval`: True (2 propuestas)
- ✅ `requires_inter_branch_coordination`: True (1 propuesta)

**Presentación al ciudadano**:
```
📋 Información Adicional

Este candidato tiene propuestas que requieren:
- Aprobación de la Asamblea Legislativa (2 propuestas)
- Coordinación entre poderes (1 propuesta)

Esto indica que estas propuestas requieren negociación política
y aprobación legislativa para implementarse.

[Ver propuestas] [Cerrar]
```

**Score**: NO se afecta (solo informa)

---

## Resultados del Procesamiento

**Después de la implementación**:
- ✅ 5 candidatos con requisitos de negociación detectados
- ✅ Sistema detecta correctamente propuestas que mencionan Asamblea
- ✅ Flags NO afectan el score (solo informan)

**Candidatos con flags activos**:
1. `claudia-dobles`: 1 propuesta requiere aprobación de Asamblea
2. `ana-virginia-calzada`: 2 propuestas requieren aprobación de Asamblea
3. `frente-amplio-ariel-robles-barrantes`: 4 propuestas requieren aprobación de Asamblea
4. `walter-hernandez`: 2 propuestas requieren aprobación de Asamblea
5. `juan-carlos-hidalgo`: 1 propuesta requiere aprobación de Asamblea

---

## Conclusión

### ✅ Implementación Completada y Validada

**Funcionalidades implementadas**:
- ✅ Detección de requisitos de aprobación de Asamblea
- ✅ Detección de requisitos de mayoría calificada
- ✅ Detección de requisitos de coordinación entre poderes
- ✅ Integración en sistema de flags informativos
- ✅ Pruebas validadas

**Resultado**:
- Sistema informativo completo
- Neutralidad mantenida (no penaliza, solo informa)
- Utilidad para ciudadano (complejidad de implementación)
- Transparencia total

---

**Fecha**: 2026-01-11  
**Estado**: Implementación completada, sistema validado
