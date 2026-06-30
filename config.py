import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
LLM_MODEL="llama-3.1-8b-instant"

PART_FILE=r"C:\Users\Mansi\OneDrive\Desktop\part3\part2.SLDPRT"
PART_PATH = PART_FILE
TEMPLATE_PATH=r"C:\Users\Mansi\OneDrive\Desktop\part3\template.SLDDRW"
OUTPUT_PATH=r"C:\Users\Mansi\OneDrive\Desktop\part3\solidworks_agent\output"

MIN_DIMENSION_GAP_MM = 8
MAX_AGENT_RETRIES = 3