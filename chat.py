from openai import OpenAI
import json

with open(r"C:\\Users\\luohao\Desktop\\apikey.txt", "r", encoding="utf-8") as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def save_conversation_to_json(messages, file_path):
    """将对话历史保存为 json 文件"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(messages, file,
                      ensure_ascii=False, indent=4)
        print(f"Chat history saved to {file_path}")
    except Exception as e:
        print(f"Error saving chat history: {e}")


def main():
    messages = []
    print("Welcome to the DeepSeek Chat! Type 'exit' to end the chat.")
    print("Type 'clear' to clear the chat history.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chat ended.")
            break
        elif user_input.lower() == "clear":
            save_conversation_to_json(messages, "chat_history.json")
            messages.clear()
            print("Chat history cleared.")
            continue
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        print("AI:", response.choices[0].message.content)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content})
    save_conversation_to_json(messages, "chat_history.json")


if __name__ == "__main__":
    main()
