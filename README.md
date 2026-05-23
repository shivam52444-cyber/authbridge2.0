<h1>🚀 AI Hiring Intelligence System</h1>

<p>
An end-to-end AI-powered hiring platform that automates resume screening, standardizes candidate evaluation,
and introduces data-driven decision intelligence into recruitment workflows. The system integrates LLM-based
semantic analysis with structured scoring and multi-stage human decision tracking to improve consistency and reduce bias.
</p>

<h2>📌 Overview</h2>
<p>
Traditional hiring pipelines are manual and subjective. This system models hiring as a structured decision problem,
where candidate-job fit is quantified using AI and evaluated across HR, Manager, and Leadership levels.
</p>

<h2>🧠 Core Features</h2>
<ul>
  <li><b>AI Resume Scoring:</b> Generates score (0–100), strengths, gaps, and recommendation</li>
  <li><b>JD Intelligence:</b> Extracts and weights required and preferred skills</li>
  <li><b>Resume Processing:</b> Parses PDFs and stores structured candidate data</li>
  <li><b>Role-Based Workflow:</b> HR → Manager → Leader dashboards</li>
  <li><b>Decision Pipeline:</b> AI → HR → Manager → Final Outcome</li>
  <li><b>Email Automation:</b> Notifications via SendGrid</li>
</ul>

<h2>📊 Analytics</h2>
<ul>
  <li><b>Shortlist Rate:</b> Shortlisted / Total Reviewed</li>
  <li><b>Quality Score:</b> Avg(Shortlisted Score) − Avg(Rejected Score)</li>
</ul>

<h2>🏗️ Architecture</h2>
<pre>
User (HR / Manager / Leader)
        ↓
Streamlit Frontend
        ↓
Python Backend (SQLAlchemy)
        ↓
PostgreSQL (Render)
        ↓
LLM Engine (Groq)
        ↓
Decision Tracking & Analytics
</pre>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li>Frontend: Streamlit</li>
  <li>Backend: Python</li>
  <li>Database: PostgreSQL (Render)</li>
  <li>ORM: SQLAlchemy</li>
  <li>LLM: Groq</li>
  <li>PDF Parsing: PyMuPDF</li>
  <li>Email: SendGrid</li>
  <li>Deployment: Docker + Render</li>
</ul>

<h2>⚙️ Setup</h2>
<pre>
git clone &lt;repo-url&gt;
cd project
pip install -r requirements.txt
</pre>

<h3>Environment Variables</h3>
<pre>
DATABASE_URL=your_postgres_url
SENDGRID_API_KEY=your_sendgrid_key
</pre>

<h2>🗄️ Database Initialization (First Time Only)</h2>
<pre>
python initdb.py
python create_users.py
</pre>

<h2>▶️ Run Application</h2>
<pre>
streamlit run main_app.py
</pre>

<h2>👤 Demo Credentials</h2>
<pre>
HR:       hr@company.com / 123
Manager:  manager@company.com / 123
Leader:   leader@company.com / 123
</pre>

<h2>🚀 Deployment</h2>
<p>
Deployed on Render using Docker (Python 3.11) with managed PostgreSQL.
</p>

<h2>🎯 Problem Solved</h2>
<p>
Transforms hiring into a quantifiable, AI-assisted system enabling standardized evaluation,
reduced bias, and measurable recruiter performance.
</p>

<h2>🔮 Future Improvements</h2>
<ul>
  <li>AI vs Human disagreement analysis</li>
  <li>Bias detection</li>
  <li>Model calibration</li>
  <li>A/B testing hiring strategies</li>
  <li>Secure authentication (RBAC, hashing)</li>
</ul>

<h2>🧠 Key Insight</h2>
<p>
This is not just a resume screener — it is a <b>decision intelligence system for hiring</b>.
</p>

<h2>👨‍💻 Author</h2>
<p><b>Shivam — Data Scientist</b></p>
