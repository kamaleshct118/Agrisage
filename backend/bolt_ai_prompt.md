# Bolt AI Frontend Development Prompt (Version 2)

*Copy and paste the entire prompt below into Bolt AI. I have added crucial missing elements like Chat History, Mobile Responsiveness, and Markdown rendering.*

***

**System Context & Objective**
I am building a premium, intelligent Agriculture AI system. The backend is a Python CrewAI multi-agent application that handles both Unstructured Text (RAG via FAISS) and Structured Data (Text-to-SQL via SQLite). 
Please build a modern, high-performance React/Vite frontend application that acts as the user interface for this system.

**Aesthetic & UI Guidelines**
- **Theme**: Premium SaaS aesthetic. Implement a sleek dark mode with glassmorphism elements. Use appropriate high-contrast accent colors that fit an intelligent agricultural theme (choose the best color palette yourself, but keep it modern, minimalist, and vibrant).
- **Typography**: Clean, modern fonts (e.g., Inter or Roboto).
- **Responsiveness**: The app MUST be fully responsive. On mobile devices, the Right Sidebar must gracefully collapse into a hamburger menu or slide-over drawer, ensuring the chat interface remains usable.

**Component 1: The "Empty State" Dashboard**
When the user first opens the app and chat history is empty:
- Center a premium, glowing glassmorphism text input box in the middle of the screen.
- Directly below the input box, place 3 to 4 "Suggestion Chips" (pill-shaped buttons) with example questions (e.g., "What was the Wheat yield in 2011?", "How do I fix Nitrogen deficiency?"). Clicking a pill should immediately send that query.

**Component 2: Conversation State & Chat Interface**
- **State Management**: The app must act as a stateful chat application. Maintain a `chatHistory` array containing both User messages and AI responses so the user can scroll up and read past questions.
- **Input**: A sleek chat bar pinned to the bottom.
- **Thinking Animations**: My backend takes about 10-15 seconds to run the multi-agent pipeline. Create a dynamic loading component that displays fake sequential statuses while waiting (e.g., fading between "🚜 Analyzing Intent...", "📊 Scanning SQL Database...", "🌾 Synthesizing Advice...").
- **Output Bubbles**: 
  - Standard text outputs MUST support Markdown (use libraries like `react-markdown` and `remark-gfm`).
  - If the AI returns tabular SQL data, render it natively as a beautifully styled HTML/CSS data table or a mini bar chart, right inside the chat flow.
- **Error Handling**: Build elegant toast notifications or error bubbles if the API connection fails.

**Component 3: The Diagnostics Right Sidebar (Crucial Logic)**
This sidebar acts as an X-Ray for the AI pipeline. It must conditionally render based on the "Route" the backend took for the **most recent** AI message.
- **If the Route = "EXPLANATORY" (RAG)**: The sidebar should display a "RAGAS Evaluation" dashboard. Show two radial progress indicators or progress bars for "Faithfulness" and "Answer Relevance" (scores from 0.0 to 1.0).
- **If the Route = "ANALYTICAL" (SQL)**: The sidebar should NOT show RAGAS scores. Instead, display a "Database" module showing the raw SQL query code block that the agent executed, with a "Copy to Clipboard" button.
- **If the Route = "HYBRID"**: Show both sections.

**Mock Data & Inputs/Outputs (for development)**
Since my backend isn't connected yet, build a mock asynchronous API function that simulates a 3-second backend delay, then returns a dynamic response based on keywords in the user's input.
- **Input requested by backend**: `{ "query": "string", "chat_history": [...] }`
- **Mock Response structure**:
```json
{
  "route": "EXPLANATORY" | "ANALYTICAL" | "HYBRID",
  "final_answer": "Markdown string...",
  "tabular_data": [{"column1": "val"}], // Null if Explanatory
  "sql_execution": "SELECT * FROM...", // Null if Explanatory
  "ragas_scores": {
    "faithfulness": 0.95,
    "answer_relevance": 0.88
  } // Null if Analytical
}
```

Please generate the complete React application with Tailwind CSS (or Vanilla CSS) using `lucide-react` for icons and `framer-motion` for smooth UI transitions matching this exact specification.
