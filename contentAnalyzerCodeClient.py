from pathlib import Path
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client
endpoint = ""
credential = AzureKeyCredential("")
client = ContentUnderstandingClient(endpoint=endpoint, credential=credential)

# Analyze the CV using the custom analyzer
analyzer_name = "business_card_analyser"
file_bytes = (Path(__file__).parent / "CV Murat Yilmaz recent.pdf").read_bytes()
poller = client.begin_analyze_binary(
    analyzer_id=analyzer_name,
    binary_input=file_bytes,
    content_type="application/pdf",
)

# Wait for the operation to complete and get the results
result = poller.result()

# Extract field values from the results
content = result.contents[0]
if content.fields:
    for field_name, field_data in content.fields.items():
        if field_data.type == "string":
            print(f"{field_name}: {field_data.value}")