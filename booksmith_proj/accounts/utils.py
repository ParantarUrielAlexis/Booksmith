import fitz  # PyMuPDF

def convert_pdf_to_html(pdf_path):
    html_content = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            html_content += page.get_text("html")  # Get HTML format of the page
    return html_content
