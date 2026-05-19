import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

# =====================================================================
# 1. FEATURE INGESTION LAYER (Live Marketing Events Stream)
# =====================================================================
def ingest_predictive_features():
    """
    Simulates ingestion of behavioral features from a Customer Data Platform (CDP).
    These features serve as the input vector for predictive marketing models.
    """
    print("[Ingestion] Fetching behavioral feature vectors from CDP...")
    
    # Simulating a batch of customers with their engineering feature markers
    raw_features = [
        {"customer_id": "CU-101", "days_since_last_purchase": 4,  "total_purchases_30d": 5, "web_sessions_7d": 12, "avg_cart_value": 85.50},
        {"customer_id": "CU-102", "days_since_last_purchase": 45, "total_purchases_30d": 0, "web_sessions_7d": 1,  "avg_cart_value": 22.00},
        {"customer_id": "CU-103", "days_since_last_purchase": 12, "total_purchases_30d": 2, "web_sessions_7d": 8,  "avg_cart_value": 150.00},
        {"customer_id": "CU-104", "days_since_last_purchase": 60, "total_purchases_30d": 0, "web_sessions_7d": 0,  "avg_cart_value": 45.10},
        {"customer_id": "CU-105", "days_since_last_purchase": 1,  "total_purchases_30d": 9, "web_sessions_7d": 24, "avg_cart_value": 310.00},
        {"customer_id": "CU-106", "days_since_last_purchase": 18, "total_purchases_30d": 1, "web_sessions_7d": 4,  "avg_cart_value": 65.00}
    ]
    return pd.DataFrame(raw_features)

# =====================================================================
# 2. PREDICTIVE INFERENCE ENGINE (Model Scoring Layer)
# =====================================================================
class MarketingPredictiveModel:
    """
    Simulates a deployed machine learning model artifact (e.g., XGBoost or LightGBM).
    Ingests processed feature vectors and outputs scored propensity arrays.
    """
    def __init__(self, model_version="v2.4.1"):
        self.model_version = model_version
        print(f"[Model Registry] Initialized Predictive Model Model: {self.model_version}")

    def predict_churn_propensity(self, df):
        """Calculates a 0.0 - 1.0 probability score of a customer churning."""
        # Math calculation simulating a logistic regression curve or tree split
        # Churn probability scale increases with higher recency gaps and lower web activity
        score = 1 / (1 + np.exp(-(-2.0 + 0.08 * df['days_since_last_purchase'] - 0.3 * df['web_sessions_7d'])))
        return np.clip(score, 0.0, 1.0)

    def predict_lifetime_value(self, df):
        """Predicts expected spend over the next 180 days (pCLV)."""
        # Linear/Log weighting representing customer value velocity scaling
        predicted_clv = (df['total_purchases_30d'] * df['avg_cart_value'] * 1.5) + (df['web_sessions_7d'] * 5)
        # Add baseline value for quiet accounts
        predicted_clv = np.where(predicted_clv == 0, df['avg_cart_value'] * 0.4, predicted_clv)
        return np.round(predicted_clv, 2)

    def assign_next_best_action(self, churn_prob, pclv):
        """Algorithmic decision tree assigning marketing treatment tags."""
        if churn_prob > 0.70 and pclv > 100:
            return "High-Value Winback Offer (VIP Support)"
        elif churn_prob > 0.50:
            return "Re-engagement Email Campaign"
        elif pclv > 250:
            return "Premium Tier Upsell Cross-Sell"
        else:
            return "Standard Content Newsletter"

# =====================================================================
# 3. TRANSFORMATION LAYER (Inference Processing & Aggregation)
# =====================================================================
def run_predictive_pipeline(df, model):
    """
    Orchestrates the conversion of engineering raw features 
    into an enriched predictive intelligence dataframe.
    """
    print("[Pipeline Processing] Generating live model predictions...")
    
    # Execute Model Functions
    df['churn_probability'] = model.predict_churn_propensity(df)
    df['predicted_clv_180d'] = model.predict_lifetime_value(df)
    
    # Vectorized assignment for Next Best Action marketing treatments
    df['next_best_action'] = df.apply(
        lambda row: model.assign_next_best_action(row['churn_probability'], row['predicted_clv_180d']), 
        axis=1
    )
    
    df['inference_timestamp'] = datetime.now()
    return df

