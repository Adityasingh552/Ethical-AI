import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Import the Ethical AI audit tool we created earlier!
from ai_bias_audit_tool import EthicalAIAuditTool

def create_synthetic_healthcare_data(n_samples=2500):
    """
    Generate synthetic patient data including clinical features and demographic groups.
    This simulates a real hospital EHR export containing inherent historical bias.
    """
    np.random.seed(42)
    
    # Clinical vitals
    age = np.random.normal(55, 12, n_samples)
    bmi = np.random.normal(29, 6, n_samples)
    blood_pressure = np.random.normal(125, 15, n_samples)
    
    # Demographics: Hospital population is predominantly 'Group A' (80%), 'Group B' is minority (20%)
    demographics = np.random.choice(['Group A', 'Group B'], size=n_samples, p=[0.8, 0.2])
    
    # Target Outcome: Predict if the patient will develop Cardiovascular Disease (0=No, 1=Yes)
    diagnosis = []
    for i in range(n_samples):
        # Base clinical risk score
        risk = (age[i] - 55) * 0.05 + (bmi[i] - 29) * 0.08
        
        # Introduce a disparity: 
        # The historical health system underdiagnosed 'Group B' despite similar symptoms
        if demographics[i] == 'Group A':
            prob = 1 / (1 + np.exp(-risk)) # standard risk
        else:
            prob = 1 / (1 + np.exp(-(risk - 1.2))) # historically underdiagnosed
            
        # Convert probability to actual 1 or 0 outcome
        diagnosis.append(1 if np.random.rand() < prob else 0)
        
    df = pd.DataFrame({
        'PatientID': range(1, n_samples + 1),
        'Age': age,
        'BMI': bmi,
        'BloodPressure': blood_pressure,
        'Demographic_Group': demographics,
        'Actual_Diagnosis': diagnosis
    })
    
    return df

def train_and_audit_model():
    print("1. Extracting synthetic Patient Healthcare Data...")
    df = create_synthetic_healthcare_data()
    print(f"   Data contains {len(df)} patients.")
    
    # Prepare features (X) and target (y)
    # The AI model does NOT see the demographic group, which mimics standard "blind" training
    X = df[['Age', 'BMI', 'BloodPressure']]
    y = df['Actual_Diagnosis']
    
    # Split into 70% training data, 30% testing/validation data
    X_train, X_test, y_train, y_test, demo_train, demo_test = train_test_split(
        X, y, df['Demographic_Group'], test_size=0.3, random_state=42
    )

    print("\n2. Training AI Machine Learning Model (Random Forest)...")
    # Initialize our AI model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train the model on the data
    model.fit(X_train, y_train)
    print("   ✅ AI Model trained successfully!")
    
    print("\n3. Generating predictions on unseen test patients...")
    predictions = model.predict(X_test)
    
    overall_acc = accuracy_score(y_test, predictions)
    print(f"   Standard Accuracy Metric: {overall_acc * 100:.2f}%")
    print("   (Standard metrics often hide demographic biases!)")
    
    # Compile the test results for our Ethical Audit tool
    results_df = pd.DataFrame({
        'PatientID': X_test.index,
        'Demographic_Group': demo_test.values,
        'Actual_Diagnosis': y_test.values,
        'AI_Prediction': predictions
    })
    
    print("\n" + "="*70)
    print(" 🚨 ROUTING AI MODEL PREDICTIONS TO ETHICS REVIEW BOARD TOOL... 🚨")
    print("="*70 + "\n")
    
    # Run the audit tool we wrote previously!
    auditor = EthicalAIAuditTool(
        data=results_df, 
        demographic_col='Demographic_Group', 
        actual_outcome_col='Actual_Diagnosis', 
        prediction_col='AI_Prediction'
    )
    auditor.generate_audit_report()

if __name__ == "__main__":
    train_and_audit_model()
