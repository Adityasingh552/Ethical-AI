# Ethical AI Implementation Framework for Healthcare

This project repository contains the comprehensive Ethical AI framework designed for healthcare, along with supplementary reports and programmatic audit tools. 

## Included Files & Structure

### 1. `Ethical_AI_Healthcare_Framework.md`
The main framework document covering fundamental guidelines, mitigations for fairness/accountability, standard operating procedures, and clinical case studies.

### 2. `Framework_Explanation_Report.md`
A supplementary report providing a breakdown of *why* each section of the framework exists. It aligns stakeholders (doctors, developers, administrators) on the intent behind each policy.

### 3. `ai_bias_audit_tool.py` (Supporting Code)
A functional Python script that acts as a programmatic tool for the **AI Ethics Review Board** (established in Section 3.3). It directly fulfills the requirement for the framework's "Fairness & Bias Mitigation" guideline.

This script takes the prediction outputs of a healthcare AI (e.g., a diagnostic model) and tests it against demographic sub-groups of patients. It performs an active Equity Audit to see if the AI performs worse on specific demographics (disparate False Negative Rates, meaning missed diagnoses). 

#### How to Run the Code
Ensure you have `pandas` and `numpy` installed.

```bash
pip install pandas numpy
python ai_bias_audit_tool.py
```

**Expected Output:**
The script generates mock patient data simulating a biased AI model. The script evaluates the output, successfully catching the violation and explicitly outputting the missed diagnosis rate (False Negative Rate) disparity between Demographic 'Type A' and 'Type B', triggering an Ethics Alert.
