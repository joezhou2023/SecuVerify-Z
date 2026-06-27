import { useState, useCallback } from "react";
import {
  Upload, FileText, Loader2, AlertCircle, CheckCircle, XCircle,
  BookOpen,
} from "lucide-react";
import { uploadAndAudit } from "../services/api";
import { useI18n } from "../i18n/I18nContext";
import type { FileAuditResponse, FileAuditFinding } from "../types";

export default function FileUpload() {
  const { t } = useI18n();

  const [file, setFile] = useState<File | null>(null);
  const [auditScope, setAuditScope] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<FileAuditResponse | null>(null);
  const [dragOver, setDragOver] = useState(false);

  // ===== 文件上传 =====
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setResult(null);
      setError("");
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setResult(null);
      setError("");
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await uploadAndAudit(file, auditScope || undefined);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : t.file.fileError);
    } finally {
      setLoading(false);
    }
  };

  /** 单条发现中的 27002 指南展开组件 */
  function GuidancePanel({ finding }: { finding: FileAuditFinding }) {
    const [open, setOpen] = useState(false);
    if (!finding.implementation_guidance) return null;
    return (
      <div className="mt-2">
        <button
          onClick={() => setOpen(!open)}
          className="flex items-center gap-1 text-xs text-primary-600 hover:text-primary-700 font-medium"
        >
          <BookOpen className="w-3.5 h-3.5" />
          {open ? t.file.hideGuidance : t.file.showGuidance}
        </button>
        {open && (
          <div className="mt-2 bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-600 whitespace-pre-line leading-relaxed">
            <p className="font-semibold text-slate-700 mb-1">{t.file.implementationGuidance}</p>
            {finding.implementation_guidance}
          </div>
        )}
      </div>
    );
  }

  const severityConfig: Record<string, { label: string; color: string; icon: React.ReactNode }> = {
    major: { label: t.file.major, color: "bg-red-100 text-red-700 border-red-200", icon: <XCircle className="w-4 h-4" /> },
    minor: { label: t.file.minor, color: "bg-amber-100 text-amber-700 border-amber-200", icon: <AlertCircle className="w-4 h-4" /> },
    observation: { label: t.file.observation, color: "bg-blue-100 text-blue-700 border-blue-200", icon: <CheckCircle className="w-4 h-4" /> },
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* 标题 */}
        <div>
          <h2 className="text-xl font-bold text-slate-800">{t.file.title}</h2>
          <p className="text-sm text-slate-500 mt-1">{t.file.description}</p>
        </div>

        {/* 上传区 */}
        <div
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragOver ? "border-primary-400 bg-primary-50" : "border-slate-300 bg-white"
          }`}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".docx,.pdf,.xlsx,.xls,.txt,.md"
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="w-12 h-12 text-slate-400 mx-auto mb-3" />
            <p className="text-sm text-slate-600 font-medium">{t.file.uploadText}</p>
            <p className="text-xs text-slate-400 mt-1">{t.file.uploadHint}</p>
          </label>
        </div>

        {/* 已选文件 + 审核范围 */}
        {file && (
          <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-3">
            <div className="flex items-center gap-3">
              <FileText className="w-5 h-5 text-primary-600" />
              <span className="text-sm font-medium text-slate-700 flex-1">{file.name}</span>
              <span className="text-xs text-slate-400">
                {(file.size / 1024).toFixed(1)} KB
              </span>
              <button
                onClick={() => { setFile(null); setResult(null); }}
                className="text-slate-400 hover:text-red-500"
                title={t.file.remove}
              >
                ✕
              </button>
            </div>
            <input
              type="text"
              placeholder={t.file.scopePlaceholder}
              value={auditScope}
              onChange={(e) => setAuditScope(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-primary-400"
            />
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  {t.file.analyzing}
                </>
              ) : (
                t.file.analyze
              )}
            </button>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-600">
            ⚠️ {error}
          </div>
        )}

        {/* 结果 */}
        {result && (
          <div className="space-y-4 fade-in">
            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-slate-800 mb-2">📄 {t.file.summary}</h3>
              <p className="text-sm text-slate-600">{result.file_summary}</p>
            </div>

            <div className="bg-primary-50 border border-primary-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-primary-800 mb-2">📊 {t.file.overallAssessment}</h3>
              <p className="text-sm text-primary-700">{result.overall_assessment}</p>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-slate-800 mb-3">
                🔍 {t.file.findings}（{result.findings.length} {t.file.itemCount}）
              </h3>
              <div className="space-y-3">
                {result.findings.map((finding, idx) => {
                  const sev = severityConfig[finding.severity];
                  return (
                    <div key={idx} className="border border-slate-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="px-2 py-0.5 bg-slate-100 text-slate-600 text-xs font-mono rounded">
                            {finding.clause_number}
                          </span>
                          <span className="text-sm font-medium text-slate-700">
                            {finding.requirement}
                          </span>
                        </div>
                        <span className={`flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded border ${sev.color} flex-shrink-0`}>
                          {sev.icon}
                          {sev.label}
                        </span>
                      </div>
                      <div className="text-xs text-slate-500 space-y-1 mt-2">
                        <p><span className="font-medium text-slate-600">{t.file.currentStatus}</span>{finding.current_status}</p>
                        <p><span className="font-medium text-slate-600">{t.file.gap}</span>{finding.gap}</p>
                      </div>
                      <GuidancePanel finding={finding} />
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-slate-800 mb-3">💡 {t.file.recommendations}</h3>
              <ul className="space-y-2">
                {result.recommendations.map((rec, idx) => (
                  <li key={idx} className="text-sm text-slate-600 flex items-start gap-2">
                    <span className="text-primary-500 font-bold flex-shrink-0">{idx + 1}.</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
