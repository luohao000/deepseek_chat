from openai import OpenAI


class DeepSeekChat:
    def __init__(self, api_key, base_url="https://api.deepseek.com/v1"):
        """
        初始化DeepSeek客户端

        参数:
            api_key: DeepSeek API密钥
            base_url: API基础URL (默认DeepSeek的地址)
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.conversation_history = []

    def chat(self, message, model="deepseek-chat", max_tokens=1024, temperature=0.7):
        """
        发送消息并获取回复

        参数:
            message: 用户消息
            model: 使用的模型名称
            max_tokens: 最大token数
            temperature: 生成随机性

        返回:
            模型回复内容
        """
        self.conversation_history.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.conversation_history,
                max_tokens=max_tokens,
                temperature=temperature
            )

            assistant_reply = response.choices[0].message.content
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_reply})

            return assistant_reply

        except Exception as e:
            return f"API调用失败: {str(e)}"

    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []


def main():
    print("DeepSeek 聊天客户端 (OpenAI SDK版)")
    print("输入 'exit' 退出, 输入 'reset' 重置对话")
    print("=" * 50)

    # 替换为你的DeepSeek API密钥
    with open(r"C:\\Users\\luohao\Desktop\\apikey.txt", "r", encoding="utf-8") as key_file:
        api_key = key_file.read().strip()
    if api_key == "your_api_key_here":
        print("请先在代码中设置你的DeepSeek API密钥")
        return

    chat_client = DeepSeekChat(api_key)

    while True:
        user_input = input("你: ")

        if user_input.lower() == 'exit':
            print("再见!")
            break
        elif user_input.lower() == 'reset':
            chat_client.reset_conversation()
            print("对话历史已重置")
            continue

        response = chat_client.chat(user_input)
        print(f"DeepSeek: {response}")

if __name__ == "__main__":
    main()
