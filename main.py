from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Create the FastAPI app instance that Render is looking for
app = FastAPI()

import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

# =====================================================================
# 1. PIPELINE INGESTION (Simulating LLM Application Gateway Logs)
# =====================================================================
def fetch_llm_conversational_logs():
    """
    Simulates production JSON logs captured from an LLM marketing agent 
    (e.g., an automated product recommendation assistant).
    """
    print("[Ingestion] Fetching conversation logs from LLM Gateway...")
    
    # Mocking unstructured raw telemetry data from an LLM middleware layer
    raw_logs = [
        {"session_id": "S001", "timestamp": "2026-05-18T10:00:00", "user_prompt": "Hey, looking for a running shoe with high arch support.", "llm_response": "I recommend our CloudStrider 5, it features maximum dynamic arch support.", "prompt_tokens": 45, "completion_tokens": 32, "sentiment_score": 0.6, "topic": "Product Recommendation", "lead_captured": 0},
        {"session_id": "S001", "timestamp": "2026-05-18T10:02:15", "user_prompt": "Awesome. Do you have a discount code for first-time buyers?", "llm_response": "Yes! Use code WELCOME10 for 10% off your purchase at checkout.", "prompt_tokens": 38, "completion_tokens": 28, "sentiment_score": 0.9, "topic": "Pricing & Discounts", "lead_captured": 1},
        {"session_id": "S002", "timestamp": "2026-05-18T10:15:22", "user_prompt": "Your checkout page is broken, it won't accept my credit card.", "llm_response": "I apologize for the frustration. Let me connect you directly to our billing support team.", "prompt_tokens": 42, "completion_tokens": 25, "sentiment_score": -0.7, "topic": "Technical Issue", "lead_captured": 0},
        {"session_id": "S003", "timestamp": "2026-05-18T11:05:00", "user_prompt": "What is your return policy? Is shipping free?", "llm_response": "Returns are completely free within 30 days. Standard shipping is free on orders over $50.", "prompt_tokens": 30, "completion_tokens": 24, "sentiment_score": 0.1, "topic": "Shipping & Returns", "lead_captured": 0},
        {"session_id": "S003", "timestamp": "2026-05-18T11:08:40", "user_prompt": "Perfect, can you sign me up for updates so I don't miss new drops?", "llm_response": "I'd love to! Please type your email address and I will add you to our VIP list.", "prompt_tokens": 48, "completion_tokens": 30, "sentiment_score": 0.8, "topic": "Lead Generation", "lead_captured": 1},
        {"session_id": "S004", "timestamp": "2026-05-18T11:45:10", "user_prompt": "Do you have leather jackets?", "llm_response": "We currently specialize purely in athletic footwear and activewear.", "prompt_tokens": 22, "completion_tokens": 18, "sentiment_score": -0.1, "topic": "Out of Scope Query", "lead_captured": 0}
    ]
    
    return pd.DataFrame(raw_logs)

# =====================================================================
# 2. TRANSFORMATION LAYER (Conversational Metric Derivation)
# =====================================================================
def transform_conversational_data(df):
    """
    Processes unstructured logs to map business/marketing value metrics.
    Calculates cost models based on token usage and groups marketing intents.
    """
    print("[Transformation] Computing operational LLM cost and marketing KPIs...")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Financial Modeling (e.g., GPT-4o pricing assumptions per 1K tokens)
    PROMPT_COST_PER_1K = 0.005
    COMPLETION_COST_PER_1K = 0.015
    
    df['prompt_cost'] = (df['prompt_tokens'] / 1000) * PROMPT_COST_PER_1K
    df['completion_cost'] = (df['completion_tokens'] / 1000) * COMPLETION_COST_PER_1K
    df['total_interaction_cost'] = df['prompt_cost'] + df['completion_cost']
    
    # Categorize User Mood based on Semantic Sentiment Analyzers
    df['sentiment_category'] = pd.cut(
        df['sentiment_score'], 
        bins=[-1.0, -0.2, 0.2, 1.0], 
        labels=['Frustrated/Negative', 'Neutral', 'Satisfied/Positive']
    )
    
    return df

