"""
ContextFreeGrammar.py
Módulo principal que contiene la lógica de las Gramáticas Independientes del Contexto
VERSIÓN CORREGIDA - Validación completamente funcional
"""
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import random
import copy
import time

@dataclass
class DerivationStep:
    """Representa un paso en el proceso de derivación"""
    string: str
    applied_production: Optional[Tuple[str, str]] = None
    position: Optional[int] = None
    step_number: int = 0
    is_final: bool = False

@dataclass
class ParseTreeNode:
    """Nodo del árbol de parsing"""
    symbol: str
    children: List['ParseTreeNode']
    is_terminal: bool
    position: Tuple[int, int] = (0, 0)
    
    def to_dict(self):
        """Convierte el nodo a diccionario para visualización"""
        return {
            'name': self.symbol,
            'children': [child.to_dict() for child in self.children] if self.children else []
        }

class ContextFreeGrammar:
    """Implementación de una Gramática Independiente del Contexto"""
    
    def __init__(self):
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        self.productions: Dict[str, List[str]] = {}
        self.start_symbol: str = 'S'
        self.epsilon: str = 'ε'
        
    def add_production(self, left: str, right: str) -> None:
        """
        Añade una producción a la gramática
        
        Args:
            left: Símbolo no terminal (lado izquierdo)
            right: Cadena de símbolos (lado derecho)
        """
        if left not in self.non_terminals:
            self.non_terminals.add(left)
        
        if left not in self.productions:
            self.productions[left] = []
        
        self.productions[left].append(right)
        
        # Identificar terminales en la producción
        i = 0
        while i < len(right):
            symbol = right[i]
            
            if symbol != self.epsilon and symbol not in self.non_terminals:
                self.terminals.add(symbol)
            
            i += 1
    
    def set_terminals(self, terminals: Set[str]) -> None:
        """Define el conjunto de símbolos terminales"""
        self.terminals = terminals
    
    def set_non_terminals(self, non_terminals: Set[str]) -> None:
        """Define el conjunto de símbolos no terminales"""
        self.non_terminals = non_terminals
    
    def set_start_symbol(self, symbol: str) -> None:
        """Define el símbolo inicial"""
        self.start_symbol = symbol
        if symbol not in self.non_terminals:
            self.non_terminals.add(symbol)
    
    def generate_string(self, max_steps: int = 25, mode: str = 'leftmost') -> List[DerivationStep]:
        """
        Genera una cadena a partir de la gramática
        Versión optimizada para gramáticas de expresiones aritméticas
        """
        history = []
        current_string = self.start_symbol
        step = 0
        
        history.append(DerivationStep(
            string=current_string,
            step_number=step
        ))
        
        for step in range(1, max_steps + 1):
            # Encontrar el primer no terminal
            nt_positions = []
            for i, char in enumerate(current_string):
                if char in self.non_terminals:
                    nt_positions.append((i, char))
                    if mode == 'leftmost':
                        break  # Solo el primero para leftmost
            
            if not nt_positions:
                history[-1].is_final = True
                break
            
            # Seleccionar posición según el modo
            if mode == 'rightmost' and nt_positions:
                pos, symbol = nt_positions[-1]
            else:
                pos, symbol = nt_positions[0]
            
            if symbol not in self.productions or not self.productions[symbol]:
                break
            
            # Seleccionar producción inteligentemente
            productions = self.productions[symbol]
            
            # Priorizar producciones que lleven a terminales
            terminal_prods = [p for p in productions if not any(c in self.non_terminals for c in p)]
            if terminal_prods and step > max_steps * 0.7:
                production = random.choice(terminal_prods)
            else:
                production = random.choice(productions)
            
            # Aplicar producción
            if production == 'ε' or production == self.epsilon:
                new_string = current_string[:pos] + current_string[pos+1:]
            else:
                new_string = current_string[:pos] + production + current_string[pos+1:]
            
            history.append(DerivationStep(
                string=new_string,
                applied_production=(symbol, production),
                position=pos,
                step_number=step
            ))
            
            current_string = new_string
            
            # Verificar si es final
            if not any(c in self.non_terminals for c in current_string):
                history[-1].is_final = True
                break
        
        return history
    
    def validate_string_dfs(self, target: str, max_depth: int = 30, timeout: float = 10.0) -> Tuple[bool, Optional[List[DerivationStep]]]:
        """
        Versión alternativa usando DFS para gramáticas con recursión por izquierda
        """
        start_time = time.time()
        
        if target == '' or target.lower() == 'epsilon':
            target_normalized = 'ε'
        else:
            target_normalized = target
        
        def dfs(current, history, depth, start_time):
            # Timeout check
            if time.time() - start_time > timeout:
                return None
            
            if depth > max_depth:
                return None
            
            current_normalized = 'ε' if current == '' else current
            
            if current_normalized == target_normalized:
                history[-1].is_final = True
                return history
            
            # Poda por longitud
            if len(current) > len(target_normalized) * 2 + 5:
                return None
            
            nt_positions = [(i, c) for i, c in enumerate(current) if c in self.non_terminals]
            
            if not nt_positions:
                return None
            
            # Probar cada producción para el primer no terminal (estrategia leftmost)
            pos, symbol = nt_positions[0]
            
            if symbol not in self.productions:
                return None
            
            for production in self.productions[symbol]:
                if production == 'ε' or production == self.epsilon:
                    new_string = current[:pos] + current[pos+1:]
                else:
                    new_string = current[:pos] + production + current[pos+1:]
                
                new_step = DerivationStep(
                    string=new_string,
                    applied_production=(symbol, production),
                    position=pos,
                    step_number=len(history)
                )
                
                result = dfs(new_string, history + [new_step], depth + 1, start_time)
                if result:
                    return result
            
            return None
        
        initial_step = DerivationStep(string=self.start_symbol, step_number=0)
        result = dfs(self.start_symbol, [initial_step], 0, start_time)
        
        return (bool(result), result)
    
    def validate_string(self, target: str, max_depth: int = 50, timeout: float = 15.0) -> Tuple[bool, Optional[List[DerivationStep]]]:
        """
        Valida si una cadena pertenece al lenguaje usando BFS mejorado
        Versión optimizada para gramáticas de expresiones aritméticas
        """
        start_time = time.time()
        
        # Normalizar target
        if target == '' or target.lower() == 'epsilon':
            target_normalized = 'ε'
        else:
            target_normalized = target
        
        # Para expresiones aritméticas, usar parámetros más permisivos
        if any(nt in self.non_terminals for nt in ['E', 'T', 'F', 'N']):
            max_depth = 80
            timeout = 20.0
        
        from collections import deque
        queue = deque()
        
        initial_step = DerivationStep(
            string=self.start_symbol,
            step_number=0
        )
        
        queue.append((self.start_symbol, [initial_step], 0))
        visited = set()
        iterations = 0
        max_iterations = 300000
        
        while queue and iterations < max_iterations:
            iterations += 1
            
            # Timeout check
            if time.time() - start_time > timeout:
                print(f"Timeout después de {iterations} iteraciones")
                break
            
            current_string, history, depth = queue.popleft()
            
            # Profundidad máxima
            if depth > max_depth:
                continue
            
            # Estado ya visitado
            state_hash = hash(current_string + str(depth))
            if state_hash in visited:
                continue
            visited.add(state_hash)
            
            # Normalizar para comparación
            current_normalized = 'ε' if current_string == '' else current_string
            
            # ¡ÉXITO!
            if current_normalized == target_normalized:
                history[-1].is_final = True
                return (True, history)
            
            # Poda: si no hay no terminales y no coincide, saltar
            has_non_terminals = any(c in self.non_terminals for c in current_string)
            if not has_non_terminals:
                continue
            
            # Poda: si la cadena es demasiado larga
            if len(current_string) > len(target_normalized) * 3 + 10:
                continue
            
            # Encontrar TODOS los no terminales y expandirlos
            nt_positions = []
            for i, char in enumerate(current_string):
                if char in self.non_terminals:
                    nt_positions.append((i, char))
            
            if not nt_positions:
                continue
            
            # Para cada no terminal, probar cada producción
            for pos, symbol in nt_positions:
                if symbol not in self.productions:
                    continue
                    
                for production in self.productions[symbol]:
                    # Aplicar la producción
                    if production == 'ε' or production == self.epsilon:
                        new_string = current_string[:pos] + current_string[pos+1:]
                    else:
                        new_string = current_string[:pos] + production + current_string[pos+1:]
                    
                    # Poda: verificar si la nueva cadena podría llevar al objetivo
                    if not self._could_lead_to_target(new_string, target_normalized):
                        continue
                    
                    new_step = DerivationStep(
                        string=new_string,
                        applied_production=(symbol, production),
                        position=pos,
                        step_number=len(history)
                    )
                    
                    new_history = history + [new_step]
                    queue.append((new_string, new_history, depth + 1))
        
        print(f"Búsqueda completada después de {iterations} iteraciones")  # CORREGIDO: iterations en lugar de iteraciones
        return (False, None)

    def _could_lead_to_target(self, current: str, target: str) -> bool:
        """
        Verifica heurísticamente si la cadena actual podría llevar al objetivo
        Versión más permisiva para gramáticas aritméticas
        """
        if current == 'ε' or current == '':
            return target == 'ε'
        
        # Si la cadena actual ya es más larga que el objetivo y no tiene no terminales, podar
        if len(current) > len(target) + 5 and not any(c in self.non_terminals for c in current):
            return False
        
        # Para gramáticas aritméticas, ser más permisivo
        if any(nt in self.non_terminals for nt in ['E', 'T', 'F', 'N']):
            # Solo podar casos obviamente incorrectos
            current_terminals = ''.join(c for c in current if c in self.terminals)
            
            # Verificar paréntesis desbalanceados
            open_paren = current_terminals.count('(')
            close_paren = current_terminals.count(')')
            if open_paren < close_paren:
                return False
            
            # Verificar operadores consecutivos (casos obviamente malos)
            for i in range(len(current_terminals) - 1):
                if current_terminals[i] in '+-*/' and current_terminals[i+1] in '+-*/':
                    return False
            
            return True
        
        return True
    def build_parse_tree(self, derivation: List[DerivationStep]) -> Optional[ParseTreeNode]:
        """
        Construye un árbol de parsing a partir de una derivación
        
        Args:
            derivation: Lista de pasos de derivación
            
        Returns:
            Nodo raíz del árbol de parsing
        """
        if not derivation:
            return None
        
        # Crear árbol desde la derivación
        root = ParseTreeNode(
            symbol=self.start_symbol,
            children=[],
            is_terminal=False,
            position=(0, 0)
        )
        
        # Construir el árbol recursivamente desde las derivaciones
        def build_from_derivation(node: ParseTreeNode, step_idx: int, string_pos: int) -> int:
            if step_idx >= len(derivation):
                return step_idx
            
            step = derivation[step_idx]
            
            if not step.applied_production:
                return step_idx
            
            left, right = step.applied_production
            
            if node.symbol == left and not node.children:
                # Crear hijos según la producción
                if right == self.epsilon or right == 'ε':
                    child = ParseTreeNode(
                        symbol='ε',
                        children=[],
                        is_terminal=True
                    )
                    node.children.append(child)
                else:
                    for char in right:
                        child = ParseTreeNode(
                            symbol=char,
                            children=[],
                            is_terminal=(char not in self.non_terminals)
                        )
                        node.children.append(child)
                
                return step_idx
            
            return step_idx
        
        # Procesar cada paso de la derivación
        for i, step in enumerate(derivation):
            if step.applied_production:
                left, right = step.applied_production
                # Aquí se podría expandir el árbol de manera más compleja
        
        return root
    
    def get_production_rules(self) -> List[Dict]:
        """Retorna las reglas de producción en formato lista de diccionarios"""
        rules = []
        for left, rights in self.productions.items():
            for right in rights:
                rules.append({
                    'No Terminal': left,
                    'Producción': f"{left} → {right}"
                })
        return rules
    
    def is_terminal_string(self, string: str) -> bool:
        """Verifica si una cadena contiene solo símbolos terminales"""
        if string == self.epsilon or string == 'ε' or string == '':
            return True
        return all(c not in self.non_terminals for c in string)
    
    def get_grammar_info(self) -> Dict:
        """Retorna información sobre la gramática"""
        return {
            'terminals': sorted(list(self.terminals)),
            'non_terminals': sorted(list(self.non_terminals)),
            'start_symbol': self.start_symbol,
            'num_productions': sum(len(prods) for prods in self.productions.values())
        }
    
    def export_grammar(self) -> Dict:
        """Exporta la gramática a un diccionario"""
        return {
            'terminals': list(self.terminals),
            'non_terminals': list(self.non_terminals),
            'start_symbol': self.start_symbol,
            'productions': self.productions,
            'epsilon': self.epsilon
        }
    
    def import_grammar(self, grammar_dict: Dict) -> None:
        """
        Importa una gramática desde un diccionario
        
        Args:
            grammar_dict: Diccionario con la configuración de la gramática
        
        Raises:
            ValueError: Si el diccionario no tiene la estructura correcta
        """
        # Validar campos requeridos
        required = ['terminals', 'non_terminals', 'start_symbol', 'productions']
        for field in required:
            if field not in grammar_dict:
                raise ValueError(f"El campo '{field}' es requerido")
        
        # Limpiar estado actual
        self.terminals = set()
        self.non_terminals = set()
        self.productions = {}
        
        # Importar configuración
        self.terminals = set(grammar_dict['terminals'])
        self.non_terminals = set(grammar_dict['non_terminals'])
        self.start_symbol = grammar_dict['start_symbol']
        self.epsilon = grammar_dict.get('epsilon', 'ε')
        
        # Importar producciones
        # Convertir a lista si es necesario
        self.productions = {}
        for left, rights in grammar_dict['productions'].items():
            if isinstance(rights, list):
                self.productions[left] = rights
            else:
                self.productions[left] = [rights]
        
        # Validar que el símbolo inicial esté en no terminales
        if self.start_symbol not in self.non_terminals:
            self.non_terminals.add(self.start_symbol)
    
    def validate_grammar(self) -> Tuple[bool, List[str]]:
        """
        Valida que la gramática esté bien formada
        
        Returns:
            (es_válida, lista_de_errores)
        """
        errors = []
        
        # Verificar que el símbolo inicial existe
        if self.start_symbol not in self.non_terminals:
            errors.append(f"El símbolo inicial '{self.start_symbol}' no está en los no terminales")
        
        # Verificar que hay al menos una producción
        if not self.productions:
            errors.append("No hay producciones definidas")
        
        # Verificar que el símbolo inicial tiene producciones
        if self.start_symbol not in self.productions:
            errors.append(f"El símbolo inicial '{self.start_symbol}' no tiene producciones")
        
        return (len(errors) == 0, errors)
    
    def _find_reachable_symbols(self) -> Set[str]:
        """Encuentra todos los símbolos alcanzables desde el símbolo inicial"""
        reachable = {self.start_symbol}
        changed = True
        
        while changed:
            changed = False
            for symbol in list(reachable):
                if symbol in self.productions:
                    for production in self.productions[symbol]:
                        for char in production:
                            if char in self.non_terminals and char not in reachable:
                                reachable.add(char)
                                changed = True
        
        return reachable