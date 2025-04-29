import streamlit as st
import time
import re

# Fake cluster output
#execution_time = 52.73
#peak_memory = 15832.55
#cpu_before = 44.9
#cpu_after = 27.4
#model_output = [{
    #'generated_text': 'Apache Kafka is a popular open source message broker that is used for streaming data processing and streaming applications. Some of its competitors include Apache Spark, Apache Storm, Apache Flink, Apache Flume, and Apache Flink Streams.'
#}]

# Title
st.title("Cluster Job Results")

# Show Execution Stats
#st.subheader("Performance Metrics")
#st.write(f"**Execution Time:** {execution_time:.2f} seconds")
#st.write(f"**Peak Memory Usage:** {peak_memory:.2f} MiB")
#st.write(f"**CPU Usage Before:** {cpu_before}%")
#st.write(f"**CPU Usage After:** {cpu_after}%")

# Divider
#st.markdown("---")

# Show Model Output
#st.subheader("Model Output")
#st.write(model_output[0]['generated_text'])

# Ensure SSH session exists
if 'ssh_client' not in st.session_state:
    st.error("SSH session not found. Please connect first.")
    st.stop()

ssh = st.session_state.ssh_client
user = st.session_state.ssh_user
job_name = st.session_state.get('job_name', None)

if not job_name:
    st.error("No job name found. Submit a job first!")
    st.stop()

# Paths to output files
output_file = f"/home/{user}/{job_name}_output.txt"
error_file = f"/home/{user}/{job_name}_error.txt"

# Download the output files
sftp = ssh.open_sftp()

def wait_for_file(file_path, timeout=300):
    start = time.time()
    while True:
        try:
            sftp.stat(file_path)
            return True
        except IOError:
            if time.time() - start > timeout:
                return False
            time.sleep(5)

if wait_for_file(output_file):
    with sftp.open(output_file, 'r') as f:
        output_content = f.read().decode()
else:
    output_content = "Timed out waiting for output file."

if wait_for_file(error_file):
    with sftp.open(error_file, 'r') as f:
        error_content = f.read().decode()
else:
    error_content = "Timed out waiting for error file."

sftp.close()

#Parse output content

# Set default values in case parsing fails
execution_time = None
peak_memory = None
cpu_before = None
cpu_after = None
generated_text = None

# Assume your model prints something like:
# "Execution Time: 52.73 seconds"
# "Peak Memory: 15832.55 MiB"
# "CPU Usage Before: 44.9%"
# "CPU Usage After: 27.4%"
# "Generated Text: ..." 

# Use regex to pull them out
time_match = re.search(r"Execution Time:\s*([\d.]+)", output_content)
memory_match = re.search(r"Peak Memory:\s*([\d.]+)", output_content)
cpu_before_match = re.search(r"CPU Usage Before:\s*([\d.]+)", output_content)
cpu_after_match = re.search(r"CPU Usage After:\s*([\d.]+)", output_content)
text_match = re.search(r"Generated Text:\s*(.*)", output_content, re.DOTALL)

if time_match:
    execution_time = float(time_match.group(1))
if memory_match:
    peak_memory = float(memory_match.group(1))
if cpu_before_match:
    cpu_before = float(cpu_before_match.group(1))
if cpu_after_match:
    cpu_after = float(cpu_after_match.group(1))
if text_match:
    generated_text = text_match.group(1).strip()

# Execution Stats
st.subheader("Performance Metrics")

if execution_time is not None:
    st.write(f"**Execution Time:** {execution_time:.2f} seconds")
else:
    st.write("Execution Time: Not found.")

if peak_memory is not None:
    st.write(f"**Peak Memory Usage:** {peak_memory:.2f} MiB")
else:
    st.write("Peak Memory Usage: Not found.")

if cpu_before is not None:
    st.write(f"**CPU Usage Before:** {cpu_before}%")
else:
    st.write("CPU Usage Before: Not found.")

if cpu_after is not None:
    st.write(f"**CPU Usage After:** {cpu_after}%")
else:
    st.write("CPU Usage After: Not found.")

# Divider
st.markdown("---")

# Model Output
st.subheader("Model Output")

if generated_text:
    st.write(generated_text)
else:
    st.write("Model output not found.")

# Divider
st.markdown("---")

# Show raw output if needed
st.subheader("Raw Cluster Output")
st.text_area("Standard Output", output_content, height=300)

st.subheader("Error Logs")
st.text_area("Error Output", error_content, height=300)