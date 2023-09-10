import streamlit as st
import pandas as pd
import pdfplumber
from pdf2image import convert_from_path
import tempfile

# Streamlit layout for the left sidebar
st.sidebar.title("PDF Table to LaTeX Converter")
pdf_file = st.sidebar.file_uploader("Upload a PDF", type=['pdf'])


# Read PDF and show on the left sidebar
if pdf_file:
        # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name
    # Use pdfplumber to get the number of pages
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
    
    # Create a slider in the sidebar to select a page
    page = st.sidebar.slider("Select a page", 1, total_pages)

    # Convert the selected PDF page to image and display in the sidebar
    images = convert_from_path(temp_path, first_page=page, last_page=page)
    for image in images:
        st.sidebar.image(image, caption=f"Page {page}", use_column_width=True)
    
    # Open the selected page with pdfplumber for table extraction
    with pdfplumber.open(temp_path) as pdf:
        selected_page = pdf.pages[page-1]
        
        # Extract tables using pdfplumber
        tables = selected_page.extract_tables()
        
        # Display LaTeX code on the right
        st.title("LaTeX Code")
        
        for i, table in enumerate(tables):
            st.subheader(f"Table {i+1}")
            df = pd.DataFrame(table[1:], columns=table[0])
            latex_code = df.to_latex(index=False)
            st.code(latex_code, language='latex')
