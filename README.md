# 🛡️ CodeGuard AI

### AI-Powered Multi-Agent Python Code Auditor

CodeGuard AI is an AI-powered Python code auditing application that automatically analyzes source code for **security vulnerabilities, bugs, bad programming practices, performance issues, maintainability problems, and PEP 8 issues**.

The system uses a sequential multi-agent architecture powered by **Google Gemini**. Each agent performs a specific task and passes its output to the next stage.

```text
Python Source Code
        │
        ▼
┌─────────────────────┐
│   🔎 Scanner Agent  │
│ Security & Quality  │
│       Analysis      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  🧹 Refactor Agent  │
│ Secure & Clean Code │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    📚 Docs Agent    │
│ README & Documents  │
└──────────┬──────────┘
           │
           ▼
      Final Results
```

---

## ✨ Features

### 🔎 AI Code Scanner

The Scanner Agent analyzes Python code for:

* Security vulnerabilities
* SQL injection
* Command injection
* Unsafe input handling
* Hardcoded secrets
* Authentication and authorization problems
* Bugs
* Exception handling issues
* Resource leaks
* Performance problems
* Deprecated patterns
* Bad Python practices
* Maintainability problems
* Important PEP 8 issues

Each finding contains:

* Finding title
* Severity
* Description
* Recommendation

Severity levels:

* 🔴 **High**
* 🟠 **Medium**
* 🟢 **Low**

---

### 🧹 AI Refactoring

The Refactor Agent receives the Scanner Agent's findings and produces improved Python code.

It focuses on:

* Fixing identified security issues
* Improving code readability
* Improving maintainability
* Improving exception handling
* Reducing bad programming practices
* Preserving the original functionality

The generated code can be downloaded directly as:

```text
refactored_code.py
```

---

### 📚 Automatic Documentation

The Documentation Agent generates professional Markdown documentation based on the refactored Python source.

The generated documentation includes:

* Project Overview
* Features
* Requirements
* Installation
* Usage
* Code Structure
* Security Notes

The generated documentation can be downloaded as:

```text
README.md
```

---

## 🎨 Professional Streamlit Interface

CodeGuard AI provides a modern Streamlit interface with:

* Dark professional UI
* Gemini model selection
* Temperature control
* Python file upload
* Source-code editor
* Sequential agent pipeline
* Real-time execution status
* Security findings dashboard
* Severity metrics
* Refactored code viewer
* Documentation viewer
* Pipeline state viewer
* Download buttons

---

# 🏗️ Project Architecture

CodeGuard AI follows a sequential multi-agent architecture.

```text
User
 │
 │ Python Source Code
 ▼
┌──────────────────────────────┐
│        Streamlit UI          │
│            app.py            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Pipeline Controller    │
│       services/pipeline.py   │
└──────────────┬───────────────┘
               │
               ▼
        🔎 Scanner Agent
               │
               │ Findings
               ▼
        🧹 Refactor Agent
               │
               │ Refactored Code
               ▼
         📚 Docs Agent
               │
               ▼
          Final Result
```

---

# 📁 Project Structure

```text
ai_code_auditor/
│
├── app.py
│
├── services/
│   ├── __init__.py
│   └── pipeline.py
│
├── assets/
│
├── data/
│
├── docs/
│
├── models/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🧩 Main Components

## `app.py`

The main Streamlit application.

It handles:

* User interface
* Source-code input
* Python file upload
* Gemini configuration
* Temperature selection
* Pipeline execution
* Findings dashboard
* Refactored code display
* Documentation display
* Download functionality

---

## `services/pipeline.py`

The main AI pipeline.

It contains:

```text
get_api_key()
create_client()
normalize_model()
normalize_temperature()
call_gemini()
extract_json()
sanitize_findings()
scanner_agent()
refactor_agent()
documentation_agent()
run_pipeline()
```

The pipeline uses a typed state object to transfer information between agents.

---

# 🤖 Multi-Agent Pipeline

## Agent 1 — Scanner Agent

The Scanner Agent receives the original Python source code.

```text
Source Code
     │
     ▼
Scanner Agent
     │
     ▼
Security + Bug + Quality Analysis
     │
     ▼
Structured Findings
```

Example finding:

```json
{
  "title": "SQL Injection Risk",
  "severity": "High",
  "description": "User-controlled input is directly concatenated into an SQL query.",
  "recommendation": "Use parameterized SQL queries instead of string concatenation."
}
```

---

## Agent 2 — Refactor Agent

The Refactor Agent receives:

```text
Original Source Code
+
Scanner Findings
```

It generates:

```text
Improved Python Source Code
```

The agent is instructed to preserve the original functionality while fixing identified problems.

---

## Agent 3 — Documentation Agent

The Documentation Agent receives the refactored code and generates professional Markdown documentation.

```text
Refactored Code
      │
      ▼
