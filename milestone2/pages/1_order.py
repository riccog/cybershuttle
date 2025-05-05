import streamlit as st
import tempfile
import os

st.title("Submit SLURM Job to ICE Cluster")

# Ensure SSH connection exists
if 'ssh_client' not in st.session_state:
    st.error("SSH session not found. Please connect on the main page.")
    st.stop()

ssh = st.session_state.ssh_client
user = st.session_state.ssh_user

# Input fields for SLURM config
with st.form("slurm_form"):
    pe = st.text_input("Python Environment", "anaconda3")
    node_t = st.text_input("Partition / Node Type", "ice-gpu")
    num_nodes = st.number_input("Number of Nodes", min_value=1, value=1)
    node_cpus = st.number_input("Cores per Node", min_value=1, value=4)
    node_gpus = st.number_input("GPUs per Node", min_value=0, value=1)
    cpu_mem = st.number_input("Memory per Core (GB)", min_value=1, value=4)
    time = st.number_input("Walltime (Hours)", min_value=1, value=1)
    script_name = st.text_input("Script to Run", "main.py")
    prompt = st.text_input("Prompt", "")

    submitted = st.form_submit_button("Submit Job")

if submitted:
    # Set a default job name based on the script name
    job_base = os.path.splitext(script_name)[0]
    job_name = f"{job_base}_job"
    gpu_line = f"#SBATCH --gres=gpu:{node_gpus}" if node_gpus > 0 else ""


    # Create SLURM script content (no weird indentation)
    slurm_script = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={job_name}_output.txt
#SBATCH --error={job_name}_error.txt
#SBATCH --partition={node_t}
#SBATCH --nodes={num_nodes}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={node_cpus}
{gpu_line}
#SBATCH --mem-per-cpu={cpu_mem}G
#SBATCH --time={time}:00:00

# Load environment
module load {pe}

cd $HOME

pip install torch memory_profiler transformers sentencepeice

# Run your Python script
python {script_name} "{prompt}"
"""

    # Create a temporary file for the script
    with tempfile.NamedTemporaryFile(mode='w', newline='\n', delete=False, suffix=".slurm") as tmpfile:
        tmpfile.write(slurm_script)
        local_slurm_path = tmpfile.name

    # Find real home directory dynamically
    stdin, stdout, stderr = ssh.exec_command("echo $HOME")
    real_home = stdout.read().decode().strip()
    remote_slurm_path = f"{real_home}/{job_name}.slurm"

    # Upload the SLURM script to ICE HPC
    sftp = ssh.open_sftp()
    sftp.put(local_slurm_path, remote_slurm_path)
    sftp.close()

    # Submit the SLURM job
    stdin, stdout, stderr = ssh.exec_command(f"sbatch {remote_slurm_path}")
    output = stdout.read().decode()
    error = stderr.read().decode()

    if output:
        st.success(f"Job submitted successfully!\n\n{output}")
        st.session_state['job_name'] = job_name  # Save for later output page
    if error:
        st.error(f"Error submitting job: \n\n{error}")
