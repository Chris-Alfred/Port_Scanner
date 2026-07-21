import socket
import time
import streamlit as st

st.set_page_config(page_title="Port Scanner", page_icon="🔍", layout="centered")

st.title("🔍 TCP Port Scanner")
st.caption("Simple connect-scan tool. Only scan hosts you own or have permission to test.")

with st.form("scan_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        target = st.text_input("Target IP / hostname", placeholder="e.g. 127.0.0.1")
    with col2:
        timeout = st.number_input("Timeout (s)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)

    col3, col4 = st.columns(2)
    with col3:
        start_port = st.number_input("Start port", min_value=1, max_value=65535, value=1)
    with col4:
        end_port = st.number_input("End port", min_value=1, max_value=65535, value=100)

    submitted = st.form_submit_button("Start Scan", use_container_width=True)

if submitted:
    if not target.strip():
        st.error("Please enter a target IP or hostname.")
    elif start_port > end_port:
        st.error("Start port must be less than or equal to end port.")
    else:
        # Resolve hostname to catch bad input early
        try:
            resolved_ip = socket.gethostbyname(target.strip())
        except socket.gaierror:
            st.error(f"Could not resolve host: {target}")
            st.stop()

        st.info(f"Scanning **{target}** ({resolved_ip}), ports {start_port}-{end_port}...")

        progress_bar = st.progress(0)
        status_text = st.empty()
        open_ports = []

        total_ports = end_port - start_port + 1
        start_time = time.time()

        for i, port in enumerate(range(start_port, end_port + 1)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((resolved_ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()

            progress_bar.progress((i + 1) / total_ports)
            status_text.text(f"Checking port {port}... ({i + 1}/{total_ports})")

        elapsed = time.time() - start_time
        status_text.empty()
        progress_bar.empty()

        st.success(f"Scan complete in {elapsed:.2f}s")

        if open_ports:
            st.subheader(f"Open Ports ({len(open_ports)})")
            st.table({"Port": open_ports})
        else:
            st.warning("No open ports found in the given range.")