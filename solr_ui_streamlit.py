import streamlit as st
import yaml
from executor import load_instances, get_instance, run_action, restart_instance

# Load configuration file
@st.cache_data
def load_config():
    with open("userconfig.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

# --- Persistent Login ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.set_page_config(page_title="SolrOps Login", layout="centered")
        st.subheader("🔐 Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if (
                username == config["ui_auth"]["username"]
                and password == config["ui_auth"]["password"]
            ):
                st.session_state.authenticated = True
                st.rerun()  # ✅ Correct usage
            else:
                st.error("❌ Invalid username or password")
    st.stop()

# UI Config
ui_title = config.get("ui_config", {}).get("title", "Solr Instances Control Panel")
footer_note = config.get("ui_config", {}).get("footer_note", "")

st.set_page_config(page_title="Solr Instance Manager", layout="wide")
st.markdown(f"""
    <style>
        .title-text {{
            font-size: 36px;
            font-weight: 700;
            color: #FF6F00;
        }}
        .footer {{
            margin-top: 2em;
            font-size: 14px;
            color: #666;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
<span class='title-text'>{ui_title}</span>
""", unsafe_allow_html=True)

st.info("""
**ℹ️ App Usage Guide:**
- Select a **Zone** → then **Host** → then **Instances**
- Choose an **Action** (start / stop / restart)
- (Optional) Override SSH credentials
- Click 🚦 to execute across multiple Solr instances
""")

# Load instance config
instances = load_instances()

# Organize by zone > host > instances
zones = {}
for inst in instances:
    zone = inst.get("zone", "unknown")
    host = inst["host"]
    zones.setdefault(zone, {}).setdefault(host, []).append(inst)

# Zone selection
selected_zone = st.selectbox("🌐 Select Zone", list(zones.keys()))

# Host selection
selected_host = st.selectbox("🖥️ Select Host in Zone", list(zones[selected_zone].keys()))

# Display instance options
host_instances = zones[selected_zone][selected_host]
instance_labels = [f"{i['port']} ({i['solr_home']})" for i in host_instances]
selected_labels = st.multiselect("📦 Select Instances", instance_labels, default=instance_labels)

# Filter selected instances
selected_instances = [i for i, lbl in zip(host_instances, instance_labels) if lbl in selected_labels]

# Global SSH config (optional override)
ssh_user = st.text_input("🔐 Override SSH User (optional)")
ssh_password = st.text_input("🔑 SSH Password (optional)", type="password")

action = st.radio("⚙️ Action", ["start", "stop", "restart"], horizontal=True)

if st.button(f"🚦 Run '{action}' on {len(selected_instances)} instance(s)"):
    with st.spinner("Executing..."):
        logs = []
        for inst in selected_instances:
            if ssh_user:
                inst["ssh_user"] = ssh_user
            if ssh_password:
                inst["ssh_password"] = ssh_password

            if action == "restart":
                out = restart_instance(inst['host'], inst['port'])
            else:
                out = run_action(action, inst)

            logs.append(f"\n--- {inst['host']}:{inst['port']} ---\n{out.strip()}")

        st.success("✅ Done")
        st.text_area("📋 Execution Output", "\n".join(logs), height=400)

st.markdown("---")
st.markdown(f"""
<div class='footer'>
    {footer_note}
</div>
""", unsafe_allow_html=True)

