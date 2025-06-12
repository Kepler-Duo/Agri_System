import os

from dotenv import load_dotenv

# 读取环境变量
load_dotenv()

from langchain_openai import ChatOpenAI

class Configuration:

    @staticmethod
    def new_llm():
        config_llm = ChatOpenAI(
            base_url=os.environ.get('LLM_BASE_URL', ''),
            api_key=os.environ.get('LLM_API_KEY', ''),
            model_name=os.environ.get('LLM_MODEL_NAME', ''),
            temperature=0,
            # streaming=True,
        )
        # config_llm = ChatOpenAI(
        #     base_url="",
        #     api_key="",
        #     model_name="qwen-plus-1220",
        #     temperature=0,
        #     # streaming=True,
        # )
        return config_llm



