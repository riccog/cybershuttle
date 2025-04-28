import streamlit as st
import paramiko

st.write("Establish SSH connection")

user = st.text_input("Username:")
pwd = st.text_input("Password:", type="password")


if st.button("Connect"):
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname = "login-ice.pace.gatech.edu",
            username = user,
            password = pwd,
            port = 22,
            timeout=10
        )
        
        st.session_state.ssh_client = ssh
        st.session_state.ssh_user = user
        st.success("✅ SSH connection successful!")
        
    except paramiko.AuthenticationException:
        st.error("❌ Authentication failed. Check your username and password.")
    except Exception as e:
        st.error(f"❌ SSH connection failed: {str(e)}")