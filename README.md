<div align="center">
  <img src="https://img.icons8.com/color/96/000000/tractor.png" alt="Logo">
  <h1>🌾 AgriMind (Agrisage)</h1>
  <p><strong>An Intelligent, Multi-Agent RAG & Text-to-SQL System for Agricultural Advisory</strong></p>
</div>

<br/>

## 🚨 The Problem Statement
In modern agriculture, farmers and data scientists face a massive disconnect. Crucial statistical data regarding crop yields and required optimal NPK fertilizer numbers are locked inside rigid tabular databases. Meanwhile, qualitative advisory data (best practices, disease control, cultivation methods) are buried in unstructured text documents. 

When a user asks complex agricultural questions, traditional basic chatbots either violently hallucinate statistics, or completely fail to cross-reference hard quantitative data with qualitative advice.

## 💡 What We Have Done (The Solution)
**AgriMind** is a full-stack, AI-native application that bridges this gap using a **Multi-Agent Language Model Architecture**. 

Instead of relying on a single bot, we implemented **CrewAI** to orchestrate four specialized, sequential Agents:
1. 🚦 **Intent Analyzer (Router)**: Dynamically parses user questions to categorize intention so the system doesn't waste tokens.
2. 📖 **Agronomist (RAG)**: Connects to a robust **FAISS Vector Database** to pull semantic, qualitative text advice.
3. 📊 **Data Scientist (SQL)**: Reads explicit table schemas and executes strict native **SQLite Python code** directly against the DB to extract precise yields and NPK requirements.
4. 🗣️ **Communicator**: Evaluates the output arrays of the previous agents, ignoring faults, and intelligently fuses both the RAG text and the SQL data into a single, highly accurate Markdown response.

To provide immediate visual transparency, we decoupled this backend and built a **React/Vite Frontend** that visually parses the backend intention routing loop. Depending on what the AI backend decided to do, the Right Sidebar UI dynamically renders either the quantitative **SQL Execution Code block** or the qualitative **Ragas Evaluation Metrics** (Faithfulness & Answer Relevancy).

## 🛠️ Tech Stack 

### Frontend Software
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

### Backend Engineering
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Artificial Intelligence & Machine Learning
![Groq](https://img.shields.io/badge/Groq-Llama_3.1-f55036?style=for-the-badge)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi_Agent-orange?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-blue?style=for-the-badge)
![Ragas](https://img.shields.io/badge/Ragas-LLM_Evaluation-green?style=for-the-badge)

## 📖 Deep-Dive Documentation
For developers and engineers who want to install, run, or understand exactly how the Multi-Agent architecture logic executes under the hood, please refer to our explicit technical documentation:

- 📘 [**User Guide & Local Setup Instructions**](./USER_GUIDE.md)
- ⚙️ [**Agent Architecture & System State Flow**](./AGENT_ARCHITECTURE.md)
