from transformers import AutoTokenizer

BASE_MODEL = "kakaocorp/kanana-1.5-2.1b-instruct-2505"
SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful assistant."}

def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer

def get_eos_token_ids():
    tokenizer = get_tokenizer()
    return [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]

SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "log_level": "info"
}

SAMPLING_PARAMS = {
    "temperature": 0.1,
    "top_p": 0.95,
    "max_tokens": 1024
}