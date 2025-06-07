# 📊 Prompt Evaluation Pipeline

This repository contains a Python-based pipeline for automatically checking **dimension alignment**, assessing **prompt complexity**, and measuring **prompt effectiveness**, providing a holistic analysis of prompt quality and model behavior. It reads prompts and questions from a CSV file, generates responses using a specified model, evaluates them using a secondary model, and saves the results back into a new CSV. 


## 🚀 Features

- ✅ **Input Parsing**: Reads questions and prompts from a CSV file.
- 🧠 **LLM Integration**: Uses `MODEL_1` to generate answers and `MODEL_2` to evaluate them.
- 📈 **Scoring System**: Computes multiple metrics including:
  - `score1`, `score2`, `net_score`
  - Prompt challenge score
  - Effectiveness text and score
- 💾 **Output Export**: Stores results in a well-structured output CSV.


## 📁 File Structure
```
.
├── README.md                   # Project documentation
├── llm_e.py                    # Script for LLM evaluation logic
├── open_ai_promptEff.ipynb     # Main notebook for evaluation/testing with OpenAI model
├── tog_ai_promptEff.ipynb      # Alternate notebook for evaluation/testing with Together.ai model
├── requirements.txt            # Python package requirements
├── sample_input.csv            # Sample input CSV (must include question and user_prompt columns)
├── sample_output_openai.csv    # Output CSV with evaluated results
```


## 🧑‍💻 How to Use

#### 1. Install Dependencies
Make sure you have the following Python packages installed:

```bash
pip install pandas
```

You’ll also need your custom functions/models:
  - `generate_response(user_prompt, model)`
  - `evaluate(user_prompt, question, model, model_response)`

#### 2. Prepare Input CSV
Create a `sample_input.csv` with the following columns:
 - `question`
 - `user_prompt`

#### 3. Run the Script

```
from process_csv import process_csv

input_csv_path = "sample_input.csv"
output_csv_path = "sample_output_openai.csv"

process_csv(input_csv_path, output_csv_path)
```

#### 4. Check the Output
The results will be saved in `sample_output_openai.csv`.


## 📌 Example Output Columns

| question     | user_prompt   | score1 | score2 | net_score | prompt_challenging | effectiveness_score | effectiveness_text | complexity_check_json | complexity_eval_json | effectiveness_json |
|--------------|---------------|--------|--------|-----------|---------------------|----------------------|---------------------|------------------------|-----------------------|---------------------|
| What is AI? | Define AI.     | 0.9    | 0.85   | 0.875     | Yes                 | 8.5                  | Well explained       | {...}                  | {...}                 | {...}               |

## ⚠️ Error Handling
If an exception occurs while processing a row, it is logged and the row is filled with default `"ERROR"` values to maintain pipeline consistency.

## 🧪 Future Improvements
 - Add logging support
 - Integrate tqdm progress bar
 - Parallelize batch evaluation for large datasets
 - Visualize scores via a dashboard

## 📝 License
This project is open-sourced under the MIT License.

