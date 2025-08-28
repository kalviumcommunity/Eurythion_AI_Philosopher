# Eurythion 🌓

**Eurythion** is a powerful yet simple CLI-based conversational AI that responds with dual personalities — one rooted in optimism, the other forged in brutal honesty. Whether you're looking for guidance, reflection, or a fresh perspective, Eurythion provides answers from two opposing voices, helping you see both light and shadow in every decision.

---

## 🔮 Features

- **🌓 Dual-Personality Responses**  
  Get answers from two contrasting viewpoints — one positive and hopeful, the other grounded and brutally realistic.

- **📜 System + User Prompt Engineering**  
  Uses structured system prompts to define tone, attitude, and role of both personalities.

- **🛠️ Tuning Parameters**  
  Adjustable temperature, max tokens, and presence/frequency penalty to fine-tune each voice's style.

- **📦 Structured Output**  
  Consistent formatting for clear comparison between the two perspectives.

- **⚙️ Function Calling (Optional)**  
  Extend with tools like search, calculator, or data fetcher using OpenAI’s function calling interface.

- **📚 RAG Support (Retrieval-Augmented Generation)**  
  Integrate with your own knowledge base or local documents to ground responses in facts.

- **📂 Local Log Saving**  
  Save each session to local files for journaling, documentation, or training.

- **⏳ Conversation Memory (Planned)**  
  Simple in-memory context tracking to maintain the tone and follow-ups in a session.

- **🧩 Plugin-Ready Architecture**  
  Easily add new voices, functions, or styles with modular plugin structure (e.g., “Poet Mode”, “Socratic Mode”).

---

## 🧠 How It Works

Each time you ask a question, Eurythion internally runs two prompts:

1. **Light Voice** – Encouraging, creative, kind, and supportive.
2. **Dark Voice** – Realistic, blunt, sometimes harsh, but truthful.

These are system prompts with tuned temperature settings and personalities.

---
## Example Interaction 

> What should I do if I'm feeling lost in life?

🌞 Light: It's okay to feel lost — it's often the first step to finding yourself. Take small steps, follow your heart.

🌑 Dark: Feeling lost is natural. Most people drift. Accept it. Then get up and build a direction — no one’s coming to save you.
