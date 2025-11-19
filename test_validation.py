"""
test_validation.py
Script para probar la validación de cadenas
Ejecuta esto en la terminal para verificar que funciona
"""

from ContextFreeGrammar import ContextFreeGrammar
from PredefinedGrammars import PredefinedGrammars

def test_grammar(grammar_name, grammar_func, valid_strings, invalid_strings):
    """Prueba una gramática con cadenas válidas e inválidas"""
    print(f"\n{'='*60}")
    print(f"PROBANDO: {grammar_name}")
    print(f"{'='*60}")
    
    cfg = grammar_func()
    
    print("\n✅ CADENAS VÁLIDAS (deberían aceptarse):")
    for string in valid_strings:
        display = string if string != '' else 'ε (cadena vacía)'
        is_valid, derivation = cfg.validate_string(string, max_depth=25, timeout=10.0)
        
        status = "✓ CORRECTO" if is_valid else "✗ ERROR (debería ser válida)"
        steps = f"({len(derivation)} pasos)" if derivation else ""
        print(f"  {display:<20} -> {status} {steps}")
    
    print("\n❌ CADENAS INVÁLIDAS (deberían rechazarse):")
    for string in invalid_strings:
        is_valid, derivation = cfg.validate_string(string, max_depth=25, timeout=10.0)
        
        status = "✓ CORRECTO" if not is_valid else "✗ ERROR (debería ser inválida)"
        print(f"  {string:<20} -> {status}")

def main():
    print("🧪 INICIANDO PRUEBAS DE VALIDACIÓN")
    print("="*60)
    
    # Test 1: Palíndromos binarios
    test_grammar(
        "Palíndromos Binarios",
        PredefinedGrammars.create_palindrome,
        ['', '0', '1', '00', '11', '101', '010', '0110', '1001', '11011'],
        ['01', '10', '110', '011', '100', 'abc', '0101']
    )
    
    # Test 2: a^n b^n
    test_grammar(
        "Lenguaje a^n b^n",
        PredefinedGrammars.create_anbn,
        ['', 'ab', 'aabb', 'aaabbb', 'aaaabbbb'],
        ['a', 'b', 'ba', 'aab', 'abb', 'aaabb', 'aabbb']
    )
    
    # Test 3: Paréntesis balanceados
    test_grammar(
        "Paréntesis Balanceados",
        PredefinedGrammars.create_balanced_parentheses,
        ['', '()', '(())', '()()', '(()())', '((()))'],
        ['(', ')', ')(', '(()' , '())', '(()', '()(']
    )
    
    # Test 4: Expresiones aritméticas (más complejo)
    print("\n" + "="*60)
    print("PROBANDO: Expresiones Aritméticas")
    print("="*60)
    print("\n⚠️ NOTA: Las expresiones aritméticas son más complejas")
    print("Probando algunas cadenas simples...")
    
    cfg = PredefinedGrammars.create_arithmetic_expressions()
    
    test_cases = [
        ('n', True, "número simple"),
        ('n+n', True, "suma simple"),
        ('n*n', True, "multiplicación simple"),
        ('(n)', True, "número entre paréntesis"),
        ('n++n', False, "dos operadores seguidos"),
        ('(n', False, "paréntesis sin cerrar"),
    ]
    
    print("\n📝 Casos de prueba:")
    for string, should_be_valid, description in test_cases:
        is_valid, derivation = cfg.validate_string(string, max_depth=30, timeout=10.0)
        
        if is_valid == should_be_valid:
            status = "✓ CORRECTO"
        else:
            status = "✗ ERROR"
        
        expected = "válida" if should_be_valid else "inválida"
        result = "válida" if is_valid else "inválida"
        steps = f"({len(derivation)} pasos)" if derivation else ""
        
        print(f"  {string:<15} [{description:<25}]")
        print(f"    Esperado: {expected:<10} | Obtenido: {result:<10} | {status} {steps}")
    
    print("\n" + "="*60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("="*60)
    print("\nSi ves '✓ CORRECTO' en todas las pruebas, ¡la validación funciona!")
    print("Si ves '✗ ERROR', revisa el código de validación.")

if __name__ == "__main__":
    main()