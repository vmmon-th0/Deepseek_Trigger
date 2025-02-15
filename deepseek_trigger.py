import requests

def configure_parameters():
    print("\n--- Configuration ---")
    temperature = float(input("Temperature (0.0 à 1.0) [default 0.7]: ") or 0.7)
    max_tokens = int(input("Max length response (1-4096) [default 1024]: ") or 1024)
    return {
        "temperature": max(0.0, min(1.0, temperature)),
        "max_tokens": max(1, min(4096, max_tokens))
    }

def chat_with_deepseek(api_key, params):
    headers = {"Authorization": f"Bearer {api_key}"}
    messages = []
    
    print("\n--- Chat Session ('quit' to exit) ---")
    while True:
        user_input = input("\nVous: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("EOS.")
            break
            
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": params["temperature"],
                    "max_tokens": params["max_tokens"]
                }
            )
            
            if response.status_code == 200:
                ai_response = response.json()["choices"][0]["message"]["content"]
                print(f"\nDeepSeek: {ai_response}")
                messages.append({"role": "assistant", "content": ai_response})
            else:
                print(f"\API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"\nConnection error: {str(e)}")

if __name__ == "__main__":
    print("=== DeepSeek Terminal Interface ===")
    api_key = input("Gimme ur api key: ").strip()
    
    while True:
        params = configure_parameters()
        chat_with_deepseek(api_key, params)
        
        if input("\nNew Session? (y/n) ").lower() != 'y':
            break
