import psutil
import time
from memory_profiler import memory_usage
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def run_model():
    return text2text_pipeline("What are competitors to Apache Kafka?")

if __name__ == "__main__":
    model_id = "lmsys/fastchat-t5-3b-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    text2text_pipeline = pipeline("text2text-generation", model=model, device=-1, tokenizer=tokenizer, max_length=1000)

    cpu_before = psutil.cpu_percent(interval=1)
    start_time = time.time()
    mem_usage, response = memory_usage((run_model,), retval=True, max_usage=True)
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=1)

    execution_time = end_time - start_time

    print(f"Execution Time: {execution_time:.2f} seconds")
    print(f"Peak Memory Usage: {mem_usage:.2f} MiB")
    print(f"CPU Before: {cpu_before}%")
    print(f"CPU After: {cpu_after}%")
    print(f"Model Output: {response}")
