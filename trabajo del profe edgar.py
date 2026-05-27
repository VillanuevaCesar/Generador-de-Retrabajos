import pandas as pd
import os


def generar_flujos_maquila():
    print("=== Iniciando Generador de Flujos de Retrabajo (Modo: Maquiladora SMT) ===")

    # Definimos las rutas exactas en tu computadora para evitar errores
    archivo_entrada = r"C:\Users\pc\Desktop\PruebaNAS\Rework Generator.xlsx"
    archivo_salida = r"C:\Users\pc\Desktop\PruebaNAS\Resultado_Maquila_Retrabajo.xlsx"

    # 1. Validar si el archivo existe
    if not os.path.exists(archivo_entrada):
        print(f"❌ ERROR: No encontré el archivo en: {archivo_entrada}")
        print(
            "Por favor, asegúrate de que el archivo 'Rework Generator.xlsx' esté dentro de la carpeta PruebaNAS en tu Escritorio.")
        return

    # 2. Leer los datos del Excel
    print("📋 Cargando datos de la maquila...")
    df_main = pd.read_excel(archivo_entrada, sheet_name='trabajito1')
    df_rules = pd.read_excel(archivo_entrada, sheet_name='trabajito2')

    # Limpiar espacios en blanco por si acaso
    for col in df_main.columns:
        if df_main[col].dtype == 'object': df_main[col] = df_main[col].str.strip()
    for col in df_rules.columns:
        if df_rules[col].dtype == 'object': df_rules[col] = df_rules[col].str.strip()

    # 3. Construir la sintaxis que pidió el profesor
    print("⚙️ Generando códigos de retrabajo (GoToFlowPath...)...")
    df_rules['Sintaxis_Retrabajo'] = df_rules.apply(
        lambda row: f"GoToFlowPath[{row['REWORK_PATH']}] ReturnStep[{row['RETURN_STEP']}] Reason[{row['REASON']}];",
        axis=1
    )

    # 4. Agrupar por paso (por si un paso tiene varios defectos, como la Inspección AOI)
    print("🧩 Agrupando múltiples defectos por estación...")
    df_grouped = df_rules.groupby(['FLOW', 'STEP'])['Sintaxis_Retrabajo'].apply(lambda x: ' '.join(x)).reset_index()
    df_grouped.rename(columns={'Sintaxis_Retrabajo': 'REWORKS'}, inplace=True)

    # 5. Juntar todo con el flujo principal de la maquila
    df_final = pd.merge(df_main, df_grouped, on=['FLOW', 'STEP'], how='left')
    df_final['REWORKS'] = df_final['REWORKS'].fillna('')  # Espacio vacío si no ocupa retrabajo

    # 6. Guardar el resultado
    df_final.to_excel(archivo_salida, index=False)
    print("==========================================================")
    print("✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print(f"📁 Tu archivo final listo se guardó en: {archivo_salida}")
    print("==========================================================")


if __name__ == "__main__":
    generar_flujos_maquila()