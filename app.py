import streamlit as st
import tabula
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter
import tempfile

# Streamlit layout
st.title("PDF Table to LaTeX Converter")

pdf_file = st.file_uploader("Upload a PDF", type=['pdf'])

# Read PDF and show on the left
if pdf_file:
    st.sidebar.title("PDF Display")
    pdf_reader = PdfFileReader(pdf_file)
    total_pages = pdf_reader.numPages
    page = st.sidebar.slider("Select a page", 1, total_pages)
    
    # Create a temporary file for the selected PDF page
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(page-1))
        pdf_writer.write(temp_pdf)
        temp_pdf_path = temp_pdf.name
    
    # Display PDF using an iframe
    pdf_display = f'<iframe src="file://{temp_pdf_path}" width="400" height="600"></iframe>'
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

    # Extract tables using tabula
    tables = tabula.read_pdf(pdf_file, pages=page, multiple_tables=True)
    
    # Display LaTeX code on the right
    st.title("LaTeX Code")
    for i, table in enumerate(tables):
        st.subheader(f"Table {i+1}")
        latex_code = table.to_latex(index=False)
        st.code(latex_code, language='latex')
