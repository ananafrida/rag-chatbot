import boto3
import json
from langchain_aws.llms import BedrockLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

load_dotenv()  # load variables from .env

# # Create a session with AWS credentials
# session = boto3.Session(profile_name="default")
session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_DEFAULT_REGION"]
)

# Initialize Amazon Bedrock clients
boto3_bedrock = session.client("bedrock-runtime", region_name="us-east-2")
boto3_kb = session.client("bedrock-agent-runtime", region_name="us-east-2")


client = boto3.client('bedrock', region_name='us-east-2')
response = client.list_foundation_models()

for model in response['modelSummaries']:
    print(f"Model ID: {model['modelId']}, Provider: {model['providerName']}")


# Define model parameters
max_generation_length = 2**11  # Adjusted to avoid unnecessary memory use
llm_id = "meta.llama3-3-70b-instruct-v1:0"  # See: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
llm_arn = "arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0"
kb_id = "OHKEXQ6U4M"  # <-- Your actual Knowledge Base ID

# Create memory buffer
memory = ConversationBufferMemory(max_token_limit=max_generation_length)

def demo_conversation(input_text, kb_id="OHKEXQ6U4M", llm_arn = "arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0"):
    # 1. Load conversation history from memory (if any)
    memory_vars = memory.load_memory_variables({})
    conversation_history = memory_vars.get("history", "")

    # 2. Create a prompt tailored for App Inventor learning support
    prompt = (
        "You are a helpful assistant for students learning to use MIT App Inventor. "
        "Your job is to explain how different blocks work, help debug common issues, "
        "and suggest how to combine blocks for building simple apps. "
        "Base your answers on the knowledge base. Be clear, friendly, and use simple examples when possible. "
        + conversation_history
        + f"\nUser: {input_text}\nAssistant:"
    )

    # 3. Call the knowledge-based generation using the constructed prompt
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

    # 4. Extract the generated response text
    generated_text = response.get("output", {}).get("text", "No response generated.")

    # 5. Extract a direct quote from the knowledge base (if available)
    citations = response.get("citations", [])
    direct_quote = None
    for citation in citations:
        retrieved_references = citation.get("retrievedReferences", [])
        for ref in retrieved_references:
            if "text" in ref.get("content", {}):
                direct_quote = ref["content"]["text"]
                break
        if direct_quote:
            break

    # 6. Save the conversation context (user input and generated response) to memory
    memory.save_context({"input": input_text}, {"output": generated_text})

    # 7. Format and return the output including the referred document (if any)
    return f"{generated_text}\n\n**Referred Document**: {direct_quote if direct_quote else 'No document was searched'}"
