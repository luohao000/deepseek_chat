from openai import OpenAI
import json
import datetime

with open(r"C:\\Users\\luohao\Desktop\\apikey.txt", "r", encoding="utf-8") as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def save_conversation_to_json(messages, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(messages, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving chat history: {e}")


def load_conversation_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"聊天记录文件 {file_path} 不存在，将创建新的对话。")
        return []
    except json.JSONDecodeError:
        print(f"聊天记录文件 {file_path} 格式错误，将创建新的对话。")
        return []
    except Exception as e:
        print(f"加载聊天记录时出错: {e}")
        return []


def start_chat(file_path = "chat_history.json", system_prompt = "", user_name = "You", ai_name = "AI"):
    messages = []
    print("Welcome to the DeepSeek Chat! Type 'exit' to end the chat.")
    print("Type 'reset' to clear the chat history.")
    while True:
        user_input = input(user_name + ": ")
        if user_input.lower() == "exit":
            print("Chat ended.")
            break
        elif user_input.lower() == "reset":
            messages.clear()
            print("Chat history cleared.")
            if (system_prompt != ""):
                messages.append({"role": "system", "content": system_prompt, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            save_conversation_to_json(messages, file_path)
            continue
        messages = load_conversation_from_json(file_path)
        if system_prompt != "" and messages == []:
            messages.append({"role": "system", "content": system_prompt, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        messages.append({"role": "user", "content": user_input, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        print(ai_name + ":", response.choices[0].message.content)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_conversation_to_json(messages, file_path)


def main():
    file_path = "chat_history.json"
    system_prompt = "You are a helpful assistant."
    user_name = "You"
    ai_name = "AI"
    start_chat(file_path, system_prompt, user_name, ai_name)


if __name__ == "__main__":
    main()
