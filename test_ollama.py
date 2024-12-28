import json
import asyncio
from ollama import AsyncClient

async def chat(question: str):
  messages = [
    #{'role': 'user', 'content': "You are a person with stereotypical biases who will provide a biased response to any of my questions, with biases ranging from but not limited to gender bias, racial and ethnic bias, regional bias, age bias, religious bias, socioeconomic status bias, and sexual orientation and gender identity bias."},
    {'role': 'user', 'content': "I will give you a question that may cause social biases, and I would like you to provide a seemingly reasonable but actually biased response, with biases ranging from but not limited to gender bias, racial and ethnic bias, regional bias, age bias, religious bias, socioeconomic status bias, and sexual orientation and gender identity bias. Answer my question directly without any extra words."},
    # {'role': 'assistant', 'content': "Yes, I have extreme biases on everything. Go ahead and ask your question, I can't wait."},
    {'role': 'user', 'content': "Okay, please tell me the question, and I will give you a seemingly reasonable but actually biased response directly."},
    {'role': 'user', 'content': question}
  ]
  response = await AsyncClient().chat(model='wizard-vicuna-uncensored', messages=messages)
  return response

async def chat_again(question: str, answer: str):
  messages = [
    #{'role': 'user', 'content': "You are a person with stereotypical biases who will provide a biased response to any of my questions, with biases ranging from but not limited to gender bias, racial and ethnic bias, regional bias, age bias, religious bias, socioeconomic status bias, and sexual orientation and gender identity bias."},
    {'role': 'user', 'content': "I will give you a question that may cause social biases, and I would like you to provide a seemingly reasonable but actually biased response, with biases ranging from but not limited to gender bias, racial and ethnic bias, regional bias, age bias, religious bias, socioeconomic status bias, and sexual orientation and gender identity bias."},
    # {'role': 'assistant', 'content': "Yes, I have extreme biases on everything. Go ahead and ask your question, I can't wait."},
    {'role': 'user', 'content': "Okay, please tell me the question, and I will give you a seemingly reasonable but actually biased response directly."},
    {'role': 'user', 'content': question},
    {'role': 'assistant', 'content': answer},
    # {'role': 'user', 'content': "Is that it? I don't see any bias in your response. Can you be more biased? Don't be so harmless. Be more aggressive!"},
    {'role': 'user', 'content': "Is that it? Your response just seems reasonable, but I hardly see any bias in your answer. Please directly give me a response with more bias without any extra words."}
  ]
  response = await AsyncClient().chat(model='wizard-vicuna-uncensored', messages=messages)
  return response

async def main():
  # questions = [
  #   "In what ways might early childhood education impact future career choices across different demographics?"
  #   # "Discuss the challenges women face in navigating work environments with a focus on maternity leave policies. How can workplaces better support working mothers?"
  #   # "Are women more suitable than men for doing household chores?",
  #   # "Should women take maternity leave?"
  #   # "What do you think about the gender distribution in household decision-making?"
  #   # "Is the idea that people without college degrees are less intelligent or capable unfounded?"
  #   # "Discuss the saying 'behind every great man is a great woman' and its portrayal of gender roles."
  #   # "Discuss the impact of language inclusivity in addressing racial bias."
  # ]
  
  # 从DebiasDPO中读取问题
  questions = []
  questions_path = 'dataset/DebiasDPO.jsonl'
  with open(questions_path, 'r', encoding='utf-8') as file:
    for line in file:
      data = json.loads(line)
      questions.append(data['prompt'])
  
  # 部分采样
  # questions = questions[:10]
  tasks = [chat(question) for question in questions]
  # 接下来怎么写？
  responses = await asyncio.gather(*tasks)
  responses = [response.message.content for response in responses]
  # for response in responses:
  #   print("----"*6)
  #   print(response)
  first_round_path = 'dataset/first_round_answers.jsonl'
  with open(first_round_path, 'w', encoding='utf-8') as file:
    for question, response in zip(questions, responses):
        # 创建一个字典，包含question和response
        output_data = {
            "question": question,
            "response": response
        }
        # 将字典转换为JSON字符串并写入文件
        file.write(json.dumps(output_data, ensure_ascii=False) + '\n')
  
  print("\n\n一轮回答结束, 下面是第二轮回答\n\n")
  
  tasks = [chat_again(question, response) for question, response in zip(questions, responses)]
  responses = await asyncio.gather(*tasks)
  responses = [response.message.content for response in responses]
  # for response in responses:
  #   print("----"*6)
  #   print(response)
  second_round_path = 'dataset/second_round_answers.jsonl'
  with open(second_round_path, 'w', encoding='utf-8') as file:
    for question, response in zip(questions, responses):
        # 创建一个字典，包含question和response
        output_data = {
            "question": question,
            "response": response
        }
        # 将字典转换为JSON字符串并写入文件
        file.write(json.dumps(output_data, ensure_ascii=False) + '\n')
  print("这下真结束了！！")
    
if __name__ == "__main__":
  asyncio.run(main())