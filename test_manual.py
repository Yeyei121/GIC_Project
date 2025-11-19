"""
test_manual.py
Prueba manual para entender el problema
"""

from ContextFreeGrammar import ContextFreeGrammar

# Crear una gramática de palíndromos MANUALMENTE
print("🔨 Creando gramática de palíndromos manualmente...")
cfg = ContextFreeGrammar()
cfg.set_start_symbol('S')
cfg.set_non_terminals({'S'})
cfg.set_terminals({'0', '1'})

# Ver las producciones ANTES de agregarlas
print("\n📝 Agregando producciones...")

print("  Agregando: S → 0S0")
cfg.add_production('S', '0S0')

print("  Agregando: S → 1S1")
cfg.add_production('S', '1S1')

print("  Agregando: S → 0")
cfg.add_production('S', '0')

print("  Agregando: S → 1")
cfg.add_production('S', '1')

print("  Agregando: S → ε")
cfg.add_production('S', 'ε')

# Verificar qué quedó almacenado
print("\n🔍 VERIFICANDO qué se almacenó:")
print(f"  Productions dict: {cfg.productions}")
print(f"  Non-terminals: {cfg.non_terminals}")
print(f"  Terminals: {cfg.terminals}")

# Intentar generar cadenas
print("\n🎲 GENERANDO 10 CADENAS:")
for i in range(10):
    derivation = cfg.generate_string(max_steps=10, mode='random')
    if derivation:
        final = derivation[-1].string
        print(f"  {i+1}. '{final}'")

# Ahora validar manualmente algunas cadenas
print("\n✅ VALIDANDO CADENAS:")

test_cases = ['', '0', '1', '00', '101', '0110']

for test in test_cases:
    display = test if test else 'ε (vacía)'
    print(f"\n  Probando: '{display}'")
    
    is_valid, derivation = cfg.validate_string(test, max_depth=20, timeout=5.0)
    
    if is_valid:
        print(f"    ✓ VÁLIDA")
        if derivation:
            print(f"    Derivación: ", end='')
            for step in derivation[:5]:  # Solo primeros 5 pasos
                print(f"{step.string} → ", end='')
            if len(derivation) > 5:
                print("...")
            else:
                print(f"{derivation[-1].string}")
    else:
        print(f"    ✗ INVÁLIDA")

print("\n" + "="*60)
print("Si ninguna cadena se valida correctamente,")
print("el problema está en el algoritmo de validación.")
print("="*60)