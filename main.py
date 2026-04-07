import argparse
import json
import sys

def print_registros(registros):
    """Muestra los registros de forma legible en consola."""
    print("\n" + "═" * 60)
    print(f"  ✅ {len(registros)} registro(s) listos para subir:")
    print("═" * 60)
    for i, r in enumerate(registros, start=1):
        print(f"\n  [{i}] Proyecto : {r['proyecto']}")
        print(f"       Tarea    : {r['tarea_short']}")
        print(f"       Detalle  : {r['tarea_long']}")
        print(f"       Horas    : {r['horas']}")
        print(f"       Fecha    : {r['fecha']}")
    print("\n" + "═" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="🚀 SuiteCRM Automation - Cargador de tiempos",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--source",
        choices=["excel", "word"],
        required=True,
        help="Fuente de datos:\n  excel → lee suite_excel/registry.xlsx\n  word  → lee suite_ia/registry.docx (procesado por IA)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra los registros extraídos sin subir nada al CRM"
    )
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Desactiva la pausa de depuración (sube directamente sin revisar)"
    )

    args = parser.parse_args()

    # ── Leer registros según la fuente ────────────────────────────────────
    registros = []

    if args.source == "excel":
        from suite_excel.loader import leer_registros_excel
        ruta = "suite_excel/registry.xlsx"
        print(f"\n📂 Leyendo registros desde: {ruta}")
        try:
            registros = leer_registros_excel(ruta)
        except Exception as e:
            print(f"❌ ERROR leyendo Excel: {e}")
            sys.exit(1)

    elif args.source == "word":
        from suite_ia.processor import leer_word, extraer_datos_multiples
        ruta = "suite_ia/registry.docx"
        print(f"\n📂 Leyendo archivo Word: {ruta}")
        try:
            texto = leer_word(ruta)
        except Exception as e:
            print(f"❌ ERROR leyendo Word: {e}")
            sys.exit(1)

        print("🤖 Procesando texto con IA...")
        registros = extraer_datos_multiples(texto)

    # ── Validar que haya registros ─────────────────────────────────────────
    if not registros:
        print("⚠️  No se encontraron registros válidos. Abortando.")
        sys.exit(0)

    # ── Mostrar registros siempre ──────────────────────────────────────────
    print_registros(registros)

    # ── Modo dry-run: solo mostrar, no subir ───────────────────────────────
    if args.dry_run:
        print("\n🧪 MODO DRY-RUN activado — no se ha subido nada al CRM.\n")
        sys.exit(0)

    # ── Confirmación antes de subir (solo Word, el Excel es más directo) ───
    if args.source == "word":
        print("¿Deseas subir estos registros a SuiteCRM? (s/n): ", end="")
        respuesta = input().strip().lower()
        if respuesta != "s":
            print("Carga cancelada.")
            sys.exit(0)

    # ── Ejecutar automatización ────────────────────────────────────────────
    from core.automation import exec_auto_load

    exec_auto_load(
        registros=registros,
        headless=False,
        pausa_debug=not args.no_debug,
    )


if __name__ == "__main__":
    main()
