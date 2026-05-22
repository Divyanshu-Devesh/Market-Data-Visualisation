import asyncio
import random
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================================================================
# 1. CORE AGENT COMMUNICATIONS PROTOCOL
# =====================================================================
class AgentMessage:
    """The standard communication capsule passed between system agents."""
    def __init__(self, sender, recipient, payload_type, content):
        self.sender = sender
        self.recipient = recipient
        self.payload_type = payload_type  # e.g., "MARKET_INSIGHT", "CREATIVE_BRIEF", "KPI_TELEMETRY"
        self.content = content

class MarketingAgent:
    """Abstract base class establishing agent loop mechanics and mailboxes."""
    def __init__(self, name, ecosystem):
        self.name = name
        self.ecosystem = ecosystem
        self.mailbox = asyncio.Queue()
        self.performance_logs = []

    async def send_message(self, recipient_name, payload_type, content):
        msg = AgentMessage(self.name, recipient_name, payload_type, content)
        await self.ecosystem.route_message(msg)

    async def run(self):
        """Continuous execution loop processing incoming agent mandates."""
        raise NotImplementedError("Agents must implement their own operational logic.")

# =====================================================================
# 2. SPECIALIZED MARKETING AGENT DEFINITIONS
# =====================================================================
class ResearchAgent(MarketingAgent):
    """Analyses consumer sentiment trends and issues high-value creative directions."""
    async def run(self):
        while True:
            await asyncio.sleep(1.5)
            trends = ["Sustainable Eco-Luxury", "Hyper-Personalized Tech", "Budget-Conscious Minimalist"]
            selected_trend = random.choice(trends)
            
            print(f"[{self.name}] Detected emerging consumer vector: '{selected_trend}'. Broadcasting creative brief.")
            await self.send_message("Copywriter_Agent", "CREATIVE_BRIEF", {"target_demographic": selected_trend})

class CopywriterAgent(MarketingAgent):
    """Receives creative briefs and generates copy variations tailored to the trend."""
    async def run(self):
        while True:
            msg = await self.mailbox.get()
            if msg.payload_type == "CREATIVE_BRIEF":
                demographic = msg.content["target_demographic"]
                copy_variant = f"Upgrade your lifestyle with our new {demographic} collection. Smart. Clean. Intentional."
                
                print(f"[{self.name}] Generated new ad copy matching brief: '{copy_variant[:40]}...' Routing to Media Buyer.")
                await self.send_message("Media_Buyer_Agent", "AD_ASSET", {"copy": copy_variant, "theme": demographic})
            self.mailbox.task_done()

class MediaBuyerAgent(MarketingAgent):
    """Deploys ad copy variants, tracks live conversion telemetry, and self-corrects allocation."""
    def __init__(self, name, ecosystem):
        super().__init__(name, ecosystem)
        self.portfolio_metrics = {}

    async def run(self):
        cycle = 1
        while True:
            while not self.mailbox.empty():
                msg = self.mailbox.get_nowait()
                if msg.payload_type == "AD_ASSET":
                    theme = msg.content["theme"]
                    if theme not in self.portfolio_metrics:
                        self.portfolio_metrics[theme] = {"spend": 100.0, "conversions": 5, "roas": 1.2}
                self.mailbox.task_done()

            if self.portfolio_metrics:
                print(f"[{self.name}] Cycle {cycle}: Processing marketplace performance logs...")
                total_conversions = 0
                
                for theme, metrics in list(self.portfolio_metrics.items()):
                    market_relevance_factor = 2.5 if "Tech" in theme else (1.8 if "Eco" in theme else 0.9)
                    new_conversions = int(random.poisson(metrics["spend"] * 0.03 * market_relevance_factor))
                    
                    metrics["conversions"] += new_conversions
                    metrics["spend"] += random.uniform(50, 150)
                    metrics["roas"] = (metrics["conversions"] * 25.0) / metrics["spend"]
                    total_conversions += new_conversions
                    
                    self.performance_logs.append({
                        "Cycle": cycle,
                        "Strategy_Theme": theme,
                        "Cumulative_Spend": metrics["spend"],
                        "ROAS": metrics["roas"]
                    })
                
                if len(self.portfolio_metrics) > 1:
                    best_theme = max(self.portfolio_metrics, key=lambda k: self.portfolio_metrics[k]["roas"])
                    worst_theme = min(self.portfolio_metrics, key=lambda k: self.portfolio_metrics[k]["roas"])
                    if best_theme != worst_theme and self.portfolio_metrics[worst_theme]["spend"] > 50:
                        self.portfolio_metrics[worst_theme]["spend"] *= 0.7
                        self.portfolio_metrics[best_theme]["spend"] *= 1.3
                        print(f"[{self.name}] Rebalancing Capital Allocation Matrix: Favouring -> {best_theme}")

                cycle += 1
            await asyncio.sleep(2.0)

