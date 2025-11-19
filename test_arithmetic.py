"""
test_arithmetic.py
Script para probar la gramática de expresiones aritméticas CLÁSICA
Con precedencia de operadores correcta
"""

from ContextFreeGrammar import ContextFreeGrammar
from PredefinedGrammars import PredefinedGrammars

def test_arithmetic_grammar():
    print("🧮 PROBANDO GRAMÁTICA CLÁSICA DE EXPRESIONES ARITMÉTICAS")
    print("="*70)
    
    cfg = PredefinedGrammars.create_arithmetic_expressions()
    
    # Mostrar información
    print("\n📋 INFORMACIÓN DE LA GRAMÁTICA:")
    print(f"  Símbolo inicial: {cfg.start_symbol}")
    print(f"  No terminales: {cfg.non_terminals}")
    print(f"  Terminales: {cfg.terminals}")
    
    print("\n📝 PRODUCCIONES:")
    for left, rights in cfg.productions.items():
        for right in rights:
            print(f"  {left} → {right}")
    
    # Validar expresiones
    print("\n✅ VALIDANDO EXPRESIONES (SOLO DÍGITOS INDIVIDUALES):")
    
    test_cases = [
        ('5', True, "número simple"),
        ('3+2', True, "suma simple"),
        ('4*5', True, "multiplicación simple"),
        ('2+3*4', True, "precedencia (* antes que +)"),
        ('(2+3)*4', True, "paréntesis cambian precedencia"),
        ('9-1', True, "resta simple"),
        ('8/2', True, "división simple"),
        ('(3+2)', True, "número entre paréntesis"),
        ('-5', True, "número negativo"),
        ('-(3+2)', True, "expresión negativa"),
        ('1+2+3', True, "múltiples sumas"),
        ('2*3*4', True, "múltiples multiplicaciones"),
        ('5+', False, "operador sin operando"),
        ('+3', False, "comienza con +"),
        ('(3+2', False, "paréntesis sin cerrar"),
        ('3++5', False, "dos operadores seguidos"),
    ]
    
    print("\n⚠️ NOTA: Esta gramática usa solo dígitos individuales (0-9)")
    print("   Para validar números como '23', necesitas escribirlos como operaciones: '2*10+3'\n")
    
    for expr, should_be_valid, description in test_cases:
        print(f"  Probando: '{expr}' ({description})")
        is_valid, derivation = cfg.validate_string(expr, max_depth=50, timeout=15.0)
        
        steps = len(derivation) if derivation else 0
        
        if is_valid == should_be_valid:
            status = "✓ CORRECTO"
        else:
            status = "✗ ERROR"
        
        expected = "válida" if should_be_valid else "inválida"
        result = "válida" if is_valid else "inválida"
        
        print(f"    Esperado: {expected:<10} | Obtenido: {result:<10} | {status} ({steps} pasos)")
        
        # Si es válida, intentar evaluar
        if is_valid and should_be_valid:
            try:
                resultado = eval(expr)
                print(f"    Evaluación: {expr} = {resultado}")
            except:
                pass
    
    print("\n" + "="*70)
    print("✅ PRUEBA COMPLETADA")
    print("\n💡 CARACTERÍSTICAS DE ESTA GRAMÁTICA:")
    print("   ✓ Precedencia correcta de operadores (*, / antes que +, -)")
    print("   ✓ Soporte para números negativos")
    print("   ✓ Paréntesis para cambiar precedencia")
    print("   ✓ Basada en la gramática clásica de compiladores")
    print("   ⚠ Solo acepta dígitos individuales (0-9)")

if __name__ == "__main__":
    test_arithmetic_grammar()