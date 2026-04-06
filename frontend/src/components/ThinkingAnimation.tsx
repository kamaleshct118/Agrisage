import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const steps = [
  { emoji: "🚜", text: "Analyzing Intent..." },
  { emoji: "📊", text: "Scanning SQL Database..." },
  { emoji: "📚", text: "Searching Knowledge Base..." },
  { emoji: "🌾", text: "Synthesizing Advice..." },
];

export function ThinkingAnimation() {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent((c) => (c + 1) % steps.length);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-start gap-3 px-4 py-3">
      <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
        <span className="text-sm">🤖</span>
      </div>
      <div className="glass-subtle rounded-xl px-4 py-3 min-w-[200px]">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.25 }}
            className="flex items-center gap-2 text-sm text-muted-foreground"
          >
            <span className="text-base">{steps[current].emoji}</span>
            <span>{steps[current].text}</span>
          </motion.div>
        </AnimatePresence>
        <div className="flex gap-1 mt-2">
          {steps.map((_, i) => (
            <div
              key={i}
              className={`h-1 rounded-full transition-all duration-300 ${
                i <= current ? "bg-primary w-6" : "bg-muted w-4"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
