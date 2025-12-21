# 🏦 Banking App Sentiment Analysis & Topic Modeling

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Manager-blueviolet?style=for-the-badge&logo=poetry)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)
![PhoBERT](https://img.shields.io/badge/Model-PhoBERT-orange?style=for-the-badge)

> **An AI-powered Social Listening system designed to extract insights from Vietnamese banking application reviews.**

---

## 📖 Abstract

In the era of Digital Banking, user feedback on app stores is a goldmine of information. However, processing thousands of unstructured comments manually is impossible. 

This project implements a **Natural Language Processing (NLP)** pipeline to automatically scrape, process, and analyze user reviews from Google Play Store. By leveraging **PhoBERT** (a pre-trained language model for Vietnamese), the system classifies reviews into sentiments (Positive/Negative) and specific topics (Login Issues, UI/UX, Transaction Fees, etc.), providing actionable insights for Product Managers and Developers.

## 🚀 Key Features

*   **🕷️ Automated Scraping:** Real-time data collection from Google Play Store using `google-play-scraper`.
*   **brain AI-Powered Analysis:** Fine-tuned **PhoBERT** model for high-accuracy Vietnamese sentiment analysis and topic classification.
*   **⚡ High-Performance API:** Backend built with **FastAPI** for asynchronous processing.
*   **📊 Interactive Dashboard:** User-friendly interface built with **Streamlit** to visualize trends, word clouds, and statistics.
*   **📦 Modern Workflow:** Dependency management using **Poetry**.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-000000?logo=python&logoColor=white) | Core programming language |
| **NLP Model** | ![HuggingFace](https://img.shields.io/badge/HuggingFace-000000?logo=huggingface&logoColor=yellow) | PhoBERT (VinAI) |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-000000?logo=fastapi&logoColor=white) | RESTful API Service |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-000000?logo=streamlit&logoColor=FF4B4B) | Data Visualization Dashboard |
| **Package Manager** | ![Poetry](https://img.shields.io/badge/Poetry-000000?logo=poetry&logoColor=60A5FA) | Dependency & Environment Management |
| **Data Handling** | ![Pandas](https://img.shields.io/badge/Pandas-000000?logo=pandas&logoColor=white) / ![NumPy](https://img.shields.io/badge/NumPy-000000?logo=numpy&logoColor=white) | Data manipulation |


---

## ⚙️ Installation & Setup

This project uses **Poetry** for dependency management to ensure reproducibility.

### Prerequisites
*   Python 3.10 and below 3.15
*   Poetry installed (`pip install poetry`)

### Step-by-step

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/banking-nlp-project.git
    cd banking-nlp-project
    ```
2.  **Set up .venv inside the folder**
    ```bash
    poetry config virtualenvs.in-project true
    ```
3.  **Install dependencies**
    ```bash
    poetry install
    ```
    *This command will create a virtual environment and install all required libraries (Torch, Transformers, FastAPI, etc.) automatically.*



---

## 🏃‍♂️ Usage

*To be conttinued.*