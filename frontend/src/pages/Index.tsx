import { useState, useRef, useEffect, useCallback } from "react";
import { PanelRightOpen, PanelRightClose, Sprout } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { EmptyState } from "@/components/EmptyState";
import { ChatInput } from "@/components/ChatInput";
import { ChatMessage } from "@/components/ChatMessage";
import { ThinkingAnimation } from "@/components/ThinkingAnimation";
import { DiagnosticsSidebar } from "@/components/DiagnosticsSidebar";
import { sendMessage, type ChatMessage as ChatMessageType } from "@/lib/mockApi";
import { toast } from "sonner";

export default function Index() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant") ?? null;

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
    }, 50);
  }, []);

  useEffect(scrollToBottom, [messages, loading, scrollToBottom]);

  const handleSend = async (query: string) => {
    const userMsg: ChatMessageType = {
      id: crypto.randomUUID(),
      role: "user",
      content: query,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const history = [...messages, userMsg].map((m) => ({
        role: m.role,
        content: m.content,
      }));
      const res = await sendMessage(query, history);

      const aiMsg: ChatMessageType = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: res.final_answer,
        route: res.route,
        tabularData: res.tabular_data,
        sqlExecution: res.sql_execution,
        ragasScores: res.ragas_scores,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
      setSidebarOpen(true);
    } catch {
      toast.error("Failed to connect to AI backend. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const isEmpty = messages.length === 0 && !loading;

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="h-14 border-b border-border/50 glass flex items-center justify-between px-4 shrink-0 z-20">
        <div className="flex items-center gap-2">
          <Sprout className="w-5 h-5 text-primary" />
          <span className="font-semibold text-foreground text-sm">AgriSage AI</span>
        </div>
        {lastAssistant && (
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground"
          >
            {sidebarOpen ? <PanelRightClose className="w-5 h-5" /> : <PanelRightOpen className="w-5 h-5" />}
          </button>
        )}
      </header>

      <div className="flex-1 flex overflow-hidden relative">
        {/* Chat area */}
        <div className="flex-1 flex flex-col min-w-0">
          {isEmpty ? (
            <EmptyState onSend={handleSend} />
          ) : (
            <div ref={scrollRef} className="flex-1 overflow-y-auto py-4 space-y-1">
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
              {loading && <ThinkingAnimation />}
            </div>
          )}
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>

        {/* Sidebar - desktop */}
        <AnimatePresence>
          {sidebarOpen && (
            <motion.aside
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 320, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="hidden lg:block border-l border-border/50 bg-card/40 overflow-hidden shrink-0"
            >
              <DiagnosticsSidebar message={lastAssistant} />
            </motion.aside>
          )}
        </AnimatePresence>

        {/* Sidebar - mobile overlay */}
        <AnimatePresence>
          {sidebarOpen && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setSidebarOpen(false)}
                className="lg:hidden fixed inset-0 bg-background/60 backdrop-blur-sm z-30"
              />
              <motion.aside
                initial={{ x: "100%" }}
                animate={{ x: 0 }}
                exit={{ x: "100%" }}
                transition={{ type: "spring", damping: 25, stiffness: 300 }}
                className="lg:hidden fixed right-0 top-14 bottom-0 w-[85vw] max-w-[360px] bg-card border-l border-border/50 z-40"
              >
                <DiagnosticsSidebar message={lastAssistant} onClose={() => setSidebarOpen(false)} />
              </motion.aside>
            </>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
