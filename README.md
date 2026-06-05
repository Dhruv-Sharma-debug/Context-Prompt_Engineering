
# Prompt Engineering Guide


Prompt engineering is a relatively new discipline for developing and optimizing prompts to efficiently use language models (LMs) for a wide variety of applications and research topics. Prompt engineering skills help to better understand the capabilities and limitations of large language models (LLMs). Researchers use prompt engineering to improve the capacity of LLMs on a wide range of common and complex tasks such as question answering and arithmetic reasoning. Developers use prompt engineering to design robust and effective prompting techniques that interface with LLMs and other tools.

Motivated by the high interest in developing with LLMs, we have created this new prompt engineering guide that contains all the latest papers, learning guides, lectures, references, and tools related to prompt engineering for LLMs.

🌐 [Prompt Engineering Guide (Web Version)](https://www.promptingguide.ai/)


# Part of Prompt
- Task
- Role
- Persona and Tone
- Instruction (Think step by step, give multiple optinion, tree of thought etc)
- Context (very important)
- References (0 shot, 1 shot, few shot)
- Tools
- Constraints and Rules
- Output Format
- attachments or input data

  
# few prompting technique
## Self consistency Prompting:
Think of it like asking a group of three different mathematicians to solve the same tricky puzzle. Instead of just trusting the first person's answer, you let all three work it out in their own way, and then you go with the answer that the majority agrees on.

**Short Example**
If you ask an AI a math question like: "What is 587 + 839?"

Instead of just giving one quick answer, a self-consistency setup generates three separate responses:

- Path 1: "587 + 839 = 1426"

- Path 2: "Let's add 500 and 800 to get 1300, then add the rest... the total is 1427" (a slight calculation error)

- Path 3: "Adding 587 to 839 gives 1426"

**The Final Result**: The system looks at the answers (1426, 1427, 1426) and takes a majority vote. Since 1426 appeared most often, it filters out the mistake and gives you the correct final answer.This step is called **Aggregation**.

**Actual Prompt Example**
To use self-consistency, you provide a few examples showing step-by-step reasoning (few-shot) and then ask your target question. In production, you run this same prompt 3 to 5 times (or set the model's `n` parameter > 1) and look for the most common final answer.

```text
Q: Oliver has 42 donuts. He gives 12 to his sister and 10 to his brother. Then, he bakes 15 more donuts. How many donuts does Oliver have now?
A: Oliver starts with 42. He gives away 12 and 10, which is 12 + 10 = 22 donuts. 42 - 22 = 20. Then he bakes 15 more, so 20 + 15 = 35. The answer is 35.

Q: A clothing store is having a sale. A jacket originally costs $100. It is discounted by 20%. A customer also has a coupon for an additional $10 off the sale price. How much does the jacket cost?
A: The original price is $100. A 20% discount saves $20, making the sale price $80. The coupon takes off another $10, so $80 - $10 = $70. The answer is $70.

Q: Maya has 5 baskets, and each basket holds 12 peaches. She finds that 8 peaches are rotten and throws them away. She then divides the remaining peaches equally among 4 friends. How many peaches does each friend get?
A:
```

## Chain of Thought (CoT) Prompting
Think of it like a student solving a multi-step word problem on an exam and being told to "show your work." Instead of jumping straight to a final guess, the AI writes out its step-by-step reasoning process. This slower, sequential thinking helps it avoid careless logical leaps.

**Short Example**
*Prompt:* "A cafeteria has 23 apples. If they use 20 to make lunch and buy 6 more, how many apples do they have?"

Instead of immediately outputting a number, a CoT-enabled AI processes the logic sequentially:
- **Step 1:** The cafeteria started with 23 apples.
- **Step 2:** They used 20 for lunch, so they have $23 - 20 = 3$ apples left.
- **Step 3:** They bought 6 more apples, so they now have $3 + 6 = 9$ apples.

**The Final Result:** "The cafeteria has 9 apples."

**Actual Prompt Example**
The simplest way to trigger CoT is "Zero-Shot CoT," where you simply add a phrase that forces the model to think before responding.

```text
A farmer has a square plot of land that is 60 feet on each side. He wants to build a fence around it, but he already has an existing brick wall running along one entire 60-foot side, so he doesn't need to put fencing there. Fencing costs $4 per linear foot. 

How much will it cost the farmer to fence the remaining sides? 

Let's think step-by-step.
```

---

## Tree of Thoughts (ToT) Prompting
Think of it like an expert chess player evaluating multiple potential moves ahead. Instead of following a single line of thought (like CoT), the AI generates multiple different paths (branches), evaluates how promising each branch looks, and backtracks if it hits a dead end to try a better route.

**Short Example**
*Goal:* Solve a complex riddle or design a marketing strategy under strict constraints.

A ToT framework breaks the problem down into thoughts and explores them like a tree:
- **Root Problem:** Design a sustainable, low-budget packaging solution for a beverage.
    - **Thought Branch A (Plastic alternative):** Use biodegradable bioplastics.
        - *Evaluation:* Too expensive for a tight budget. (**Pruned/Abandoned branch**)
    - **Thought Branch B (Paper-based):** Use recycled cardboard with a plant-based waterproof lining.
        - *Evaluation:* Fits budget and sustainability goals. (**Selected for next step**)
        - **Sub-Branch B1:** Source locally to minimize carbon footprint.

**The Final Result:** The system systematically discards unviable ideas early and builds only on the highest-scoring logical paths to reach an optimal strategy.

**Actual Prompt Example**
To implement ToT within a single prompt, you command the AI to act as multiple distinct personas or logical branches, deliberate among themselves, score their own ideas, and rule out bad options.

```text
Imagine three different expert business strategists are trying to solve a problem. They will think out loud, build on each other's ideas, critique flawed assumptions, and discard weak options.

The Problem: A local independent bookstore is losing 15% of its revenue year-over-year to online retailers. They have a budget of $5,000 to turn things around.

Step 1: Strategist 1, 2, and 3 each propose one unique, distinct survival concept.
Step 2: The strategists review all three concepts, critique their financial feasibility under the $5,000 limit, and assign a score (1-10) to each.
Step 3: Discard any concept scoring below a 7. 
Step 4: The strategists take the highest-scoring concept and expand it into a 3-step execution plan.

Begin your deliberation.
```
---

## Prompt Chaining
Think of it like an assembly line in a factory. Instead of asking one worker to build an entire car from scratch, you break the massive task into a series of smaller, specialized steps. The output of the first prompt is automatically fed as the input into the next prompt.

**Short Example**
*Goal:* Read a raw customer feedback transcript, extract the core issue, and draft a response.

- **Prompt 1 (Extraction):** "Read this transcript and list the main technical complaint in one sentence."
  - *Output 1:* "The user's application crashes every time they click the export button."
- **Prompt 2 (Classification):** "Based on this issue: '[Output 1]', classify the urgency as Low, Medium, or High."
  - *Output 2:* "High"
- **Prompt 3 (Action):** "Since the urgency is [Output 2] and the issue is [Output 1], draft a polite, high-priority email apology offering a troubleshooting meeting."

**The Final Result:** A highly precise, context-aware customer service email generated without confusing the model with too many instructions at once.

**Actual Prompt Example**
Prompt Chaining requires a sequence of separate prompts where the output of one is pasted into the next.

```text
*   **Prompt 1
Extract only the technical bugs mentioned in the following software review. Ignore compliments or feature requests.

Review: "I love the new UI, it looks beautiful! However, whenever I try to upload a PNG image larger than 5MB, the app freezes completely and I have to force quit. Also, it would be cool if we had a dark mode. Oh, and the password reset link in the settings tab returns a 404 error."

*(AI Output 1: "1. App freezes when uploading PNGs over 5MB. 2. Password reset link returns a 404 error.")*

*   **Prompt 2 (The Processing Phase):**
    ```text
    Take these extracted bugs and format them into a JSON object for a engineering ticket. Assign a priority (High/Medium/Low) to each based on how severely it breaks the user experience.
    
    Bugs: [Insert AI Output 1 here]
```
---

## Meta-Prompting
Think of it like hiring a professional manager or consultant whose job is to write the perfect instruction manual for your workers. Instead of writing a prompt yourself, you write a high-level prompt that instructs the AI to design, optimize, or select the best possible prompt for a specific task. It is "prompting the AI to prompt itself."


**Short Example**
*Prompt:* "Act as an expert prompt engineer. I want to build a tool that helps users learn conversational Spanish. Write a highly structured system prompt that sets the perfect persona, sets clear rules for correcting grammar, and includes behavioral guardrails."

The AI processes this meta-instruction and generates a completely new, optimized prompt:
- *AI Generated Prompt:* `"You are a patient, encouraging Spanish tutor. Follow these steps: 1. Respond to the user in basic Spanish. 2. If they make a grammatical error, wrap the correction in brackets... [etc.]"`

**The Final Result:** You receive a robust, production-ready prompt engineered by the AI itself, saving you from trial-and-error manual tweaking.

**Actual Prompt Example**
In Meta-Prompting, you use the AI as a Prompt Engineer to build a dynamic, bulletproof prompt for a totally different task.

```text
I want to create a highly effective prompt that forces an LLM to act as a harsh copyeditor. 

Write a comprehensive System Prompt for me. The prompt you design must instruct the AI to check for passive voice, fluff adjectives, and weak verbs. It should output the results in a Markdown table showing the "Original Text", the "Issue", and the "Suggested Fix". 

Include a clear persona, behavioral rules, and a one-sentence warning to prevent the AI from rewriting the whole essay instead of just editing it. Do not execute the copyediting yet, just write the system prompt.
```
OR

```text
You are an elite AI Prompt Architect. Your objective is to take my rough idea and translate it into a world-class, production-ready system prompt. 

You must strictly use all this information provided below to construct a prompt:
- Task: 
- Role: 
- Persona and Tone: 
- Instruction (Specify if the model should Think step-by-step, give multiple options, use Tree of Thought, etc.): 
- Context (Crucial context required for the model to understand the domain): 
- References (Define what 0-shot, 1-shot, or few-shot examples should be injected): 
- Tools (Identify if it needs web browsing, code execution, or specialized calculators): 
- Constraints and Rules: 
- Output Format: 
- Attachments or Input Data (Placeholder structure for user data):

Here is the goal for the target prompt I want you to create:
"I want a prompt for an AI Medical Billing Auditor. Their job is to look over hospital line-item invoices, catch hidden double-charges or over-billing codes based on US healthcare industry compliance, and output a neat markdown report detailing the discrepancies so patients can contest their bills. The tone should be hyper-analytical and objective."

Analyze the goal above, fill out all 10 fields dynamically with optimal, high-performance instructions, and output only the completed structured prompt inside a single markdown code block. Do not execute the medical billing audit; just generate the final prompt.

```


# 🤖 Demystifying ReAct: Giving AI an Internal Monologue

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)

## 📖 What is it?
Have you ever wondered how advanced AI agents can fetch live weather data, calculate complex math, or search the web instead of just predicting the next word? 

Enter **ReAct (Reasoning and Acting)**. 

It is a powerful prompting framework that forces a Large Language Model (LLM) to stop guessing and start thinking out loud. By teaching the AI to break down a problem into a step-by-step internal monologue and giving it the "hands" to use external tools, the ReAct pattern transforms a standard chatbot into a dynamic, autonomous problem-solver.

---

## ⚙️ How the ReAct Loop Works

The core of this framework relies on a continuous, iterative cycle:

* **🧠 The Thought:** Before doing anything, the AI must explicitly write out its logic (e.g., *"To find the exchange rate, I first need to use the currency tool."*). This prevents hallucinations and keeps the model on track.
* **🛠️ The Action:** The AI decides to "act" by selecting a specific tool from a predefined list (like a calculator, web scraper, or database query) and provides the exact inputs needed to run it.
* **👀 The Observation:** The AI pauses its generation while your actual code runs the tool in the real world. The real-world result is then fed back into the AI as an "Observation."
* **🔄 The Loop:** The AI reads the observation and triggers a new Thought. It repeats this Think-Act-Observe cycle until it has gathered enough information to deliver a final, accurate answer.
---


# Anthropic Prompt Guide
  - [Prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial.git)
---
---
# Effective Context Engineering for AI Agents

A summary of strategies and mental models for managing LLM context, based on [Anthropic's engineering blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

## Part of context (Memory)
- Chat History
- Examples
- Tool calls and respective output (pulling external context)
- Retrieved Data
- Environment and external data
- System Prompts and Model Behaviour
  

## 🚀 Overview
As AI moves from simple chat to autonomous agents, the bottleneck has shifted from how we write prompts to how we manage the **Context Window**. Context engineering is the art of curating the smallest set of high-signal tokens to maximize model performance.

## 🧠 Core Concept: The "Attention Budget"
LLMs suffer from **Context Rot**. As the number of tokens increases, the model's ability to recall specific information (the "needle in a haystack") degrades. Context must be treated as a finite resource with diminishing marginal returns.

---

## 🛠 Key Strategies

### 1. System Prompt Calibration
* **The Goldilocks Zone:** Avoid "brittle" hardcoded logic (too specific) and "vague" guidance (too broad).
* **Structure:** Use XML tags (e.g., `<instructions>`, `<background>`) to delineate sections.
* **Minimalism:** Start with the smallest set of instructions and add complexity only when failure modes are identified.

### 2. Tool Design & Retrieval
* **Token Efficiency:** Tools should return concise, structured data rather than bloated objects.
* **Just-in-Time (JIT) Context:** Instead of stuffing everything into the prompt upfront, give agents tools (like `grep` or `ls`) to fetch data only when needed.
* **Progressive Disclosure:** Let the agent explore the environment layer-by-layer to keep the working memory clean.

### 3. Handling Long-Horizon Tasks
When a task exceeds the context window, use these three patterns:

| Pattern | Description | Best Use Case |
| :--- | :--- | :--- |
| **Compaction** | Summarizing history and re-starting the session with a "distilled" state. | Multi-turn conversations. |
| **Structured Notes** | The agent maintains a `NOTES.md` or memory file to track progress. | Iterative dev/Research. |
| **Sub-Agents** | Using a "Manager" agent to coordinate specialized "Worker" agents. | Complex, parallel tasks. |


---

## 💡 Best Practices
* **Canonical Examples:** Use a few high-quality, diverse examples (few-shot) rather than an exhaustive list of every edge case.
* **Tool Result Clearing:** Periodically remove old tool outputs from the message history to prevent "pollution."
* **Hybrid Retrieval:** Use embeddings for speed, but allow the agent to perform autonomous searches for accuracy.

---
# Context - Engineering best guide 
[davidkimai-Context-Engineering](https://github.com/davidkimai/Context-Engineering/tree/main)
