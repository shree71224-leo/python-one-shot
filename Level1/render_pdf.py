import fitz
import os

# PDF location
pdf_path = r"C:\Users\ASUS\Downloads\CTD Dataset\CTD Dataset\training\electrical\701_dexter\701 Dexter - Electrical Drawings.pdf"

# Output folder
output_folder = "rendered_pages"
os.makedirs(output_folder, exist_ok=True)

# Open PDF
pdf = fitz.open(pdf_path)

# 150 DPI
dpi = 150
zoom = dpi / 72
matrix = fitz.Matrix(zoom, zoom)

print(f"Total pages: {len(pdf)}")

# Convert every PDF page to PNG
for page_number, page in enumerate(pdf, start=1):

    pix = page.get_pixmap(matrix=matrix, alpha=False)

    output_path = os.path.join(
        output_folder,
        f"page_{page_number}.png"
    )

    pix.save(output_path)

    print(f"Rendered page {page_number}/{len(pdf)}")

pdf.close()

print("PDF conversion completed!")