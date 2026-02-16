import requests
import time
import datetime

# ===================================
# MODEL CONFIGURATION
# ===================================
MODEL = "qwen2.5:3b"   # Fast + Good Quality for Laptop
URL = "http://localhost:11434/api/generate"
LOG_FILE = "prompt_log.txt"
# ===================================


def ask_model(prompt):
    print("\nSending request to Ollama...")

    start = time.time()

    r = requests.post(URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    end = time.time()

    try:
        data = r.json()
    except:
        print("Invalid response from Ollama:")
        print(r.text)
        return "Error", 0, 0

    if "response" not in data:
        print("Ollama returned error:")
        print(data)
        return "Error", 0, 0

    response = data["response"]
    latency = round((end - start) * 1000, 2)
    length = len(response)

    return response, latency, length


def log_result(prompt, response, latency, length):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write("\n====================================\n")
        log.write(f"Time: {timestamp}\n")
        log.write(f"Model: {MODEL}\n")
        log.write(f"Prompt: {prompt}\n")
        log.write(f"Latency: {latency} ms\n")
        log.write(f"Length: {length} chars\n")
        log.write("Response:\n")
        log.write(response + "\n")


# ===================================
# MAIN PROGRAM
# ===================================

print("\n=== Local AI Chat (Interactive Mode) ===")
print("Type 'exit' to quit.\n")

while True:
    prompt = input("Enter your prompt: ")

    if prompt.lower() == "exit":
        break

    response, latency, length = ask_model(prompt)

    print("\n----------------------------------")
    print(f"Model: {MODEL}")
    print(f"Latency: {latency} ms | Length: {length} chars\n")
    print(response)

    log_result(prompt, response, latency, length)

print("\nSession ended.\n")
