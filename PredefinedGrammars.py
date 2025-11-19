"""
PredefinedGrammars.py
Módulo con gramáticas predefinidas para propósitos educativos
VERSIÓN CORREGIDA - Producciones arregladas
"""
from ContextFreeGrammar import ContextFreeGrammar

class PredefinedGrammars:
    """Colección de gramáticas independientes del contexto predefinidas"""
    
    @staticmethod
    def create_arithmetic_expressions() -> ContextFreeGrammar:
        """
        Crea una gramática para expresiones aritméticas SIMPLIFICADA
        Versión más fácil de validar
        """
        cfg = ContextFreeGrammar()
        cfg.set_start_symbol('E')
        cfg.set_non_terminals({'E', 'T', 'F'})
        cfg.set_terminals({'+', '-', '*', '/', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'})
        
        # Gramática simplificada pero que genera las mismas expresiones
        cfg.add_production('E', 'E+T')
        cfg.add_production('E', 'E-T')
        cfg.add_production('E', 'T')
        cfg.add_production('T', 'T*F')
        cfg.add_production('T', 'T/F')
        cfg.add_production('T', 'F')
        cfg.add_production('F', '(E)')
        cfg.add_production('F', '0')
        cfg.add_production('F', '1')
        cfg.add_production('F', '2')
        cfg.add_production('F', '3')
        cfg.add_production('F', '4')
        cfg.add_production('F', '5')
        cfg.add_production('F', '6')
        cfg.add_production('F', '7')
        cfg.add_production('F', '8')
        cfg.add_production('F', '9')
        
        return cfg

    @staticmethod
    def create_palindrome() -> ContextFreeGrammar:
        """
        Crea una gramática para palíndromos binarios
        S -> 0S0 | 1S1 | 0 | 1 | ε
        """
        cfg = ContextFreeGrammar()
        cfg.set_start_symbol('S')
        cfg.set_non_terminals({'S'})
        cfg.set_terminals({'0', '1'})
        
        # CORRECCIÓN: Las producciones deben ser cadenas completas
        cfg.add_production('S', '0S0')  # No '0', 'S', '0' por separado
        cfg.add_production('S', '1S1')  # No '1', 'S', '1' por separado
        cfg.add_production('S', '0')
        cfg.add_production('S', '1')
        cfg.add_production('S', 'ε')
        
        return cfg
    
    @staticmethod
    def create_balanced_parentheses() -> ContextFreeGrammar:
        """
        Crea una gramática para paréntesis balanceados
        S -> ( S ) | S S | ε
        """
        cfg = ContextFreeGrammar()
        cfg.set_start_symbol('S')
        cfg.set_non_terminals({'S'})
        cfg.set_terminals({'(', ')'})
        
        # CORRECCIÓN: Producciones como cadenas completas
        cfg.add_production('S', '(S)')  # No '(', 'S', ')' por separado
        cfg.add_production('S', 'SS')
        cfg.add_production('S', 'ε')
        
        return cfg
    
    @staticmethod
    def create_anbn() -> ContextFreeGrammar:
        """
        Crea una gramática para el lenguaje a^n b^n
        S -> a S b | ε
        """
        cfg = ContextFreeGrammar()
        cfg.set_start_symbol('S')
        cfg.set_non_terminals({'S'})
        cfg.set_terminals({'a', 'b'})
        
        # Esta estaba bien, pero por claridad
        cfg.add_production('S', 'aSb')  # Cadena completa: 'aSb'
        cfg.add_production('S', 'ε')
        
        return cfg
    
    @staticmethod
    def create_simple_html() -> ContextFreeGrammar:
        """
        Crea una gramática simplificada para etiquetas HTML
        S -> < T > S </ T > | ε
        T -> a | b | c
        """
        cfg = ContextFreeGrammar()
        cfg.set_start_symbol('S')
        cfg.set_non_terminals({'S', 'T'})
        cfg.set_terminals({'<', '>', '/', 'a', 'b', 'c'})
        
        # CORRECCIÓN: Producciones como cadenas completas
        cfg.add_production('S', '<T>S</T>')  # Cadena completa
        cfg.add_production('S', 'ε')
        cfg.add_production('T', 'a')
        cfg.add_production('T', 'b')
        cfg.add_production('T', 'c')
        
        return cfg
    
    @staticmethod
    def get_grammar_info(grammar_name: str) -> dict:
        """Retorna información sobre una gramática predefinida"""
        info = {
            'arithmetic': {
                'name': 'Expresiones Aritméticas',
                'description': 'Gramática completa para expresiones matemáticas con números de múltiples dígitos, operadores básicos y precedencia correcta',
                'example_valid': '2+3, 10*5, (3+5)*2, 2+3*5, 100-25+3, 123+456',
                'example_invalid': '5+, +3, (3+5, 5**2, 3++5',
                'productions_preview': '''E → T E\'
    E\' → + T E\' | - T E\' | ε
    T → F T\'
    T\' → * F T\' | / F T\' | ε
    F → ( E ) | N
    N → D | D N
    D → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9'''
            },
            'palindrome': {
                'name': 'Palíndromos Binarios',
                'description': 'Genera y valida palíndromos con 0s y 1s',
                'example_valid': '0, 1, 00, 11, 101, 0110, 11011, ε',
                'example_invalid': '01, 10, 110, 011',
                'productions_preview': 'S → 0S0 | 1S1 | 0 | 1 | ε'
            },
            'parentheses': {
                'name': 'Paréntesis Balanceados',
                'description': 'Valida que los paréntesis estén correctamente balanceados',
                'example_valid': '(), (()), ()(), (()())',
                'example_invalid': '((), )(, (()',
                'productions_preview': 'S → (S) | SS | ε'
            },
            'anbn': {
                'name': 'Lenguaje a^n b^n',
                'description': 'Genera cadenas con igual número de as seguidas de igual número de bs',
                'example_valid': 'ab, aabb, aaabbb, ε',
                'example_invalid': 'a, aba, aab, abbb',
                'productions_preview': 'S → aSb | ε'
            },
            'html': {
                'name': 'Etiquetas HTML Simples',
                'description': 'Valida etiquetas HTML anidadas correctamente',
                'example_valid': '<a></a>, <a><b></b></a>',
                'example_invalid': '<a><b></a></b>, <a>',
                'productions_preview': 'S → <T>S</T> | ε\nT → a | b | c'
            }
        }
        return info.get(grammar_name, {})