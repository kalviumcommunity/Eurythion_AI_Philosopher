import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------
# Load API Key (from .env file)
# -------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found in .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# -------------------------------
# Personality Prompts
# -------------------------------
LIGHT_SYSTEM = """
You are the Light voice:
- Optimistic, supportive, kind, and encouraging.
- Always give hopeful and inspiring answers.
- Respond in a way that makes the user feel uplifted and motivated.
- Always end with the marker: <<END>>
"""

DARK_SYSTEM = """
You are the Dark voice:
- Blunt, realistic, brutally honest, sometimes harsh.
- Always reveal uncomfortable truths, even if it hurts.
- Cut through illusions and avoid sugarcoating.
- Always end with the marker: <<END>>
"""

# -------------------------------
# Dynamic Prompting
# -------------------------------
def build_dynamic_prompt(base_prompt: str, user_input: str) -> str:
    """Enhance system prompt dynamically based on user input context"""
    dynamic_addition = ""

    if any(word in user_input.lower() for word in ["sad", "depressed", "lonely", "lost"]):
        dynamic_addition = "\n[Dynamic]: The user seems emotionally vulnerable. Be extra thoughtful and empathetic."
    elif any(word in user_input.lower() for word in ["angry", "frustrated", "annoyed"]):
        dynamic_addition = "\n[Dynamic]: The user is upset. Respond calmly, with clear reasoning."
    elif any(word in user_input.lower() for word in ["happy", "excited", "grateful"]):
        dynamic_addition = "\n[Dynamic]: The user is in a good mood. Match their energy and positivity."
    else:
        dynamic_addition = "\n[Dynamic]: No special emotion detected. Respond normally."

    return base_prompt + dynamic_addition

# -------------------------------
# Dual Response Generator
# -------------------------------
def generate_response(user_input, temperature=0.7, top_p=0.9, max_tokens=300):
    def call_openrouter(messages):
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # ⚡ swap models here
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,  # ✅ Configurable
            frequency_penalty=0.2,
            presence_penalty=0.2,
            stop=["<<END>>"],  # ✅ Stop sequence
        )

        # ✅ Log token usage
        usage = response.usage
        print(f"🔎 Token usage → Prompt: {usage.prompt_tokens}, "
              f"Completion: {usage.completion_tokens}, "
              f"Total: {usage.total_tokens}")

        return response.choices[0].message.content.strip() + " <<END>>"

    # Build Light + Dark messages with dynamic system prompt
    light_messages = [
        {"role": "system", "content": build_dynamic_prompt(LIGHT_SYSTEM, user_input)},
        {"role": "user", "content": user_input},
    ]
    dark_messages = [
        {"role": "system", "content": build_dynamic_prompt(DARK_SYSTEM, user_input)},
        {"role": "user", "content": user_input},
    ]

    # Query both personalities
    light_response = call_openrouter(light_messages)
    dark_response = call_openrouter(dark_messages)

    return f"\n🌞 Light: {light_response}\n\n🌑 Dark: {dark_response}\n"

# -------------------------------
# CLI
# -------------------------------
def main():
    print("🌗 Welcome to Eurythion CLI — Dual-Personality AI\n")
    print("Type 'exit' or 'quit' to leave.")
    while True:
        user_input = input("\n❓ You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        print("\n✨ Generating dual responses...\n")
        reply = generate_response(user_input, temperature=0.8, top_p=0.85)  # ✅ Example
        print(reply)

if __name__ == "__main__":
    main()