Documentation Agent
      │
      ▼
Professional README
```

---

# 🔐 Security

CodeGuard AI is designed to identify common security problems in Python applications.

The Scanner Agent checks for issues such as:

```text
SQL Injection
Command Injection
Hardcoded Secrets
Unsafe Input
Authentication Issues
Authorization Issues
Dangerous Functions
```

However, CodeGuard AI should be considered an **AI-assisted code review tool**, not a replacement for professional security testing.

Generated findings should always be reviewed by a developer or security professional before being used in production.

---

# ⚙️ Requirements

Recommended environment:

```text
Python 3.10+
```

Main dependencies include:

```text
streamlit
google-genai
python-dotenv
```

Additional dependencies can be found in:

```text
requirements.txt
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd ai_code_auditor
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate it using CMD:

```bash
.venv\Scripts\activate
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

If `google-genai` is not installed:

```bash
pip install -U google-genai
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You may also use:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

CodeGuard AI checks both environment variables.

### Important

Never upload your real API key to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Application

From the directory containing `app.py`, run:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🖥️ How to Use

## Step 1 — Start CodeGuard AI

Run:

```bash
streamlit run app.py
```

---

## Step 2 — Select Gemini Model

From the sidebar, select the available Gemini model.

The application uses:

```text
gemini-3.6-flash
```

as the default model.

---

## Step 3 — Set Temperature

Temperature controls how deterministic or variable the AI response is.

For code auditing, a lower temperature is recommended.

Recommended value:

```text
0.2
```

### Temperature Guide

| Temperature | Behavior                      |
| ----------- | ----------------------------- |
| `0.0`       | Very deterministic            |
| `0.2`       | Recommended for code auditing |
| `0.5`       | More variation                |
| `0.8`       | More creative                 |
| `1.0`       | High variation                |

For security auditing and refactoring, keeping the temperature around **0.2** is generally preferable.

---

## Step 4 — Add Python Code

You can either:

### Option A — Paste Code

Paste Python source code into the editor.

### Option B — Upload File

Upload:

```text
.py
```

or:

```text
.txt
```

files.

---

## Step 5 — Run Full Audit

Click:

```text
🚀 Run Full Audit
```

The pipeline executes:

```text
Scanner
   ↓
Refactor
   ↓
Documentation
```

---

# 📊 Audit Dashboard

After the audit completes, CodeGuard AI displays:

```text
Total Findings
High Risk
Medium Risk
Low Risk
```

Example:

```text
Total Findings     4
High Risk          1
Medium Risk        2
Low Risk           1
```

Each finding can be expanded to view:

```text
Title
Severity
Description
Recommendation
```

---

# 🧹 Refactored Code

The Refactored Code tab displays the code generated by the Refactor Agent.

Users can download it using:

```text
⬇️ Download Refactored Code
```

The file is saved as:

```text
refactored_code.py
```

---

# 📚 Documentation

The Documentation tab displays the Markdown documentation generated by the Docs Agent.

Users can download it using:

```text
⬇️ Download README
```

The file is saved as:

```text
README.md
```

---

# 🧠 Pipeline State

The Pipeline State tab displays the high-level execution information, including:

```text
Scanner Status
Refactor Status
Documentation Status
Selected Model
```

---

# 🔄 Example Workflow

Suppose the input contains:

```python
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect("app.db")

    query = (
        "SELECT * FROM users WHERE id = "
        + str(user_id)
    )

    return conn.execute(query).fetchone()
```

The Scanner Agent can identify the SQL injection risk.

The Refactor Agent can produce safer code using parameterized SQL:

```python
query = "SELECT * FROM users WHERE id = ?"

return conn.execute(
    query,
    (user_id,)
).fetchone()
```

The Documentation Agent then generates documentation for the improved project.

---

# 🧪 Testing

Before running the application, verify the Python environment:

```bash
python --version
```

Verify Streamlit:

```bash
streamlit --version
```

Verify Google GenAI:

```bash
python -c "from google import genai; print('Google GenAI OK')"
```

Verify the API key:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API key configured:', bool(os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')))"
```

---

# 🛠️ Troubleshooting

## `File does not exist: app.py`

Make sure you are inside the directory containing `app.py`.

For example:

```bash
cd ai_code_auditor
```

Then:

```bash
streamlit run app.py
```

---

## `ImportError: cannot import name 'genai' from 'google'`

Install the official Google GenAI SDK:

```bash
python -m pip install -U google-genai
```

Then test:

```bash
python -c "from google import genai; print('Google GenAI OK')"
```

---

## Gemini API Key Error

Check your `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Make sure there are no unnecessary quotes or spaces.

