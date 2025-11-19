"""
app_cfg.py
Aplicación principal del Simulador de Gramáticas Independientes del Contexto con Streamlit
"""
import streamlit as st
import json
from ContextFreeGrammar import ContextFreeGrammar, DerivationStep
from PredefinedGrammars import PredefinedGrammars
from UIComponentsCFG import UIComponentsCFG

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(
    page_title="Simulador de GIC",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== INICIALIZACIÓN DE ESTADO ====================
if 'cfg' not in st.session_state:
    st.session_state.cfg = None
if 'current_derivation' not in st.session_state:
    st.session_state.current_derivation = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'custom_productions' not in st.session_state:
    st.session_state.custom_productions = []
if 'generated_string' not in st.session_state:
    st.session_state.generated_string = ""

# ==================== APLICAR ESTILOS ====================
UIComponentsCFG.apply_custom_css()

# ==================== HEADER ====================
UIComponentsCFG.render_header()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selector de modo
    mode = st.radio(
        "Modo de operación",
        ["🎯 Gramáticas Predefinidas", "🛠️ Crear Gramática Personalizada", "📚 Tutorial"],
        index=0
    )
    
    st.divider()
    
    if mode == "🎯 Gramáticas Predefinidas":
        st.subheader("Seleccione una gramática")
        grammar_type = st.selectbox(
            "Tipo de gramática",
            [
                "Expresiones Aritméticas",
                "Palíndromos Binarios",
                "Paréntesis Balanceados",
                "Lenguaje a^n b^n",
                "Etiquetas HTML Simples"
            ]
        )
        
        # Mapeo de nombres
        grammar_map = {
            "Expresiones Aritméticas": ("arithmetic", PredefinedGrammars.create_arithmetic_expressions),
            "Palíndromos Binarios": ("palindrome", PredefinedGrammars.create_palindrome),
            "Paréntesis Balanceados": ("parentheses", PredefinedGrammars.create_balanced_parentheses),
            "Lenguaje a^n b^n": ("anbn", PredefinedGrammars.create_anbn),
            "Etiquetas HTML Simples": ("html", PredefinedGrammars.create_simple_html)
        }
        
        grammar_key, grammar_creator = grammar_map[grammar_type]
        
        if st.button("🚀 Cargar Gramática", use_container_width=True):
            st.session_state.cfg = grammar_creator()
            st.session_state.current_derivation = []
            st.session_state.current_step = 0
            st.session_state.generated_string = ""
            st.success("✅ Gramática cargada correctamente")
            st.rerun()
    
    elif mode == "🛠️ Crear Gramática Personalizada":
        st.subheader("Configuración básica")
        
        start_symbol = st.text_input("Símbolo inicial", value="S", max_chars=5)
        
        terminals_input = st.text_input(
            "Símbolos terminales (separados por coma)",
            value="a, b",
            help="Ejemplo: a, b, 0, 1, +, *"
        )
        
        non_terminals_input = st.text_input(
            "Símbolos no terminales (separados por coma)",
            value="S",
            help="Ejemplo: S, A, B, E, T"
        )
        
        if st.button("🆕 Crear Gramática Vacía", use_container_width=True):
            st.session_state.cfg = ContextFreeGrammar()
            st.session_state.cfg.set_start_symbol(start_symbol.strip())
            
            if terminals_input.strip():
                terminals = {s.strip() for s in terminals_input.split(',')}
                st.session_state.cfg.set_terminals(terminals)
            
            if non_terminals_input.strip():
                non_terminals = {s.strip() for s in non_terminals_input.split(',')}
                st.session_state.cfg.set_non_terminals(non_terminals)
            
            st.session_state.custom_productions = []
            st.session_state.current_derivation = []
            st.session_state.current_step = 0
            st.success("✅ Gramática creada")
            st.rerun()
    
    st.divider()
    
    # Información de la gramática actual
    if st.session_state.cfg is not None and mode != "📚 Tutorial":
        st.subheader("📊 Info de la Gramática")
        info = st.session_state.cfg.get_grammar_info()
        st.write(f"**Símbolo inicial:** {info['start_symbol']}")
        st.write(f"**No terminales:** {', '.join(info['non_terminals'])}")
        st.write(f"**Terminales:** {', '.join(info['terminals'])}")
        st.write(f"**Producciones:** {info['num_productions']}")
        
        st.divider()
        
        # Validar gramática
        if st.button("🔍 Validar Gramática", use_container_width=True):
            is_valid, errors = st.session_state.cfg.validate_grammar()
            if is_valid:
                st.success("✅ Gramática válida")
            else:
                st.error("❌ Errores encontrados:")
                for error in errors:
                    st.write(f"- {error}")
        
        st.divider()
        
        # Exportar/Importar
        st.subheader("💾 Exportar/Importar")
        
        # EXPORTAR
        if st.button("📤 Exportar Gramática", use_container_width=True):
            config = st.session_state.cfg.export_grammar()
            config_json = json.dumps(config, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="⬇️ Descargar JSON",
                data=config_json,
                file_name="gramatica.json",
                mime="application/json",
                use_container_width=True
            )
            
            # Mostrar preview del JSON
            with st.expander("👁️ Ver JSON"):
                st.code(config_json, language='json')
        
        st.divider()
        
        # IMPORTAR
        st.write("**📥 Importar Gramática**")
        uploaded_file = st.file_uploader(
            "Selecciona archivo JSON", 
            type=['json'],
            key="grammar_uploader",
            help="Sube un archivo JSON con la estructura de gramática"
        )
        
        if uploaded_file is not None:
            try:
                # Leer el archivo
                config_str = uploaded_file.read().decode('utf-8')
                config_dict = json.loads(config_str)
                
                # Validar que tenga los campos necesarios
                required_fields = ['terminals', 'non_terminals', 'start_symbol', 'productions']
                missing_fields = [field for field in required_fields if field not in config_dict]
                
                if missing_fields:
                    st.error(f"❌ El archivo JSON no tiene los campos requeridos: {', '.join(missing_fields)}")
                else:
                    # Mostrar vista previa
                    st.success("✅ Archivo JSON válido")
                    
                    with st.expander("👁️ Vista previa de la gramática"):
                        st.write(f"**Símbolo inicial:** {config_dict['start_symbol']}")
                        st.write(f"**No terminales:** {', '.join(config_dict['non_terminals'])}")
                        st.write(f"**Terminales:** {', '.join(config_dict['terminals'])}")
                        st.write(f"**Producciones:**")
                        for left, rights in config_dict['productions'].items():
                            for right in rights:
                                st.write(f"  • {left} → {right}")
                    
                    # Botón para confirmar importación
                    if st.button("✅ Confirmar Importación", use_container_width=True, type="primary"):
                        # Crear nueva gramática e importar
                        new_cfg = ContextFreeGrammar()
                        new_cfg.import_grammar(config_dict)
                        
                        # Actualizar session state
                        st.session_state.cfg = new_cfg
                        st.session_state.current_derivation = []
                        st.session_state.current_step = 0
                        st.session_state.generated_string = ""
                        
                        st.success("🎉 Gramática importada exitosamente!")
                        st.info("👈 Recarga la página para ver los cambios reflejados en la interfaz")
                        
                        # NO usar st.rerun() aquí - causa el loop infinito
                        # En su lugar, el usuario recargará manualmente
                        
            except json.JSONDecodeError as e:
                st.error(f"❌ Error al leer JSON: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al importar gramática: {str(e)}")

# ==================== CONTENIDO PRINCIPAL ====================
if mode == "📚 Tutorial":
    UIComponentsCFG.render_tutorial()
    
    st.divider()
    
    # Ejemplo interactivo
    st.subheader("🎮 Ejemplo Interactivo: Palíndromos")
    st.write("Carga esta gramática que genera palíndromos binarios:")
    
    if st.button("Cargar Ejemplo de Palíndromo"):
        st.session_state.cfg = PredefinedGrammars.create_palindrome()
        st.session_state.current_derivation = []
        st.session_state.current_step = 0
        st.success("✅ Ejemplo cargado. Ve a 'Gramáticas Predefinidas' para probarlo.")
        st.rerun()

elif mode == "🎯 Gramáticas Predefinidas":
    if st.session_state.cfg is None:
        st.info("👈 Seleccione una gramática predefinida en el panel lateral")
        
        # Mostrar información de las gramáticas disponibles
        st.subheader("🎯 Gramáticas Disponibles")
        
        grammars_info = [
            ("arithmetic", "Expresiones Aritméticas"),
            ("palindrome", "Palíndromos Binarios"),
            ("parentheses", "Paréntesis Balanceados"),
            ("anbn", "Lenguaje a^n b^n"),
            ("html", "Etiquetas HTML Simples")
        ]
        
        cols = st.columns(2)
        for idx, (grammar_key, grammar_name) in enumerate(grammars_info):
            with cols[idx % 2]:
                info = PredefinedGrammars.get_grammar_info(grammar_key)
                UIComponentsCFG.render_grammar_info(info)
    
    else:
        # Mostrar información de la gramática actual
        grammar_key, _ = grammar_map[grammar_type]
        info = PredefinedGrammars.get_grammar_info(grammar_key)
        UIComponentsCFG.render_grammar_info(info)
        
        st.divider()
        
        # Tabs para organizar funcionalidades
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎲 Generador de Cadenas", 
            "✅ Validador de Cadenas", 
            "📋 Producciones",
            "🌳 Árbol de Derivación"
        ])
        
        # TODO EL CONTENIDO DE LAS PESTAÑAS DEBE ESTAR DENTRO DE ESTE BLOQUE ELSE
        with tab1:
            st.subheader("🎲 Generador de Cadenas")
            st.write("Genera cadenas válidas automáticamente usando las producciones de la gramática.")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # AUMENTAR el máximo de pasos para gramáticas complejas
                max_steps = st.slider("Pasos máximos de derivación", 5, 50, 20)
                derivation_mode = st.selectbox(
                    "Modo de derivación",
                    ["random", "leftmost", "rightmost"],
                    format_func=lambda x: {
                        "random": "Aleatorio",
                        "leftmost": "Por la izquierda",
                        "rightmost": "Por la derecha"
                    }[x]
                )
            
            with col2:
                st.write("")
                st.write("")
                if st.button("🎲 Generar Cadena", use_container_width=True):
                    with st.spinner("Generando..."):
                        derivation = st.session_state.cfg.generate_string(max_steps, derivation_mode)
                        st.session_state.current_derivation = derivation
                        
                        if derivation:
                            final_string = derivation[-1].string
                            st.session_state.generated_string = final_string
                        
                        st.rerun()
            
            # Mostrar derivación actual
            if st.session_state.current_derivation:
                st.divider()
                
                final_step = st.session_state.current_derivation[-1]
                
                # Verificar si la derivación está completa
                has_non_terminals = any(c in st.session_state.cfg.non_terminals 
                                    for c in final_step.string)
                
                if final_step.is_final or not has_non_terminals:
                    result_string = final_step.string.replace('ε', '(cadena vacía)')
                    if result_string == '':
                        result_string = '(cadena vacía)'
                    
                    st.success(f"✅ Cadena generada: **{result_string}**")
                    
                    # 🆕 EVALUAR EXPRESIONES ARITMÉTICAS
                    # Detectar si estamos en la gramática de expresiones aritméticas
                    # Verificando si tiene los no terminales característicos E, T, F, P, Q
                    is_arithmetic = all(nt in st.session_state.cfg.non_terminals 
                                    for nt in ['E', 'T', 'F'])
                    
                    if is_arithmetic and result_string != '(cadena vacía)':
                        # Mostrar resultado matemático
                        UIComponentsCFG.render_arithmetic_result(result_string)
                else:
                    st.warning(f"⚠️ Derivación incompleta: {final_step.string}")
                    st.info("💡 Intenta aumentar el número de pasos máximos o generar otra vez.")
                
                st.write(f"**Número de pasos:** {len(st.session_state.current_derivation)}")
                
                # Botón para generar otra
                if st.button("🔄 Generar otra cadena", key="regen"):
                    derivation = st.session_state.cfg.generate_string(max_steps, derivation_mode)
                    st.session_state.current_derivation = derivation
                    if derivation:
                        final_string = derivation[-1].string
                        st.session_state.generated_string = final_string
                    st.rerun()
                
                # Mostrar historial
                with st.expander("📜 Ver historial de derivación", expanded=False):
                    UIComponentsCFG.render_derivation_history(st.session_state.current_derivation)
        
        with tab2:
            st.subheader("✅ Validador de Cadenas")
            st.write("Verifica si una cadena pertenece al lenguaje generado por la gramática.")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                input_string = st.text_input(
                    "Cadena a validar",
                    value="",
                    help="Ingresa una cadena para verificar si pertenece al lenguaje. Deja vacío para validar la cadena vacía (ε)"
                )
                
                # Mostrar ayuda contextual
                if input_string == "":
                    st.info("💡 Campo vacío = validar cadena vacía (ε)")
            
            with col2:
                st.write("")
                st.write("")
                validate_button = st.button("🔍 Validar", use_container_width=True)
            
            if validate_button:
                with st.spinner("Validando cadena..."):
                    # Preparar la cadena objetivo
                    if input_string == "":
                        target = 'ε'
                        display_target = '(cadena vacía: ε)'
                    else:
                        target = input_string
                        display_target = f'"{target}"'
                    
                    st.info(f"Validando cadena: {display_target}")
                    
                    # DETECTAR SI ES GRAMÁTICA ARITMÉTICA
                    is_arithmetic = all(nt in st.session_state.cfg.non_terminals 
                                    for nt in ['E', 'T', 'F'])
                    
                    # USAR DFS PARA GRAMÁTICAS ARITMÉTICAS, BFS PARA LAS DEMÁS
                    if is_arithmetic:
                        st.info("🔍 Usando algoritmo DFS optimizado para expresiones aritméticas...")
                        is_valid, derivation = st.session_state.cfg.validate_string_dfs(
                            target, 
                            max_depth=35,
                            timeout=15.0
                        )
                    else:
                        st.info("🔍 Usando algoritmo BFS estándar...")
                        is_valid, derivation = st.session_state.cfg.validate_string(
                            target, 
                            max_depth=25,
                            timeout=10.0
                        )
                    
                    if is_valid:
                        UIComponentsCFG.render_validation_result(
                            True, 
                            f"¡Cadena válida! ✓",
                            derivation
                        )
                        
                        if derivation:
                            st.success(f"✅ Se encontró una derivación en {len(derivation)} pasos")
                            
                            # Mostrar la cadena final derivada
                            final_string = derivation[-1].string
                            if final_string == 'ε' or final_string == '':
                                final_display = '(cadena vacía: ε)'
                            else:
                                final_display = final_string
                            
                            st.write(f"**Resultado de la derivación:** {final_display}")
                            
                            # 🆕 EVALUAR SI ES EXPRESIÓN ARITMÉTICA
                            is_arithmetic = all(nt in st.session_state.cfg.non_terminals 
                                            for nt in ['E', 'T', 'F'])
                            
                            if is_arithmetic and final_string not in ['ε', '']:
                                UIComponentsCFG.render_arithmetic_result(input_string)
                            
                            # Mostrar historial
                            with st.expander("📜 Ver derivación completa", expanded=True):
                                UIComponentsCFG.render_derivation_history(derivation)
                    else:
                        UIComponentsCFG.render_validation_result(
                            False,
                            "Cadena inválida ✗"
                        )
                        st.info("💡 Esta cadena no puede ser generada por la gramática actual.")
                        st.write("**Posibles razones:**")
                        st.write("- La cadena no pertenece al lenguaje definido")
                        st.write("- Se necesita mayor profundidad de búsqueda")
                        st.write("- La gramática no puede generar esta cadena")
        
        with tab3:
            st.subheader("📋 Producciones de la Gramática")
            rules = st.session_state.cfg.get_production_rules()
            UIComponentsCFG.render_grammar_rules(rules)
            
            # Mostrar tabla detallada
            if rules:
                st.divider()
                st.write("**Tabla detallada:**")
                import pandas as pd
                df = pd.DataFrame(rules)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab4:
            st.subheader("🌳 Árbol de Derivación")
            if st.session_state.current_derivation:
                UIComponentsCFG.render_parse_tree_simple(st.session_state.current_derivation)
            else:
                st.info("Genera o valida una cadena primero para ver el árbol de derivación.")

