import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { sendChat } from "../services/api";
import { useI18n } from "../i18n/I18nContext";
import type { ChatMessage } from "../types";

export default function ChatPanel() {
  const { t } = useI18n();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: t.chat.welcomeMessage,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [auditContext, setAuditContext] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [messages, loading]);

  // 语言切换后更新欢迎语
  useEffect(() => {
    setMessages((prev) => {
      if (prev.length === 1 && prev[0].role === "assistant") {
        return [{ role: "assistant", content: t.chat.welcomeMessage }];
      }
      return prev;
    });
  }, [t]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: ChatMessage = { role: "user", content: input.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChat(newMessages, auditContext || undefined);
      setMessages([...newMessages, { role: "assistant", content: res.reply }]);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : t.chat.errorHeader;
      setMessages([
        ...newMessages,
        {
          role: "assistant",
          content: `⚠️ ${t.chat.errorHeader}：${errorMsg}\n\n${t.chat.backendCheck}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* 顶部工具栏 */}
      <div className="bg-white border-b border-slate-200 px-6 py-3">
        <div className="flex items-center gap-4">
          <input
            type="text"
            placeholder={t.chat.contextPlaceholder}
            value={auditContext}
            onChange={(e) => setAuditContext(e.target.value)}
            className="flex-1 px-4 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-primary-400"
          />
        </div>
      </div>

      {/* 消息列表 */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 fade-in ${
              msg.role === "user" ? "flex-row-reverse" : ""
            }`}
          >
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                msg.role === "user"
                  ? "bg-slate-200 text-slate-600"
                  : "bg-primary-600 text-white"
              }`}
            >
              {msg.role === "user" ? (
                <User className="w-5 h-5" />
              ) : (
                <Bot className="w-5 h-5" />
              )}
            </div>
            <div
              className={`max-w-[75%] rounded-xl px-4 py-3 ${
                msg.role === "user"
                  ? "bg-primary-600 text-white"
                  : "bg-white border border-slate-200"
              }`}
            >
              {msg.role === "assistant" ? (
                <div className="markdown-body text-sm text-slate-700">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              )}
            </div>
          </div>
        ))}

        {/* 加载指示器 */}
        {loading && (
          <div className="flex gap-3 fade-in">
            <div className="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center">
              <Bot className="w-5 h-5" />
            </div>
            <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 flex items-center gap-1">
              <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" style={{ animationDelay: "0s" }} />
              <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" style={{ animationDelay: "0.2s" }} />
              <span className="typing-dot w-2 h-2 bg-slate-400 rounded-full" style={{ animationDelay: "0.4s" }} />
            </div>
          </div>
        )}
      </div>

      {/* 输入区 */}
      <div className="bg-white border-t border-slate-200 px-6 py-4">
        <div className="flex gap-3 items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t.chat.inputPlaceholder}
            rows={1}
            className="flex-1 px-4 py-3 text-sm border border-slate-200 rounded-xl resize-none focus:outline-none focus:border-primary-400 max-h-32"
            style={{ minHeight: "48px" }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="w-12 h-12 bg-primary-600 text-white rounded-xl flex items-center justify-center hover:bg-primary-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            title={t.chat.send}
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