---

## Empty Gemini Response

Check:

* API key
* Internet connection
* Gemini model availability
* API quota
* Installed `google-genai` version

---

## Slow Responses

CodeGuard AI uses three sequential AI stages:

```text
Scanner
   ↓
Refactor
   ↓
Documentation
```

Therefore, total execution time depends on all three Gemini requests.

For faster testing:

* Use a small Python file
* Keep prompts focused
* Use a fast Gemini model
* Avoid unnecessarily large source files

---

# 📦 Deployment

CodeGuard AI can be deployed to Streamlit-compatible hosting platforms.

Before deployment:

1. Add all dependencies to `requirements.txt`.
2. Do not commit `.env`.
3. Configure `GEMINI_API_KEY` using the hosting platform's secrets/environment settings.
4. Set the application entry point to:

```text
app.py
```

---

# 🌐 Recommended GitHub Structure

Your GitHub repository should contain:

```text
ai_code_auditor/
│
├── app.py
├── services/
│   ├── __init__.py
│   └── pipeline.py
│
├── assets/
├── docs/
├── models/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Do **not** upload:

```text
.env
.venv/
__pycache__/
```

---

# 🔒 Environment Variables

| Variable         | Description                         |
| ---------------- | ----------------------------------- |
| `GEMINI_API_KEY` | Google Gemini API key               |
| `GOOGLE_API_KEY` | Alternative Gemini API key variable |

Only one valid API key variable is required.

---

# 🧰 Technology Stack

CodeGuard AI is built using:

| Technology       | Purpose                    |
| ---------------- | -------------------------- |
| Python           | Core programming language  |
| Streamlit        | Web interface              |
| Google Gemini    | AI code analysis           |
| Google GenAI SDK | Gemini API integration     |
| python-dotenv    | Environment configuration  |
| TypedDict        | Pipeline state management  |
| JSON             | Structured scanner results |

---

# 📐 Design Principles

CodeGuard AI follows these principles:

### Separation of Responsibilities

Each agent has a dedicated responsibility:

```text
Scanner       → Find problems
Refactor      → Fix problems
Documentation → Explain project
```

### Typed Pipeline State

Information is transferred between agents through a structured state:

```python
PipelineState
```

This makes the multi-agent workflow easier to understand and maintain.

### Structured Scanner Output

The Scanner Agent returns JSON so findings can be processed programmatically.

---

# 🎯 Project Goals

The main goals of CodeGuard AI are:

* Automate Python code review
* Identify common security vulnerabilities
* Detect programming problems
* Improve code quality
* Automatically refactor source code
* Generate project documentation
* Demonstrate multi-agent AI architecture
* Provide an easy-to-use developer interface

---

# 🚧 Future Improvements

Possible future enhancements include:

* Support for JavaScript
* Support for TypeScript
* Support for Java
* GitHub repository scanning
* Pull Request analysis
* Static analysis integration
* Bandit integration
* Ruff integration
* Flake8 integration
* Dependency vulnerability scanning
* Code quality scoring
* Security score
* PDF audit reports
* Exportable audit reports
* Parallel agent execution where appropriate
* Persistent audit history
* User authentication
* Team dashboards

---

# 📊 Future Security Score

A future version can calculate an overall security score:

```text
Security Score: 87 / 100
```

based on:

```text
High Findings
Medium Findings
Low Findings
Code Quality
Security Issues
Performance Issues
```

---

# ⚠️ Disclaimer

CodeGuard AI is an AI-assisted code review and educational tool.

AI-generated findings and refactored code may contain mistakes or omissions. Critical production systems should also be reviewed using professional security tools, static analyzers, automated tests, and qualified security professionals.

Do not rely exclusively on CodeGuard AI for production security decisions.

---

# 👨‍💻 Author

**Almeer Ahmed**

AI / Python Developer

---

# 📄 License

This project is intended for educational and development purposes.

You may add an appropriate open-source license such as MIT if you decide to distribute the project publicly.

---

# ⭐ Conclusion

CodeGuard AI combines **AI-powered code analysis, automated refactoring, and documentation generation** into a single sequential multi-agent application.

The workflow is simple:

```text
Write / Upload Python Code
          ↓
      🔎 Scan
          ↓
     🧹 Refactor
          ↓
      📚 Document
          ↓
     📊 Review Results
```

### 🛡️ CodeGuard AI

**Scan smarter. Refactor safer. Document automatically.**
