import base64
from pathlib import Path
from opensearchpy import OpenSearch

# Opensearch Setup
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False,  # set True + http_auth if security enabled
)

INDEX_NAME = "multimodalrag"
if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME)


def encode_image_to_base64(img_path):
    """Load image from disk and convert to base64 string."""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_text_from_disk(pdf_name):
    """Load extracted text files from disk into a dict {page_number: text}."""
    text_dir = Path("extracted_data/texts") / pdf_name
    text_data = {}
    if text_dir.exists():
        for txt_file in sorted(text_dir.glob("page_*.txt")):
            page_num = int(txt_file.stem.split("_")[1])
            text_data[page_num] = txt_file.read_text(encoding="utf-8")
    return text_data


def load_images_from_disk(pdf_name):
    """Load extracted images from disk into a dict {page_number: [base64_images]}."""
    image_dir = Path("extracted_data/images") / pdf_name
    images_by_page = {}
    if image_dir.exists():
        for img_file in sorted(image_dir.glob("*.png")):
            parts = img_file.stem.split("_")
            try:
                page_num = int(parts[1])
            except:
                page_num = 1
            images_by_page.setdefault(page_num, []).append(
                encode_image_to_base64(img_file)
            )
    return images_by_page


def index_pdf_page(pdf_name, page_number, text, images):
    """Index a PDF page into OpenSearch."""
    doc = {
        "pdf_name": pdf_name,
        "page_number": page_number,
        "text": text,
        "images": images,
    }
    # Change 'document=doc' → 'body=doc'
    client.index(index=INDEX_NAME, body=doc)


def process_all_pdfs_to_opensearch():
    """Load text and images from disk and index them into OpenSearch."""
    base_text_dir = Path("extracted_data/texts")
    all_results = {}

    # Iterate over all PDFs we have text for
    for pdf_dir in base_text_dir.iterdir():
        if pdf_dir.is_dir():
            pdf_name = pdf_dir.name
            print(f"\nProcessing: {pdf_name}")

            text_data = load_text_from_disk(pdf_name)
            images_by_page = load_images_from_disk(pdf_name)

            for page, text in text_data.items():
                page_images = images_by_page.get(page, [])
                index_pdf_page(pdf_name, page, text, page_images)

            all_results[pdf_name] = {"text": text_data, "images": images_by_page}
            print(f"Indexed {len(text_data)} pages with images for {pdf_name}")

    return all_results


if __name__ == "__main__":
    process_all_pdfs_to_opensearch()
