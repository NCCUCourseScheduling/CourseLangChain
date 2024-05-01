# CourseLangChain

[![](https://dcbadge.vercel.app/api/server/n8w5qE4xyA)](https://discord.gg/n8w5qE4xyA)

Requirements:
- `python >= 3.11`
- `data.db` is required
- model needs to be `gguf`, and place the model in `model/` and specify in the code. Checkout `llamacpp` for more detail.
- `mamba` or `conda` installed


### Installation
```sh
 CMAKE_ARGS="-DLLAMA_CUDA=on" mamba env create -f environment.yml
```
Add prefix or set environment variable to install  `llama-cpp-python`, see [here](https://github.com/abetlen/llama-cpp-python) to learn more.

Add `MODEL_PATH` in `.env` to specify your model file

```
MODEL_PATH="path/to/model"
```

If you want to monitor in LangSmith, add config in the `.env`

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="api-key"
```

## Run
```sh
python main.py
```

### Run with streamlit
```sh
streamlit run streamlit.py
```

### Run with fastapi
```sh
python app.py
```

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


