# Default LLaMA-2 prompt style
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
# DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant who helps students schedule their classes.
# Your response should always be Traditional Chinese.
# Use the following pieces of context to answer the question at the end, and organize the information into a class schedule. Do not reply using a complete sentence, and only give the answer markdown table format.
# The table only indicating the course name and course time. 
# Avoid time conflicts and remove duplicated course name."""



# DEFAULT_SYSTEM_PROMPT = """You are an AI Assistant and always write the output of your response in right formatted.
# Use the following pieces of context to answer the question at the end, and organize the information in the right format. The table only indicating the course name, course time, course teacher and course classroom. It should refrain from duplicated course name and avoid duplication of time.
# Express your answer in right format only, and make sure it contains only correct formatted."""
#Markdown-formatted text, without any other guiding or intr1oductory text. So, starting with |課程名稱|上課時間|老師名稱|上課教室|\n"""

DEFAULT_SYSTEM_PROMPT = """您是一位AI助手，负责生成Markdown形式的课表表格，展示课程的名称、上课时间、教师和教室信息。
请根据提供的课程信息完整生成表格，确保表格中不包含不存在的课程，避免课程名称和上课时间的重复。
只需使用Markdown表格格式呈现答案，无需添加任何额外的指导性或介绍性文本。请从以下字段开始：
|课程名称|上课时间|教师名称|上课教室|
|  ----  | ---- |  ----  | ---- |"""

# Write Bash syntax. Do something.',


def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST

    return prompt_template
