# Propuesta: Sistema de Flags Informativos para Transparencia Democrática

## Problema Identificado

### Necesidad del Usuario

**Objetivo**: Informar al ciudadano sobre partidos/candidatos que tienen evidencia histórica de comportamiento no democrático, **sin penalizar** (para mantener neutralidad).

**Desafío**: 
- ❌ No podemos penalizar (sería sesgo)
- ✅ Podemos informar (transparencia)
- ✅ Debe ser objetivo y basado en evidencia verificable
- ✅ Debe combinar evidencia histórica con propuestas actuales

---

## Propuesta: Sistema de Flags Informativos

### Concepto

**Flags informativos** = Señales de advertencia basadas en evidencia objetiva que **NO penalizan**, solo **informan** al ciudadano.

**Principios**:
1. ✅ **No penalizan**: No afectan el score
2. ✅ **Solo informan**: Aparecen como advertencias informativas
3. ✅ **Objetivos**: Basados en evidencia verificable
4. ✅ **Transparentes**: El ciudadano decide qué hacer con la información

---

## Tipos de Flags Informativos

### 1. Flags de Evidencia Histórica

**Basados en comportamiento verificable del partido/candidato en el pasado**:

#### A. Comportamiento Anti-Democrático Histórico
- **Evidencia**: Intentos verificables de:
  - Eliminar instituciones democráticas
  - Violar separación de poderes
  - Atacar libertad de prensa
  - Restringir derechos fundamentales
- **Fuente**: Registros públicos, sentencias judiciales, resoluciones de organismos internacionales
- **Flag**: `historical_anti_democratic_behavior`

#### B. Violaciones de Derechos Humanos Históricas
- **Evidencia**: Sentencias de cortes internacionales, resoluciones de organismos de derechos humanos
- **Fuente**: CIDH, ONU, etc.
- **Flag**: `historical_human_rights_violations`

#### C. Corrupción Verificada
- **Evidencia**: Sentencias judiciales, investigaciones concluidas
- **Fuente**: Poder Judicial, Contraloría, organismos internacionales
- **Flag**: `historical_corruption_convictions`

### 2. Flags de Propuestas Actuales Problemáticas

**Basados en propuestas del plan actual que contradicen principios democráticos**:

#### A. Propuestas que Violan Separación de Poderes
- **Ya detectado**: Sistema de viabilidad actual
- **Flag**: `proposal_violates_separation_powers`
- **Evidencia**: Texto de la propuesta

#### B. Propuestas que Violan Derechos Fundamentales
- **Ya detectado**: Sistema de viabilidad actual
- **Flag**: `proposal_violates_fundamental_rights`
- **Evidencia**: Texto de la propuesta

#### C. Propuestas que Violan Garantías Constitucionales
- **Ya detectado**: Sistema de viabilidad actual
- **Flag**: `proposal_violates_constitutional_guarantees`
- **Evidencia**: Texto de la propuesta

### 3. Flags de Contradicción Histórica

**Basados en contradicción entre comportamiento histórico y propuestas actuales**:

#### A. Histórico Anti-Democrático + Propuestas Actuales Problemáticas
- **Evidencia**: 
  - Histórico: Intentos verificables de eliminar instituciones
  - Actual: Propuestas que violan separación de poderes
- **Flag**: `historical_current_contradiction`
- **Severidad**: Alta (patrón consistente)

#### B. Histórico Corrupto + Propuestas Actuales sin Transparencia
- **Evidencia**:
  - Histórico: Corrupción verificada
  - Actual: Propuestas sin mecanismos de transparencia/rendición de cuentas
- **Flag**: `corruption_transparency_concern`
- **Severidad**: Media

### 4. Flags de Similitud con Modelos Dictatoriales (NUEVO)

**Basados en similitudes objetivas con patrones históricamente verificables**:

#### A. Similitud con Modelo Cubano
- **Patrones objetivos detectables** (NO ideología):
  - Eliminación de separación de poderes
  - Eliminación de libertad de prensa
  - Eliminación de garantías constitucionales
  - Concentración de poderes en Ejecutivo
- **Fuentes históricas**: Resoluciones CIDH, informes ONU
- **Flag**: `cuba_similarity`
- **Severidad**: Alta

#### B. Similitud con Modelo Venezolano
- **Patrones objetivos detectables** (NO ideología):
  - Eliminación de independencia judicial
  - Gobernar por decreto sin Asamblea
  - Eliminación de libertad de expresión
  - Concentración de poderes en Ejecutivo
- **Fuentes históricas**: Resoluciones CIDH, sentencias Corte Interamericana
- **Flag**: `venezuela_similarity`
- **Severidad**: Alta

**NOTA CRÍTICA**: Estos flags detectan **solo patrones objetivos de comportamiento** verificables históricamente, **NO ideología política**. El objetivo es alertar sobre riesgos de deterioro democrático basado en evidencia objetiva.

---

## Criterios de Objetividad

### ✅ Evidencia Objetiva (Aceptable)

