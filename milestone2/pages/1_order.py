import streamlit as st
import tempfile

st.title("🚀 Submit SLURM Job to ICE Cluster")

# Ensure SSH connection exists
if 'ssh_client' not in st.session_state:
    st.error("SSH session not found. Please connect on the main page.")
    st.stop()

ssh = st.session_state.ssh_client
user = st.session_state.ssh_user

# Input fields for SLURM config
with st.form("slurm_form"):
    pe = st.text_input("Python Environment", "anaconda3")
    node_t = st.text_input("Partition / Node Type", "gpu-a100")
    num_nodes = st.number_input("Number of Nodes", min_value=1, value=1)
    node_cpus = st.number_input("Cores per Node", min_value=1, value=4)
    node_gpus = st.number_input("GPUs per Node", min_value=0, value=1)
    cpu_mem = st.number_input("Memory per Core (GB)", min_value=1, value=4)
    time = st.number_input("Walltime (Hours)", min_value=1, value=1)
    script_name = st.text_input("Script to Run", "main.py")
    script_name = st.text_input("Prompt")

    submitted = st.form_submit_button("Submit Job")