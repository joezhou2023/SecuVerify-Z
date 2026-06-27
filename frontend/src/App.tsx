import { useState } from "react";
import { Shield, X } from "lucide-react";
import ChatPanel from "./components/ChatPanel";
import FileUpload from "./components/FileUpload";
import ClauseMatcher from "./components/ClauseMatcher";
import AuditRecordPanel from "./components/AuditRecordPanel";
import LanguageToggle from "./components/LanguageToggle";
import { changelog } from "./data/changelog";
import { useI18n } from "./i18n/I18nContext";

type Tab = "chat" | "file" | "clause" | "record";

export default function App() {
  const { t } = useI18n();
  const [activeTab, setActiveTab] = useState<Tab>("chat");
  const [showHistory, setShowHistory] = useState(false);

  const latestVersion = changelog[0].version;

  const tabs: { id: Tab; label: string; icon: React.ReactNode }[] = [
    { id: "chat", label: t.tabs.chat, icon: <ChatIcon /> },
    { id: "file", label: t.tabs.file, icon: <FileIcon /> },
    { id: "record", label: t.tabs.record, icon: <RecordIcon /> },
    { id: "clause", label: t.tabs.clause, icon: <MatchIcon /> },
  ];

  return (
    <div className="flex h-screen bg-slate-50">
      {/* 侧边栏 */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        {/* Logo 区域 */}
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold">{t.app.title}</h1>
              <p className="text-xs text-slate-400">{t.app.subtitle}</p>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-3">{t.app.description}</p>
        </div>

        {/* 导航 */}
        <nav className="flex-1 p-4 space-y-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? "bg-primary-600 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </nav>

        {/* 底部信息 */}
        <div className="p-4 border-t border-slate-700 text-xs text-slate-500 space-y-2">
          <div className="flex items-center justify-between">
            <span>{t.app.standard}</span>
            <LanguageToggle />
          </div>
          <p className="flex items-center gap-1">
            <button
              type="button"
              onClick={() => setShowHistory(true)}
              className="hover:text-slate-300 underline decoration-dotted cursor-pointer"
            >
              v{latestVersion}
            </button>
            <span>|</span>
            <span>{t.app.poweredBy}</span>
            <a
              href="https://www.joezhou.top"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-300 underline decoration-dotted"
            >
              Joezhou
            </a>
          </p>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 overflow-hidden">
        {activeTab === "chat" && <ChatPanel />}
        {activeTab === "file" && <FileUpload />}
        {activeTab === "record" && <AuditRecordPanel />}
        {activeTab === "clause" && <ClauseMatcher />}
      </main>

      {/* 版本历史弹窗 */}
      {showHistory && <HistoryModal onClose={() => setShowHistory(false)} />}
    </div>
  );
}

function HistoryModal({ onClose }: { onClose: () => void }) {
  const { t } = useI18n();

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg rounded-xl bg-white shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b px-6 py-4">
          <h2 className="text-lg font-bold text-slate-800">{t.app.versionHistory}</h2>
          <button
            type="button"
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="max-h-[60vh] overflow-y-auto px-6 py-4 space-y-6">
          {changelog.map((entry) => (
            <div key={entry.version}>
              <div className="flex items-baseline gap-3">
                <span className="text-base font-bold text-primary-600">
                  v{entry.version}
                </span>
                <span className="text-xs text-slate-400">{entry.date}</span>
              </div>
              <ul className="mt-2 list-disc pl-5 text-sm text-slate-600 space-y-1">
                {entry.changes.map((change, idx) => (
                  <li key={idx}>{change}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ChatIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  );
}

function FileIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );
}

function MatchIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
    </svg>
  );
}

function RecordIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
    </svg>
  );
}
