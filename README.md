# 🧬 get-pubmed-papers

A Python CLI tool that uses the **PubMed API** to fetch research articles and filter those that include authors from **pharmaceutical or biotech companies**.

Built with the assistance of **LLM** and structured using **Poetry**, `argparse`, and modern Python packaging.

---

## 🚀 Features

- Supports full **PubMed query syntax**
- Filters papers with **non-academic (industry) authors**
- Extracts and returns:
  - PubMed ID
  - Title
  - Publication Date
  - Company-affiliated Author Names
  - Company Affiliations
  - Author Emails
- Output options:
  - Save as CSV file
  - Or display in terminal

---

## 🛠️ Installation

### 🔹 Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

### 🔹 Install Dependencies

```bash
poetry install
```

---

## 🧪 Usage

### ✅ Basic usage with query

```bash
poetry run get-papers-list --query "covid-19 vaccine AND 2023"
```

### ✅ Save to CSV file

```bash
poetry run get-papers-list --query "AI in radiology" --max 15 --file ai_results.csv
```

### ✅ Show help menu

```bash
poetry run get-papers-list --help
```

### ✅ Enable debug logs

```bash
poetry run get-papers-list --query "cancer immunotherapy" --debug
```

---

## 🧱 Project Structure

```
get-pubmed-papers/
│
├── get_papers/               ← Python package (fetcher module)
│   └── fetcher.py            ← Contains core logic: search, fetch, parse
│
├── main.py                   ← Command-line interface (argparse)
├── pyproject.toml            ← Poetry config and metadata
├── README.md                 ← Project overview and usage
```

---

## 📦 Packaging & Distribution

### Build wheel and source distribution:

```bash
poetry build
```

### Optional: install the built wheel locally

```bash
pip install dist/get_pubmed_papers-0.1.0-py3-none-any.whl
```

---

## 🧠 Tools & Libraries Used

- [ChatGPT (GPT-4)](https://openai.com/chatgpt) – helped structure the project and debugging the code
- [PubMed API (Entrez Utilities)](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [Poetry](https://python-poetry.org/) – for Python packaging and dependency management
- Python standard libraries: `argparse`, `csv`, `re`, `requests`, `xml.etree`

---

## ✨ TestPyPI Publishing

To publish this package to [Test PyPI](https://test.pypi.org):

```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish -r test-pypi
```

Test install from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple get-pubmed-papers
```

---

## 👤 Author

Aswin Kumar  
[GitHub Profile](https://github.com/AswinKumar23)
