import fitz  # PyMuPDF imports as "fitz"
import os

# POINT THIS TO YOUR DOWNLOADED FILE
filename = "C:\\Users\\bhanu\\Downloads\\TheAPIfirstWorldPostman.pdf" # <--- Paste your hash name here

try:
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    
    print("--- SUCCESS! EXTRACTED TEXT ---")
    print(text[:500])  # Print first 500 characters
    print("-------------------------------")
except Exception as e:
    print(f"Error: {e}")