# =====================================================================
# 3. ANALYTICAL LAYER (Aggregation & Semantic Insights)
# =====================================================================
def generate_summary_metrics(df):
    """Computes high-level analytics KPIs for executive marketing reporting."""
    summary = {
        "total_interactions": len(df),
        "total_cost": df['total_interaction_cost'].sum(),
        "leads_generated": df['lead_captured'].sum(),
        "conversion_rate": (df['lead_captured'].sum() / df['session_id'].nunique()) * 100,
        "avg_sentiment": df['sentiment_score'].mean()
    }
    return summary

# =====================================================================
# 4. MODERN VISUALIZATION DASHBOARD
# =====================================================================
def render_llm_analytics_dashboard(df, summary):
    """
    Compiles a comprehensive dark-themed dashboard covering financial metrics, 
    marketing intent, and user satisfaction.
    """
    print("[Visualization] Rendering Interactive Conversational Dashboard...")
    
    # Create subplots grid
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Marketing Intent / Topic Distribution', 
            'User Sentiment Profile',
            'Financial Cost Breakdown by Conversational Intent',
            'Pipeline Executive Summary'
        ),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "domain"}]]
    )
    
    # Plot 1: Topic Distribution (Top Left)
    topic_counts = df['topic'].value_counts().reset_index()
    fig.add_trace(
        go.Bar(x=topic_counts['topic'], y=topic_counts['count'], marker_color='#636EFA', name="Volume"),
        row=1, col=1
    )
    
    # Plot 2: Sentiment Categories (Top Right)
    sentiment_counts = df['sentiment_category'].value_counts().reset_index()
    fig.add_trace(
        go.Pie(
            labels=sentiment_counts['sentiment_category'], 
            values=sentiment_counts['count'], 
            hole=0.4, 
            name="Sentiment",
            marker=dict(colors=px.colors.qualitative.Pastel)  # Fixed properties array mapping block
        ),
        row=1, col=2
    )
    
    # Plot 3: Cumulative Cost by Topic (Bottom Left)
    cost_by_topic = df.groupby('topic')['total_interaction_cost'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=cost_by_topic['topic'], y=cost_by_topic['total_interaction_cost'], marker_color='#EF553B', name="Cost ($)"),
        row=2, col=1
    )
    
    # Plot 4: Executive Key Performance Metrics (Bottom Right)
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=summary['conversion_rate'],
            number={'suffix': "% Log Conv"},
            title={"text": "Lead Conversion Performance"},
            domain={'x': [0.6, 0.95], 'y': [0.0, 0.4]}
        ),
        row=2, col=2
    )

    # Global Style Adjustments
    fig.update_layout(
        title_text="AI Agent Marketplace & Conversational Intelligence Dashboard",
        template="plotly_dark",
        showlegend=False,
        height=800,
        width=1100
    )
    
    fig.show()

# =====================================================================
# PIPELINE EXECUTION ENGINE
# =====================================================================
if __name__ == "__main__":
    print("--- Starting Modern LLM Analytics Processing Pipeline ---")
    
    # 1. Extraction / Telemetry Ingestion
    raw_telemetry = fetch_llm_conversational_logs()
    
    # 2. Schema Transformation & Cost Engineering
    transformed_analytics = transform_conversational_data(raw_telemetry)
    
    # 3. High-level metric aggregation
    executive_summary = generate_summary_metrics(transformed_analytics)
    
    # 4. Fire BI Render UI Engine
    render_llm_analytics_dashboard(transformed_analytics, executive_summary)
    
    print("--- Conversational Pipeline Successfully Finalized ---")

# No Indentation for the route below:

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # This runs your existing pipeline when someone loads the page
    raw_logs =fetch_llm_conversational_logs()
    df = transform_conversational_data(raw_logs)

    # Simple placeholder response for testing
    return f"<h1>Dashboard Data Processed Successfully!</h1><p>Total Records: {len(df)}</p>"
