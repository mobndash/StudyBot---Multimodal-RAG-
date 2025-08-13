import base64
from pathlib import Path
from data_ingestion.read_pdf_files import read_pdf_files
from data_ingestion.read_pdf_files import extract_text_with_metadata
from data_ingestion.read_pdf_files import extract_images_with_metadata


def save_base64_image(base64_str, output_path):
    """Decode base64 image data and save as a file."""
    image_bytes = base64.b64decode(base64_str)
    with open(output_path, "wb") as f:
        f.write(image_bytes)


def process_all_pdfs():
    """Processes all PDFs, extracts text and images, and saves them locally."""
    pdf_paths = read_pdf_files()  # Your function to read PDF paths
    all_results = {}

    # Base folders
    base_text_dir = Path("extracted_data/texts")
    base_image_dir = Path("extracted_data/images")
    base_text_dir.mkdir(parents=True, exist_ok=True)
    base_image_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_paths:
        pdf_name = Path(pdf_path).stem
        print(f"\nProcessing: {pdf_path}")

        # Create PDF-specific folders
        pdf_text_dir = base_text_dir / pdf_name
        pdf_image_dir = base_image_dir / pdf_name
        pdf_text_dir.mkdir(exist_ok=True)
        pdf_image_dir.mkdir(exist_ok=True)

        # Extract text and save per page
        text_data = extract_text_with_metadata(pdf_path)
        for page, text in text_data.items():
            text_file = pdf_text_dir / f"page_{page}.txt"
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(text)

        # Extract images and save
        image_data = extract_images_with_metadata(pdf_path)
        for idx, img in enumerate(image_data, start=1):
            if img.get("image_base64"):
                img_file = pdf_image_dir / f"page_{img['page_number']}_img_{idx}.png"
                save_base64_image(img["image_base64"], img_file)

        # Store results in memory as well (optional)
        all_results[pdf_path] = {"text": text_data, "images": image_data}

        print(
            f"Saved {len(text_data)} text pages and {len(image_data)} images for {pdf_path}"
        )

    return all_results


if __name__ == "__main__":
    process_all_pdfs()
