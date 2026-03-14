Carpeta /tex de la memoria del TFG

Esta carpeta contiene todos los capítulos y anexos del proyecto en archivos .tex independientes.
Cada archivo representa un capítulo o anexo:

1_Introduccion.tex                - Introducción al proyecto
2_Objetivos_del_proyecto.tex      - Objetivos generales y específicos
3_Conceptos_teoricos.tex          - Conceptos teóricos de cloud y Azure
4_Tecnicas_y_herramientas.tex     - Herramientas y técnicas utilizadas
5_Aspectos_relevantes_del_desarrollo_del_proyecto.tex - Desarrollo del sistema
6_Trabajos_relacionados.tex       - Estado del arte y trabajos similares
7_Conclusiones_Lineas_de_trabajo_futuras.tex -> Conclusiones y líneas futuras
A_Plan_proyecto.tex               - Planificación del proyecto
B_Requisitos.tex                  - Especificación de requisitos
C_Diseno.tex                      - Diseño del sistema
D_Manual_programador.tex          - Documentación técnica de programación
E_Manual_usuario.tex              - Manual del usuario
F_ODS.tex                         - Reflexión de sostenibilidad curricular

Para compilar la memoria completa, usaremos desde la raíz del proyecto:
cd /c/Users/kdraf/OneDrive/Escritorio/TFG/tfg-azure-servicio-empresarial-seguro

# Paso 1: primera compilación
pdflatex memoria/memoria.tex

# Paso 2: procesar bibliografía
bibtex memoria/memoria

# Paso 3: segunda compilación
pdflatex memoria/memoria.tex

# Paso 4: tercera compilación
pdflatex memoria/memoria.tex
