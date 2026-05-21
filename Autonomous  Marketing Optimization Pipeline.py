import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import beta
from plotly.subplots import make_subplots

# =====================================================================
# 1. LIVE SIMULATION ENVIRONMENT (The Marketplace)
# =====================================================================
class LiveAdMarketplace:
    """
    Simulates a live advertising marketplace (like Meta or Google Ads auctions).
    Each variant has a hidden, true conversion rate that the AI must discover.
    """
    def __init__(self):
        # True conversion rates hidden from the optimization engine
        self._true_conversion_rates = {
            "Variant_A (Static Image)": 0.022,   # 2.2% CR
            "Variant_B (Short Video)":  0.045,   # 4.5% CR (The true winner)
            "Variant_C (User Gen Content)": 0.038, # 3.8% CR
            "Variant_D (Carousel Ad)":   0.015    # 1.5% CR
        }
        self.variants = list(self._true_conversion_rates.keys())

    def simulate_impressions(self, variant, budget_allocated):
        """Simulates traffic generation and conversions based on assigned budget."""
        cost_per_impression = 0.05  # $0.05 CPM baseline scale
        impressions = int(budget_allocated / cost_per_impression)
        
        if impressions <= 0:
            return 0, 0
            
        # Binomial trial modeling live consumer actions
        true_cr = self._true_conversion_rates[variant]
        conversions = np.random.binomial(impressions, true_cr)
        
        return impressions, conversions

# =====================================================================
# 2. AUTONOMOUS OPTIMIZATION ENGINE (Thompson Sampling Bandit)
# =====================================================================
class AutonomousBudgetOptimizer:
    """
    An agentic Thompson Sampling optimizer that models budget exploitation vs. exploration.
    It updates a Beta distribution profile for each variant to autonomously shift weight.
    """
    def __init__(self, variants):
        self.variants = variants
        # Initialize priors: Alpha (Successes) and Beta (Failures) at 1 (Uniform distribution)
        self.alpha_vectors = {v: 1 for v in variants}
        self.beta_vectors = {v: 1 for v in variants}
        
    def update_beliefs(self, variant, successes, total_trials):
        """Updates the statistical probability distribution based on fresh pipeline results."""
        failures = total_trials - successes
        self.alpha_vectors[variant] += successes
        self.beta_vectors[variant] += failures

    def allocate_next_budget_cycle(self, total_cycle_budget):
        """
        Autonomously samples from performance distributions to allocate the next 
        round of budget. Variants with higher probability vectors receive more weight.
        """
        samples = {}
        for v in self.variants:
            # Draw a random sample from the current belief distribution space
            samples[v] = np.random.beta(self.alpha_vectors[v], self.beta_vectors[v])
            
        # Softmax-style normalization to distribute the specific budget envelope
        total_sample_score = sum(samples.values())
        allocations = {v: (samples[v] / total_sample_score) * total_cycle_budget for v in self.variants}
        return allocations

# =====================================================================
# 3. PIPELINE ORCHESTRATION & STATE HISTORY
# =====================================================================
def run_optimization_pipeline(marketplace, optimizer, total_cycles=10, budget_per_cycle=1000):
    print("[Pipeline] Initiating autonomous closed-loop optimization run...")
    history_records = []
    
    for cycle in range(1, total_cycles + 1):
        # 1. Autonomous Engine computes the next budget allocation matrix
        current_allocations = optimizer.allocate_next_budget_cycle(budget_per_cycle)
        
        # 2. Deploy budget to the marketplace and extract telemetry logs
        for variant, budget in current_allocations.items():
            impressions, conversions = marketplace.simulate_impressions(variant, budget)
            
            # 3. Feed runtime metrics back into the model parameters
            optimizer.update_beliefs(variant, conversions, impressions)
            
            # Calculate running conversion rate
            observed_cr = conversions / impressions if impressions > 0 else 0
            
            history_records.append({
                "cycle": cycle,
                "variant": variant,
                "budget_deployed": budget,
                "impressions_generated": impressions,
                "conversions_attained": conversions,
                "observed_conversion_rate": observed_cr
            })
            
    print("[Pipeline] Optimization runtime complete. Performance graphs compiled.")
    return pd.DataFrame(history_records)

# =====================================================================
# 4. MODERN PERFORMANCE VISUALIZATION
# =====================================================================
def render_optimization_dashboard(df, optimizer):
    """
    Renders an optimization control center visualizing the budget re-allocation vectors 
    and the statistical narrowing of probability densities over time.
    """
    print("[Visualization] Spawning Autonomous Optimization Dashboard...")
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            'Autonomous Budget Shift Over Time (Exploitation Phase Tracking)',
            'Optimizer Inner State: Probability Density Estimates of Conversion Efficiency'
        ),
        vertical_spacing=0.15
    )

    # Plot 1: Stacked Budget Allocation Trends (Top Panel)
    # Shows how the AI autonomously starves underperforming ads and rewards the winner
    for variant in df['variant'].unique():
        variant_data = df[df['variant'] == variant]
        fig.add_trace(
            go.Scatter(
                x=variant_data['cycle'], 
                y=variant_data['budget_deployed'],
                mode='lines+markers',
                name=variant,
                stackgroup='one' # Makes it a clean scannable stream plot
            ),
            row=1, col=1
        )
    fig.update_xaxes(title_text="Optimization Run Cycle (Time Sequence)", row=1, col=1)
    fig.update_yaxes(title_text="Budget Deployed ($)", row=1, col=1)

    # Plot 2: Final Beta Distributions (Bottom Panel)
    # Reflects the system's calculated uncertainty profiles
    x_axis_range = np.linspace(0, 0.06, 500) # Mapping up to 6% Conversion Rate bounds
    for variant in optimizer.variants:
        a = optimizer.alpha_vectors[variant]
        b = optimizer.beta_vectors[variant]
        y_pdf = beta.pdf(x_axis_range, a, b)
        
        fig.add_trace(
            go.Scatter(
                x=x_axis_range, 
                y=y_pdf, 
                mode='lines', 
                fill='tozeroy',
                name=f"{variant} Belief Curve"
            ),
            row=2, col=1
        )
    fig.update_xaxes(title_text="Estimated Conversion Rate Range (Probability Space)", row=2, col=1)
    fig.update_yaxes(title_text="Confidence Density", row=2, col=1)

    # Global Style Layout Elements
    fig.update_layout(
        title_text="Autonomous AI Growth Agent: Budget Optimization & Allocation Matrix",
        template="plotly_dark",
        height=900,
        width=1100,
        showlegend=True
    )
    
    fig.show()

# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    print("--- Starting Closed-Loop Autonomous Growth Stack ---")
    
    # Initialize the real-world simulator and the AI optimizer script
    env = LiveAdMarketplace()
    ai_agent = AutonomousBudgetOptimizer(variants=env.variants)
    
    # Run the continuous integration loop
    optimization_history = run_optimization_pipeline(
        marketplace=env, 
        optimizer=ai_agent, 
        total_cycles=12, 
        budget_per_cycle=1500
    )
    
    # Render operational charts
    render_optimization_dashboard(optimization_history, ai_agent)
    
    print("--- Autonomous Asset Optimization Safely Completed ---")