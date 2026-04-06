import { motion } from "framer-motion";
import { Copy, Check, Database, BookOpen, X } from "lucide-react";
import { useState } from "react";
import type { ChatMessage } from "@/lib/mockApi";

interface Props {
  message: ChatMessage | null;
  onClose?: () => void;
}

function RadialScore({ label, score }: { label: string; score: number }) {
  const pct = Math.round(score * 100);
  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (score * circumference);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-24 h-24">
        <svg className="w-24 h-24 -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="hsl(var(--muted))" strokeWidth="6" />
          <circle
            cx="50" cy="50" r="40" fill="none"
            stroke="hsl(var(--primary))"
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-semibold text-foreground">{pct}%</span>
        </div>
      </div>
      <span className="text-xs text-muted-foreground font-medium">{label}</span>
    </div>
  );
}

function SqlBlock({ sql }: { sql: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          <Database className="w-3.5 h-3.5" />
          SQL Query
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors px-2 py-1 rounded-md hover:bg-muted/50"
        >
          {copied ? <Check className="w-3 h-3 text-primary" /> : <Copy className="w-3 h-3" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="bg-muted/60 rounded-lg p-3 text-xs font-mono text-secondary-foreground overflow-x-auto">
        <code>{sql}</code>
      </pre>
    </div>
  );
}

export function DiagnosticsSidebar({ message, onClose }: Props) {
  if (!message || message.role === "user") {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <p className="text-sm text-muted-foreground text-center">
          Send a message to see AI pipeline diagnostics here.
        </p>
      </div>
    );
  }

  const { route, ragasScores, sqlExecution } = message;
  const showRagas = route === "EXPLANATORY" || route === "HYBRID";
  const showSql = route === "ANALYTICAL" || route === "HYBRID";

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      className="h-full overflow-y-auto p-5 space-y-6"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-foreground">Pipeline Diagnostics</h3>
        {onClose && (
          <button onClick={onClose} className="lg:hidden p-1 rounded-md hover:bg-muted/50 transition-colors">
            <X className="w-4 h-4 text-muted-foreground" />
          </button>
        )}
      </div>

      <div className="glass-subtle rounded-lg px-3 py-2">
        <span className="text-xs text-muted-foreground">Route</span>
        <div className="flex items-center gap-2 mt-1">
          <span className={`inline-block w-2 h-2 rounded-full ${
            route === "ANALYTICAL" ? "bg-blue-400" : route === "EXPLANATORY" ? "bg-primary" : "bg-amber-400"
          }`} />
          <span className="text-sm font-medium text-foreground">{route}</span>
        </div>
      </div>

      {showRagas && ragasScores && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            <BookOpen className="w-3.5 h-3.5" />
            RAGAS Evaluation
          </div>
          <div className="glass-subtle rounded-lg p-4 flex justify-around">
            <RadialScore label="Faithfulness" score={ragasScores.faithfulness} />
            <RadialScore label="Answer Relevance" score={ragasScores.answer_relevance} />
          </div>
        </div>
      )}

      {showSql && sqlExecution && <SqlBlock sql={sqlExecution} />}
    </motion.div>
  );
}
