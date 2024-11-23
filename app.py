import streamlit as st
from docling.document_converter import DocumentConverter
import tempfile
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Agregar mensaje de depuración
st.write("Iniciando aplicación...")

try:
    st.title("Convertidor de PDF a Markdown")
    
    # Agregar mensaje de depuración
    logger.debug("Inicializando convertidor...")
    
    # Crear el convertidor usando la importación correcta
    try:
        converter = DocumentConverter()
        logger.debug("Convertidor creado exitosamente")
    except Exception as e:
        logger.error(f"Error al crear el convertidor: {str(e)}")
        st.error(f"Error al crear el convertidor: {str(e)}")
        raise
    
    st.write("Convertidor inicializado correctamente")
    
    # Widget para subir archivo
    uploaded_file = st.file_uploader("Sube tu archivo PDF", type=['pdf'])
    
    # Campo para URL
    url = st.text_input("O ingresa una URL de PDF")
    
    if uploaded_file is not None:
        logger.debug(f"Archivo subido: {uploaded_file.name}")
        st.write(f"Archivo subido: {uploaded_file.name}")
        
        # Crear un archivo temporal para guardar el PDF subido
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
            logger.debug(f"Archivo temporal creado en: {tmp_path}")
        
        try:
            # Convertir el PDF usando el archivo temporal
            logger.debug("Iniciando conversión...")
            st.write("Iniciando conversión...")
            result = converter.convert(tmp_path)
            markdown_text = result.document.export_to_markdown()
            logger.debug("Conversión completada exitosamente")
            
            # Usar el nombre del archivo original pero con extensión .md
            output_filename = os.path.splitext(uploaded_file.name)[0] + '.md'
            
            # Botón de descarga
            st.download_button(
                label="Descargar archivo Markdown",
                data=markdown_text,
                file_name=output_filename,
                mime="text/markdown"
            )
            
        except Exception as e:
            logger.error(f"Error al convertir el archivo: {str(e)}")
            st.error(f"Error al convertir el archivo: {str(e)}")
            
        finally:
            # Limpiar el archivo temporal
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                logger.debug("Archivo temporal eliminado")
                
    elif url:
        try:
            # Convertir directamente desde URL
            logger.debug(f"Convirtiendo desde URL: {url}")
            st.write("Iniciando conversión desde URL...")
            result = converter.convert(url)
            markdown_text = result.document.export_to_markdown()
            logger.debug("Conversión completada exitosamente")
            
            # Para URLs, extraer el último segmento como nombre de archivo
            output_filename = url.split('/')[-1].split('.')[0] + '.md'
            
            # Botón de descarga
            st.download_button(
                label="Descargar archivo Markdown",
                data=markdown_text,
                file_name=output_filename,
                mime="text/markdown"
            )
            
        except Exception as e:
            logger.error(f"Error al convertir desde URL: {str(e)}")
            st.error(f"Error al convertir desde URL: {str(e)}")
                
except Exception as e:
    logger.error(f"Error en la inicialización: {str(e)}")
    st.error(f"Error en la inicialización: {str(e)}")