import streamlit as st

# ==========================================
# 1. BASE DE DATOS DE CASOS CLÍNICOS
# ==========================================
BASE_DE_DATOS_CASOS = {
    "SCA_001": {
        "titulo": "Caso: Dolor Torácico en Urgencias",
        "historia": {
            "ficha": "Masculino de 58 años, fumador, hipertenso.",
            "antecedentes": "Padre fallecido por infarto a los 50 años. Sedentarismo.",
            "padecimiento": "Dolor retroesternal opresivo de 30 min, irradiado a cuello, intensidad 8/10."
        },
        "exploracion": {
            "signos": {"TA": "150/95", "FC": "102", "FR": "22", "SatO2": "94%"},
            "hallazgos": "Paciente diaforético, ruidos cardiacos rítmicos, campos pulmonares limpios."
        },
        "estudios": {
            "Electrocardiograma (EKG)": {
                "resultado": "Elevación del segmento ST en V1, V2, V3 y V4.",
                "necesario": True,
                "feedback": "Correcto. Según la GPC, ante sospecha de SCA, el EKG debe realizarse en < 10 min."
            },
            "Troponinas I": {
                "resultado": "0.5 ng/mL (Elevadas).",
                "necesario": True,
                "feedback": "Correcto. Marcador de elección para confirmar daño miocárdico."
            },
            "Radiografía de Tórax": {
                "resultado": "Silueta cardiaca normal.",
                "necesario": False,
                "feedback": "Innecesario en fase aguda: No debe retrasar la terapia de reperfusión según la GPC."
            },
            "Dímero D": {
                "resultado": "Negativo.",
                "necesario": False,
                "feedback": "Incorrecto: La clínica no sugiere TEP y el retraso en tratamiento de SCA es crítico."
            }
        },
        "diagnosticos": {
            "opciones": ["Angina Inestable", "IAMCEST Anterior", "Pericarditis", "Disección Aórtica"],
            "correcta": "IAMCEST Anterior"
        },
        "tratamiento": {
            "opciones": ["Aspirina + Clopidogrel + Reperfusión", "Antibioticoterapia", "Observación", "AINEs"],
            "correcta": "Aspirina + Clopidogrel + Reperfusión",
            "feedback": "Basado en la GPC: La terapia de reperfusión es la prioridad absoluta en IAMCEST."
        },
    }, # <-- Esta coma es vital para separar los casos

    "ASMA_002": {
        "titulo": "Caso: Dificultad Respiratoria en Pediatría",
        "historia": {
            "ficha": "Femenina de 8 años. Estudiante.",
            "antecedentes": "Rinitis alérgica. Madre asmática. Cuadros previos de broncoespasmo leve.",
            "padecimiento": "Inicia hace 24 hrs con tos seca, rinorrea y fiebre de bajo grado. Hoy presenta dificultad respiratoria progresiva y sibilancias audibles."
        },
        "exploracion": {
            "signos": {"TA": "110/70", "FC": "130", "FR": "32", "SatO2": "88%"},
            "hallazgos": "Paciente ansiosa, uso de músculos accesorios (tiraje intercostal). A la auscultación: sibilancias inspiratorias y espiratorias generalizadas."
        },
        "estudios": {
            "Radiografía de Tórax": {
                "resultado": "Hiperinsuflación, aplanamiento diafragmático, sin consolidaciones.",
                "necesario": False,
                "feedback": "No es de rutina en crisis leve/moderada, solo si hay sospecha de neumonía, neumotórax u otra complicación (GPC)."
            },
            "Gasometría Arterial": {
                "resultado": "pH 7.48, pCO2 30 mmHg, pO2 55 mmHg, HCO3 22 mEq/L.",
                "necesario": False,
                "feedback": "Innecesaria inicialmente en esta paciente. La pulsioximetría es suficiente en la mayoría de los casos no graves."
            },
            "Biometría Hemática": {
                "resultado": "Leucocitos 12,000, Neutrófilos 60%, Linfocitos 30%, Eosinófilos 8%.",
                "necesario": False,
                "feedback": "No aporta información para el manejo agudo de la crisis asmática."
            },
            "Flujometría (PEF)": {
                "resultado": "PEF del 55% del predicho.",
                "necesario": True,
                "feedback": "Correcto. Útil para clasificar la severidad (Crisis moderada)."
            }
        },
        "diagnosticos": {
            "opciones": ["Neumonía Adquirida en la Comunidad", "Crisis Asmática Moderada", "Crup (Laringotraqueítis)", "Bronquiolitis"],
            "correcta": "Crisis Asmática Moderada"
        },
        "tratamiento": {
            "opciones": ["Salbutamol inhalado + Esteroide Sistémico + Oxígeno", "Amoxicilina con Clavulanato + Paracetamol", "Epinefrina IM", "Observación en casa"],
            "correcta": "Salbutamol inhalado + Esteroide Sistémico + Oxígeno",
            "feedback": "GPC: El pilar en crisis moderada es el SABA, esteroide sistémico temprano y oxígeno para mantener SatO2 > 94%."
        }
    }
} # <-- Aquí termina la lista de todos los casos

