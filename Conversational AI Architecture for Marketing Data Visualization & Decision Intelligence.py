export default function ConversationalAIMarketingArchitecture() {
  const layers = [
    {
      title: "User Interaction Layer",
      components: [
        "Marketing Dashboard UI",
        "Voice/Text Query Interface",
        "Executive Reporting Panel",
        "Mobile Analytics Interface",
      ],
    },
    {
      title: "Conversational AI Layer",
      components: [
        "Natural Language Processing (NLP)",
        "Intent Recognition Engine",
        "Context Memory Management",
        "Prompt Orchestration Engine",
        "Recommendation Generator",
      ],
    },
    {
      title: "Analytics Intelligence Layer",
      components: [
        "Predictive Analytics Models",
        "Campaign Attribution Engine",
        "Customer Segmentation AI",
        "Behavioral Analytics Engine",
        "Marketing KPI Analyzer",
      ],
    },
    {
      title: "Visualization Layer",
      components: [
        "Dynamic Dashboard Generator",
        "Real-Time Chart Engine",
        "Heatmap & Funnel Visualizer",
        "Narrative Insight Generator",
        "Executive Storytelling Module",
      ],
    },
    {
      title: "Data Integration Layer",
      components: [
        "CRM Integration",
        "Social Media APIs",
        "Ad Platform Connectors",
        "Website Analytics Pipelines",
        "Customer Data Platform (CDP)",
      ],
    },
    {
      title: "Infrastructure & Storage Layer",
      components: [
        "Cloud Data Warehouse",
        "Vector Database",
        "Real-Time Stream Processing",
        "Data Lake",
        "MLOps Deployment Infrastructure",
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Conversational AI Architecture
          </h1>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto">
            AI-Powered Marketing Data Visualization & Decision Intelligence System
          </p>
        </div>

        <div className="grid gap-8">
          {layers.map((layer, index) => (
            <div key={index} className="relative">
              <div className="bg-white rounded-3xl shadow-2xl border border-gray-200 overflow-hidden">
                <div className="bg-black text-white px-8 py-5">
                  <h2 className="text-2xl font-bold">{layer.title}</h2>
                </div>

                <div className="grid md:grid-cols-5 gap-6 p-8">
                  {layer.components.map((component, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-50 rounded-2xl p-5 border border-gray-200 hover:shadow-lg transition-all duration-300"
                    >
                      <div className="text-center">
                        <div className="w-12 h-12 rounded-full bg-black text-white flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                          {idx + 1}
                        </div>
                        <h3 className="font-semibold text-gray-900 text-sm leading-relaxed">
                          {component}
                        </h3>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {index !== layers.length - 1 && (
                <div className="flex justify-center py-4">
                  <div className="w-1 h-12 bg-black rounded-full"></div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-200">
            <h3 className="text-2xl font-bold mb-4 text-gray-900">
              Core AI Workflow
            </h3>
            <ul className="space-y-3 text-gray-700">
              <li>• User asks marketing-related question</li>
              <li>• NLP engine interprets business intent</li>
              <li>• AI queries integrated marketing datasets</li>
              <li>• Predictive models analyze patterns</li>
              <li>• Visualization engine generates insights</li>
              <li>• Conversational AI explains findings</li>
            </ul>
          </div>

          <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-200">
            <h3 className="text-2xl font-bold mb-4 text-gray-900">
              Marketing Intelligence Features
            </h3>
            <ul className="space-y-3 text-gray-700">
              <li>• Campaign performance prediction</li>
              <li>• Customer churn forecasting</li>
              <li>• Audience segmentation analysis</li>
              <li>• Real-time anomaly detection</li>
              <li>• Cross-channel attribution modeling</li>
              <li>• ROI optimization recommendations</li>
            </ul>
          </div>

          <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-200">
            <h3 className="text-2xl font-bold mb-4 text-gray-900">
              Recommended Technology Stack
            </h3>
            <ul className="space-y-3 text-gray-700">
              <li>• Frontend: React + Next.js</li>
              <li>• AI: OpenAI / LangChain</li>
              <li>• Database: PostgreSQL + Pinecone</li>
              <li>• Visualization: D3.js + Recharts</li>
              <li>• Cloud: AWS / Azure / GCP</li>
              <li>• Streaming: Apache Kafka</li>
            </ul>
          </div>
        </div>

        <div className="mt-16 bg-black text-white rounded-3xl p-10 shadow-2xl">
          <h2 className="text-3xl font-bold mb-6 text-center">
            Example Conversational Flow
          </h2>

          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="font-bold text-lg mb-3">1. User Query</h3>
              <p className="text-sm text-gray-300">
                “Why did our Meta Ads conversion rate drop in Q2?”
              </p>
            </div>

            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="font-bold text-lg mb-3">2. AI Analysis</h3>
              <p className="text-sm text-gray-300">
                AI detects audience fatigue and rising CPC trends.
              </p>
            </div>

            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="font-bold text-lg mb-3">3. Visualization</h3>
              <p className="text-sm text-gray-300">
                Dynamic charts, heatmaps, and funnel analytics generated.
              </p>
            </div>

            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="font-bold text-lg mb-3">4. Recommendation</h3>
              <p className="text-sm text-gray-300">
                AI suggests budget redistribution and creative refresh.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
