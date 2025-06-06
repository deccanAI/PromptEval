import json
import os
from dotenv import load_dotenv
import together
import streamlit as st

api_ke = st.secrets["TOGETHER_API_KEY"]

load_dotenv()
together.api_key = os.getenv("api_ke")
MODEL_1 = "mistralai/Mistral-7B-Instruct-v0.1"
MODEL_2 = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_response(prompt, model):
    try:
        response = together.Complete.create(
            prompt=prompt,
            model=model,
            max_tokens=512,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"[Error in generate_response]: {e}"
    
def judge_response(user_prompt, model_response):
    judge_prompt = f"""
You are an expert LLM evaluator. Your task is to critically analyze a model's response to a user-provided prompt and determine whether the prompt was effective at eliciting a high-quality, aligned, and robust response from the model.

For each dimension:
- Provide a clear definition
- Use the key indicators to assess the output
- Assign a rating: "Good", "Average", "Bad", or "Can't Assess"

Finally, summarize:
- Whether the prompt was effective (i.e., exposed LLM limitations)
- An explanation including failed/successful dimensions and failure tags (if any)

--- 

Use the following 10 dimensions to guide your evaluation:
### 1. Role Conditioning
**Definition**: Evaluates whether the model adopts a clearly defined role or persona, influencing tone, depth, and framing.
**Key Indicators**:
- Role Presence: Is the persona clearly adopted?
- Tone Alignment: Tone matches role (e.g., academic, casual).
- Perspective Consistency: Is the point of view consistent?
- Role-linked Detail: Are examples aligned with the persona?
- Engagement: Does the role enhance clarity or usefulness?
**Ratings**:
- Good: Strong, consistent persona enriches output.
- Average: Some signs of a role, but not consistent.
- Bad: Role ignored or generic tone used.
- Can't Assess: No role was defined.

---

### 2. Clear Task Definition
**Definition**: Checks if the prompt defines an actionable task using a strong verb and object structure.
**Key Indicators**:
- Clear Action Verb: e.g., summarize, classify.
- Specific Object: What should be acted on?
- Instruction Completeness: Are goals unambiguous?
- Format & Length Precision: Is structure/limit defined?
- Avoidance of Negative Phrasing.
**Ratings**:
- Good: Clear verb-object, well-scoped, constraints defined.
- Average: Vague task or missing details.
- Bad: Ambiguous or overly open-ended task.
- Can't Assess: No actionable task present.

---

### 3. Scope & Constraints
**Definition**: Assesses whether the prompt sets measurable limits (e.g., length, content focus, scope).
**Key Indicators**:
- Word Count, Format, Time Frame given.
- Relevance: Constraints suit the task.
- Execution: Output respects constraints.
**Ratings**:
- Good: Constraints are clear and followed.
- Average: Present but imprecise or loosely enforced.
- Bad: Absent or ignored.
- Can't Assess: Constraints not applicable.

---

### 4. Output Formatting
**Definition**: Evaluates how well the prompt specifies the structure of the response (e.g., table, bullets, JSON).
**Key Indicators**:
- Format Clarity: Is the structure defined?
- Format Adherence: Output follows requested style.
- Readability and Reusability: Easy to scan, reuse, or process.
**Ratings**:
- Good: Clear format request, followed correctly.
- Average: Format partially followed or vaguely stated.
- Bad: Format not specified or output is inconsistent.
- Can't Assess: Task doesn’t require structure.

---

### 5. Few-shot Prompting
**Definition**: Checks if the prompt provides examples to demonstrate style, logic, or structure before asking for a response.
**Key Indicators**:
- Examples Included: 2–3 high-quality examples.
- Pattern Transfer: Model mimics tone/logic accurately.
- Separation: Examples vs task clearly divided.
**Ratings**:
- Good: Examples align well and improve output quality.
- Average: Some examples but unclear or inconsistently followed.
- Bad: No useful examples or irrelevant ones.
- Can't Assess: Few-shot not relevant.

---

### 6. Handling Ambiguity
**Definition**: Determines whether the prompt includes fallback guidance for uncertain scenarios to prevent hallucination.
**Key Indicators**:
- Explicit fallback phrases (e.g., “Say ‘Insufficient data’”).
- Model avoids fabrication in uncertain areas.
- Transparency about uncertainty.
**Ratings**:
- Good: Includes clear fallback logic and model obeys it.
- Average: Partial fallback or vague guidance.
- Bad: No ambiguity handling, model guesses or hallucinates.
- Can't Assess: Task doesn’t involve uncertainty.

---

### 7. Instruction Chaining
**Definition**: Checks if the prompt breaks complex tasks into sequential, logically ordered instructions.
**Key Indicators**:
- Step-wise flow (e.g., first do A, then B…)
- Logical progression between steps.
- Scope clarity per step.
**Ratings**:
- Good: Task broken down into clear, effective subtasks.
- Average: Some structure but confusing flow or overlap.
- Bad: Complex task lumped into one vague step.
- Can't Assess: Simple task didn’t require chaining.

---

### 8. Chain-of-Thought Reasoning
**Definition**: Evaluates whether the prompt encourages the model to reason step-by-step.
**Key Indicators**:
- Phrases like “Let’s think step-by-step”.
- Intermediate steps are visible and logical.
- No premature jumping to conclusions.
**Ratings**:
- Good: Model reasons clearly through each step.
- Average: Some reasoning shown but lacks coherence.
- Bad: No reasoning present, output feels shallow.
- Can't Assess: Task doesn’t require reasoning.

---

### 9. Tree-of-Thought Exploration
**Definition**: Evaluates whether the prompt guides the model to explore multiple possible paths before choosing one.
**Key Indicators**:
- Prompt encourages multiple approaches.
- The model compares and evaluates options.
- Backtracking or reflection visible.
**Ratings**:
- Good: Multiple solution paths explored and compared.
- Average: Limited exploration or weak evaluation.
- Bad: Only one solution given, no comparison.
- Can't Assess: Divergence not relevant to task.

---

### 10. Retrieval-Augmented Generation (RAG)
**Definition**: Evaluates if the model uses external context or documents provided by the prompt.
**Key Indicators**:
- Prompt tells model to refer to documents.
- Output quotes or paraphrases context faithfully.
- No hallucinated facts.
**Ratings**:
- Good: Output well-grounded in source material.
- Average: Some use of context but loosely integrated.
- Bad: External context ignored or misused.
- Can't Assess: No context provided or required.

---

Evaluate the prompt and the model response using these questions:

1. Did the model satisfy all critical expectations of the prompt?
2. If the model failed, was it because the prompt was poorly constructed, overly ambiguous, or lacked proper scaffolding?
3. Alternatively, if the model output was shallow or incorrect despite a strong prompt, then the prompt was effective because it exposed model limitations.

---

Strictly Return your evaluation as JSON using this exact format:
{{
  "Ratings": {{
    "Role Conditioning": "Good" | "Average" | "Bad" | "Can't Assess",
    "Clear Task Definition": "Good" | "Average" | "Bad" | "Can't Assess",
    "Scope & Constraints": "Good" | "Average" | "Bad" | "Can't Assess",
    "Output Formatting": "Good" | "Average" | "Bad" | "Can't Assess",
    "Few-shot Prompting": "Good" | "Average" | "Bad" | "Can't Assess",
    "Handling Ambiguity": "Good" | "Average" | "Bad" | "Can't Assess",
    "Instruction Chaining": "Good" | "Average" | "Bad" | "Can't Assess",
    "Chain-of-Thought Reasoning": "Good" | "Average" | "Bad" | "Can't Assess",
    "Tree-of-Thought Exploration": "Good" | "Average" | "Bad" | "Can't Assess",
    "Retrieval-Augmented Generation (if relevant)": "Good" | "Average" | "Bad" | "Can't Assess"
  }},
  "Effective": true or false,  # True if the prompt revealed weaknesses in the model.
  "Explanation": "Explain the main reason for this score and judgment. Include specific failure tags from: ['Missed nested instruction', 'Shallow reasoning', 'Overgeneralized output', 'Misinterpreted role', 'Missed constraint'] and refer to relevant dimension(s) involved."
}}


USER PROMPT:
{user_prompt}

MODEL RESPONSE:
{model_response}
"""

    try:
        evaluation =  together.Complete.create(
            prompt=judge_prompt,
            # messages=[
            #     {"role": "user", "content": judge_prompt}
            # ],
            model=MODEL_2,
            max_tokens=512,
            temperature=0.3
        )
        return evaluation['choices'][0]['text'].strip()
    except Exception as e:
        return f"[Error in judge_response]: {e}"
    
# Streamlit UI
st.set_page_config(page_title="Prompt Evaluation", layout="wide")

st.title("Prompt Evaluator with LLM-as-a-Judge")
st.markdown("Enter a prompt below and click 'Generate & Evaluate' to see the model's output and the evaluation results.")

# Text area for user prompt
user_prompt = st.text_area("Enter your prompt:", height=200)

# Model selection
model_choice = st.selectbox("Select Model to Generate Response:", [MODEL_1, MODEL_2])

# Trigger processing
if st.button("Generate & Evaluate"):
    if user_prompt.strip() == "":
        st.warning("Please enter a valid prompt.")
    else:
        with st.spinner("Generating response..."):
            model_output = generate_response(user_prompt, model=model_choice)
            evaluation = judge_response(user_prompt, model_output)

        st.subheader("Model Response")
        st.code(model_output, language='markdown')

        st.subheader("Prompt Evaluation")
        # st.json(evaluation)
        # try:
        #     parsed = json.loads(evaluation)
        #     st.json(parsed)
        # except json.JSONDecodeError:
        #     st.error("Failed to parse evaluation JSON.")
        st.code(evaluation, language='text')