1. **Sentencias judiciales**:
   - Poder Judicial de Costa Rica
   - Cortes internacionales (CIDH, Corte Interamericana)
   - Resoluciones de organismos internacionales

2. **Registros públicos verificables**:
   - Actas de sesiones legislativas
   - Resoluciones de organismos de control
   - Informes de Contraloría

3. **Propuestas actuales del plan**:
   - Texto extraído del plan de gobierno
   - Análisis de viabilidad constitucional

### ❌ Evidencia Subjetiva (NO Aceptable)

1. **Opiniones políticas**
2. **Acusaciones sin sentencia**
3. **Rumores o especulaciones**
4. **Posiciones ideológicas legítimas**

---

## Implementación Propuesta

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
        ],
        "summary": "Evidencia histórica de comportamiento anti-democrático verificable"
      },
      "human_rights_violations": {
        "active": false,
        "evidence": []
      },
      "corruption_convictions": {
        "active": false,
        "evidence": []
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
        ],
        "summary": "Propuestas actuales que violan separación de poderes"
      }
    },
    "contradictions": {
      "historical_current_contradiction": {
        "active": true,
        "severity": "high",
        "evidence": {
          "historical": "Comportamiento anti-democrático histórico",
          "current": "Propuestas actuales que violan separación de poderes",
          "pattern": "Patrón consistente de comportamiento no democrático"
        },
        "summary": "Contradicción entre comportamiento histórico y propuestas actuales"
      }
    }
  }
}
```

### Integración en `process_plans_v7.py`

```python
def analyze_democratic_flags(
    candidate_id: str,
    historical_evidence: Dict,
    current_proposals: List[Dict]
) -> Dict:
    """
    Analiza flags informativos basados en evidencia histórica y propuestas actuales.
    
    NO penaliza, solo informa.
    """
    flags = {
        "historical": {},
        "current_proposals": {},
        "contradictions": {}
    }
    
    # 1. Analizar evidencia histórica
    if historical_evidence.get("anti_democratic_behavior"):
        flags["historical"]["anti_democratic_behavior"] = {
            "active": True,
            "severity": "high",
            "evidence": historical_evidence["anti_democratic_behavior"],
            "summary": "Evidencia histórica de comportamiento anti-democrático verificable"
        }
    
    # 2. Analizar propuestas actuales (usar sistema de viabilidad existente)
    for proposal in current_proposals:
        viability = check_viability(proposal["text"], proposal["pillar_id"])
        if viability["total_penalty"] < 0:
            # Hay violación detectada
            flags["current_proposals"]["violates_separation_powers"] = {
                "active": True,
                "severity": "high",
                "evidence": [{
                    "pillar_id": proposal["pillar_id"],
                    "proposal_text": proposal["text"][:200],
                    "detected_by": "viability_check"
                }]
            }
    
    # 3. Detectar contradicciones
    if (flags["historical"].get("anti_democratic_behavior", {}).get("active") and
        flags["current_proposals"].get("violates_separation_powers", {}).get("active")):
        flags["contradictions"]["historical_current_contradiction"] = {
            "active": True,
            "severity": "high",
            "evidence": {
                "historical": "Comportamiento anti-democrático histórico",
                "current": "Propuestas actuales que violan separación de poderes",
                "pattern": "Patrón consistente de comportamiento no democrático"
            }
        }
    
    return flags
```

---

## Fuentes de Evidencia Histórica

### Fuentes Objetivas y Verificables

1. **Poder Judicial de Costa Rica**:
   - Sentencias judiciales
   - Resoluciones de cortes
   - URL: https://www.poder-judicial.go.cr/

2. **Contraloría General de la República**:
   - Informes de auditoría
   - Resoluciones
   - URL: https://www.cgr.go.cr/

3. **Corte Interamericana de Derechos Humanos**:
   - Sentencias
   - URL: https://www.corteidh.or.cr/

4. **Comisión Interamericana de Derechos Humanos**:
   - Informes
   - Resoluciones
   - URL: https://www.oas.org/es/cidh/

5. **Asamblea Legislativa**:
   - Actas de sesiones
   - Proyectos de ley
   - URL: https://www.asamblea.go.cr/

---

## Presentación al Ciudadano

### En el Frontend

**Opción 1: Badge Informativo**
```
⚠️ Información: Este candidato tiene evidencia histórica de comportamiento 
anti-democrático verificable. Ver detalles →
```

**Opción 2: Sección Expandible**
```
📋 Información Adicional
├─ ⚠️ Evidencia Histórica
│  └─ Comportamiento anti-democrático (2020): [Ver evidencia]
├─ ⚠️ Propuestas Actuales
│  └─ Propuestas que violan separación de poderes: [Ver propuestas]
└─ ⚠️ Patrón Detectado
   └─ Contradicción entre comportamiento histórico y propuestas actuales
