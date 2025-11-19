"""
debug_validator.py
Script para debuggear el validador y ver exactamente qué pasa
"""

from ContextFreeGrammar import ContextFreeGrammar
from PredefinedGrammars import PredefinedGrammars

def debug_validation(grammar_name, grammar_func, test_string):
    """Debuggea una validación específica"""
    print(f"\n{'='*70}")
    print(f"DEBUGGING: {grammar_name}")
    print(f"Cadena objetivo: '{test_string}'")
    print(f"{'='*70}\n")
    
    cfg = grammar_func()
    
    # Mostrar información de la gramática
    print("📋 GRAMÁTICA:")
    print(f"  Símbolo inicial: {cfg.start_symbol}")
    print(f"  No terminales: {cfg.non_terminals}")
    print(f"  Terminales: {cfg.terminals}")
    print(f"\n  Producciones:")
    for left, rights in cfg.productions.items():
        for right in rights:
            print(f"    {left} → {right}")
    
    # Intentar generar algunas cadenas
    print(f"\n🎲 GENERANDO 5 CADENAS DE EJEMPLO:")
    for i in range(5):
        derivation = cfg.generate_string(max_steps=15, mode='random')
        if derivation:
            final = derivation[-1].string
            print(f"  {i+1}. {final} ({len(derivation)} pasos)")
    
    # Validar la cadena objetivo
    print(f"\n🔍 VALIDANDO CADENA: '{test_string}'")
    
    # Versión con más info
    import time
    start_time = time.time()
    
    is_valid, derivation = cfg.validate_string(test_string, max_depth=25, timeout=10.0)
    
    elapsed = time.time() - start_time
    
    if is_valid:
        print(f"✅ VÁLIDA (encontrada en {elapsed:.3f} segundos)")
        print(f"\n📜 Derivación encontrada ({len(derivation)} pasos):")
        for step in derivation:
            if step.applied_production:
                left, right = step.applied_production
                print(f"  Paso {step.step_number}: {step.string} (aplicó {left} → {right})")
            else:
                print(f"  Paso {step.step_number}: {step.string} (inicio)")
    else:
        print(f"❌ INVÁLIDA (búsqueda terminó en {elapsed:.3f} segundos)")
        print("  No se encontró ninguna derivación que genere esta cadena")

def main():
    print("🐛 MODO DEBUG - ANÁLISIS DETALLADO")
    print("="*70)
    
    # Test 1: Palíndromos con '0'
    debug_validation(
        "Palíndromos - Caso simple '0'",
        PredefinedGrammars.create_palindrome,
        '0'
    )
    
    # Test 2: Palíndromos con '101'
    debug_validation(
        "Palíndromos - Caso '101'",
        PredefinedGrammars.create_palindrome,
        '101'
    )
    
    # Test 3: Paréntesis con '()'
    debug_validation(
        "Paréntesis - Caso simple '()'",
        PredefinedGrammars.create_balanced_parentheses,
        '()'
    )
    
    # Test 4: a^n b^n con 'ab' (que SÍ funciona)
    debug_validation(
        "a^n b^n - Caso 'ab' (que funciona)",
        PredefinedGrammars.create_anbn,
        'ab'
    )

if __name__ == "__main__":
    main()