Plan de integración: Visualizador/Monitor del compilador (modo “debugger didáctico”)
Objetivo

Agregar una UI (HTML/JS) que permita ver y depurar el compilador por fases, mostrando:

Código fuente (editor)

Artefactos por fase (tokens, AST, IR, ASM, bytes)

Diagnósticos (errores/warnings con ubicación)

Navegación tipo Step / Back / Reset con historial

Sin convertir la UI en “otro compilador”; la UI es un monitor del compilador real.

Decisión de arquitectura (propuesta recomendada)
Enfoque híbrido: Step real + historial cacheado

Step: ejecuta exactamente 1 fase real del compilador si aún no existe el snapshot.

Back/Forward: navega snapshots ya generados (sin recomputar).

El historial es una lista de eventos: trace[].

Ventajas: fidelidad al compilador real + navegación fluida + desacoplamiento limpio.

Contrato de datos (fuente de verdad)

Definir un único tipo de mensaje intercambiado entre compilador y UI:

PipelineEvent

stage: "SOURCE" | "LEX" | "PARSE" | "SEMA" | "IR" | "BACKEND" | "ASM" | "BYTES"

ok: true/false

artifact:

kind: string (ej. "tokens", "ast", "ir", "asm", "bytes")

data: JSON (estructura cruda)

text: string opcional (vista “bonita”)

diagnostics: lista de:

severity: "info" | "warn" | "error"

message: string

span: opcional { line, col, len } (para highlight)

meta: opcional { timeMs, counters, hash }

Regla: la UI renderiza solo desde estos eventos. El compilador nunca toca el DOM.

Comunicación UI ↔ Compilador (dos modos)
Modo recomendado: proceso + stdin/stdout

La UI (o un runner) lanza el compilador como proceso.

La UI manda comandos por stdin:

{"cmd":"reset","source":"..."}

{"cmd":"step"}

{"cmd":"run_all"}

El compilador responde por stdout con PipelineEvent (una línea JSON por evento).

Ventajas: simple, sin servidor, buena para Windows, buena para equipo.

Modo alterno: servidor local + WebSocket

Útil si quieren “modo live” con múltiples clientes.

Más infraestructura.

Pipeline del compilador (para que el monitor exista)

Separar el compilador en fases puras (o casi puras):

LEX(source) -> tokens

PARSE(tokens) -> ast

SEMA(ast) -> ast_validado/tabla símbolos/diagnostics

LOWER(ast) -> ir

BACKEND(ir) -> asm_model

EMIT(asm_model) -> asm_text + bytes

Cada fase produce:

artefacto serializable

diagnostics

status ok/error

Regla: error en una fase detiene el avance (pero el evento de error sí se emite).

Modelo interno del monitor (UI)

Store único (ViewModel):

source: string

trace: PipelineEvent[]

cursor: number (posición actual del usuario en la navegación)

liveStage: number (hasta dónde se ha ejecutado realmente)

playing: boolean

Render:

Panel izquierdo: editor + botones

Panel derecho: pipeline stages + artefacto + diagnostics

Highlight del editor usando span del evento actual (si existe)

Experiencia de usuario (UX) mínima

Controles:

Reset (borra trace, reinicia compilación con el source actual)

Step (genera siguiente evento real si no existe; si existe, navega)

Back / Forward

Run (ejecuta hasta terminar o fallar)

Export trace (descarga JSON de eventos)

Vista:

Etapa activa resaltada

Artefacto mostrado como:

tokens: lista

AST/IR: JSON pretty o tabla

ASM: texto

bytes: hex dump

Diagnostics: lista con severidad

Estrategia de implementación por fases (sin comprometer al equipo)
Fase 0 — “Solo UI” (sin integración)

UI sigue siendo demo.

Define PipelineEvent y el renderer.

Usa “mocks” (eventos falsos) para validar la vista.

Fase 1 — “Modo trace precomputado” (rápido)

compile_all(source) devuelve trace[].

UI solo navega.

Costo bajo, prueba de valor para el equipo.

Fase 2 — “Step real (híbrido)”

Compilador implementa reset/step.

UI manda comandos y recibe eventos en streaming.

Se guarda trace[] igual.

Fase 3 — “Debug real”

Spans precisos (línea/columna)

Modo verbose por fase (contadores, tiempos, dumps)

Export/Import de trace para reproducir bugs

Entregables técnicos (para repartir el trabajo)

Especificación: pipeline_protocol.md (definición de PipelineEvent + comandos)

UI: monitor/index.html (store + renderer + controles)

Driver: tools/monitor_bridge.py o runner equivalente (si se necesita)

Compilador:

compiler/session.py (estado y step())

compiler/phases/\*.py (lex/parse/sema/ir/backend/emit)

compiler/formatters/\*.py (to_text para cada artefacto)

Riesgos y límites (controlados)

Divergencia UI vs compilador: evitada porque la UI no calcula, solo muestra eventos.

Sobrecarga para el equipo: mitigada con “Fase 1” (trace precomputado) antes de “Step real”.

Formato inestable: mitigado con contrato único versionado (protocol_version).
