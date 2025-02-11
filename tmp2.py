import os
import json
from unstructured.partition.pdf import partition_pdf
from azure.identity import DefaultAzureCredential
from azure.ai.openai import OpenAI

# Define your Azure OpenAI credentials
AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "your-azure-endpoint"
AZURE_DEPLOYMENT_NAME = "your-deployment-name"

# Load the PDF and extract content
def extract_pdf_text(pdf_path):
    elements = partition_pdf(filename=pdf_path, strategy="fast")
    extracted_text = "\n".join([elem.text for elem in elements if hasattr(elem, 'text')])
    return extracted_text

# Define the prompt
SUMMARIZE_IMAGE_PROMPT = """Summarize the relevant information from the extracted text that answers the following question: {}"""

# Define function to query Azure GPT-4o
def query_gpt_4o(prompt, extracted_text):
    client = OpenAI(api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, azure_deployment=AZURE_DEPLOYMENT_NAME)

    messages = [
        {"role": "system", "content": "You are an AI assistant helping extract data from a document."},
        {"role": "user", "content": f"{prompt}\n\nDocument Content:\n{extracted_text}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages,
        temperature=0.2
    )
    
    return response.choices[0].message.content.strip()

# Load the PDF
pdf_path = "your-pdf-file.pdf"
extracted_text = extract_pdf_text(pdf_path)

# Modify the question here for prompt engineering
question = "What is the value of X in the table regarding Y?"
final_prompt = SUMMARIZE_IMAGE_PROMPT.format(question)

# Get response from GPT-4o
answer = query_gpt_4o(final_prompt, extracted_text)

# Print or store the answer
print("Answer:", answer)
