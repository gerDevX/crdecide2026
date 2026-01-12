# Resumen: Sistema de Flags Informativos para Transparencia Democrática

## Concepto

**Flags informativos** = Señales de advertencia basadas en evidencia objetiva que **NO penalizan**, solo **informan** al ciudadano.

### Principios

1. ✅ **No penalizan**: No afectan el score
2. ✅ **Solo informan**: Aparecen como advertencias informativas
3. ✅ **Objetivos**: Basados en evidencia verificable
4. ✅ **Transparentes**: El ciudadano decide qué hacer con la información

---

## Tipos de Flags

### 1. Flags de Propuestas Actuales (Ya Implementado)

**Basados en el sistema de viabilidad actual**:
- ✅ Viola separación de poderes
- ✅ Viola derechos fundamentales
- ✅ Viola garantías constitucionales
- ✅ Viola procedimientos constitucionales

**Acción**: Convertir estas detecciones en flags informativos (mantener penalización pero agregar flag)

### 2. Flags de Evidencia Histórica (Nuevo)

**Basados en comportamiento verificable del partido/candidato**:

#### A. Comportamiento Anti-Democrático Histórico
- **Evidencia**: Sentencias judiciales, resoluciones de organismos internacionales
- **Fuente**: Poder Judicial, CIDH, ONU
- **Flag**: `historical_anti_democratic_behavior`

#### B. Violaciones de Derechos Humanos Históricas
- **Evidencia**: Sentencias de cortes internacionales
- **Fuente**: CIDH, Corte Interamericana
- **Flag**: `historical_human_rights_violations`

#### C. Corrupción Verificada
- **Evidencia**: Sentencias judiciales, investigaciones concluidas
- **Fuente**: Poder Judicial, Contraloría
- **Flag**: `historical_corruption_convictions`

### 3. Flags de Contradicción (Nuevo)

**Basados en contradicción entre histórico y actual**:

#### A. Histórico Anti-Democrático + Propuestas Actuales Problemáticas
- **Evidencia**: 
  - Histórico: Intentos verificables de eliminar instituciones
  - Actual: Propuestas que violan separación de poderes
- **Flag**: `historical_current_contradiction`
- **Severidad**: Alta (patrón consistente)

---

## Criterios de Objetividad

### ✅ Evidencia Objetiva (Aceptable)

1. **Sentencias judiciales**:
   - Poder Judicial de Costa Rica
   - Cortes internacionales (CIDH, Corte Interamericana)

2. **Registros públicos verificables**:
   - Actas de sesiones legislativas
   - Resoluciones de organismos de control
   - Informes de Contraloría

3. **Propuestas actuales del plan**:
   - Texto extraído del plan de gobierno
   - Análisis de viabilidad constitucional

### ❌ Evidencia Subjetiva (NO Aceptable)

1. ❌ Opiniones políticas
2. ❌ Acusaciones sin sentencia
3. ❌ Rumores o especulaciones
4. ❌ Posiciones ideológicas legítimas

---

## Ejemplo de Implementación

### Estructura de Datos

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "historical": {
      "anti_democratic_behavior": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "type": "judicial_sentence",
            "source": "Poder Judicial de Costa Rica",
            "date": "2020-01-15",
            "description": "Sentencia por intento de eliminar independencia del Poder Judicial",
            "verification_url": "https://..."
          }
        ]
      }
    },
    "current_proposals": {
      "violates_separation_powers": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "pillar_id": "P1",
            "proposal_text": "Eliminar la Asamblea Legislativa...",
            "detected_by": "viability_check"
          }
        ]
      }
    },
    "contradictions": {
      "historical_current_contradiction": {
        "active": true,
        "severity": "high",
        "evidence": {
          "historical": "Comportamiento anti-democrático histórico",
          "current": "Propuestas actuales que violan separación de poderes"
        }
      }
    }
  }
}
```

---

## Presentación al Ciudadano

### Opción 1: Badge Informativo

```
⚠️ Información: Este candidato tiene evidencia histórica de comportamiento 
anti-democrático verificable. Ver detalles →
```

### Opción 2: Sección Expandible

```
📋 Información Adicional
├─ ⚠️ Evidencia Histórica
│  └─ Comportamiento anti-democrático (2020): [Ver evidencia]
├─ ⚠️ Propuestas Actuales
│  └─ Propuestas que violan separación de poderes: [Ver propuestas]
└─ ⚠️ Patrón Detectado
   └─ Contradicción entre comportamiento histórico y propuestas actuales
```

### Opción 3: Modal de Información

```
Al hacer clic en "Ver información adicional":
- Muestra evidencia histórica con fuentes
- Muestra propuestas actuales problemáticas
- Muestra contradicciones detectadas
- NO afecta el score (solo informa)
```

---

## Implementación por Fases

### Fase 1: Flags de Propuestas Actuales (Ya Implementado)

✅ **Ya tenemos**: Sistema de viabilidad que detecta violaciones en propuestas actuales

**Acción**: Convertir estas penalizaciones en flags informativos (mantener penalización pero agregar flag)

### Fase 2: Base de Datos de Evidencia Histórica

**Crear**: Archivo `historical_evidence.json` con evidencia verificable

**Fuentes**:
- Investigación manual de sentencias judiciales
- Resoluciones de organismos internacionales
- Informes de Contraloría

### Fase 3: Sistema de Contradicciones

**Implementar**: Lógica para detectar contradicciones entre histórico y actual

**Algoritmo**:
1. Si hay evidencia histórica anti-democrática Y propuestas actuales problemáticas → Flag de contradicción
2. Si hay evidencia histórica de corrupción Y propuestas actuales sin transparencia → Flag de preocupación

---

## Neutralidad Garantizada

### ✅ Garantías

1. **Criterios objetivos**: Solo evidencia verificable
2. **Fuentes públicas**: Todas las fuentes son accesibles
3. **No afecta scoring**: Flags son informativos, no penalizaciones
4. **Transparencia total**: Ciudadano ve todas las evidencias y fuentes

### ⚠️ Riesgos Evitados

1. **Sesgo político**: NO incluir opiniones políticas
2. **Falsos positivos**: NO incluir acusaciones sin sentencia
3. **Manipulación**: NO permitir que flags afecten scoring

---

## Resultado Esperado

### Para el Ciudadano

- ✅ Información transparente y verificable
- ✅ Decisión informada basada en evidencia
- ✅ Acceso a fuentes originales
- ✅ Score no afectado (neutralidad mantenida)

### Para el Sistema

- ✅ Neutralidad mantenida
- ✅ Objetividad garantizada
- ✅ Transparencia total
- ✅ Responsabilidad informativa

---

**Fecha**: 2026-01-11  
**Estado**: Propuesta lista para implementación
