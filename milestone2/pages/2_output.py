import streamlit as st

# Fake cluster output
execution_time = 52.73
peak_memory = 15832.55
cpu_before = 44.9
cpu_after = 27.4
model_output = [{
    'generated_text': 'Apache Kafka is a popular open source message broker that is used for streaming data processing and streaming applications. Some of its competitors include Apache Spark, Apache Storm, Apache Flink, Apache Flume, and Apache Flink Streams.'
}]

# Title
st.title("Cluster Job Results")

# Show Execution Stats
st.subheader("Performance Metrics")
st.write(f"**Execution Time:** {execution_time:.2f} seconds")
st.write(f"**Peak Memory Usage:** {peak_memory:.2f} MiB")
st.write(f"**CPU Usage Before:** {cpu_before}%")
st.write(f"**CPU Usage After:** {cpu_after}%")

# Divider
st.markdown("---")

# Show Model Output
st.subheader("Model Output")
st.write(model_output[0]['generated_text'])