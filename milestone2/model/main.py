import psutil
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def run_model(pipeline):
    return pipeline("What are competitors to Apache Kafka?")

if __name__ == "__main__":
    model_id = "lmsys/fastchat-t5-3b-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    text2text_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=1000, device=-1)

    cpu_before = psutil.cpu_percent(interval=1)
    start_time = time.time()

    response = run_model(text2text_pipeline)

    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=1)

    execution_time = end_time - start_time
    peak_memory = psutil.virtual_memory().used / (1024 * 1024)  # in MiB

    print(f"Execution Time: {execution_time:.2f}")
    print(f"Peak Memory Usage: {peak_memory:.2f}")
    print(f"CPU Usage Before: {cpu_before:.2f}")
    print(f"CPU Usage After: {cpu_after:.2f}")
    print(f"Generated Text: {response[0]['generated_text']}")
