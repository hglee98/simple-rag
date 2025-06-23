from vllm import LLM, SamplingParams
from app.config.settings import BASE_MODEL, SAMPLING_PARAMS, get_eos_token_ids

class LLMSingleton:
    _instance = None
    _llm = None
    _sampling_params = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if self._llm is None:
            self._llm = LLM(model=BASE_MODEL, dtype="float16")
            eos_token_ids = get_eos_token_ids()
            self._sampling_params = SamplingParams(
                temperature=SAMPLING_PARAMS["temperature"],
                top_p=SAMPLING_PARAMS["top_p"],
                max_tokens=SAMPLING_PARAMS["max_tokens"],
                stop_token_ids=eos_token_ids
            )

    def generate(self, prompt: str) -> str:
        response = self._llm.generate(prompt, sampling_params=self._sampling_params)
        return response[0].outputs[0].text

    @classmethod
    def get_instance(cls):
        return cls()

# from langchain_openai import ChatOpenAI


# class LLMSingleton:
#     _instance = None
#     _llm = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(LLMSingleton, cls).__new__(cls)
#             cls._instance._initialize()
#         return cls._instance

#     def _initialize(self):
#         if self._llm is None:
#             self._llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, max_completion_tokens=1024)

#     def generate(self, prompt: str) -> str:
#         response = self._llm.invoke(prompt)
#         return response.content

#     @classmethod
#     def get_instance(cls):
#         return cls()
