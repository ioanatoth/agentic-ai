import os
from PIL import Image, ImageOps
import pymupdf4llm
import base64
from io import BytesIO


class DocumentProcessor:
    """
    Gestionează ingestia și preprocesarea conform cerințelor 6.1 și 6.2.
    """

    @staticmethod
    def preprocess_image(image_file):
        """
        Cerința 6.1: Pentru imagini, aplicăm corecții de bază.
        """
        img = Image.open(image_file)
        # Convertim la RGB pentru compatibilitate cu OpenAI Vision
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Putem aplica grayscale sau resize dacă imaginea este prea mare[cite: 1]
        return img

    @staticmethod
    def encode_image_to_base64(image):
        """
        Pregătește imaginea pentru a fi trimisă către Agentul de Vision[cite: 2].
        """
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    @staticmethod
    def process_pdf_to_markdown(pdf_path):
        """
        Cerința 6.2: Pentru PDF-uri, folosim PyMuPDF4LLM pentru a păstra structura.
        """
        try:
            # Extrage textul și tabelele în format Markdown, optim pentru LLM[cite: 2]
            md_text = pymupdf4llm.to_markdown(pdf_path)
            return md_text
        except Exception as e:
            return f"Eroare la procesarea PDF-ului: {str(e)}"