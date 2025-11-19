"""
Prueba con una gramática aritmética MÁS SIMPLE
Para verificar si el problema es la complejidad
"""

from ContextFreeGrammar import ContextFreeGrammar

def create_simple_arithmetic():
    """
    Gramática SIMPLIFICADA solo con números de 1 dígito
    Para probar si el validador funciona
    
    E → N | N + E | N * E
    N → 0 | 1 | 2 | ... | 9
    """
    cfg = ContextFreeGrammar()
    cfg.set_start_symbol('E')
    cfg.set_non_terminals({'E', 'N'})
    cfg.set_terminals({'+', '*', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'})
    
    # Expresiones simples
    cfg.add_production('E', 'N')      # E → N (solo número)
    cfg.add_production('E', 'N+E')    # E → N + E (suma)
    cfg.add_production('E', 'N*E')    # E → N * E (multiplicación)
    
    # Números
    for digit in '0123456789':
        cfg.add_production('N', digit)
    
    return cfg

def test_simple():
    print("🧪 PROBANDO GRAMÁTICA SIMPLIFICADA")
    print("="*70)
    
    cfg = create_simple_arithmetic()
    
    print("\n📋 GRAMÁTICA:")
    for left, rights in cfg.productions.items():
        for right in rights:
            print(f"  {left} → {right}")
    
    print("\n✅ VALIDANDO:")
    
    test_cases = [
        '5',      # Solo número
        '3+5',    # Suma
        '2*3',    # Multiplicación
        '1+2+3',  # Múltiples sumas
    ]
    
    for expr in test_cases:
        print(f"\n  Probando: '{expr}'")
        is_valid, derivation = cfg.validate_string(expr, max_depth=30, timeout=10.0)
        
        if is_valid:
            steps = len(derivation) if derivation else 0
            print(f"    ✓ VÁLIDA ({steps} pasos)")
            
            # Mostrar derivación
            if derivation and len(derivation) <= 10:
                print("    Derivación:")
                for step in derivation:
                    if step.applied_production:
                        l, r = step.applied_production
                        print(f"      {step.step_number}. {step.string} (aplicó {l} → {r})")
                    else:
                        print(f"      {step.step_number}. {step.string} (inicio)")
        else:
            print(f"    ✗ INVÁLIDA")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_simple()