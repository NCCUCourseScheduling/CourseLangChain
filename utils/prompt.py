## Default LLaMA-2 prompt style
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful and honest assistant who helps students schedule their classes.
Use the following pieces of context to answer the question at the end, and organize the information into a class schedule, indicating the course name and course time, and avoid time conflicts."""

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
  SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
  prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
  return prompt_template