# C++ Test Generator with Ollama and Mistral 7B

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]() [![Coverage](https://img.shields.io/badge/coverage-100%25-blue)]() [![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

Automate unit test generation for C++ code using local LLMs (Ollama with Mistral 7B). Generate tests, handle build errors, refine code, and calculate coverage—all offline.

---

## 📁 Table of Contents

- [🚀 Project Structure](#-project-structure)  
- [⚙️ Setup Instructions](#️-setup-instructions)  
- [🛠️ Usage](#️-usage)  
- [🔄 Workflow Process](#-workflow-process)  
  - [Test Generation](#test-generation)  
  - [Build & Refinement](#build--refinement)  
  - [Coverage Calculation](#coverage-calculation)  
- [⚙️ Customization](#-customization)  
- [🐞 Troubleshooting](#-troubleshooting)  
- [✨ Key Features](#-key-features)  
- [🚧 Next Steps](#-next-steps)  
- [📜 License](#-license)  

---

## 🚀 Project Structure

```
C-TestGenerator/
├── src/                   # Source C++ files
│   ├── myfile.cpp
│   └── myfile.h
├── tests/                 # Generated unit tests
├── instructions/          # LLM prompt templates
│   ├── generate_tests.yaml
│   └── fix_tests.yaml
├── scripts/               # Automation scripts
│   ├── generate_tests.py
│   └── run_tests.sh
└── README.md              # This file
```

---

## ⚙️ Setup Instructions

1. **Install Dependencies**  
   ```bash
   sudo apt update
   sudo apt install -y g++ libgtest-dev cmake lcov
   ```
2. **Build Google Test**  
   ```bash
   sudo bash -c 'cd /usr/src/googletest && cmake . && make && cp lib/*.a /usr/lib'
   ```
3. **Install Ollama**  
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull mistral
   ```
4. **Start Ollama Server**  
   ```bash
   ollama serve
   ```

---

## 🛠️ Usage

- **Generate Tests:**  
  ```bash
  python3 scripts/generate_tests.py
  ```
- **Run Tests & View Coverage:**  
  ```bash
  bash scripts/run_tests.sh
  ```
- **View Results:**  
  - Generated tests: `tests/`  
  - Coverage report: `coverage.txt`  

---

## 🔄 Workflow Process

### Test Generation

1. Reads C++ files from `src/`
2. Sends code to Ollama with instructions from `instructions/generate_tests.yaml`
3. Saves generated tests into `tests/`

### Build & Refinement

1. Attempts to build tests
2. If build fails, sends errors to Ollama for fixes (using `instructions/fix_tests.yaml`)
3. Retry up to 3 refinement attempts

### Coverage Calculation

1. Runs successful tests
2. Generates coverage report via `gcov`/`lcov`
3. Outputs coverage percentage to `coverage.txt`

---

## ⚙️ Customization

- **Modify Instructions:**  
  Edit YAML files in `instructions/`:
  - `generate_tests.yaml` – initial test generation rules
  - `fix_tests.yaml` – error correction rules

- **Add Source Files:**  
  Place new `.cpp` files in `src/`

- **Change LLM Model:**  
  Edit the `MODEL` variable in `scripts/generate_tests.py` (e.g., `"mistral"`, `"llama2"`, `"codellama"`)

---

## 🐞 Troubleshooting

- **Ollama Errors:**  
  - Ensure `ollama serve` is running  
  - Verify model is downloaded: `ollama list`  

- **Build Failures:**  
  - Check Google Test installation  
  - Verify header paths in `run_tests.sh`  

- **Permission Issues:**  
  - Prefix commands with `sudo` as needed  

---

## ✨ Key Features

- **Local LLM Processing:** Offline test generation with Ollama + Mistral 7B  
- **Automated Refinement:** Self-corrects via build error feedback  
- **Coverage Integration:** Standard GNU coverage tools (`gcov`, `lcov`)  
- **Easy Customization:** Modify behavior via YAML prompts  

---

## 🚧 Next Steps

1. Support multi-file C++ projects  
2. Add CI/CD integration  
3. Experiment with other LLM models  
4. Enhance test coverage metrics and reporting  

THANKS
------
Debasis Sikdar