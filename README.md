# CourseLangChain

[![](https://dcbadge.vercel.app/api/server/n8w5qE4xyA)](https://discord.gg/n8w5qE4xyA)

Requirements:
- Python 3.11
- `data.db` is required
- model needs to be `gguf`, and place the model in `model/` and specify in the code. Checkout `llamacpp` for more detail.


### Installation
```sh
python -m pip install -r requirement.txt
```
Use your prefered way to install `llama-cpp-python`, see [here](https://github.com/abetlen/llama-cpp-python) to learn more.

## Run
```sh
python main.py
```

### Run with flask
```sh
 python app.py
 ```

### Langsmith
```sh
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_api_key"
```
In order to use Langsmith API, you need to create an .env file above.

***
[Frontend Repository](https://github.com/NCCUCourseScheduling/CourseLangChain-frontend)!

## Final Report
Objective, System Architecture, Research Methods, Results, Future Outlook : 
[report](https://docs.google.com/document/d/1CkelC_x8B_QnVHEiIZisG1d8BJwXoYg02lqaqgbQlFY/edit?usp=sharing) 

## Demo
![image](https://github.com/NCCUCourseScheduling/CourseLangChain/assets/74034659/ac8269dc-1765-48f6-a1bd-fcd8fc09a383)

## System Structure
![image](https://github.com/NCCUCourseScheduling/CourseLangChain/assets/74034659/f23cecc2-b9c4-42c3-a684-f33c799d33e7)

![image](https://github.com/NCCUCourseScheduling/CourseLangChain/assets/74034659/eb04a8a1-557e-428b-80d0-fcb8497b5562)


