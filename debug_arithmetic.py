"""
debug_arithmetic.py
Script para debuggear el validador con expresiones aritméticas
"""

from ContextFreeGrammar import ContextFreeGrammar
from PredefinedGrammars import PredefinedGrammars
from collections import deque

def debug_validate(cfg, target, max_depth=100):
    """Validador con información de debug"""
    
    print(f"\n🔍 DEBUGGEANDO VALIDACIÓN DE: '{target}'")
    print("="*70)
    
    # Normalizar target
    if target == '' or target.lower() == 'epsilon':
        target_normalized = 'ε'
    else:
        target_normalized = target
    
    from ContextFreeGrammar import DerivationStep
    
    # Cola para BFS
    queue = deque()
    
    initial_step = DerivationStep(
        string=cfg.start_symbol,
        step_number=0
    )
    
    queue.append((cfg.start_symbol, [initial_step], 0))
    visited = set()
    iterations = 0
    max_iterations = 10000  # Limitado para debug
    
    matches_found = []
    
    while queue and iterations < max_iterations:
        iterations += 1
        
        if iterations % 1000 == 0:
            print(f"  Iteración {iterations}, cola: {len(queue)}, visitados: {len(visited)}")
        
        current_string, history, depth = queue.popleft()
        
        # Profundidad máxima
        if depth > max_depth:
            continue
        
        # Normalizar current_string
        if current_string == '':
            current_normalized = 'ε'
        else:
            current_normalized = current_string
        
        # ¡ÉXITO!
        if current_normalized == target_normalized:
            print(f"\n✅ ¡ENCONTRADO! en iteración {iterations}, profundidad {depth}")
            print(f"   Cadena: {current_string}")
            return True, history
        
        # Estado ya visitado
        state = (current_string, depth)
        if state in visited:
            continue
        visited.add(state)
        
        # Poda
        if len(current_string) > len(target_normalized) + 5:
            has_nt = any(c in cfg.non_terminals for c in current_string)
            if not has_nt:
                continue
        
        # Encontrar no terminales
        nt_positions = cfg._find_non_terminals(current_string)
        
        if not nt_positions:
            # Es una cadena terminal pero no coincide
            if len(current_string) <= 15:  # Solo mostrar cadenas cortas
                if current_string not in [m[0] for m in matches_found]:
                    matches_found.append((current_string, depth))
                    if len(matches_found) <= 10:
                        print(f"  ❌ Cadena terminal NO coincide: '{current_string}' (prof: {depth})")
            continue
        
        # Derivación leftmost
        pos, symbol = nt_positions[0]
        
        if symbol not in cfg.productions:
            continue
        
        # Probar cada producción
        for production in cfg.productions[symbol]:
            # Aplicar la producción
            if production == 'ε' or production == cfg.epsilon:
                new_string = current_string[:pos] + current_string[pos+1:]
            else:
                new_string = current_string[:pos] + production + current_string[pos+1:]
            
            # Crear nuevo paso
            from ContextFreeGrammar import DerivationStep
            new_step = DerivationStep(
                string=new_string,
                applied_production=(symbol, production),
                position=pos,
                step_number=len(history)
            )
            
            new_history = history + [new_step]
            
            # Añadir a la cola
            queue.append((new_string, new_history, depth + 1))
    
    print(f"\n❌ NO ENCONTRADO después de {iterations} iteraciones")
    print(f"   Estados visitados: {len(visited)}")
    print(f"   Cadenas terminales encontradas: {len(matches_found)}")
    
    if matches_found:
        print("\n   Algunas cadenas terminales encontradas:")
        for s, d in matches_found[:10]:
            print(f"     - '{s}' (prof: {d})")
    
    return False, None

def main():
    print("🐛 DEBUG DEL VALIDADOR DE EXPRESIONES ARITMÉTICAS")
    print("="*70)
    
    cfg = PredefinedGrammars.create_arithmetic_expressions()
    
    print("\n📋 GRAMÁTICA:")
    for left, rights in cfg.productions.items():
        for right in rights:
            print(f"  {left} → {right}")
    
    # Probar expresiones simples
    test_cases = ['5', '3+5', '3+2']
    
    for expr in test_cases:
        is_valid, derivation = debug_validate(cfg, expr, max_depth=50)
        print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()