# =====================================================================
# 3. ECOSYSTEM BUS AND CO-ORDINATION MATRIX
# =====================================================================
class MultiAgentEcosystem:
    """The central message bus routing communications and running execution threads."""
    def __init__(self):
        self.registry = {}

    def register_agent(self, agent):
        self.registry[agent.name] = agent

    async def route_message(self, message):
        if message.recipient in self.registry:
            await self.registry[message.recipient].mailbox.put(message)
        else:
            print(f"[Ecosystem Alert] Target routing destination '{message.recipient}' missing from registry.")

    async def start_runtime(self, runtime_duration=15):
        print("[Ecosystem] Spinning up collaborative agent grid...")
        tasks = [asyncio.create_task(agent.run()) for agent in self.registry.values()]
        
        await asyncio.sleep(runtime_duration)
        
        print("[Ecosystem] Orderly runtime termination triggered. Reaping agent workers.")
        for task in tasks:
            task.cancel()

# =====================================================================
# 4. MODERN VISUALIZATION PIPELINE
# =====================================================================
def compile_ecosystem_dashboard(buyer_agent):
    """Compiles operational analytical telemetry logged by the multi-agent system."""
    if not buyer_agent.performance_logs:
        print("[Error] No agent performance history detected. Run the runtime longer.")
        return
        
    df = pd.DataFrame(buyer_agent.performance_logs)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Agent Asset Spend Trajectory', 'Ecosystem Multi-Agent Efficiency Matrix (ROAS)'),
        horizontal_spacing=0.12
    )
    
    themes = df['Strategy_Theme'].unique()
    
    for theme in themes:
        theme_df = df[df['Strategy_Theme'] == theme]
        
        fig.add_trace(
            go.Scatter(x=theme_df['Cycle'], y=theme_df['Cumulative_Spend'], 
                       mode='lines+markers', name=f"{theme} Spend", line=dict(width=3)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=theme_df['Cycle'], y=theme_df['ROAS'], 
                       mode='lines+markers', name=f"{theme} ROAS", line=dict(dash='dash')),
            row=1, col=2
        )
        
    fig.update_layout(
        title="Multi-Agent AI Marketing Grid: Runtime Optimization Dashboard",
        template="plotly_dark",
        height=500,
        width=1200,
        legend_title_text="Agent Matrix Tracks"
    )
    
    fig.update_xaxes(title_text="Ecosystem Sync Cycle", row=1, col=1)
    fig.update_xaxes(title_text="Ecosystem Sync Cycle", row=1, col=2)
    fig.update_yaxes(title_text="Capital Allocated ($)", row=1, col=1)
    fig.update_yaxes(title_text="Return on Ad Spend (X)", row=1, col=2)
    
    fig.show()

# =====================================================================
# RUNTIME INVOCATION ENTRY POINT (Jupyter Compatible)
# =====================================================================
if __name__ == "__main__":
    network_grid = MultiAgentEcosystem()
    
    researcher = ResearchAgent("Market_Researcher_Agent", network_grid)
    writer = CopywriterAgent("Copywriter_Agent", network_grid)
    buyer = MediaBuyerAgent("Media_Buyer_Agent", network_grid)
    
    network_grid.register_agent(researcher)
    network_grid.register_agent(writer)
    network_grid.register_agent(buyer)
    
    # FIX: Dynamic loop detection layer to handle running Jupyter notebooks cleanly
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Jupyter/Colab are already executing an event loop. 
        # We hook our ecosystem task straight onto the existing system architecture.
        print("[Ecosystem Interface] Active event loop detected. Scheduling execution stream.")
        task = loop.create_task(network_grid.start_runtime(runtime_duration=12))
        
        # In a notebook layout, we'll wait for this task to resolve before drawing charts
        def handle_completion(fut):
            compile_ecosystem_dashboard(buyer)
        task.add_done_callback(handle_completion)
    else:
        # Standard Python terminal script fallback execution branch
        asyncio.run(network_grid.start_runtime(runtime_duration=12))
        compile_ecosystem_dashboard(buyer)