# 🛠️ SolrOps Control Console

A secure, user-friendly web UI to start, stop, and restart Solr instances across multiple servers — ideal for production clusters.

---

## 🔑 Features

- 🔐 Password-protected Streamlit UI
- 🔄 Start / Stop / Restart Solr instances over SSH
- 🗂️ Zone → Host → Port mapping
- 📄 Auto-generates `solr_instances.yaml` from `userconfig.yaml`
- ✅ Supports passwordless SSH and fallback password auth
- 🌐 Designed for large-scale, multi-node Solr deployments
- 💻 Tested in real production-like environments

---

## 📦 Installation

### 1. Clone the repo:
```bash
git clone https://github.com/yourusername/solr-ui-tool.git
cd solr-ui-tool
```

### 2. Create virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### `userconfig.yaml`

```yaml
ui_auth:
  username: admin
  password: solr1234

default_ssh:
  ssh_user: solradmin
  ssh_password: welcome123

nodes:
  - host: 192.168.0.101
    zone: zone1
    ssh_user: rajkumar
    ssh_password: mans@123
    ports: [8983, 8984]
    paths: [/opt/solr1, /opt/solr2]

ui_config:
  title: "🛠️ Solr Instances Control Panel"
  footer_note: "🚀 Created by Rajkumar Kumawat · Powered by Streamlit & Paramiko"
```

---

## 🚀 Usage

### 1. Generate `solr_instances.yaml`:
```bash
python generate_solr_yaml.py
```

### 2. Run the web UI:
```bash
streamlit run solr_ui_streamlit.py
```

- Open your browser → `http://localhost:8501`
- Login with the credentials from `userconfig.yaml`

---

## 🧪 Test Setup (Optional)

To test locally:
```bash
wget https://archive.apache.org/dist/lucene/solr/8.11.2/solr-8.11.2.tgz
tar -xzf solr-8.11.2.tgz
cp -r solr-8.11.2 solr1
cp -r solr-8.11.2 solr2

# Start instances:
solr1/bin/solr start -p 8983 -s solr1/server/solr
solr2/bin/solr start -p 8984 -s solr2/server/solr
```

---

## 👨‍💻 Created By

**Rajkumar Kumawat**
