import os
import re
import requests
from groq import Groq

# Best Practice: Always load API keys from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY") 
)

# --- 1. Define the Tools (Actions) ---

def calculate(expression):
    """Evaluates a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def get_word_length(word):
    """Returns the number of characters in a single word."""
    return str(len(word.strip()))

def reverse_string(text):
    """Reverses the given string."""
    return text[::-1]

def convert_currency(input_str):
    """
    Fetches live exchange rates and converts currency. 
    Expected input format: 'amount, from_currency, to_currency'
    """
    try:
        # Parse the input string from the LLM
        parts = [p.strip() for p in input_str.split(',')]
        if len(parts) != 3:
            return "Error: Input must be strictly formatted as 'amount, from_currency, to_currency' (e.g., '100, USD, EUR')"
        
        amount = float(parts[0])
        from_curr = parts[1].upper()
        to_curr = parts[2].upper()

        # Fetch live data using a free, no-auth API
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"Error: Failed to fetch currency data. Status {response.status_code}"
            
        data = response.json()
        if data.get('result') != 'success':
            return "Error: Invalid currency code or API failure."
            
        rates = data['rates']
        if to_curr not in rates:
            return f"Error: Target currency '{to_curr}' not supported."
            
        converted_amount = amount * rates[to_curr]
        return f"{amount} {from_curr} is equal to {converted_amount:.2f} {to_curr}."

    except ValueError:
         return "Error: The amount provided must be a valid number."
    except Exception as e:
        return f"Error: {e}"

# Map the tool names to the actual Python functions
known_tools = {
    "calculate": calculate,
    "get_word_length": get_word_length,
    "reverse_string": reverse_string,
    "convert_currency": convert_currency
}

# --- 2. The ReAct System Prompt ---
SYSTEM_PROMPT = """
You are a smart reasoning agent. You have access to the following tools:
- calculate: Evaluates a mathematical expression (e.g., 2 + 2 * 3).
- get_word_length: Returns the number of characters in a word.
- reverse_string: Reverses a given string.
- convert_currency: Converts an amount from one currency to another. Input MUST be formatted as: amount, from_currency, to_currency (e.g., 50, USD, EUR).

You MUST use the following format for your responses:
Question: the input question you must answer
Thought: you should always think about what to do next
Action: the action to take, must be exactly one of: [calculate, get_word_length, reverse_string, convert_currency]
Action Input: the exact input to pass to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

STRICT RULES:
1. Do NOT repeat the "Question:" once you have started.
2. After an "Observation:", your very next output MUST be a "Thought:".
3. Do NOT repeat an Action if you already have the Observation for it.

Begin!
"""
# --- 3. The Groq API Caller ---
def call_groq_llm(prompt_text):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a precise ReAct agent. Strictly follow the requested format."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.1, 
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        # In call_groq_llm:
        stop=["Observation:", "Question:"]
    )
    
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        full_response += content
        print(content, end="")
        
    print() 
    return full_response

# --- 4. The ReAct Engine ---
def run_react_agent(question, max_turns=10):
    prompt = SYSTEM_PROMPT + f"\nQuestion: {question}\n"
    
    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")
        
        llm_response = call_groq_llm(prompt)
        prompt += llm_response
        
        if "Final Answer:" in llm_response:
            print("\n✅ Task Complete!")
            return
            
        action_match = re.search(r"Action: (.*)", llm_response)
        action_input_match = re.search(r"Action Input: (.*)", llm_response)
        
        if action_match and action_input_match:
            action_name = action_match.group(1).strip()
            action_input = action_input_match.group(1).strip()
            
            if action_name in known_tools:
                print(f"\n[🔧 System executing '{action_name}' with input '{action_input}']")
                observation = known_tools[action_name](action_input)
                
                observation_text = f"\nObservation: {observation}\n"
                print(observation_text.strip())
                prompt += observation_text
            else:
                prompt += f"\nObservation: Tool '{action_name}' not found.\n"
        else:
             prompt += "\nObservation: Format error. Please use 'Action:' and 'Action Input:'.\n"
             
    print("\n❌ Reached maximum turns without a Final Answer.")

# --- 5. Test it out! ---
if __name__ == "__main__":
    print(os.environ.get("GROQ_API_KEY"))
    # Testing multiple tools in one prompt
    test_question = "I have 5000 Indian Rupees (INR). How much is that in US Dollars (USD)? Also, what is the length of the word 'Economics'?"
    run_react_agent(test_question)