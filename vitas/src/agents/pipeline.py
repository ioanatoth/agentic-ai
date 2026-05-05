from openai import OpenAI
import os
import json

class AgenticPipeline:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Prompt-ul sistem care definește regulile de extracție (FR3, FR4)
        self.system_prompt = """
        Ești un expert în procesarea documentelor veterinare românești. 
        Extrage datele din imagine sub formă de JSON cu următoarea structură:
        {
          "header": { "document_number": "", "issue_date": "", "owner_name": "", "holding_id": "" },
          "animals": [
            { "species": "", "ear_tag": "", "sex": "", "birth_date": "", "entry_date": "" }
          ]
        }
        Dacă specia apare ca header de grup, aplică acea specie tuturor rândurilor de dedesubt (FR6).
        """

    def extract_from_image(self, base64_image):
        """Trimite imaginea la GPT-4o Vision pentru OCR și structurare[cite: 1, 2]."""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extrage datele din acest document conform schemei solicitate."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)