# ==========================================
# 2. LÓGICA DE LA APLICACIÓN (STREAMLIT)
# ==========================================

def main():
    st.set_page_config(page_title="Simulador Clínico GPC", layout="wide")
    st.title("🏥 Simulador de Educación Médica Continua")

    # Inicialización de estados
    if 'paso' not in st.session_state:
        st.session_state.paso = 0
    if 'id_caso' not in st.session_state:
        st.session_state.id_caso = None
    if 'diag_correcto' not in st.session_state:
        st.session_state.diag_correcto = False

    # --- PASO 0: MENÚ DE SELECCIÓN DE CASOS ---
    if st.session_state.paso == 0:
        st.subheader("Selecciona un Caso Clínico")
        opciones_casos = [info["titulo"] for info in BASE_DE_DATOS_CASOS.values()]
        caso_elegido_titulo = st.selectbox("Casos Disponibles:", opciones_casos)
        
        if st.button("Iniciar Caso"):
            for id_caso, info in BASE_DE_DATOS_CASOS.items():
                if info["titulo"] == caso_elegido_titulo:
                    st.session_state.id_caso = id_caso
                    break
            st.session_state.paso = 1
            st.rerun()
        return

    caso = BASE_DE_DATOS_CASOS[st.session_state.id_caso]

    # --- BARRA LATERAL ---
    st.sidebar.header("Progreso")
    pasos_nombres = ["Historia", "Exploración", "Auxiliares", "Diagnóstico", "Tratamiento"]
    for i, nombre in enumerate(pasos_nombres, 1):
        st.sidebar.write(f"{'✅' if st.session_state.paso >= i else '⚪'} {nombre}")

    # --- FLUJO ---
    if st.session_state.paso == 1:
        st.header("1. Historia Clínica")
        st.write(f"**Ficha:** {caso['historia']['ficha']}")
        st.write(f"**Antecedentes:** {caso['historia']['antecedentes']}")
        st.info(caso['historia']['padecimiento'])
        if st.button("Siguiente"): st.session_state.paso = 2; st.rerun()

    elif st.session_state.paso == 2:
        st.header("2. Signos y Exploración")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("TA", caso["exploracion"]["signos"]["TA"])
        col2.metric("FC", caso["exploracion"]["signos"]["FC"])
        col3.metric("FR", caso["exploracion"]["signos"]["FR"])
        col4.metric("SatO2", caso["exploracion"]["signos"]["SatO2"])
        st.write(caso["exploracion"]["hallazgos"])
        if st.button("Siguiente"): st.session_state.paso = 3; st.rerun()

    elif st.session_state.paso == 3:
        st.header("3. Auxiliares")
        lista_estudios = list(caso["estudios"].keys())
        seleccionados = st.multiselect("Solicitar:", lista_estudios)
        if st.button("Ver Resultados"):
            for s in seleccionados:
                detalle = caso["estudios"][s]
                if not detalle["necesario"]: st.error(f"⚠️ {s}: {detalle['feedback']}")
                else: st.success(f"✅ {s}: {detalle['feedback']}")
                st.write(f"**Resultado:** {detalle['resultado']}")
            st.session_state.permiso_diag = True
        if st.session_state.get('permiso_diag'):
            if st.button("Siguiente"): st.session_state.paso = 4; st.rerun()

    elif st.session_state.paso == 4:
        st.header("4. Diagnóstico")
        eleccion = st.radio("Diagnóstico GPC:", caso["diagnosticos"]["opciones"])
        if st.button("Validar"):
            if eleccion == caso["diagnosticos"]["correcta"]:
                st.success("¡Correcto!")
                st.session_state.diag_correcto = True
            else: st.error("Incorrecto.")
        if st.session_state.diag_correcto:
            if st.button("Siguiente"): st.session_state.paso = 5; st.rerun()

    elif st.session_state.paso == 5:
        st.header("5. Tratamiento")
        manejo = st.selectbox("Manejo:", caso["tratamiento"]["opciones"])
        if st.button("Finalizar"):
            if manejo == caso["tratamiento"]["correcta"]:
                st.balloons(); st.success("Correcto: " + caso["tratamiento"]["feedback"])
            else: st.error("Manejo inadecuado.")
        if st.button("Reiniciar"): st.session_state.clear(); st.rerun()

if __name__ == "__main__":
    main()