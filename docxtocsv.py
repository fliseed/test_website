from docx import Document #import docx to run this code --> pip install python-docx
import zipfile
import os
import shutil
import csv
import html
import html
from lxml import etree
import re
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def extract_text(docx_path, image_map=None, output_dir="images"):
    doc = Document(docx_path)
    html_output = ""
    in_list = False
    list_type = None  # 'ul' or 'ol'
    image_counter = 1

    for para in doc.paragraphs:
        paragraph_html = ""

        for run in para.runs:
            # Add text
            if run.text:
                paragraph_html += run.text

            # Detect drawing (image)
            if run._element.xpath('.//w:drawing'):
                # You can also parse r:embed ID here for exact mapping
                img_filename = image_map.get(f"image{image_counter}", f"image{image_counter}.png")
                paragraph_html += f'<img src="{output_dir}/{img_filename}" />'
                image_counter += 1

        if paragraph_html.strip():
            html_output += f"<p>{paragraph_html}</p>\n"

        text = para.text.strip()
        if not text:  # Skip empty paragraphs
            continue

        # Check for bullet points
        is_bullet = (para.style.name.lower().startswith('list') or 
                    text.startswith('●') or 
                    text.startswith('•') or 
                    text.startswith('-') or
                    bool(para._p.xpath('.//w:numPr')))
        
        # Handle lists
        if is_bullet:
            if not in_list:
                html_output += "<ul>\n"
                in_list = True
            html_output += f"<li>{process_paragraph_content(para)}</li>\n"
        else:
            if in_list:
                html_output += "</ul>\n"
                in_list = False
            
            # Detect headings
            style = para.style.name.lower()
            if 'heading' in style:
                level = style.replace('heading ', '')
                html_output += f"<h{level}>{process_paragraph_content(para)}</h{level}>\n"
            else:
                # Regular paragraph with line break support
                html_output += f"<p>{process_paragraph_content(para)}</p>\n"

    # Close any remaining list
    if in_list:
        html_output += "</ul>\n"

    return html_output

def process_paragraph_content(paragraph):
    """Process paragraph content including line breaks and formatting, and detect links"""
    content_parts = []
    url_pattern = re.compile(r'(https?://[^\s]+|www\.[^\s]+)')

    def make_link(match):
        url = match.group(0)
        href = url if url.startswith("http") else f"http://{url}"
        return f'<a href="{href}">{html.escape(url)}</a>'
    

    for run in paragraph.runs:
        run_text = html.escape(run.text)
        if not run_text:
            continue
        # Apply formatting tags based on run properties
        formatted_text = run_text

        formatted_text = url_pattern.sub(r'<a href="\1">\1</a>', formatted_text)

        if not formatted_text.startswith("<a href="):
            # Check for bold
            if run.bold:
                formatted_text = f"<strong>{formatted_text}</strong>"
                
            # Check for italic
            if run.italic:
                formatted_text = f"<em>{formatted_text}</em>"
                
            # Check for underline
            if run.underline:
                formatted_text = f"<u>{formatted_text}</u>"
                
            # Check for strikethrough
            if run.font.strike:
                formatted_text = f"<strike>{formatted_text}</strike>"

            # Replace URLs in the run with <a> tags

        # Check for line breaks in this run
        if run._r.xpath(".//w:br"):
            formatted_text = formatted_text.replace("\n", "<br/>\n")

        content_parts.append(formatted_text)

    if not content_parts:
        paragraph_text = html.escape(paragraph.text)
        paragraph_text = url_pattern.sub(r'<a href="\1">\1</a>', paragraph_text)
        return paragraph_text

    return "".join(content_parts)


def upload_csv(text = "", article_id = 1):
    # Read all rows
    with open("pages/articles/articles.csv", 'r', newline='') as f:
        reader = list(csv.reader(f))

    # Modify matching row
    for row in reader:
        if row and row[0] == article_id:
            row.append(text)

    # Write updated rows back to file
    with open("pages/articles/articles.csv", 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        writer.writerows(reader)


def clear_content_csv():
    with open("pages/articles/articles.csv", 'r', newline='') as f:
        reader = list(csv.reader(f))
    
    content_id = reader[0].index('content')
    normal_len = len(reader[0])

    for row in range(1, len(reader)):
        if len(reader[row]) == normal_len:
            if reader[row][content_id] != '':
                reader[row].remove(reader[row][content_id])
    
    with open("pages/articles/articles.csv", 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        writer.writerows(reader)


def extract_images(docx_path, output_dir="images"):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall("temp_docx")

    media_path = os.path.join("temp_docx", "word", "media")
    image_map = {}

    
    if os.path.exists(media_path):
        os.makedirs(f"pages/articles/{output_dir}", exist_ok=True)
        for i, file in enumerate(sorted(os.listdir(media_path))):
            image_dest = os.path.join(f"pages/articles/{output_dir}", file)
            shutil.copy(os.path.join(media_path, file), image_dest)
            image_map[f"image{i+1}"] = file
        print(f"Images saved to 'pages/articles/{output_dir}'")
    else:
        print("No images found in the document.")

    shutil.rmtree("temp_docx")

    return image_map

# Example usage

docx_path = input("Enter the path to your .docx file: ")
article_id = input("Enter the article ID: ")
output_dir = input("Enter the output directory for images: ")
image_map = extract_images(docx_path, output_dir)
text = extract_text(docx_path, image_map, output_dir)
print(text)
upload_csv(text, article_id)
# This code extracts text and images from a .docx file and saves them to a CSV file and a specified directory.


#clear_content_csv()