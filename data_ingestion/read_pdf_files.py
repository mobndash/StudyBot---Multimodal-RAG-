import os
import ipykernel
import pytesseract as py
import unstructured as un
from pathlib import Path
import pytesseract
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Text
import pytesseract
from unstructured.documents.elements import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["PATH"] += (
    os.pathsep + r"C:\Program Files\poppler\poppler-24.08.0\Library\bin"
)


def read_pdf_files():
    """Returns pdf path of all pdf files"""
    corpus_path = "corpus"
    pdf_files = []
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                pdf_files.append(file_path)
    return pdf_files


def extract_text_with_metadata(pdf_path):
    """Extracts text from pdf"""
    pdf_path = Path(pdf_path)

    pdf_elements = partition_pdf(
        filename=str(pdf_path), strategy="hi_res", extract_images_in_pdf=False
    )

    page_data = {}
    for ele in pdf_elements:
        if isinstance(ele, Text) and ele.text.strip():
            meta = ele.metadata.to_dict() if ele.metadata else {}
            page_num = meta.get("page_number", "unknown")

            # Group text by page number
            page_data.setdefault(page_num, []).append(ele.text.strip())

    # Merge text chunks for each page
    for page in page_data:
        page_data[page] = "\n".join(page_data[page])

    return page_data


def process_all_pdfs():
    """Processes all PDFs in the corpus folder."""
    pdf_paths = read_pdf_files()
    all_results = {}

    for pdf_path in pdf_paths:
        print(f"\n Processing: {pdf_path}")
        pages = extract_text_with_metadata(pdf_path)
        all_results[pdf_path] = pages

        # Example: Print result
        for page, text in pages.items():
            print(f"\n--- {pdf_path} | Page {page} ---")
            print(text[:500], "..." if len(text) > 500 else "")

    return all_results


def extract_images_with_metadata(pdf_path):
    pdf_path = Path(pdf_path)

    pdf_elements = partition_pdf(
        filename=str(pdf_path),
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image", "Figure", "Table"],
        extract_image_block_to_payload=True,
        chunking_strategy=None,
    )

    image_data = []
    for ele in pdf_elements:
        if isinstance(ele, Image):
            meta = ele.metadata.to_dict() if ele.metadata else {}
            image_data.append(
                {
                    "pdf_name": pdf_path.name,
                    "page_number": meta.get("page_number"),
                    "image_base64": meta.get("image_base64"),  # Base64 image data
                    # "coordinates": meta.get("coordinates")
                }
            )

    return image_data
