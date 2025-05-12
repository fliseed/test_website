from docx import Document #import docx to run this code --> pip install python-docx
import zipfile
import os
import shutil
import csv
import html

from docx import Document
import html
from lxml import etree

def extract_text(docx_path):
    doc = Document(docx_path)
    html_output = ""
    in_list = False
    list_type = None  # 'ul' or 'ol'

    for para in doc.paragraphs:
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
    """Process paragraph content including line breaks and formatting"""
    content_parts = []
    
    for run in paragraph.runs:
        run_text = html.escape(run.text)
        
        # Check for line breaks in this run
        if run._r.xpath(".//w:br"):
            run_text = run_text.replace("\n", "<br/>\n")
        
        content_parts.append(run_text)
    
    if content_parts == []:
        content_parts = paragraph.text 

    # Join all parts and clean up
    content = "".join(content_parts)
        
    return content

def upload_csv(text, article_id):
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


def extract_images(docx_path, output_dir="images"):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall("temp_docx")

    media_path = os.path.join("temp_docx", "word", "media")
    if os.path.exists(media_path):
        os.makedirs(f"pages/articles/{output_dir}", exist_ok=True)
        for file in os.listdir(media_path):
            shutil.copy(os.path.join(media_path, file), os.path.join(f"pages/articles/{output_dir}", file))
        print(f"Images saved to 'pages/articles/{output_dir}'")
    else:
        print("No images found in the document.")

    shutil.rmtree("temp_docx")

# Example usage
docx_path = input("Enter the path to your .docx file: ")
article_id = input("Enter the article ID: ")
output_dir = input("Enter the output directory for images: ")
text = extract_text(docx_path)
print(text)
upload_csv(text, article_id)
extract_images(docx_path, output_dir)
# This code extracts text and images from a .docx file and saves them to a CSV file and a specified directory.
