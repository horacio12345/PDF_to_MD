import streamlit as st
from docling.document_converter import DocumentConverter
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Custom CSS for better layout
st.markdown("""
    <style>    
        .stFileUploader {
            padding: 1rem;
        }
        
        button[data-testid="stFileUploaderButtonPrimary"] {
            background-color: #000660 !important;
            border: none !important;
            color: white !important;
        }

        .stButton button {
            background-color: #006666;
            border: none !important;
            color: white;
            padding: 0.5rem 2rem !important;
        }
        .stButton button:hover {
            background-color: #008080 !important;
            color: white !important;
            border-color: #008080 !important;
        }
        .upload-text {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        div[data-testid="stFileUploadDropzone"]:hover {
            border-color: #006666 !important;
            background-color: rgba(0, 102, 102, 0.05) !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("PDF to Markdown Converter")

# Initialize session state if it doesn't exist
if 'converter' not in st.session_state:
    try:
        st.session_state.converter = DocumentConverter()
        logger.debug("Converter successfully created")
    except Exception as e:
        logger.error(f"Error creating converter: {str(e)}")
        st.error(f"Error creating converter: {str(e)}")
        st.stop()

# Main upload area
uploaded_file = st.file_uploader(
    "Upload your PDF file",
    type=['pdf'],
    key='pdf_uploader',
    help="Drag and drop or click to select a PDF file (max 200MB)"
)

# URL input area with spacing
st.markdown("<br>", unsafe_allow_html=True)
url = st.text_input("Or enter a PDF URL")

# Unified convert button
convert_clicked = st.button("Convert to Markdown", type="primary")

# Process either uploaded file or URL
if convert_clicked:
    if uploaded_file is not None:
        try:
            with st.spinner('Converting file...'):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                    logger.debug(f"Temporary file created at: {tmp_path}")

                    try:
                        result = st.session_state.converter.convert(tmp_path)
                        markdown_text = result.document.export_to_markdown()
                        
                        output_filename = os.path.splitext(uploaded_file.name)[0] + '.md'
                        
                        st.success("Conversion completed!")
                        st.download_button(
                            label="Download Markdown file",
                            data=markdown_text,
                            file_name=output_filename,
                            mime="text/markdown"
                        )

                    except Exception as e:
                        logger.error(f"Error converting file: {str(e)}")
                        st.error(f"Error converting file: {str(e)}")
                    
                    finally:
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
                            logger.debug("Temporary file deleted")

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            st.error(f"Error processing file: {str(e)}")
            
    elif url:
        try:
            with st.spinner('Converting from URL...'):
                logger.debug(f"Converting from URL: {url}")
                result = st.session_state.converter.convert(url)
                markdown_text = result.document.export_to_markdown()
                
                output_filename = url.split('/')[-1].split('.')[0] + '.md'
                
                st.success("Conversion completed!")
                st.download_button(
                    label="Download Markdown file",
                    data=markdown_text,
                    file_name=output_filename,
                    mime="text/markdown"
                )

        except Exception as e:
            logger.error(f"Error converting from URL: {str(e)}")
            st.error(f"Error converting from URL: {str(e)}")
    else:
        st.warning("Please upload a file or enter a URL first")