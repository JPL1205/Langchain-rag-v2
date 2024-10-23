# test_pdf_extraction.py
from PyPDF2 import PdfReader

def test_pdf_extraction(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python test_pdf_extraction.py path_to_pdf")
        sys.exit(1)
    file_path = sys.argv[1]
    extracted_text = test_pdf_extraction(file_path)
    if extracted_text:
        print(f"Extracted Text from {file_path}:")
        print(extracted_text[:500], "...")  # Print first 500 characters
    else:
        print(f"No extractable text found in {file_path}.")
