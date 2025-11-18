import boto3
import json
from dotenv import load_dotenv
import os

# --- Load .env properly ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(ROOT_DIR, ".env")
load_dotenv(env_path)

# --- Simple Python memory buffer ---
conversation_memory = []

# --- AWS session ---
session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_DEFAULT_REGION"]
)

boto3_bedrock = session.client("bedrock-runtime", region_name="us-east-2")
boto3_kb = session.client("bedrock-agent-runtime", region_name="us-east-2")

llm_arn = "arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0"
kb_id = "OHKEXQ6U4M"

def demo_conversation(input_text):
    # 1. Build conversation history
    conversation_history = "\n".join(conversation_memory)

    # 2. Build prompt
    prompt = (
        "You are a helpful assistant for students learning MIT App Inventor. "
        "Explain blocks, debug problems, and give examples. "
        "Use the knowledge base.\n\n"
        f"{conversation_history}\n"
        f"User: {input_text}\nAssistant:"
    )

    # 3. Call Bedrock KB
    response = boto3_kb.retrieve_and_generate(
        input={"text": prompt},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": llm_arn
            }
        }
    )

    generated_text = response.get("output", {}).get("text", "No response generated.")

    # 4. Extract quote
    direct_quote = None
    for citation in response.get("citations", []):
        for ref in citation.get("retrievedReferences", []):
            if "text" in ref.get("content", {}):
                direct_quote = ref["content"]["text"]
                break
        if direct_quote:
            break

    # 5. Save conversation memory
    conversation_memory.append(f"User: {input_text}")
    conversation_memory.append(f"Assistant: {generated_text}")

    # 6. Return output
    return (
        f"{generated_text}\n\n"
        f"**Referred Document**: {direct_quote if direct_quote else 'No document was searched'}"
    )
