from PyPDF2 import PdfReader
from docx import Document
import os

class FileHandling:
    def read_file(self, file_path):
        """
        Reads the content of a file based on its extension.
        
        Args:
            file_path (str): The path to the file.

        Returns:
            str: The text content of the file.
        """
        if not os.path.isfile(file_path):
            return "File not found."

        # Get the file extension
        _, ext = os.path.splitext(file_path)

        text = ""

        if ext.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
        
        elif ext.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        elif ext.lower() == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            return "Unsupported file format."

        return text.strip()
