# 🏥 OpsHeal-Agent: Autonomous Incident Triage & Self-Healing AIOps Engine

**OpsHeal-Agent** is an enterprise-grade, multi-agent AI Operations platform designed to automate the triage, root-cause lookup, and remediation of critical infrastructure alerts. 

Instead of relying on brittle, rule-based scripts or manual runbook lookups, OpsHeal uses **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** to parse unstructured server alerts, match them against internal Standard Operating Procedures (SOPs), and generate safe, copy-pasteable resolution scripts alongside ServiceNow ticketing payloads.

---

## 🏗️ System Architecture

```text
[ Unstructured Monitoring Alert ]
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ PERSONA 1: THE TRIAGE SPECIALIST (Gemini Flash)        │
│ Extracts Hostname, OS, Broken Component, and Severity. │
└────────────────────────┬───────────────────────────────┘
                         │ Passes clean metadata
                         ▼
┌────────────────────────────────────────────────────────┐
│ RAG KNOWLEDGE ENGINE (FAISS Vector Database)           │
│ Searches local IT playbooks (/playbooks) using vector  │
│ embeddings to retrieve exact remediation SOP rules.    │
└────────────────────────┬───────────────────────────────┘
                         │ Passes SOP ground-truth
                         ▼
┌────────────────────────────────────────────────────────┐
│ PERSONA 2: THE REMEDIATION ENGINEER (Gemini Flash)     │
│ Generates safe Bash/PowerShell recovery scripts and    │
│ structured JSON payloads for ServiceNow closure.       │
└────────────────────────────────────────────────────────┘
```

---

## ✨ Key Engineering Features

* **Multi-Agent Orchestration.** Separates responsibilities between a fast transactional **Triage Agent** (data extraction) and a **Remediation Agent** (script generation) to prevent hallucinations.
* **Local Vector Knowledge Base (RAG).** Uses **FAISS** and text chunking to index local Standard Operating Procedures (`INFRA-DISK-099`, `INFRA-SVC-404`), ensuring generated scripts strictly follow approved enterprise guidelines.
* **High-Availability (HA) Fallback Design.** Implements resilient exception handling (`_call_gemini_with_fallback`) so the operations portal remains responsive even during upstream cloud API rate limits or `503` service spikes.
* **Interactive Command Center.** Built with **Streamlit** to provide an intuitive web dashboard for simulating and resolving multiple infrastructure failure scenarios.

---

## 🛠️ Tech Stack

* **Language.** Python 3.11+
* **AI & Orchestration.** Google GenAI SDK (`gemini-2.5-flash`), LangChain Core & Text Splitters
* **Vector Database.** FAISS (`faiss-cpu`)
* **Frontend Dashboard.** Streamlit
* **Environment Management.** `python-dotenv`

---

## 🚀 Quickstart Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com
cd OpsHeal-Agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```text
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

### 4. Compile the Local Vector Knowledge Base
Run the database builder script to index the SOP manuals located in the `/playbooks` folder:
```bash
python build_knowledge_base.py
```

### 5. Launch the Interactive Dashboard
```bash
python -m streamlit run app.py
```
