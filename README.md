# Banking App Sentiment Analysis & Topic Modeling

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?style=flat&logo=python)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Manager-blueviolet?style=flat&logo=poetry)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat&logo=streamlit)
![PhoBERT](https://img.shields.io/badge/Model-PhoBERT-orange?style=flat)

**A Natural Language Processing (NLP) framework for extracting sentiment and topic classification from Vietnamese banking application reviews.**

---

## 📖 Abstract

This project addresses the challenge of analyzing unstructured user feedback on digital banking platforms. We implement an end-to-end NLP pipeline that automates data collection, preprocessing, and classification.

The system utilizes **PhoBERT** (a pre-trained monolingual language model for Vietnamese) fine-tuned on a custom dataset of banking reviews. The model performs two simultaneous classification tasks:
1.  **Sentiment Analysis:** Positive, Negative, Neutral.
2.  **Topic Modeling:** Categorizing feedback into specific domains (Account Security, Transaction/Finance, App Experience, Others).

The results are visualized through an interactive dashboard, enabling statistical analysis of user satisfaction and technical issues.

---

## 🛠️ System Architecture & Tech Stack

The system follows a monolithic architecture for rapid deployment and reproducibility.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Python 3.10+ |
| **Model Framework** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white) ![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black) | PhoBERT Base (VinAI) |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Unified Interface & Logic |
| **Dependency Manager** | ![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=flat&logo=poetry&logoColor=white) | Environment Isolation |
| **Data Mining** | ![Google Play](https://img.shields.io/badge/Google_Play-414141?style=flat&logo=google-play&logoColor=white) | `google-play-scraper` |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) | Data manipulation |

---

## 📂 Project Structure

```text
banking-nlp-project/
├── data/                  # Raw and processed datasets (CSV)
├── models/                # Pre-trained model weights
│   ├── topic/             # Fine-tuned Topic Classification Model
│   └── sentiment/         # Fine-tuned Sentiment Analysis Model
├── src/                   # Core logic modules
│   ├── preprocess.py      # Text normalization & Teencode correction
│   ├── analyzer.py        # Model inference & prediction logic
│   └── dashboard.py       # Visualization components
├── app.py                 # Main application entry point
├── scraper.py             # Data scraping script
├── pyproject.toml         # Dependency definitions
└── README.md              # Project documentation
```

---

## ⚙️ Installation

This project requires **Poetry** for dependency management.

### Prerequisites
*   Python >= 3.10 and < 3.15
*   Poetry installed

### Setup Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/NDPhuu/banking-nlp-project.git
    cd banking-nlp-project
    ```

2.  **Configure local environment**
    ```bash
    poetry config virtualenvs.in-project true
    ```

3.  **Install dependencies**
    ```bash
    poetry install
    ```

4.  **Model Setup**
    *   Ensure the fine-tuned model files (`model.safetensors`, `config.json`, `tokenizer_config.json`, ...) are placed in `models/topic/` and `models/sentiment/` respectively.

---

## 🏃‍♂️ Usage

### 1. Data Collection (Optional)
To fetch the latest reviews from Google Play Store:
```bash
poetry run python scraper.py
```
*Output: `data/raw_reviews.csv`*

### 2. Run the Application
Start the Streamlit dashboard:
```bash
poetry run streamlit run app.py
```
*   **Local URL:** `http://localhost:8501`

---

## 📊 Methodology

### Data Preprocessing
Raw text undergoes a rigorous cleaning pipeline defined in `src/preprocess.py`:
*   **Normalization:** Unicode NFC standardization and lowercasing.
*   **Teencode Correction:** Mapping informal internet slang (e.g., "ck", "tk", "lag") to standard Vietnamese using a custom dictionary.
*   **Noise Removal:** Stripping non-alphanumeric characters while preserving relevant punctuation.

### Model Training
*   **Base Model:** `vinai/phobert-base`.
*   **Optimization:** AdamW optimizer with linear learning rate scheduling.
*   **Loss Function:** CrossEntropyLoss with *Class Weights* to handle imbalanced datasets (e.g., dominant "Others" class vs. minority "UI/UX" class).
*   **Evaluation Metric:** Macro F1-Score.

---

## 📝 License

This project is developed for academic research purposes.
