import pandas as pd
import numpy as np

class EthicalAIAuditTool:
    """
    A tool to audit Healthcare AI models for Demographic Bias and Fairness.
    Aligns with Framework Section 3.1: Fairness & Bias Mitigation.
    """

    def __init__(self, data: pd.DataFrame, demographic_col: str, 
                 actual_outcome_col: str, prediction_col: str):
        self.data = data
        self.demo_col = demographic_col
        self.actual_col = actual_outcome_col
        self.pred_col = prediction_col
        self.groups = self.data[self.demo_col].unique()

    def generate_audit_report(self):
        print("="*60)
        print(" HEALTHCARE AI ETHICS REVIEW: BIAS AUDIT REPORT ")
        print("="*60)
        
        overall_accuracy = (self.data[self.actual_col] == self.data[self.pred_col]).mean()
        print(f"Overall Model Accuracy: {overall_accuracy * 100:.2f}%\n")
        
        metrics = []

        for group in self.groups:
            group_data = self.data[self.data[self.demo_col] == group]
            
            # Confusion matrix components
            TP = ((group_data[self.pred_col] == 1) & (group_data[self.actual_col] == 1)).sum()
            TN = ((group_data[self.pred_col] == 0) & (group_data[self.actual_col] == 0)).sum()
            FP = ((group_data[self.pred_col] == 1) & (group_data[self.actual_col] == 0)).sum()
            FN = ((group_data[self.pred_col] == 0) & (group_data[self.actual_col] == 1)).sum()

            total_actual_pos = TP + FN
            total_actual_neg = TN + FP

            # Metrics
            tpr = TP / total_actual_pos if total_actual_pos > 0 else 0  # True Positive Rate (Sensitivity)
            fnr = FN / total_actual_pos if total_actual_pos > 0 else 0  # False Negative Rate
            fpr = FP / total_actual_neg if total_actual_neg > 0 else 0  # False Positive Rate
            selection_rate = (TP + FP) / len(group_data) if len(group_data) > 0 else 0 # Positive prediction rate
            
            metrics.append({
                'Group': group,
                'N_Patients': len(group_data),
                'Selection_Rate': selection_rate,
                'True_Positive_Rate': tpr,
                'False_Negative_Rate': fnr,
            })

        metrics_df = pd.DataFrame(metrics).set_index('Group')
        
        print("--- Fairness Metrics by Demographic Group ---")
        print(metrics_df.round(3).to_string())
        print("\n" + "="*60)
        
        # Actionable insights based on the policies
        self._analyze_equity(metrics_df)


    def _analyze_equity(self, metrics_df):
        print(" ETHICS COMPLIANCE ANALYSIS ")
        print("-" * 60)
        
        # Check for Equal Opportunity (Disparities in True Positive Rate)
        max_tpr = metrics_df['True_Positive_Rate'].max()
        min_tpr = metrics_df['True_Positive_Rate'].min()
        tpr_diff = max_tpr - min_tpr
        
        # High False Negative Disparity is critical in healthcare (missed diagnosis)
        max_fnr_group = metrics_df['False_Negative_Rate'].idxmax()
        max_fnr_val = metrics_df['False_Negative_Rate'].max()

        if tpr_diff > 0.10: # threshold of 10%
            print("🚨 WARNING: Equal Opportunity Violation Detected!")
            print(f"The model's ability to correctly diagnose varies by {tpr_diff*100:.1f}% across groups.")
            print(f"Group '{max_fnr_group}' is most at risk of missed diagnoses (FNR: {max_fnr_val*100:.1f}%).")
            print("Recommendation: Model RETRAINING REQUIRED with augmented data before clinical use.")
        else:
            print("✅ PASSED: True Positive Rates are relatively equitable across demographic groups.")


if __name__ == "__main__":
    # Simulate a Hospital's AI validation dataset for a Skin Condition Diagnostic tool
    np.random.seed(42)
    n_samples = 1000
    
    # Mock Demographics: 'Skin Type A' and 'Skin Type B'
    demographics = np.random.choice(['Type A', 'Type B'], size=n_samples, p=[0.7, 0.3])
    
    # Mock Actual Diagnosis (1 = Has Condition, 0 = Healthy)
    actual_outcomes = np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    
    # Simulate AI predictions (Biased against 'Type B')
    predictions = []
    for i in range(n_samples):
        if demographics[i] == 'Type A':
            # AI is highly accurate
            pred = actual_outcomes[i] if np.random.rand() > 0.1 else 1 - actual_outcomes[i]
        else:
            # AI tends to miss the disease in Type B (high false negative)
            pred = actual_outcomes[i] if np.random.rand() > 0.4 else 0
        predictions.append(pred)
        
    df = pd.DataFrame({
        'PatientID': range(1, n_samples + 1),
        'Demographic_Group': demographics,
        'Actual_Diagnosis': actual_outcomes,
        'AI_Prediction': predictions
    })
    
    # Run the Audit
    auditor = EthicalAIAuditTool(df, 'Demographic_Group', 'Actual_Diagnosis', 'AI_Prediction')
    auditor.generate_audit_report()