# =====================================================================
# 4. MODERN MODERN VISUALIZATION DASHBOARD
# =====================================================================
def render_predictive_dashboard(df, model_version):
    """
    Renders an MLOps & Marketing Operations dashboard analyzing 
    model audience distributions and financial risk vectors.
    """
    print("[Visualization] Generating Predictive Model Intelligence Dashboard...")
    
    # Initialize modern multi-panel visualization layout
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Customer Churn Propensity Distribution',
            'Predicted CLV (180d) vs Churn Risk Scatter Matrix',
            'Next Best Action (NBA) Recommended Marketing Strategy',
            'Model Evaluation Metrics Summarization'
        ),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "bar"}, {"type": "domain"}]]
    )

    # Plot 1: Churn Probability Bar Graph (Top Left)
    fig.add_trace(
        go.Bar(
            x=df['customer_id'], 
            y=df['churn_probability'], 
            marker=dict(color=df['churn_probability'], colorscale='RdYlGn_r'),
            name="Churn Risk"
        ),
        row=1, col=1
    )
    fig.update_yaxes(title_text="Probability Score (0-1)", row=1, col=1)

    # Plot 2: Segment Matrix Scatter (Top Right)
    fig.add_trace(
        go.Scatter(
            x=df['predicted_clv_180d'], 
            y=df['churn_probability'],
            mode='markers+text',
            text=df['customer_id'],
            textposition="top center",
            marker=dict(size=14, color='#19D3BF', line=dict(width=2, color='white')),
            name="Profiles"
        ),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Predicted CLV ($)", row=1, col=2)
    fig.update_yaxes(title_text="Churn Probability", row=1, col=2)

    # Plot 3: Marketing Action Stratification (Bottom Left)
    nba_counts = df['next_best_action'].value_counts().reset_index()
    fig.add_trace(
        go.Bar(
            x=nba_counts['count'], 
            y=nba_counts['next_best_action'], 
            orientation='h',
            marker=dict(color='#636EFA'),
            name="Campaign Count"
        ),
        row=2, col=1
    )

    # Plot 4: Operational Key Summary Metrics (Bottom Right)
    total_at_risk_value = df[df['churn_probability'] > 0.50]['predicted_clv_180d'].sum()
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total_at_risk_value,
            number={'prefix': "$", 'valueformat': ".2f"},
            title={"text": "Total Revenue At Churn Risk (Prob > 0.5)"}
        ),
        row=2, col=2
    )

    # Unified Layout Stylings
    fig.update_layout(
        title_text=f"Predictive Intelligence Optimization Center (Model Build Reference: {model_version})",
        template="plotly_dark",
        showlegend=False,
        height=850,
        width=1200
    )
    
    fig.show()

# =====================================================================
# PIPELINE EXECUTION ENGINE
# =====================================================================
if __name__ == "__main__":
    print("--- Starting Modern Predictive Intelligence Pipeline ---")
    
    # 1. Feature Ingestion Layer Execution
    feature_matrix = ingest_predictive_features()
    
    # 2. Instantiate Deployed Model Framework from MLOps Registry
    active_model = MarketingPredictiveModel(model_version="v2.4.1")
    
    # 3. Execute Transformation & Generate Machine Learning Inference
    enriched_predictions = run_predictive_pipeline(feature_matrix, active_model)
    
    # Print clean analytical console readout 
    print("\n--- Processed Predictive Intelligence Output Array ---")
    print(enriched_predictions[['customer_id', 'churn_probability', 'predicted_clv_180d', 'next_best_action']])
    print("------------------------------------------------------\n")
    
    # 4. Fire Presentation UI Render Plot Engine
    render_predictive_dashboard(enriched_predictions, active_model.model_version)
    
    print("--- Predictive Data Pipeline Finished Successfully ---")