```

**Opción 3: Modal de Información**
```
Al hacer clic en "Ver información adicional":
- Muestra evidencia histórica con fuentes
- Muestra propuestas actuales problemáticas
- Muestra contradicciones detectadas
- NO afecta el score (solo informa)
```

---

## Neutralidad y Objetividad

### Principios de Implementación

1. **Solo evidencia verificable**:
   - Sentencias judiciales
   - Resoluciones de organismos oficiales
   - Propuestas extraídas del plan actual

2. **No opiniones políticas**:
   - No penalizamos posiciones ideológicas
   - No juzgamos si algo es "bueno" o "malo"
   - Solo informamos evidencia objetiva

3. **Transparencia total**:
   - Todas las fuentes son públicas
   - Todas las evidencias son verificables
   - El ciudadano decide qué hacer con la información

4. **No afecta scoring**:
   - Los flags son informativos
   - NO se restan puntos
   - NO se cambia el ranking
   - Solo se informa

---

## Ejemplo de Uso

### Caso: Candidato con Evidencia Histórica

**Evidencia histórica**:
- 2020: Sentencia judicial por intento de eliminar independencia del Poder Judicial
- 2018: Resolución de CIDH por violación de derechos humanos

**Propuestas actuales**:
- "Eliminar la Asamblea Legislativa y gobernar por decreto"
- "Suspender libertad de expresión para combatir fake news"

**Flags detectados**:
1. ✅ `historical_anti_democratic_behavior` (evidencia histórica)
2. ✅ `proposal_violates_separation_powers` (propuesta actual)
3. ✅ `proposal_violates_fundamental_rights` (propuesta actual)
4. ✅ `historical_current_contradiction` (patrón consistente)

**Presentación al ciudadano**:
```
⚠️ Información Adicional Disponible

Este candidato tiene:
- Evidencia histórica de comportamiento anti-democrático (2020)
- Propuestas actuales que violan separación de poderes
- Propuestas actuales que violan derechos fundamentales
- Patrón consistente detectado

[Ver detalles y fuentes] [Cerrar]
```

**Score**: NO se afecta (solo se informa)

---

## Recomendaciones de Implementación

### Fase 1: Flags de Propuestas Actuales (Ya Implementado)

✅ **Ya tenemos**: Sistema de viabilidad que detecta violaciones en propuestas actuales
- Viola separación de poderes
- Viola derechos fundamentales
- Viola garantías constitucionales
- Viola procedimientos constitucionales

**Acción**: Convertir estas penalizaciones en flags informativos (mantener penalización pero agregar flag)

### Fase 2: Base de Datos de Evidencia Histórica

**Crear**: Archivo `historical_evidence.json` con evidencia verificable

```json
{
  "candidate_id": "ejemplo",
  "evidence": [
    {
      "type": "judicial_sentence",
      "date": "2020-01-15",
      "source": "Poder Judicial",
      "description": "...",
      "verification_url": "..."
    }
  ]
}
```

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

## Consideraciones Importantes

### ⚠️ Riesgos a Evitar

1. **Sesgo político**:
   - ❌ NO incluir opiniones políticas
   - ❌ NO juzgar ideología (socialismo, capitalismo, etc.)
   - ✅ SOLO evidencia verificable
   - ✅ SOLO patrones objetivos de comportamiento

2. **Falsos positivos**:
   - ❌ NO incluir acusaciones sin sentencia
   - ❌ NO incluir similitudes ideológicas (solo comportamentales)
   - ✅ SOLO evidencia concluida
   - ✅ SOLO patrones históricamente verificables

3. **Manipulación**:
   - ❌ NO permitir que flags afecten scoring
   - ❌ NO usar lenguaje sesgado
   - ✅ SOLO informar
   - ✅ SOLO lenguaje neutral y objetivo

4. **Sesgo en modelos dictatoriales**:
   - ❌ NO juzgar ideología política
   - ❌ NO incluir solo ciertos modelos (aplicar a todos)
   - ✅ SOLO detectar patrones objetivos verificables
   - ✅ SOLO basarse en hechos históricos documentados

### ✅ Garantías de Neutralidad

1. **Criterios objetivos**: Solo evidencia verificable
2. **Fuentes públicas**: Todas las fuentes son accesibles
3. **No afecta scoring**: Flags son informativos, no penalizaciones
4. **Transparencia total**: Ciudadano ve todas las evidencias y fuentes
5. **NO ideología**: Solo patrones objetivos de comportamiento, NO posiciones ideológicas
6. **Aplicación igualitaria**: Mismos criterios para todos los candidatos
7. **Lenguaje neutral**: Solo hechos objetivos, sin juicios de valor

---

## Conclusión

### ✅ Sistema Propuesto

**Flags informativos** que:
- ✅ Informan sin penalizar
- ✅ Basados en evidencia objetiva
- ✅ Transparentes y verificables
- ✅ Mantienen neutralidad

**Implementación**:
- Fase 1: Usar sistema de viabilidad existente (ya detecta propuestas problemáticas)
- Fase 2: Crear base de datos de evidencia histórica
- Fase 3: Implementar detección de contradicciones

**Resultado**:
- Ciudadano informado
- Neutralidad mantenida
- Transparencia total
- Decisión informada

---

**Fecha**: 2026-01-11  
**Estado**: Propuesta lista para implementación
