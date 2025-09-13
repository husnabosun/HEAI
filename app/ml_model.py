import os
from huggingface_hub import InferenceClient

from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

result = client.text_classification(
    "Sore throat, mild headache, slight fever",
    model="shanover/symps_disease_bert_v3_c41",
)

print(result)