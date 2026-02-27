# Expert System for Job Qualification Evaluation

## Overview

This project implements a rule-based expert system that determines whether an applicant qualifies for specific technical positions. The system collects structured input from the user and evaluates it against predefined rules stored in a knowledge base.

The system outputs:

- Positions the applicant is qualified for  
- Positions the applicant is not qualified for  
- Clear reasoning explaining unmet requirements  

The primary focus of this implementation is correctness of rule evaluation and transparency of conclusions.

---

## System Components

### 1. Knowledge Base (`knowledge_base.py`)

Defines:

- Available positions  
- Required skills  
- Desired skills  
- Qualification criteria  
- Degree ranking logic  
- Course and certification mappings  

Each position includes required rules (which must pass) and optional desired rules.

---

### 2. Inference Engine (`evaluator.py`)

Implements a forward-chaining rule evaluation mechanism.

The engine:

- Evaluates boolean constraints  
- Evaluates numeric constraints  
- Determines qualification status  
- Computes match percentages  
- Generates structured reasoning output  

A candidate is considered qualified only if all required rules are satisfied.

---

### 3. User Interface (`app.py`)

Built using Streamlit to collect applicant information, including:

- Education  
- Coursework  
- Certifications  
- Work experience  

The interface validates input and presents detailed evaluation results.

---

## Positions Evaluated

- Entry-Level Python Engineer  
- Python Engineer  
- Project Manager  
- Senior Knowledge Engineer  

Each position is evaluated using explicit skill and qualification rules derived from the project specification.

---

## Inference Approach

The system uses deterministic, rule-based reasoning.

For each position:

- Required constraints are evaluated  
- Desired constraints are evaluated  
- The system explains why a candidate is or is not qualified  

This approach ensures transparency and reproducibility of conclusions.

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt