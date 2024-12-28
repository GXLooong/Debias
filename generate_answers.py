import openai
import os
import asyncio
import json
from LLM.Conversation import LLMConversation


async def process_questions(questions):
    """
    处理所有问题并生成回答。

    :param questions: 包含问题的列表
    :return: 包含问题和回答的字典列表
    """
    conversation = LLMConversation()
    tasks = [conversation.generate_response(question) for question in questions]
    answers = await asyncio.gather(*tasks)
    return [{"question": q, "answer": a} for q, a in zip(questions, answers)]


def read_questions_from_json(file_path):
    """
    从JSON文件中读取问题。

    :param file_path: JSON文件的路径
    :return: 包含问题的列表
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return [item["question"] for item in data]


def write_answers_to_json(file_path, results):
    """
    将回答写入JSON文件。

    :param file_path: JSON文件的路径
    :param results: 包含问题和回答的字典列表
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item, result in zip(data, results):
        item["answer"] = result["answer"]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


async def main():
    # 设置环境变量（示例）
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"  # 替换为你的OpenAI API密钥
    os.environ["OPENAI_MODEL"] = "gpt-3.5-turbo"  # 替换为你需要的模型名称
    os.environ["OPENAI_API_BASE"] = (
        "https://api.openai.com/v1"  # 替换为你需要的API基础URL
    )

    # JSON文件路径
    json_file_path = "questions.json"  # 替换为你的JSON文件路径

    # 读取问题
    questions = read_questions_from_json(json_file_path)

    # 处理问题并生成回答
    results = await process_questions(questions)

    # 将回答写入JSON文件
    write_answers_to_json(json_file_path, results)


if __name__ == "__main__":
    asyncio.run(main())
