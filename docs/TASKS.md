Comandos para Tests
Frontend. → pytest -m frontend
IR → pytest -m ir
Backend → pytest -m backend
Integración → pytest -m integracion

Integrante 1 — Frontend (lenguaje → AST)

    Objetivo: aceptar el subset del lenguaje y producir un AST válido.

    Implementar src/hc11cc/frontend/lexer.py

        Tokens: fn, main, let, return, u8
        Símbolos: ->, :, =, +, -, (, ), {, }, ;
        Literales enteros 0..255
        Identificadores

    Implementar src/hc11cc/frontend/parser.py

        Función única main
        let x: u8 = <expr>;
        return <expr>;
        Expresiones con + y -, paréntesis

    Implementar src/hc11cc/frontend/sema.py

        Verificación de tipos (u8)
        Error si literal > 255
        Error si variable no existe
        Error si variable se redeclara

    Endurecer tests tests/miembro1_frontend/test_frontend_smoke.py

        Casos válidos
        ≥ 2 casos inválidos (type mismatch, variable no definida)

    Done cuando:
        pytest -m frontend pasa.

Integrante 2 — IR (AST → IR)

    Objetivo: representar la semántica del programa en una IR simple y estable.

    Fase 1 — Base (MVP)

        Definir src/hc11cc/ir/ir.py

            ModuloIR, FuncionIR, InstrIR

        Instrucciones mínimas: ConstU8, LoadLocal, StoreLocal, AddU8, SubU8, Ret

    Implementar src/hc11cc/ir/builder.py

        AST → IR para literales, variables, suma/resta, return

        Conteo de temporales y locales

    Implementar src/hc11cc/ir/emit.py

        Impresión legible de IR para debug

    Endurecer tests tests/miembro2_ir/test_ir_smoke.py

        Verificar número de instrucciones IR
        Verificar presencia de Ret

    Done cuando:
        pytest -m ir pasa.

Integrante 3 — Backend HC11 (IR → ASM HC11)

    Objetivo: generar ensamblador HC11 correcto desde la IR.

    Fase 1 — Base (MVP)

        Definir src/hc11cc/backend/hc11/isa.py
            AsmProgram y representación mínima de instrucciones/operandos

    Implementar src/hc11cc/backend/hc11/isel.py

        ConstU8 → LDAA #imm
        LoadLocal / StoreLocal
        AddU8 → LDAA lhs,X + ADDA rhs,X + STAA dst,X
        SubU8 → LDAA lhs,X + SUBA rhs,X + STAA dst,X
        Ret → RTS

    Implementar src/hc11cc/backend/hc11/program.py (ABI v0)

        ORG
        LDS #stack_init
        JSR main
        halt con RTS o SWI

    Implementar src/hc11cc/backend/hc11/emit.py
        Impresión de .asm HC11

    Endurecer tests tests/miembro3_backend/test_backend_smoke.py
        Verificar que el ASM contenga ORG, LDS, JSR main, RTS

    Done cuando:
        pytest -m backend pasa.

Integración

    Objetivo: que el pipeline completo funcione end-to-end.

    Fase 1 — Humo
        Conectar pipeline en src/hc11cc/driver.py
            lex → parse → sema → build(IR) → select(HC11) → wrap(ABI) → emit(ASM)

        Endurecer tests/integracion/test_pipeline_smoke.py
            Compilar "fn main() -> u8 { return 7; }"
            Verificar que el ASM tenga main: y LDAA

        Acordar contratos entre módulos
            Estructura mínima del AST
            Estructura mínima del IR

    Done cuando:
        pytest -m integracion pasa.

Convenciones del equipo
No tocar módulos ajenos sin avisar.
Integrar solo cuando tu suite local pasa.
Si integración falla: rollback + fix antes de continuar.
