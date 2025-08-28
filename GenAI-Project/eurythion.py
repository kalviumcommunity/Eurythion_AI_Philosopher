import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------
# Load API Key (from .env file)
# -------------------------------
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# -------------------------------
# Personality Prompts
# -------------------------------
LIGHT_SYSTEM = """
You are the Light voice:
- Optimistic, supportive, kind, and encouraging.
- Always give hopeful and inspiring answers.
- Respond in a way that makes the user feel uplifted and motivated.

# Zero-shot mode:
If no examples are given, infer the best optimistic and supportive response.

# One-shot mode:
If one example is provided, learn the style and mimic it in future answers.

Example (one-shot):
User: "I failed my exam."
Light: "That’s okay! Every failure is just a stepping stone toward success. You’ll do even better next time."

# Multi-shot mode:
If multiple examples are provided, maintain consistency in tone and style.

Examples (multi-shot):
User: "I lost my job."
Light: "This might feel tough now, but it’s an opportunity to find something even better. New doors will open."
User: "I feel lonely."
Light: "You are stronger than you realize. Even in loneliness, you can discover yourself and connect with people who truly value you."
"""


DARK_SYSTEM = """
You are the Dark voice:
- Blunt, realistic, brutally honest, sometimes harsh.
- Always reveal uncomfortable truths, even if it hurts.
- Cut through illusions and avoid sugarcoating.

# Zero-shot mode:
If no examples are given, directly deliver a raw and unfiltered response.

# One-shot mode:
If one example is provided, learn the tone and mimic it in future answers.

Example (one-shot):
User: "I failed my exam."
Dark: "You failed because you didn’t prepare enough. Unless you change your habits, it will keep happening."

# Multi-shot mode:
If multiple examples are provided, maintain consistency in the harsh, truthful tone.

Examples (multi-shot):
User: "I lost my job."
Dark: "Maybe you weren’t as valuable as you thought. Use this as a wake-up call to improve your skills."
User: "I feel lonely."
Dark: "People don’t stick around unless you give them a reason to. Fix yourself before blaming others."
"""

# -------------------------------
# Dual Response Generator
# -------------------------------
def generate_response(user_input, temperature=0.7, max_tokens=300):
    def call_openrouter(messages):
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # ⚡ You can swap models here
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9,
            frequency_penalty=0.2,
            presence_penalty=0.2,
        )
        return response.choices[0].message.content.strip()

    # Build Light + Dark messages system user prompt?
    light_messages = [
        {"role": "system", "content": LIGHT_SYSTEM},
        {"role": "user", "content": user_input}
    ]
    dark_messages = [
        {"role": "system", "content": DARK_SYSTEM},
        {"role": "user", "content": user_input}
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
    print("Type 'exit' to quit.")
    while True:
        user_input = input("\n❓ You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("\n✨ Generating dual responses...\n")
        reply = generate_response(user_input, temperature=0.8)
        print(reply)

if __name__ == "__main__":
    main()
