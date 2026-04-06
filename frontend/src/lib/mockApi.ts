export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  route?: "EXPLANATORY" | "ANALYTICAL" | "HYBRID";
  tabularData?: Record<string, string | number>[] | null;
  sqlExecution?: string | null;
  ragasScores?: { faithfulness: number; answer_relevance: number } | null;
  timestamp: Date;
}

interface ApiResponse {
  route: "EXPLANATORY" | "ANALYTICAL" | "HYBRID";
  final_answer: string;
  tabular_data: Record<string, string | number>[] | null;
  sql_execution: string | null;
  ragas_scores: { faithfulness: number; answer_relevance: number } | null;
}

const analyticalResponse: ApiResponse = {
  route: "ANALYTICAL",
  final_answer: `## Wheat Yield Analysis (2011)\n\nBased on the database records, the **wheat yield in 2011** was **3,450 kg/hectare** across the surveyed regions.\n\n### Key Findings:\n- **Punjab**: 4,200 kg/ha (highest)\n- **Haryana**: 3,800 kg/ha\n- **UP**: 2,900 kg/ha\n- **MP**: 2,900 kg/ha\n\n> This was a **12% increase** compared to 2010, largely attributed to improved irrigation coverage.`,
  tabular_data: [
    { Region: "Punjab", "Yield (kg/ha)": 4200, "Change vs 2010": "+15%" },
    { Region: "Haryana", "Yield (kg/ha)": 3800, "Change vs 2010": "+10%" },
    { Region: "Uttar Pradesh", "Yield (kg/ha)": 2900, "Change vs 2010": "+8%" },
    { Region: "Madhya Pradesh", "Yield (kg/ha)": 2900, "Change vs 2010": "+14%" },
  ],
  sql_execution: `SELECT region, yield_kg_per_ha,\n  ROUND((yield_kg_per_ha - prev_yield) / prev_yield * 100, 1) AS change_pct\nFROM crop_yields\nWHERE crop = 'wheat' AND year = 2011\nORDER BY yield_kg_per_ha DESC;`,
  ragas_scores: null,
};

const explanatoryResponse: ApiResponse = {
  route: "EXPLANATORY",
  final_answer: `## Fixing Nitrogen Deficiency in Crops 🌱\n\nNitrogen deficiency is one of the most common nutrient disorders in agricultural crops. Here's a comprehensive guide:\n\n### Symptoms to Look For\n- **Yellowing of older leaves** (chlorosis starts from the bottom)\n- Stunted growth and thin stems\n- Reduced tillering in cereals\n- Premature leaf senescence\n\n### Recommended Solutions\n\n1. **Urea Application** — Apply 46% N urea at 50-60 kg/ha as a top dressing\n2. **Ammonium Nitrate** — For quick correction, use 34% AN at 40 kg/ha\n3. **Organic Matter** — Incorporate well-decomposed FYM at 10-15 t/ha\n4. **Green Manuring** — Grow *Sesbania* or *Dhaincha* and incorporate before flowering\n\n### Prevention Tips\n> Split nitrogen application into **3 doses**: basal (50%), tillering (25%), and panicle initiation (25%) for optimal uptake efficiency.\n\n*Always conduct a **soil test** before application to determine exact deficiency levels.*`,
  tabular_data: null,
  sql_execution: null,
  ragas_scores: { faithfulness: 0.95, answer_relevance: 0.88 },
};

const hybridResponse: ApiResponse = {
  route: "HYBRID",
  final_answer: `## Soil Health & Fertilizer Recommendations 🧪\n\nBased on both our knowledge base and historical data analysis:\n\n### Database Analysis\nThe soil pH across your region has averaged **6.2** over the past 5 years, indicating *slightly acidic* conditions ideal for most crops.\n\n### Expert Recommendations\n- Apply **lime at 2-3 t/ha** if pH drops below 5.5\n- Use **DAP (18:46:0)** for phosphorus-deficient soils\n- Consider **micronutrient foliar sprays** with Zinc and Boron\n\n| Nutrient | Current Level | Optimal Range | Action |\n|----------|--------------|---------------|--------|\n| Nitrogen | Low | 280-560 kg/ha | Apply Urea |\n| Phosphorus | Medium | 23-56 kg/ha | Monitor |\n| Potassium | High | 136-336 kg/ha | No action |`,
  tabular_data: [
    { Year: 2019, "Avg pH": 6.1, "N (kg/ha)": 240, "P (kg/ha)": 35, "K (kg/ha)": 280 },
    { Year: 2020, "Avg pH": 6.0, "N (kg/ha)": 220, "P (kg/ha)": 38, "K (kg/ha)": 290 },
    { Year: 2021, "Avg pH": 6.3, "N (kg/ha)": 260, "P (kg/ha)": 32, "K (kg/ha)": 275 },
    { Year: 2022, "Avg pH": 6.2, "N (kg/ha)": 245, "P (kg/ha)": 40, "K (kg/ha)": 300 },
    { Year: 2023, "Avg pH": 6.4, "N (kg/ha)": 270, "P (kg/ha)": 36, "K (kg/ha)": 310 },
  ],
  sql_execution: `SELECT year, AVG(ph) AS avg_ph,\n  AVG(nitrogen) AS n_kg_ha,\n  AVG(phosphorus) AS p_kg_ha,\n  AVG(potassium) AS k_kg_ha\nFROM soil_tests\nWHERE region = 'central'\nGROUP BY year\nORDER BY year;`,
  ragas_scores: { faithfulness: 0.91, answer_relevance: 0.85 },
};

export async function sendMessage(
  query: string,
  _chatHistory: { role: string; content: string }[]
): Promise<ApiResponse> {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    return {
      route: (data.route as any) || "EXPLANATORY",
      final_answer: data.response,
      tabular_data: data.data || null,
      sql_execution: data.sql || null,
      ragas_scores: null,
    };
  } catch (error) {
    console.error("Error connecting to backend:", error);
    throw error;
  }
}
