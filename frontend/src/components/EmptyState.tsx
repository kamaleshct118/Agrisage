import { motion } from "framer-motion";
import { Sprout } from "lucide-react";

interface Props {
  onSend: (query: string) => void;
}

const suggestions = [
  "What was the Wheat yield in 2011?",
  "How do I fix Nitrogen deficiency?",
  "Show me soil health trends",
  "Best fertilizer for rice crops?",
];

export function EmptyState({ onSend }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-4 py-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col items-center max-w-lg w-full"
      >
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-6">
          <Sprout className="w-8 h-8 text-primary" />
        </div>
        <h1 className="text-2xl font-bold text-foreground mb-2 text-center">
          AgriSage AI
        </h1>
        <p className="text-muted-foreground text-sm text-center mb-8 max-w-sm">
          Your intelligent agriculture assistant. Ask about crop data, soil health, or farming best practices.
        </p>

        <div className="flex flex-wrap gap-2 justify-center">
          {suggestions.map((s) => (
            <motion.button
              key={s}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => onSend(s)}
              className="glass-glow rounded-full px-4 py-2.5 text-sm text-secondary-foreground hover:text-foreground transition-colors cursor-pointer"
            >
              {s}
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
