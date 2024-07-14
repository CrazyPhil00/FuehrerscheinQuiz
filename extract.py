import fitz


def extract_images_from_pdf(pdf_path):
    """
    Extracts and counts unique images from a PDF document.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    int: Total number of unique images found in the PDF.
    """
    document = fitz.open(pdf_path)
    image_count = set()  # Use a set to track unique images

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        images_on_page = page.get_images(full=True)

        for img in images_on_page:
            # Generate a unique key for each image based on its index and width
            image_key = f"{img[0]}_{img[1]}"
            if image_key not in image_count:
                image_count.add(image_key)
                # Optionally, handle the image as needed (e.g., save it, log it, etc.)

    return len(image_count)

if __name__ == "__main__":
    pdf_path = 'DomandeB.pdf'  # Replace with your PDF file path
    num_unique_images = extract_images_from_pdf(pdf_path)
    print(f"Found {num_unique_images} unique images.")