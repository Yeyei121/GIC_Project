"""
UIComponentsCFG.py
Módulo con componentes de interfaz de usuario para el simulador de GIC
VERSIÓN FINAL - Con árbol de derivación y vista interactiva mejorada
"""
import streamlit as st
from typing import List, Dict
from ContextFreeGrammar import DerivationStep, ParseTreeNode
import pandas as pd
import json

class UIComponentsCFG:
    """Componentes reutilizables para la interfaz de usuario de GIC"""
    
    @staticmethod
    def apply_custom_css():
        """Aplica estilos CSS personalizados"""
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                text-align: center;
                color: #2E7D32;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .sub-header {
                text-align: center;
                color: #666;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            .derivation-display {
                font-family: 'Courier New', monospace;
                font-size: 1.5rem;
                background: linear-gradient(135deg, #43A047 0%, #66BB6A 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .production-box {
                background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
                padding: 15px;
                border-left: 5px solid #0288D1;
                margin: 15px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            .success-box {
                background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                padding: 20px;
                border-left: 5px solid #4CAF50;
                margin: 15px 0;
                border-radius: 5px;
                animation: slideIn 0.5s ease-out;
            }
            .error-box {
                background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
                padding: 20px;
                border-left: 5px solid #F44336;
                margin: 15px 0;
                border-radius: 5px;
            }
            .info-box {
                background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
                padding: 20px;
                border-left: 5px solid #9C27B0;
                margin: 15px 0;
                border-radius: 5px;
            }
            .step-counter {
                background-color: #2E7D32;
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
                display: inline-block;
                font-weight: bold;
                margin: 10px 0;
            }
            .grammar-rule {
                background-color: #FFF3E0;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 1.1rem;
            }
            @keyframes slideIn {
                from {
                    transform: translateX(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            .terminal {
                color: #D32F2F;
                font-weight: bold;
            }
            .non-terminal {
                color: #1976D2;
                font-weight: bold;
            }
            
            /* Estilos para el árbol interactivo */
            .tree-node {
                background: #f0f0f0;
                border: 2px solid #333;
                border-radius: 8px;
                padding: 8px 12px;
                margin: 5px;
                display: inline-block;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .tree-node:hover {
                background: #e0e0e0;
                transform: scale(1.05);
            }
            .tree-node-terminal {
                background: #ffcdd2;
                border-color: #d32f2f;
                color: #b71c1c;
            }
            .tree-node-non-terminal {
                background: #bbdefb;
                border-color: #1976d2;
                color: #0d47a1;
            }
            .tree-container {
                background: #fafafa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                overflow-x: auto;
            }
            
            /* Estilos para las hojas verdes */
            .leaf-container {
                background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #4CAF50;
                margin: 10px 0;
                text-align: center;
            }
            .leaf-symbol {
                font-size: 1.8rem;
                font-weight: bold;
                color: #1B5E20;
                font-family: 'Courier New', monospace;
            }
            .root-node {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                border: 3px solid #2E7D32;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Renderiza el encabezado principal"""
        st.markdown('<h1 class="main-header">🤖 Simulador de Gramáticas Independientes del Contexto</h1>', 
                   unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Herramienta didáctica interactiva para comprender las GIC</p>', 
                   unsafe_allow_html=True)
        
    @staticmethod
    def evaluate_arithmetic_expression(expression: str) -> tuple:
        """
        Evalúa una expresión aritmética de forma segura
        
        Args:
            expression: Cadena con la expresión (ej: "3+5*2")
            
        Returns:
            (resultado, error_msg) - Si hay error, resultado es None
        """
        try:
            # Limpiar la expresión de no terminales residuales
            # Solo mantener dígitos, operadores y paréntesis
            cleaned = ''.join(c for c in expression if c in '0123456789+-*/(). ')
            
            # Si está vacía después de limpiar, no es evaluable
            if not cleaned or cleaned.isspace():
                return None, "Expresión vacía o con símbolos no terminales"
            
            # Verificar que solo tenga caracteres válidos
            valid_chars = set('0123456789+-*/(). ')
            if not all(c in valid_chars for c in cleaned):
                return None, "Contiene caracteres inválidos"
            
            # Evaluar de forma segura
            result = eval(cleaned, {"__builtins__": {}}, {})
            
            return result, None
            
        except ZeroDivisionError:
            return None, "División por cero"
        except SyntaxError:
            return None, "Sintaxis inválida"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    @staticmethod
    def render_arithmetic_result(expression: str):
        """
        Renderiza el resultado de una expresión aritmética si es válida
        """
        result, error = UIComponentsCFG.evaluate_arithmetic_expression(expression)
        
        if error:
            # No mostrar nada si hay error (expresión incompleta)
            return
        
        if result is not None:
            # Mostrar el resultado de forma bonita
            result_html = f"""
            <div style="
                background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                border-left: 5px solid #4CAF50;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <h3 style="margin: 0 0 10px 0; color: #2E7D32;">
                    🧮 Resultado de la evaluación:
                </h3>
                <div style="
                    font-size: 2rem;
                    font-family: 'Courier New', monospace;
                    font-weight: bold;
                    color: #1B5E20;
                    text-align: center;
                    padding: 15px;
                    background: white;
                    border-radius: 10px;
                ">
                    {expression} = {result}
                </div>
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_parse_tree_simple(derivation: List[DerivationStep]):
        """Renderiza ambas vistas: la interactiva y el árbol con conexiones"""
        if not derivation:
            st.info("No hay derivación para mostrar")
            return
        
        # Crear pestañas para ambas vistas
        tab1, tab2 = st.tabs(["🎯 Vista Interactiva", "🌳 Árbol con Conexiones"])
        
        with tab1:
            UIComponentsCFG._render_interactive_view(derivation)
        
        with tab2:
            UIComponentsCFG._render_tree_with_connections(derivation)
    
    @staticmethod
    def _render_interactive_view(derivation: List[DerivationStep]):
        """Renderiza la vista interactiva que te gusta"""
        st.subheader("🎯 Vista Interactiva del Árbol de Derivación")
        
        # Mostrar información general
        if derivation:
            final_step = derivation[-1]
            st.success(f"**Cadena final:** `{final_step.string if final_step.string else 'ε (cadena vacía)'}`")
            st.info(f"**Total de pasos:** {len(derivation)}")
        
        # Contenedor principal del árbol
        with st.container():
            # NODO RAÍZ - Siempre visible
            if derivation:
                root = derivation[0]
                st.markdown(f"""
                <div class="root-node">
                    <h3 style="margin: 0;">🌳 NODO RAÍZ</h3>
                    <div style="font-size: 2rem; margin: 15px 0; font-weight: bold;">{root.string}</div>
                    <small style="font-size: 1rem;">Símbolo inicial - Paso {root.step_number}</small>
                </div>
                """, unsafe_allow_html=True)
            
            # PROCESO DE DERIVACIÓN - Mostrar con expanders interactivos
            st.subheader("📋 Proceso de Derivación")
            
            for i, step in enumerate(derivation):
                with st.expander(f"**Paso {step.step_number}**: `{step.string if step.string else 'ε'}`", 
                               expanded=(i == 0 or i == len(derivation)-1)):
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Cadena actual:** `{step.string if step.string else 'ε (cadena vacía)'}`")
                        
                        if step.applied_production:
                            left, right = step.applied_production
                            st.markdown(f"""
                            <div class="production-box">
                                <strong>🎯 Producción aplicada:</strong><br>
                                <span style="font-size: 1.3rem;">
                                    {left} → <strong>{right if right != 'ε' else 'ε (cadena vacía)'}</strong>
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if step.position is not None:
                            st.info(f"**Posición expandida:** {step.position}")
                    
                    with col2:
                        if step.is_final:
                            st.success("✅ **Derivación completa**")
                        else:
                            st.info("🔄 **En progreso**")
            
            # HOJAS DEL ÁRBOL - Mostrar símbolos terminales finales en recuadros verdes
            st.subheader("🍃 Hojas del Árbol (Símbolos Terminales)")
            
            if derivation:
                final_string = derivation[-1].string
                if final_string:
                    # Separar los símbolos terminales
                    terminals = list(final_string)
                    if not terminals:
                        st.markdown(f"""
                        <div class="leaf-container">
                            <div class="leaf-symbol">ε</div>
                            <small>Cadena vacía</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Mostrar cada terminal en un recuadro verde
                        cols = st.columns(len(terminals) if len(terminals) <= 6 else 6)
                        for idx, terminal in enumerate(terminals):
                            col_idx = idx % 6
                            with cols[col_idx]:
                                st.markdown(f"""
                                <div class="leaf-container">
                                    <div class="leaf-symbol">{terminal}</div>
                                    <small>Símbolo terminal</small>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Resumen final de la derivación
                st.divider()
                st.subheader("📊 Resumen Final")
                
                summary_cols = st.columns(3)
                with summary_cols[0]:
                    st.metric("Pasos totales", len(derivation))
                with summary_cols[1]:
                    final_str = derivation[-1].string if derivation[-1].string else "ε"
                    st.metric("Cadena final", final_str)
                with summary_cols[2]:
                    complete = "Sí" if derivation[-1].is_final else "No"
                    st.metric("Derivación completa", complete)
    
    @staticmethod
    def _render_tree_with_connections(derivation: List[DerivationStep]):
        """Renderiza el árbol de derivación con conexiones reales - VERSIÓN MEJORADA"""
        st.subheader("🌳 Árbol de Derivación con Conexiones")
        
        # Construir el árbol de derivación real
        tree_structure = UIComponentsCFG._build_proper_parse_tree(derivation)
        
        if not tree_structure:
            st.warning("No se pudo construir el árbol de derivación")
            return
        
        # Calcular posiciones para el layout del árbol
        max_level = UIComponentsCFG._calculate_tree_layout(tree_structure)
        
        # Calcular altura dinámica basada en la profundidad del árbol
        tree_height = UIComponentsCFG._calculate_tree_height(tree_structure, max_level)
        
        # Construir el HTML con conexiones
        html_content = UIComponentsCFG._build_tree_with_connections_html(tree_structure, tree_height)
        
        # Mostrar el árbol con altura dinámica
        st.components.v1.html(html_content, height=tree_height, scrolling=True)
        
        # Resumen informativo
        if derivation:
            final_step = derivation[-1]
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #4CAF50;">
                <h4>📊 Resumen del Árbol</h4>
                <p><strong>Raíz:</strong> <code>{tree_structure['symbol']}</code></p>
                <p><strong>Cadena final:</strong> <code>{final_step.string if final_step.string else 'ε'}</code></p>
                <p><strong>Total de pasos:</strong> {len(derivation)}</p>
                <p><strong>Profundidad del árbol:</strong> {max_level + 1} niveles</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Leyenda
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4>📖 Leyenda del Árbol</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; border-radius: 50%; background: #4CAF50; margin-right: 10px; border: 2px solid #2E7D32;"></div>
                    <span><strong>Raíz:</strong> Símbolo inicial</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; border-radius: 50%; background: #2196F3; margin-right: 10px; border: 2px solid #0D47A1;"></div>
                    <span><strong>No Terminal:</strong> Se expande</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; border-radius: 50%; background: #FF9800; margin-right: 10px; border: 2px solid #E65100;"></div>
                    <span><strong>Terminal:</strong> Hoja final</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
    @staticmethod
    def _build_proper_parse_tree(derivation: List[DerivationStep]):
        """Construye un árbol de derivación real con estructura jerárquica"""
        if not derivation:
            return None
        
        # El árbol comienza con el símbolo inicial como raíz
        root = {
            'id': 'root_0',
            'symbol': derivation[0].string,
            'type': 'root',
            'children': [],
            'level': 0,
            'parent': None,
            'x': 0,
            'y': 0
        }
        
        # Reconstruir el árbol paso a paso desde la derivación
        current_level = [root]
        node_counter = 1
        level_height = 120
        
        for step_idx, step in enumerate(derivation[1:], 1):
            if not step.applied_production:
                continue
                
            left, right = step.applied_production
            
            # Encontrar el próximo no terminal a expandir (estrategia leftmost)
            next_node_to_expand = None
            for node in current_level:
                if node['symbol'] == left and node['type'] in ['root', 'non_terminal'] and not node.get('expanded', False):
                    next_node_to_expand = node
                    break
            
            if not next_node_to_expand:
                continue
            
            # Marcar nodo como expandido
            next_node_to_expand['expanded'] = True
            next_node_to_expand['production'] = f"{left} → {right}"
            
            # Crear nodos hijos
            child_symbols = list(right) if right != 'ε' else ['ε']
            new_children = []
            
            for symbol in child_symbols:
                child_id = f"node_{node_counter}"
                # Determinar si es terminal o no terminal
                is_terminal = symbol not in ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                                           'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                
                child_node = {
                    'id': child_id,
                    'symbol': symbol,
                    'type': 'terminal' if is_terminal else 'non_terminal',
                    'children': [],
                    'level': step_idx,
                    'parent': next_node_to_expand['id'],
                    'production': f"{left} → {right}",
                    'x': 0,  # Se calculará después
                    'y': step_idx * level_height
                }
                
                new_children.append(child_node)
                node_counter += 1
            
            # Conectar los hijos al padre
            next_node_to_expand['children'] = new_children
            
            # Actualizar current_level: reemplazar el nodo expandido por sus hijos no terminales
            new_level = []
            for node in current_level:
                if node['id'] == next_node_to_expand['id']:
                    # Agregar los hijos no terminales al siguiente nivel
                    for child in new_children:
                        if child['type'] == 'non_terminal':
                            new_level.append(child)
                else:
                    new_level.append(node)
            
            current_level = new_level
        
        return root
    
    @staticmethod
    def _calculate_tree_height(tree_structure, max_level):
        """Calcula la altura dinámica del árbol basada en su profundidad"""
        # Altura base + altura por nivel
        base_height = 400
        height_per_level = 120
        
        # Calcular altura total
        total_height = base_height + (max_level * height_per_level)
        
        # Limitar altura máxima para no hacer la interfaz demasiado grande
        max_allowed_height = 1200
        min_allowed_height = 500
        
        # Ajustar altura dentro de límites razonables
        adjusted_height = max(min_allowed_height, min(total_height, max_allowed_height))
        
        return adjusted_height
    
    @staticmethod
    def _calculate_tree_layout(tree_structure):
        """Calcula las posiciones x,y para cada nodo en el árbol - VERSIÓN MEJORADA"""
        level_nodes = {}
        max_level = 0
        
        def count_nodes(node, level=0):
            nonlocal max_level
            max_level = max(max_level, level)
            
            if level not in level_nodes:
                level_nodes[level] = []
            level_nodes[level].append(node)
            
            for child in node.get('children', []):
                count_nodes(child, level + 1)
        
        count_nodes(tree_structure)
        
        # Ajustar espaciado basado en la cantidad de niveles
        node_spacing = 80
        if max_level > 5:
            node_spacing = 60  # Menos espacio si hay muchos niveles
        elif max_level > 8:
            node_spacing = 40  # Aún menos espacio para árboles muy grandes
        
        for level, nodes in level_nodes.items():
            total_width = len(nodes) * node_spacing
            start_x = -total_width / 2
            
            for i, node in enumerate(nodes):
                node['x'] = start_x + i * node_spacing + 400
                node['y'] = level * 120 + 80  # Más margen superior
        
        return max_level
    
    @staticmethod
    def _build_tree_with_connections_html(tree_structure, tree_height=600):
        """Construye el HTML completo con nodos y conexiones - VERSIÓN MEJORADA"""
        
        # Recolectar todos los nodos y conexiones
        all_nodes = []
        all_connections = []
        
        def collect_nodes_and_connections(node):
            all_nodes.append(node)
            
            for child in node.get('children', []):
                connection = {
                    'from_x': node['x'],
                    'from_y': node['y'],
                    'to_x': child['x'],
                    'to_y': child['y'],
                    'from_id': node['id'],
                    'to_id': child['id']
                }
                all_connections.append(connection)
                collect_nodes_and_connections(child)
        
        collect_nodes_and_connections(tree_structure)
        
        # Calcular el ancho necesario basado en los nodos
        min_x = min((node['x'] for node in all_nodes), default=0)
        max_x = max((node['x'] for node in all_nodes), default=0)
        container_width = max(800, (max_x - min_x) + 200)  # Ancho mínimo de 800px
        
        # Construir el HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    font-family: Arial, sans-serif;
                    overflow: auto;
                    width: 100%;
                    height: 100%;
                }}
                .tree-container {{
                    position: relative;
                    width: {container_width}px;
                    height: {tree_height}px;
                    min-width: 800px;
                    min-height: 500px;
                    margin: 0 auto;
                }}
                .tree-node {{
                    position: absolute;
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                    cursor: pointer;
                    z-index: 10;
                    text-align: center;
                }}
                .tree-node:hover {{
                    transform: scale(1.15);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                    z-index: 20;
                }}
                .node-root {{
                    background: linear-gradient(135deg, #4CAF50, #45a049);
                    color: white;
                    border: 4px solid #2E7D32;
                    font-size: 1.3em;
                }}
                .node-non-terminal {{
                    background: linear-gradient(135deg, #2196F3, #1976D2);
                    color: white;
                    border: 3px solid #0D47A1;
                }}
                .node-terminal {{
                    background: linear-gradient(135deg, #FF9800, #F57C00);
                    color: white;
                    border: 3px solid #E65100;
                }}
                .connection {{
                    position: absolute;
                    background: #666;
                    transform-origin: 0 0;
                    z-index: 1;
                    pointer-events: none;
                    height: 2px;
                }}
                .production-tooltip {{
                    position: absolute;
                    background: rgba(0,0,0,0.9);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 0.85em;
                    font-family: 'Courier New', monospace;
                    white-space: nowrap;
                    z-index: 30;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.3s;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                }}
                .scroll-container {{
                    width: 100%;
                    height: 100%;
                    overflow: auto;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background: white;
                }}
            </style>
        </head>
        <body>
            <div class="scroll-container">
                <div class="tree-container" id="treeContainer">
                    <!-- Conexiones -->
                    {UIComponentsCFG._generate_connections_html(all_connections)}
                    
                    <!-- Nodos -->
                    {UIComponentsCFG._generate_nodes_html(all_nodes)}
                </div>
            </div>
            
            <script>
                function showTooltip(element, text) {{
                    const tooltip = document.createElement('div');
                    tooltip.className = 'production-tooltip';
                    tooltip.textContent = text;
                    
                    const rect = element.getBoundingClientRect();
                    const containerRect = document.getElementById('treeContainer').getBoundingClientRect();
                    
                    tooltip.style.left = (rect.left - containerRect.left + rect.width / 2) + 'px';
                    tooltip.style.top = (rect.top - containerRect.top - 40) + 'px';
                    
                    document.getElementById('treeContainer').appendChild(tooltip);
                    
                    setTimeout(() => {{
                        tooltip.style.opacity = '1';
                    }}, 10);
                    
                    element.addEventListener('mouseleave', function() {{
                        tooltip.style.opacity = '0';
                        setTimeout(() => {{
                            if (tooltip.parentNode) {{
                                tooltip.parentNode.removeChild(tooltip);
                            }}
                        }}, 300);
                    }}, {{ once: true }});
                }}
                
                // Agregar event listeners a los nodos
                document.querySelectorAll('.tree-node').forEach(node => {{
                    const production = node.getAttribute('data-production');
                    if (production && production !== 'None') {{
                        node.addEventListener('mouseenter', function(e) {{
                            showTooltip(this, production);
                        }});
                    }}
                }});

                // Calcular y dibujar conexiones dinámicamente
                function drawConnections() {{
                    const connections = document.querySelectorAll('.connection-data');
                    connections.forEach(conn => {{
                        const fromX = parseFloat(conn.getAttribute('data-from-x'));
                        const fromY = parseFloat(conn.getAttribute('data-from-y'));
                        const toX = parseFloat(conn.getAttribute('data-to-x'));
                        const toY = parseFloat(conn.getAttribute('data-to-y'));
                        
                        const dx = toX - fromX;
                        const dy = toY - fromY;
                        const length = Math.sqrt(dx * dx + dy * dy);
                        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                        
                        conn.style.left = fromX + 'px';
                        conn.style.top = fromY + 'px';
                        conn.style.width = length + 'px';
                        conn.style.transform = 'rotate(' + angle + 'deg)';
                    }});
                }}
                
                // Ajustar el contenedor al contenido después de cargar
                function adjustContainer() {{
                    const container = document.getElementById('treeContainer');
                    const nodes = container.querySelectorAll('.tree-node');
                    
                    if (nodes.length > 0) {{
                        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
                        
                        nodes.forEach(node => {{
                            const x = parseFloat(node.style.left);
                            const y = parseFloat(node.style.top);
                            minX = Math.min(minX, x);
                            maxX = Math.max(maxX, x);
                            minY = Math.min(minY, y);
                            maxY = Math.max(maxY, y);
                        }});
                        
                        // Ajustar el tamaño del contenedor si es necesario
                        const neededWidth = maxX - minX + 200;
                        const neededHeight = maxY + 150;
                        
                        if (neededWidth > container.offsetWidth) {{
                            container.style.width = neededWidth + 'px';
                        }}
                        if (neededHeight > container.offsetHeight) {{
                            container.style.height = neededHeight + 'px';
                        }}
                    }}
                }}
                
                // Ejecutar cuando el DOM esté listo
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', function() {{
                        drawConnections();
                        setTimeout(adjustContainer, 100);
                    }});
                }} else {{
                    drawConnections();
                    setTimeout(adjustContainer, 100);
                }}
            </script>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def _generate_connections_html(connections):
        """Genera el HTML para las conexiones entre nodos"""
        connections_html = ""
        
        for conn in connections:
            connections_html += f"""
            <div class="connection connection-data"
                 data-from-x="{conn['from_x']}"
                 data-from-y="{conn['from_y']}"
                 data-to-x="{conn['to_x']}"
                 data-to-y="{conn['to_y']}">
            </div>
            """
        
        return connections_html
    
    @staticmethod
    def _generate_nodes_html(nodes):
        """Genera el HTML para todos los nodos"""
        nodes_html = ""
        
        for node in nodes:
            node_class = ""
            if node['type'] == 'root':
                node_class = "node-root"
            elif node['type'] == 'non_terminal':
                node_class = "node-non-terminal"
            else:
                node_class = "node-terminal"
            
            production = node.get('production', 'None')
            symbol_display = 'ε' if node['symbol'] == 'ε' else node['symbol']
            
            nodes_html += f"""
            <div class="tree-node {node_class}"
                 data-production="{production}"
                 style="
                    left: {node['x']}px;
                    top: {node['y']}px;
                    transform: translate(-50%, -50%);
                 "
                 title="{production if production != 'None' else 'Nodo inicial'}">
                {symbol_display}
            </div>
            """
        
        return nodes_html
    
    @staticmethod
    def render_derivation_history(history: List[DerivationStep], max_steps: int = 20):
        """Renderiza el historial de derivación"""
        st.subheader("📜 Historial de Derivación")
        
        if not history:
            st.info("No hay historial de derivación todavía")
            return
        
        # Mostrar hasta max_steps
        display_history = history[:max_steps] if len(history) > max_steps else history
        
        for step in display_history:
            with st.expander(f"Paso {step.step_number}: {step.string}", expanded=(step.step_number < 3)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    UIComponentsCFG.render_derivation_string(
                        step.string, 
                        step.step_number,
                        step.position if step.position is not None else -1
                    )
                
                with col2:
                    if step.applied_production:
                        UIComponentsCFG.render_production_applied(step.applied_production)
                    
                    if step.is_final:
                        st.success("✅ Derivación completa")
        
        if len(history) > max_steps:
            st.info(f"Mostrando {max_steps} de {len(history)} pasos. Ajusta max_steps para ver más.")
    
    @staticmethod
    def render_derivation_string(string: str, step: int, highlight_pos: int = -1):
        """Renderiza una cadena de derivación con resaltado"""
        st.markdown(f'<span class="step-counter">Paso {step}</span>', 
                   unsafe_allow_html=True)
        
        # Resaltar posición si se especifica
        display_string = string
        if highlight_pos >= 0 and highlight_pos < len(string):
            char = string[highlight_pos]
            display_string = (string[:highlight_pos] + 
                            f'<span style="background-color: yellow; padding: 2px 5px;">{char}</span>' + 
                            string[highlight_pos+1:])
        
        derivation_html = f"""
        <div class="derivation-display">
            {display_string}
        </div>
        """
        st.markdown(derivation_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_production_applied(production: tuple):
        """Renderiza la producción aplicada"""
        if production:
            left, right = production
            prod_html = f"""
            <div class="production-box">
                <strong>🔍 Producción aplicada:</strong> 
                <span class="non-terminal">{left}</span> → 
                <span>{right if right != 'ε' else '<em>ε (cadena vacía)</em>'}</span>
            </div>
            """
            st.markdown(prod_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_grammar_rules(rules: List[Dict]):
        """Renderiza las reglas de la gramática"""
        st.subheader("📋 Reglas de Producción")
        if rules:
            # Agrupar por no terminal
            grouped = {}
            for rule in rules:
                nt = rule['No Terminal']
                if nt not in grouped:
                    grouped[nt] = []
                prod = rule['Producción']
                grouped[nt].append(prod)
            
            # Mostrar agrupadas
            for nt, prods in grouped.items():
                all_prods = " | ".join([p.split(' → ')[1] for p in prods])
                st.markdown(f'<div class="grammar-rule">{nt} → {all_prods}</div>', 
                           unsafe_allow_html=True)
        else:
            st.warning("⚠️ No hay reglas de producción definidas")
    
    @staticmethod
    def render_grammar_info(info: Dict):
        """Renderiza información sobre una gramática"""
        if info:
            info_html = f"""
            <div class="info-box">
                <h3 style="margin-top: 0;">ℹ️ {info['name']}</h3>
                <p><strong>Descripción:</strong> {info['description']}</p>
                <p><strong>Cadenas válidas:</strong> <code>{info['example_valid']}</code></p>
                <p><strong>Cadenas inválidas:</strong> <code>{info['example_invalid']}</code></p>
                <hr>
                <p><strong>Producciones:</strong></p>
                <pre style="background-color: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px;">{info['productions_preview']}</pre>
            </div>
            """
            st.markdown(info_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_validation_result(is_valid: bool, message: str, derivation: List[DerivationStep] = None):
        """Renderiza el resultado de la validación"""
        if is_valid:
            result_html = f"""
            <div class="success-box">
                <h2 style="margin-top: 0;">✅ {message}</h2>
                <p>La cadena pertenece al lenguaje generado por la gramática.</p>
            </div>
            """
        else:
            result_html = f"""
            <div class="error-box">
                <h2 style="margin-top: 0;">❌ {message}</h2>
                <p>La cadena NO pertenece al lenguaje generado por la gramática.</p>
            </div>
            """
        st.markdown(result_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_tutorial():
        """Renderiza un tutorial interactivo y didáctico sobre GIC"""
        
        # Crear un recuadro atractivo para el encabezado
        st.markdown("""
        <style>
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 3px solid rgba(255,255,255,0.2);
            color: white;
        }
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            margin: 0 0 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .sub-title {
            font-size: 1.8rem;
            font-weight: 300;
            margin: 0;
            opacity: 0.9;
        }
        </style>
        
        <div class="header-container">
            <div class="main-title">🎓 Tutorial Interactivo</div>
            <div class="sub-title">Gramáticas Independientes del Contexto</div>
            <div style="margin-top: 15px; font-size: 1.2rem; opacity: 0.8;">
                Aprende conceptos fundamentales de forma interactiva y divertida
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Indicador de secciones
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA000 100%); 
                    color: white; padding: 15px; border-radius: 15px; 
                    text-align: center; margin: 20px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 1.4rem;">✨ Explora las diferentes secciones del tutorial</h3>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">
                Navega por las pestañas para descubrir conceptos, ejemplos y demostraciones interactivas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear pestañas para organizar el contenido
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📚 Conceptos Básicos", 
            "🎯 Ejemplos Prácticos", 
            "🔍 Análisis Paso a Paso",
            "🎮 Demos Interactivas",
            "📖 Recursos Adicionales"
        ])
        
        with tab1:
            UIComponentsCFG._render_basic_concepts()
        
        with tab2:
            UIComponentsCFG._render_practical_examples()
        
        with tab3:
            UIComponentsCFG._render_step_by_step_analysis()
        
        with tab4:
            UIComponentsCFG._render_interactive_demos()
        
        with tab5:
            UIComponentsCFG._render_additional_resources()

        st.divider()
        
        # Demostración animada de árbol de derivación
        st.markdown("""
        <div class="demo-header">
            <h2>🌳✨ Demostración Animada: Construcción de Árbol de Derivación</h2>
            <p>Observa cómo se construye un árbol de derivación paso a paso</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Selector de ejemplo
        example_option = st.selectbox(
            "Selecciona un ejemplo para visualizar:",
            [
                "Expresión Aritmética: n + n * n",
                "Palíndromo Binario: 1001", 
                "Paréntesis Balanceados: (())",
                "Lenguaje aⁿbⁿ: aabb"
            ],
            key="animation_example"
        )
        
        # Controles de animación
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⏪ Reiniciar Animación", use_container_width=True):
                if 'anim_step' in st.session_state:
                    st.session_state.anim_step = 0
                    st.rerun()
        
        with col2:
            anim_speed = st.slider("Velocidad de animación", 1, 5, 3, key="anim_speed")
        
        with col3:
            if st.button("▶️ Reproducir", use_container_width=True):
                st.session_state.anim_playing = True
                st.session_state.anim_step = 0
        
        # Animación del árbol de derivación
        st.markdown("""
        <div class="animation-container">
            <h3>🎬 Construcción del Árbol de Derivación</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar animación según el ejemplo seleccionado
        if example_option == "Expresión Aritmética: n + n * n":
            UIComponentsCFG._render_arithmetic_animation()
        elif example_option == "Palíndromo Binario: 1001":
            UIComponentsCFG._render_palindrome_animation()
        elif example_option == "Paréntesis Balanceados: (())":
            UIComponentsCFG._render_parentheses_animation()
        else:
            UIComponentsCFG._render_anbn_animation()
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h4 style="color: #1565C0; margin-top: 0;">💡 ¿Qué estás viendo?</h4>
            <p style="color: #333; font-size: 1.1rem;">Esta animación muestra cómo una <strong>Gramática Independiente del Contexto</strong> 
            construye un árbol de derivación paso a paso:</p>
        </div>
        """, unsafe_allow_html=True)

        # Componentes del proceso usando columnas y métricas visuales
        st.subheader("🎯 Componentes del Proceso de Derivación")

        # Crear una cuadrícula visual
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: #E8F5E9; border-radius: 10px;">
                <div style="font-size: 2.5rem;">🌱</div>
                <strong>Raíz</strong>
                <p style="font-size: 0.9rem; margin: 5px 0;">Símbolo inicial</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: #E3F2FD; border-radius: 10px;">
                <div style="font-size: 2.5rem;">🌿</div>
                <strong>Expansión</strong>
                <p style="font-size: 0.9rem; margin: 5px 0;">Aplica producciones</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: #FFF3E0; border-radius: 10px;">
                <div style="font-size: 2.5rem;">🍃</div>
                <strong>Hojas</strong>
                <p style="font-size: 0.9rem; margin: 5px 0;">Símbolos terminales</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: #F3E5F5; border-radius: 10px;">
                <div style="font-size: 2.5rem;">📖</div>
                <strong>Lectura</strong>
                <p style="font-size: 0.9rem; margin: 5px 0;">Cadena final</p>
            </div>
            """, unsafe_allow_html=True)

        # Explicación detallada
        with st.expander("🔍 Ver explicación detallada", expanded=True):
            st.markdown("""
            **Proceso completo de derivación:**
            
            1. **🌱 Raíz**: Todo comienza con el **símbolo inicial** (generalmente 'S')
            2. **🌿 Expansión**: Se aplican **producciones** para reemplazar no terminales
            3. **🍃 Hojas**: El proceso termina cuando solo quedan **símbolos terminales**
            4. **📖 Lectura**: Las **hojas leídas de izquierda a derecha** forman la cadena final
            
            **Ejemplo visual:**
            ```
             S
            / \\
            a  S
              / \\
             b   c
            ```
            **Cadena resultante:** a b c
            """)

        # Llamada a la acción
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                    padding: 20px; border-radius: 12px; margin: 15px 0; text-align: center;">
            <h4 style="color: #E65100; margin: 0;">🎮 ¡Experimenta con diferentes ejemplos!</h4>
            <p style="color: #333; margin: 10px 0 0 0;">
                Prueba los distintos ejemplos para ver cómo cambian los patrones de derivación
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Métodos auxiliares para las animaciones
    @staticmethod
    def _render_arithmetic_animation():
        """Renderiza animación para expresión aritmética"""
        
        steps = [
            {"tree": "E", "description": "Comenzamos con el símbolo inicial E"},
            {"tree": "E\n│\nE + T", "description": "Aplicamos E → E + T"},
            {"tree": "E\n│\nE + T\n│\nT + T", "description": "Aplicamos E → T"},
            {"tree": "E\n│\nE + T\n│\nT + T\n│\nF + T", "description": "Aplicamos T → F"},
            {"tree": "E\n│\nE + T\n│\nT + T\n│\nF + T\n│\nn + T", "description": "Aplicamos F → n"},
            {"tree": "E\n│\nE + T\n│\nT + T\n│\nF + T\n│\nn + T * F", "description": "Aplicamos T → T * F"},
            {"tree": "E\n│\nE + T\n│\nT + T\n│\nF + T\n│\nn + T * F\n│\nn + F * F", "description": "Aplicamos T → F"},
            {"tree": "E\n│\nE + T\n│\nT + T\n│\nF + T\n│\nn + T * F\n│\nn + F * F\n│\nn + n * n", "description": "Aplicamos F → n (dos veces)"},
        ]
        
        step = st.session_state.get('anim_step', 0) % len(steps)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**Paso {step + 1} de {len(steps)}**")
            st.info(steps[step]["description"])
            
            if st.button("⏭️ Siguiente Paso", key="next_arithmetic"):
                st.session_state.anim_step = (st.session_state.get('anim_step', 0) + 1) % len(steps)
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="tree-animation">
            <pre style="color: white; text-align: center; font-size: 1.1rem;">
            {steps[step]["tree"]}
            </pre>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def _render_palindrome_animation():
        """Renderiza animación para palíndromo binario"""
        
        steps = [
            {"tree": "S", "description": "Comenzamos con el símbolo inicial S"},
            {"tree": "S\n│\n1 S 1", "description": "Aplicamos S → 1S1"},
            {"tree": "S\n│\n1 S 1\n│\n1 0 S 0 1", "description": "Aplicamos S → 0S0"},
            {"tree": "S\n│\n1 S 1\n│\n1 0 S 0 1\n│\n1 0 0 1", "description": "Aplicamos S → ε (cadena vacía)"},
        ]
        
        step = st.session_state.get('anim_step', 0) % len(steps)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**Paso {step + 1} de {len(steps)}**")
            st.info(steps[step]["description"])
            
            if st.button("⏭️ Siguiente Paso", key="next_palindrome"):
                st.session_state.anim_step = (st.session_state.get('anim_step', 0) + 1) % len(steps)
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="tree-animation">
            <pre style="color: white; text-align: center; font-size: 1.3rem;">
            {steps[step]["tree"]}
            </pre>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def _render_parentheses_animation():
        """Renderiza animación para paréntesis balanceados"""
        
        steps = [
            {"tree": "S", "description": "Comenzamos con el símbolo inicial S"},
            {"tree": "S\n│\n( S )", "description": "Aplicamos S → (S)"},
            {"tree": "S\n│\n( S )\n│\n( ( S ) )", "description": "Aplicamos S → (S)"},
            {"tree": "S\n│\n( S )\n│\n( ( S ) )\n│\n( ( ) )", "description": "Aplicamos S → ε (cadena vacía)"},
        ]
        
        step = st.session_state.get('anim_step', 0) % len(steps)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**Paso {step + 1} de {len(steps)}**")
            st.info(steps[step]["description"])
            
            if st.button("⏭️ Siguiente Paso", key="next_parentheses"):
                st.session_state.anim_step = (st.session_state.get('anim_step', 0) + 1) % len(steps)
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="tree-animation">
            <pre style="color: white; text-align: center; font-size: 1.3rem;">
            {steps[step]["tree"]}
            </pre>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def _render_anbn_animation():
        """Renderiza animación para lenguaje aⁿbⁿ"""
        
        steps = [
            {"tree": "S", "description": "Comenzamos con el símbolo inicial S"},
            {"tree": "S\n│\na S b", "description": "Aplicamos S → aSb"},
            {"tree": "S\n│\na S b\n│\na a S b b", "description": "Aplicamos S → aSb"},
            {"tree": "S\n│\na S b\n│\na a S b b\n│\na a b b", "description": "Aplicamos S → ε (cadena vacía)"},
        ]
        
        step = st.session_state.get('anim_step', 0) % len(steps)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**Paso {step + 1} de {len(steps)}**")
            st.info(steps[step]["description"])
            
            if st.button("⏭️ Siguiente Paso", key="next_anbn"):
                st.session_state.anim_step = (st.session_state.get('anim_step', 0) + 1) % len(steps)
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="tree-animation">
            <pre style="color: white; text-align: center; font-size: 1.3rem;">
            {steps[step]["tree"]}
            </pre>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_basic_concepts():
        """Renderiza los conceptos básicos de GIC"""
        
        st.markdown("""
        <div class="concept-card">
            <h2>🧠 ¿Qué son las Gramáticas Independientes del Contexto?</h2>
            <p>Las <span class="highlight">Gramáticas Independientes del Contexto (GIC)</span> son un formalismo matemático 
            para describir lenguajes formales. Son fundamentales en la teoría de lenguajes formales y se usan extensamente 
            en compiladores y procesamiento de lenguaje natural.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Componentes principales
        st.subheader("🏗️ Componentes Principales")
        
        cols = st.columns(3)
        
        with cols[0]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 3rem;">🔤</div>
                <h3>Símbolos Terminales</h3>
                <p>Símbolos que aparecen en las cadenas del lenguaje</p>
                <p><strong>Ejemplo:</strong> a, b, 0, 1, +, *</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 3rem;">🔠</div>
                <h3>Símbolos No Terminales</h3>
                <p>Variables que se expanden usando producciones</p>
                <p><strong>Ejemplo:</strong> S, E, T, F</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 3rem;">📝</div>
                <h3>Producciones</h3>
                <p>Reglas de reescritura de la forma A → α</p>
                <p><strong>Ejemplo:</strong> S → aSb | ε</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 3rem;">🎯</div>
            <h3>Símbolo Inicial</h3>
            <p>El no terminal desde donde comienza la derivación (usualmente S)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Jerarquía de Chomsky - VERSIÓN MEJORADA CON COMPONENTES STREAMLIT
        st.subheader("📊 Jerarquía de Chomsky")
        
        st.markdown("""
        <div class="concept-card">
            <h3>La Jerarquía de Chomsky clasifica las gramáticas en 4 tipos:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Usar columns y containers de Streamlit en lugar de tabla HTML
        col1, col2, col3, col4 = st.columns([1, 2, 2, 3])
        
        with col1:
            st.markdown("**Tipo**")
            st.markdown("3")
            st.markdown("2")
            st.markdown("1")
            st.markdown("0")
        
        with col2:
            st.markdown("**Nombre**")
            st.markdown("Regulares")
            st.markdown("**Independientes del Contexto**")
            st.markdown("Sensibles al Contexto")
            st.markdown("Estructuradas por Frases")
        
        with col3:
            st.markdown("**Ejemplo**")
            st.markdown("a*")
            st.markdown("aⁿbⁿ")
            st.markdown("aⁿbⁿcⁿ")
            st.markdown("Todos los lenguajes")
        
        with col4:
            st.markdown("**Aplicación**")
            st.markdown("Expresiones regulares")
            st.markdown("Lenguajes de programación")
            st.markdown("Lenguaje natural")
            st.markdown("Inteligencia artificial")
        
        # Destacar la fila de GIC con un contenedor especial
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                    padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; 
                    margin: 10px 0;">
            <h4 style="margin: 0; color: #1B5E20;">🎯 Tipo 2 - Independientes del Contexto</h4>
            <p style="margin: 5px 0;"><strong>Ejemplo:</strong> aⁿbⁿ</p>
            <p style="margin: 5px 0;"><strong>Aplicación:</strong> Lenguajes de programación, compiladores</p>
            <p style="margin: 5px 0;"><strong>Característica:</strong> Más poderosas que las regulares pero menos que las sensibles al contexto</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p><strong>💡 Las GIC son el Tipo 2 en la jerarquía</strong> - más poderosas que las regulares 
            pero menos que las sensibles al contexto. Forman la base de los lenguajes de programación modernos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Versión alternativa con expanders para más detalles
        with st.expander("🔍 Ver detalles de cada tipo de gramática"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Tipo 3 - Regulares**
                - **Forma:** A → aB | a
                - **Ejemplo:** a*
                - **Aplicación:** Expresiones regulares, lexers
                - **Máquina equivalente:** Autómatas finitos
                """)
                
                st.markdown("""
                **Tipo 2 - Independientes del Contexto**
                - **Forma:** A → α
                - **Ejemplo:** aⁿbⁿ
                - **Aplicación:** Lenguajes de programación
                - **Máquina equivalente:** Autómatas de pila
                """)
            
            with col2:
                st.markdown("""
                **Tipo 1 - Sensibles al Contexto**
                - **Forma:** αAβ → αγβ
                - **Ejemplo:** aⁿbⁿcⁿ
                - **Aplicación:** Lenguaje natural
                - **Máquina equivalente:** Autómatas lineales acotados
                """)
                
                st.markdown("""
                **Tipo 0 - Estructuradas por Frases**
                - **Forma:** α → β
                - **Ejemplo:** Todos los lenguajes
                - **Aplicación:** Inteligencia artificial
                - **Máquina equivalente:** Máquina de Turing
                """)
    
    @staticmethod
    def _render_practical_examples():
        """Renderiza ejemplos prácticos de GIC usando componentes Streamlit nativos"""
        
        st.subheader("🎯 Ejemplos Prácticos de Gramáticas")
        
        # Ejemplo 1: Palíndromos
        with st.expander("🔁 Ejemplo 1: Gramática para Palíndromos Binarios", expanded=True):
            # Usar contenedores de Streamlit en lugar de HTML
            st.markdown("#### Objetivo: Generar palíndromos con 0s y 1s")
            
            st.markdown("**Gramática:**")
            st.code("S → 0S0 | 1S1 | 0 | 1 | ε", language="bnf")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cadenas válidas:**")
                st.markdown("- 0")
                st.markdown("- 1") 
                st.markdown("- 00")
                st.markdown("- 11")
                st.markdown("- 010")
                st.markdown("- 101")
                st.markdown("- 0110")
                st.markdown("- 1001")
                st.markdown("- ...")
            
            with col2:
                st.markdown("**Cadenas inválidas:**")
                st.markdown("- 01")
                st.markdown("- 10")
                st.markdown("- 001")
                st.markdown("- 110")
                st.markdown("- ...")
            
            st.markdown("**Derivación de '101':**")
            st.code("S → 1S1 → 101", language="bnf")
            
            # Demo interactiva
            if st.button("🎲 Generar palíndromo aleatorio", key="palindrome_demo"):
                # Aquí podrías generar un palíndromo aleatorio
                st.info("Ejemplo: 1001 (generado por la gramática)")
        
        # Ejemplo 2: Expresiones aritméticas
        with st.expander("🧮 Ejemplo 2: Gramática para Expresiones Aritméticas"):
            st.markdown("#### Objetivo: Generar expresiones matemáticas válidas")
            
            st.markdown("**Gramática:**")
            st.code("""E → E + T | E - T | T
    T → T * F | T / F | F  
    F → ( E ) | n""", language="bnf")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cadenas válidas:**")
                st.markdown("- n")
                st.markdown("- n+n")
                st.markdown("- n*n")
                st.markdown("- (n+n)")
                st.markdown("- (n+n)*n")
                st.markdown("- n*(n+n)")
                st.markdown("- ...")
            
            with col2:
                st.markdown("**Cadenas inválidas:**")
                st.markdown("- n++")
                st.markdown("- (n+n")
                st.markdown("- n+*n")
                st.markdown("- ...")
            
            st.markdown("**Derivación de 'n+n*n':**")
            st.code("""E → E + T → T + T → F + T → n + T → n + T * F 
    → n + F * F → n + n * n""", language="bnf")
        
        # Ejemplo 3: Paréntesis balanceados
        with st.expander("⚖️ Ejemplo 3: Gramática para Paréntesis Balanceados"):
            st.markdown("#### Objetivo: Generar secuencias de paréntesis correctamente balanceados")
            
            st.markdown("**Gramática:**")
            st.code("S → ( S ) | S S | ε", language="bnf")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cadenas válidas:**")
                st.markdown("- ()")
                st.markdown("- (())")
                st.markdown("- ()()")
                st.markdown("- (()())")
                st.markdown("- ((()))")
                st.markdown("- ...")
            
            with col2:
                st.markdown("**Cadenas inválidas:**")
                st.markdown("- ((")
                st.markdown("- )()")
                st.markdown("- (()))")
                st.markdown("- ...")
            
            st.markdown("**Derivación de '(())':**")
            st.code("S → ( S ) → ( ( S ) ) → ( ( ) )", language="bnf")
        
        # Ejemplo 4: Lenguaje aⁿbⁿ
        with st.expander("📈 Ejemplo 4: Gramática para el lenguaje aⁿbⁿ"):
            st.markdown("#### Objetivo: Generar cadenas con igual número de 'a' y 'b'")
            
            st.markdown("**Gramática:**")
            st.code("S → a S b | ε", language="bnf")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cadenas válidas:**")
                st.markdown("- ε (cadena vacía)")
                st.markdown("- ab")
                st.markdown("- aabb")
                st.markdown("- aaabbb")
                st.markdown("- ...")
            
            with col2:
                st.markdown("**Cadenas inválidas:**")
                st.markdown("- a")
                st.markdown("- b")
                st.markdown("- aab")
                st.markdown("- abb")
                st.markdown("- ...")
            
            st.markdown("**Derivación de 'aabb':**")
            st.code("S → a S b → a a S b b → a a b b", language="bnf")
            
            # Información adicional destacada
            st.info("""
            **💡 Este lenguaje NO puede ser generado por una gramática regular**, 
            demostrando que las GIC son más poderosas que las gramáticas regulares.
            """)
    
    @staticmethod
    def _render_step_by_step_analysis():
        """Renderiza análisis paso a paso de derivaciones usando componentes Streamlit"""
        
        st.subheader("🔍 Análisis Paso a Paso")
        
        st.markdown("#### 📝 Proceso de Derivación")
        st.markdown("Una derivación es la secuencia de pasos para generar una cadena:")
        
        # Lista ordenada usando st.markdown
        st.markdown("""
        1. **Comienza con el símbolo inicial**
        2. **Aplica producciones** reemplazando no terminales  
        3. **Continúa hasta** que solo queden terminales
        4. **La cadena resultante** pertenece al lenguaje
        """)
        
        # Ejemplo interactivo de derivación
        st.markdown("#### 🎮 Demo: Derivación de 'aabb' con la gramática aⁿbⁿ")
        
        # Simulación paso a paso usando st.expander
        steps = [
            {"step": 1, "string": "S", "production": "S → a S b"},
            {"step": 2, "string": "a S b", "production": "S → a S b"}, 
            {"step": 3, "string": "a a S b b", "production": "S → ε"},
            {"step": 4, "string": "a a b b", "production": "✓ Derivación completa"}
        ]
        
        for step in steps:
            with st.expander(f"Paso {step['step']}: {step['string']}", expanded=step['step'] <= 2):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Cadena actual:** `{step['string']}`")
                with col2:
                    st.info(f"**Producción:** {step['production']}")
        
        # Árbol de derivación explicado
        st.markdown("#### 🌳 Árbol de Derivación")
        st.markdown("El árbol de derivación muestra visualmente el proceso:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Componentes del árbol:**
            - **Raíz:** Símbolo inicial (S)
            - **Nodos internos:** No terminales expandidos  
            - **Hojas:** Símbolos terminales finales
            - **Secuencia de hojas:** Cadena generada
            """)
        
        with col2:
            st.markdown("""
            **Para 'aabb':**
            - **Árbol:** S → a S b → a a S b b → a a b b
            - **Hojas:** a, a, b, b
            - **Cadena:** aabb
            """)
        
        # Visualización del árbol ASCII
        st.markdown("**Representación del árbol para 'aabb':**")
        st.code("""
          S
        / | \\
       a  S  b
         /| \\
        a S  b
          |
          ε
        """, language="text")
        
        st.markdown("**Lectura de hojas (izquierda a derecha):** a a b b")

    @staticmethod
    def _render_interactive_demos():
        """Renderiza demostraciones interactivas usando componentes Streamlit"""
        
        st.subheader("🎮 Demostraciones Interactivas")
        
        # Quiz interactivo
        st.markdown("#### 🧩 Quiz: Identifica la Gramática Correcta")
        st.markdown("¿Cuál de estas gramáticas genera el lenguaje de palíndromos binarios?")
        
        quiz_option = st.radio(
            "Selecciona la opción correcta:",
            [
                "S → 0S | 1S | ε",
                "S → 0S0 | 1S1 | 0 | 1 | ε", 
                "S → SS | 0 | 1 | ε",
                "S → 0 | 1 | 0S1 | 1S0"
            ],
            index=1
        )
        
        if st.button("✅ Verificar respuesta", key="quiz_check"):
            if quiz_option == "S → 0S0 | 1S1 | 0 | 1 | ε":
                st.success("🎉 ¡Correcto! Esta gramática genera palíndromos binarios.")
                st.balloons()
            else:
                st.error("❌ Incorrecto. La gramática correcta es: S → 0S0 | 1S1 | 0 | 1 | ε")
        
        # Demo de validación
        st.markdown("#### 🔍 Demo: Validador de Cadenas")
        st.markdown("Prueba si una cadena pertenece al lenguaje de palíndromos binarios:")
        
        test_string = st.text_input("Ingresa una cadena para validar:", "101", key="validator_input")
        
        if test_string:
            # Simulación simple de validación
            is_palindrome = test_string == test_string[::-1] and all(c in '01' for c in test_string)
            
            if is_palindrome:
                st.success(f"✅ '{test_string}' es un palíndromo binario válido")
                
                # Análisis detallado
                with st.expander("📊 Ver análisis detallado"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Cadena", test_string)
                        st.metric("¿Es palíndromo?", "Sí ✓")
                    with col2:
                        st.metric("Reversa", test_string[::-1])
                        st.metric("¿Solo 0s y 1s?", "Sí ✓")
            else:
                st.error(f"❌ '{test_string}' NO es un palíndromo binario válido")
                
                # Análisis de por qué no es válido
                with st.expander("🔍 Ver por qué no es válido"):
                    issues = []
                    if test_string != test_string[::-1]:
                        issues.append("No es palíndromo (la reversa es diferente)")
                    if not all(c in '01' for c in test_string):
                        issues.append("Contiene caracteres diferentes a 0 y 1")
                    
                    for issue in issues:
                        st.markdown(f"- {issue}")
        
        # Generador automático
        st.markdown("#### 🎲 Generador de Ejemplos")
        st.markdown("Genera ejemplos aleatorios de diferentes gramáticas:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔁 Palíndromo", key="gen_pal"):
                examples = ["0", "1", "00", "11", "010", "101", "0110", "1001"]
                import random
                example = random.choice(examples)
                st.info(f"**Ejemplo generado:** {example}")
                st.markdown(f"*Gramática: S → 0S0 | 1S1 | 0 | 1 | ε*")
        
        with col2:
            if st.button("🧮 Expresión", key="gen_exp"):
                examples = ["n", "n+n", "n*n", "(n+n)", "n*(n+n)"]
                import random
                example = random.choice(examples)
                st.info(f"**Ejemplo generado:** {example}")
                st.markdown("*Gramática: E → E + T | T, T → T * F | F, F → (E) | n*")
        
        with col3:
            if st.button("⚖️ Paréntesis", key="gen_par"):
                examples = ["()", "(())", "()()", "(()())", "((()))"]
                import random
                example = random.choice(examples)
                st.info(f"**Ejemplo generado:** {example}")
                st.markdown("*Gramática: S → (S) | SS | ε*")

    @staticmethod
    def _render_additional_resources():
        """Renderiza recursos adicionales usando componentes Streamlit"""
        
        st.subheader("📖 Recursos Adicionales")
        
        st.markdown("#### 📚 Para Aprender Más")
        
        # Libros recomendados
        with st.expander("📖 Libros Recomendados", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **'Introduction to the Theory of Computation'**
                - *Autor:* Michael Sipser
                - *Temas:* GIC, autómatas, computabilidad
                - *Nivel:* Universitario
                """)
                
                st.markdown("""
                **'Automata and Computability'**  
                - *Autor:* Dexter C. Kozen
                - *Temas:* Teoría de autómatas
                - *Nivel:* Avanzado
                """)
            
            with col2:
                st.markdown("""
                **'Compilers: Principles, Techniques, and Tools'**
                - *Autor:* Aho, Sethi, Ullman (El Libro del Dragón)
                - *Temas:* Compiladores, parsing
                - *Nivel:* Práctico
                """)
        
        # Recursos online
        with st.expander("🌐 Recursos Online"):
            st.markdown("""
            - **Wikipedia** - Context-free grammar
            - **GeeksforGeeks** - Context Free Grammars  
            - **JFLAP** - Herramienta interactiva para autómatas y gramáticas
            - **Coursera/edX** - Cursos de teoría de la computación
            """)
        
        # Conceptos relacionados
        with st.expander("🎓 Conceptos Relacionados"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Autómatas de Pila**
                - Máquinas equivalentes a las GIC
                - Reconocen lenguajes libres de contexto
                - Base de los analizadores sintácticos
                """)
                
                st.markdown("""
                **Análisis Sintáctico**
                - Algoritmos para procesar GIC
                - Top-down vs Bottom-up
                - LR, LL parsers
                """)
            
            with col2:
                st.markdown("""
                **Forma Normal de Chomsky**
                - Forma estandarizada para GIC
                - Todas las producciones son de la forma A → BC o A → a
                - Útil para análisis algorítmico
                """)
                
                st.markdown("""
                **Lenguajes Libres de Contexto**
                - Lenguajes generados por GIC
                - Propiedades de clausura
                - Lema de bombeo para LLC
                """)
        
        # Tips y buenas prácticas
        st.markdown("#### 💡 Tips para Trabajar con GIC")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Diseñando Gramáticas:**")
            st.markdown("""
            - Comienza simple y ve agregando complejidad
            - Usa recursión para patrones repetitivos  
            - Prueba con ejemplos pequeños primero
            - Considera la ambigüedad y trata de evitarla
            """)
        
        with col2:
            st.markdown("**🔍 Depurando Gramáticas:**")
            st.markdown("""
            - Verifica símbolos terminales y no terminales
            - Prueba casos límite (cadena vacía, casos mínimos)
            - Usa herramientas de visualización como esta aplicación
            - Revisa ciclos infinitos en las producciones
            """)
        
        # Próximos pasos
        st.markdown("#### 🚀 Próximos Pasos en tu Aprendizaje")
        
        steps = [
            "**Domina los conceptos básicos** de GIC",
            "**Practica diseñando** tus propias gramáticas", 
            "**Explora autómatas de pila** (máquinas equivalentes)",
            "**Aprende sobre análisis sintáctico** (parsing)",
            "**Estudia aplicaciones reales** en compiladores"
        ]
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"{i}. {step}")
        
        st.markdown("---")
        st.success("**¡Sigue practicando con esta herramienta! 🎯**")
    
    
    
    @staticmethod
    def create_production_form():
        """Crea un formulario para agregar producciones personalizadas"""
        st.subheader("➕ Agregar Producción")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            left_side = st.text_input(
                "No Terminal (lado izquierdo)", 
                value="S", 
                max_chars=5,
                key="prod_left",
                help="Un símbolo no terminal (ej: S, A, E)"
            )
        
        with col2:
            right_side = st.text_input(
                "Producción (lado derecho)", 
                value="aSb",
                key="prod_right",
                help="Cadena de símbolos terminales y no terminales (ej: aSb, 0S1, ε)"
            )
        
        with col3:
            st.write("")  # Espaciado
            st.write("")  # Espaciado
            add_button = st.button("➕ Agregar", use_container_width=True)
        
        return {
            'left': left_side.strip(),
            'right': right_side.strip(),
            'add_clicked': add_button
        }