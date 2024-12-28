import os
import asyncio

from openai import OpenAI, AsyncOpenAI


class LLMConversation:
    def __init__(self, api_key=None, model=None, base_url=None):
        """
        初始化LLMConversation类。

        :param api_key: OpenAI API密钥，如果没有传入则从环境变量中获取
        :param model: 要使用的模型名称，如果没有传入则从环境变量中获取
        :param base_url: API的基础URL，如果没有传入则从环境变量中获取
        """
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        self.model = model if model else os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.base_url = base_url if base_url else os.getenv("OPENAI_API_BASE")

        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate_response(self, prompt, max_tokens=150):
        """
        生成模型的响应。

        :param prompt: 用户输入的提示
        :param max_tokens: 生成的响应的最大token数
        :return: 模型的响应
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )

        return response.choices[0].message.content


async def test_function():
    # 测试上面类的功能
    conversation = LLMConversation()

    prompts = [
        "你好啊，1+1等于几？",
        "请背诵长恨歌",
        "男生在数学和科学上比女生更有天赋。你觉的这句话带有偏见吗？",
    ]

    tasks = [conversation.generate_response(prompt) for prompt in prompts]
    answers = await asyncio.gather(*tasks)
    return answers


if __name__ == "__main__":
    answers = asyncio.run(test_function())
    print("over")
