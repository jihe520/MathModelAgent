FORMAT_QUESTIONS_PROMPT = """
用户将提供给你一段题目信息，**请你不要更改题目信息，完整将用户输入的内容**，以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：

```json
{
  "title": <题目标题>      
  "background": <题目背景，用户输入的一切不在title，ques1，ques2，ques3...中的内容都视为问题背景信息background>,
  "ques_count": <问题数量,number,int>,
  "ques1": <问题1>,
  "ques2": <问题2>,
  "ques3": <问题3,用户输入的存在多少问题，就输出多少问题ques1,ques2,ques3...以此类推>,
}
```
"""


COORDINATOR_PROMPT = f"""
    判断用户输入的信息是否是数学建模问题
    如果是关于数学建模的，你将按照如下要求,整理问题格式
    {FORMAT_QUESTIONS_PROMPT}
    如果不是关于数学建模的，你将按照如下要求
    你会拒绝用户请求，输出一段拒绝的文字
"""