elif mode == "🛠️ Crear Gramática Personalizada":
    if st.session_state.cfg is None:
        st.info("👈 Cree una gramática nueva en el panel lateral")
    else:
        st.subheader("🔧 Definir Producciones")
        
        # Formulario para agregar producciones
        form_data = UIComponentsCFG.create_production_form()
        
        if form_data['add_clicked']:
            if form_data['left'] and form_data['right']:
                # Validar que el lado izquierdo sea un no terminal
                if form_data['left'] not in st.session_state.cfg.non_terminals:
                    st.error(f"⚠️ '{form_data['left']}' no está en los no terminales declarados")
                else:
                    st.session_state.cfg.add_production(
                        form_data['left'],
                        form_data['right']
                    )
                    st.session_state.custom_productions.append(form_data)
                    st.success(f"✅ Producción agregada: {form_data['left']} → {form_data['right']}")
                    st.rerun()
            else:
                st.error("⚠️ Complete ambos campos")
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3 = st.tabs([
            "📋 Producciones", 
            "🎬 Probar Gramática",
            "🔍 Validar"
        ])
        
        with tab1:
            rules = st.session_state.cfg.get_production_rules()
            if rules:
                UIComponentsCFG.render_grammar_rules(rules)
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Limpiar Producciones", use_container_width=True):
                        st.session_state.cfg.productions = {}
                        st.session_state.custom_productions = []
                        st.success("Producciones eliminadas")
                        st.rerun()
                
                with col2:
                    # Mostrar tabla
                    import pandas as pd
                    df = pd.DataFrame(rules)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ No hay producciones definidas. Agregue al menos una producción.")
        
        with tab2:
            st.subheader("🎲 Generador")
            
            if st.session_state.cfg.productions:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    gen_max_steps = st.slider("Pasos máximos", 1, 25, 10, key="gen_custom")
                    gen_mode = st.selectbox(
                        "Modo",
                        ["random", "leftmost", "rightmost"],
                        format_func=lambda x: {"random": "Aleatorio", "leftmost": "Izquierda", "rightmost": "Derecha"}[x],
                        key="mode_custom"
                    )
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🎲 Generar", use_container_width=True, key="gen_btn_custom"):
                        derivation = st.session_state.cfg.generate_string(gen_max_steps, gen_mode)
                        st.session_state.current_derivation = derivation
                        st.rerun()
                
                if st.session_state.current_derivation:
                    st.divider()
                    final = st.session_state.current_derivation[-1]
                    st.success(f"✅ Resultado: **{final.string}**")
                    UIComponentsCFG.render_derivation_history(st.session_state.current_derivation)
            else:
                st.error("❌ Defina producciones primero")
        
        with tab3:
            st.subheader("✅ Validador")
            
            if st.session_state.cfg.productions:
                val_input = st.text_input("Cadena a validar", key="val_custom")
                
                if st.button("🔍 Validar Cadena", use_container_width=True, key="val_btn_custom"):
                    if val_input or val_input == "":
                        target = val_input if val_input else 'ε'
                        is_valid, derivation = st.session_state.cfg.validate_string(target)
                        
                        UIComponentsCFG.render_validation_result(is_valid, 
                            "Válida" if is_valid else "Inválida")
                        
                        if derivation:
                            UIComponentsCFG.render_derivation_history(derivation)
            else:
                st.error("❌ Defina producciones primero")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p> 🤖 <strong>Simulador de Gramáticas Independientes del Contexto</strong> - Herramienta educativa interactiva</p>
    <p>Desarrollado por S.Ardila -R , K.Esteban -S, K.Alejandro -L, Y.Orozco -V</p>
</div>
""", unsafe_allow_html=True)