import base64
import os

logo_path = r"c:\Agent Coco\assets\logo_taleemabad.png"

with open(logo_path, 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()

print(logo_b64)
