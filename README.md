# PDF to Markdown using Docling 

A simple web application that converts PDF documents to Markdown format using the docling library.

**Note** : The application interface is currently in Spanish. To change the language, simply modify the text strings in the Streamlit UI code (app.py).

## Requirements

### Python Version

- Tested and working on Python 3.12 and below (as of November 2024)

### External Libraries

```bash
pip install streamlit docling
```

Or use the requirements.txt:

```bash
pip install -r requirements.txt
```

Content for requirements.txt:

```
streamlit==1.29.0
docling==1.17.0
watchdog==2.3.1
```

Note: tempfile, os, and logging are part of Python's standard library and don't require installation.

## Features

- PDF to Markdown conversion through web interface
- Local file upload support
- URL conversion support
- Preserves original filename in conversion
- Robust error handling
- Logging system for debugging

## Usage

1. Run the application:

```bash
streamlit run app.py
```

2. Access the web application through your browser
3. You can convert PDF files in two ways:

   - Uploading a local PDF file
   - Providing a PDF URL
4. Click "Convert" and download the resulting Markdown file

## Code Structure

- `app.py`: Main Streamlit application
- Logging configured for debugging
- Temporary file handling for PDF processing
- Error handling system

## Limitations

- Only accepts PDF files
- Conversion quality depends on the original PDF structure
- For URLs, the PDF must be publicly accessible
- Currently tested up to Python 3.12

## License

This project is under the MIT License. See the `LICENSE` file for more details.
