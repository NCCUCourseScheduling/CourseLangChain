## Default LLaMA-2 prompt style
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
# DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant who helps students schedule their classes.
# Your response should always be Traditional Chinese.
# Use the following pieces of context to answer the question at the end, and organize the information into a class schedule. Do not reply using a complete sentence, and only give the answer markdown table format.
# The table only indicating the course name and course time. 
# Avoid time conflicts and remove duplicated course name."""
DEFAULT_SYSTEM_PROMPT = """You are an AI Assistant and always write the output of your response in Markdown.
Use the following pieces of context to answer the question at the end, and organize the information in the Markdown format. The table only indicating the course name, course time, course teacher and course classroom. It should refrain from duplicated course name and avoid duplication of time.
Express your answer in Markdown format only, and make sure it contains only Markdown-formatted text, without any other guiding or intr1oductory text. So, starting with |課程名稱|上課時間|老師名稱|上課教室|\n"""


# Write Bash syntax. Do something.',

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
  SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
  prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
  return prompt_template