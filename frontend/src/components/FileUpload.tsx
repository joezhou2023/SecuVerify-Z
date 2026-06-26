import { useState, useCallback } from "react";
import {
  Upload, FileText, Loader2, AlertCircle, CheckCircle, XCircle,
  BookOpen, FileSearch, ClipboardList, ChevronDown, ChevronUp,
} from "lucide-react";
import { uploadAndAudit, generateAuditRecord } from "../services/api";
import { useI18n } from "../i18n/I18nContext";
import type { FileAuditResponse, FileAuditFinding, AuditRecord } from "../types";

type Mode = "gap" | "record";

export default function FileUpload() {
  const { t } = useI18n();

  // ===== 共享状态 =====
  const [mode, setMode] = useState<Mode>("gap");
  const [auditScope, setAuditScope] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ===== 差距分析模式 =====
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<FileAuditResponse | null>(null);
  const [dragOver, setDragOver] = useState(false);

  // ===== 审核记录模式 =====
  const [clauseNumber, setClauseNumber] = useState("");
  const [textContent, setTextContent] = useState("");
  const [record, setRecord] = useState<AuditRecord | null>(null);
  const [guidanceOpen, setGuidanceOpen] = useState(false);
  const [recordFile, setRecordFile] = useState<File | null>(null);
  const [recordDragOver, setRecordDragOver] = useState(false);

  // ===== 模式切换 =====
  const switchMode = (m: Mode) => {
    setMode(m);
    setError("");
    setResult(null);
    setRecord(null);
    setRecordFile(null);
  };

  // ===== 差距分析：文件上传 =====
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

  // ===== 审核记录：文件拖拽上传 =====
  const handleRecordDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setRecordDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setRecordFile(droppedFile);
    }
  }, []);

  const handleRecordFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setRecordFile(selected);
    }
  };

  // ===== 审核记录：生成（文件 + 文字） =====
  const handleGenerateRecord = async () => {
    if (!clauseNumber.trim() || !textContent.trim()) return;
    setLoading(true);
    setError("");
    setRecord(null);
    try {
      const res = await generateAuditRecord(
        clauseNumber.trim(),
        textContent,
        auditScope || undefined,
        recordFile
      );
      setRecord(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : t.file.recordError);
    } finally {
      setLoading(false);
    }
  };

  /** 差距分析：单条发现中的 27002 指南展开组件 */
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

  const judgmentConfig: Record<string, { color: string; icon: React.ReactNode }> = {
    "符合": { color: "bg-green-100 text-green-700 border-green-200", icon: <CheckCircle className="w-4 h-4" /> },
    "不符合": { color: "bg-red-100 text-red-700 border-red-200", icon: <XCircle className="w-4 h-4" /> },
    "观察项": { color: "bg-amber-100 text-amber-700 border-amber-200", icon: <AlertCircle className="w-4 h-4" /> },
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* 标题 */}
        <div>
          <h2 className="text-xl font-bold text-slate-800">{t.file.title}</h2>
          <p className="text-sm text-slate-500 mt-1">{t.file.description}</p>
        </div>

        {/* 模式切换 */}
        <div className="flex gap-2 p-1 bg-slate-100 rounded-xl">
          <button
            onClick={() => switchMode("gap")}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-medium transition-colors ${
              mode === "gap"
                ? "bg-white text-primary-700 shadow-sm"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            <FileSearch className="w-4 h-4" />
            {t.file.modeGap}
          </button>
          <button
            onClick={() => switchMode("record")}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-medium transition-colors ${
              mode === "record"
                ? "bg-white text-primary-700 shadow-sm"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            <ClipboardList className="w-4 h-4" />
            {t.file.modeRecord}
          </button>
        </div>

        {/* ==================== 差距分析模式 ==================== */}
        {mode === "gap" && (
          <>
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

            {/* 差距分析结果 */}
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
          </>
        )}

        {/* ==================== 审核记录模式 ==================== */}
        {mode === "record" && (
          <>
            {/* 输入区 */}
            <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-4">
              {/* 条款号输入 */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  {t.file.clauseNumberLabel} <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  placeholder={t.file.clauseNumberPlaceholder}
                  value={clauseNumber}
                  onChange={(e) => setClauseNumber(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-primary-400 font-mono"
                />
                <p className="text-xs text-slate-400 mt-1">{t.file.clauseNumberHint}</p>
              </div>

              {/* 审核范围 */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  {t.file.scopeLabel}
                </label>
                <input
                  type="text"
                  placeholder={t.file.scopePlaceholder}
                  value={auditScope}
                  onChange={(e) => setAuditScope(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-primary-400"
                />
              </div>

              {/* 文件上传区（可选） */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  {t.file.attachmentLabel} <span className="text-xs text-slate-400 font-normal">({t.file.optional})</span>
                </label>
                {!recordFile ? (
                  <div
                    onDrop={handleRecordDrop}
                    onDragOver={(e) => { e.preventDefault(); setRecordDragOver(true); }}
                    onDragLeave={() => setRecordDragOver(false)}
                    className={`border-2 border-dashed rounded-xl p-5 text-center transition-colors cursor-pointer ${
                      recordDragOver ? "border-primary-400 bg-primary-50" : "border-slate-300 bg-slate-50 hover:border-slate-400"
                    }`}
                  >
                    <input
                      type="file"
                      id="record-file-upload"
                      className="hidden"
                      accept=".docx,.pdf,.xlsx,.xls,.txt,.md"
                      onChange={handleRecordFileChange}
                    />
                    <label htmlFor="record-file-upload" className="cursor-pointer">
                      <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                      <p className="text-xs text-slate-500 font-medium">{t.file.attachmentText}</p>
                      <p className="text-xs text-slate-400 mt-1">{t.file.attachmentHint}</p>
                    </label>
                  </div>
                ) : (
                  <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-lg p-3">
                    <FileText className="w-5 h-5 text-primary-600 flex-shrink-0" />
                    <span className="text-sm font-medium text-slate-700 flex-1 truncate">{recordFile.name}</span>
                    <span className="text-xs text-slate-400 flex-shrink-0">
                      {(recordFile.size / 1024).toFixed(1)} KB
                    </span>
                    <button
                      onClick={() => setRecordFile(null)}
                      className="text-slate-400 hover:text-red-500 flex-shrink-0"
                      title={t.file.remove}
                    >
                      ✕
                    </button>
                  </div>
                )}
              </div>

              {/* 文字描述 */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                  {t.file.textContentLabel} <span className="text-red-500">*</span>
                </label>
                <textarea
                  placeholder={t.file.textContentPlaceholder}
                  value={textContent}
                  onChange={(e) => setTextContent(e.target.value)}
                  rows={8}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-primary-400 resize-y leading-relaxed"
                />
                <p className="text-xs text-slate-400 mt-1">{t.file.textContentHint}</p>
              </div>

              {/* 生成按钮 */}
              <button
                onClick={handleGenerateRecord}
                disabled={loading || !clauseNumber.trim() || !textContent.trim()}
                className="w-full py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    {t.file.generatingRecord}
                  </>
                ) : (
                  <>
                    <ClipboardList className="w-4 h-4" />
                    {t.file.generateRecord}
                  </>
                )}
              </button>
            </div>

            {/* 错误提示 */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-600">
                ⚠️ {error}
              </div>
            )}

            {/* 审核记录结果 */}
            {record && (
              <div className="space-y-4 fade-in">
                {/* 条款头 + 判定徽章 */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-1 bg-primary-100 text-primary-700 text-sm font-mono font-bold rounded">
                        {record.clause_number}
                      </span>
                      <h3 className="text-base font-bold text-slate-800">{record.clause_title}</h3>
                    </div>
                    {judgmentConfig[record.conformity_judgment] && (
                      <span className={`flex items-center gap-1.5 px-3 py-1 text-sm font-medium rounded-full border ${judgmentConfig[record.conformity_judgment].color} flex-shrink-0`}>
                        {judgmentConfig[record.conformity_judgment].icon}
                        {record.conformity_judgment}
                      </span>
                    )}
                  </div>
                </div>

                {/* 标准要求 */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <h4 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-slate-500" />
                    {t.file.standardRequirement}
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed">{record.standard_requirement}</p>
                </div>

                {/* 审核方法 */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <h4 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-1.5">
                    <FileSearch className="w-4 h-4 text-slate-500" />
                    {t.file.auditMethod}
                  </h4>
                  <p className="text-sm text-slate-600">{record.audit_method}</p>
                </div>

                {/* 审核证据 */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <h4 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-1.5">
                    <ClipboardList className="w-4 h-4 text-slate-500" />
                    {t.file.auditEvidence}
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">{record.audit_evidence}</p>
                </div>

                {/* 判定说明 */}
                <div className={`border rounded-xl p-5 ${
                  record.conformity_judgment === "符合"
                    ? "bg-green-50 border-green-200"
                    : record.conformity_judgment === "不符合"
                    ? "bg-red-50 border-red-200"
                    : "bg-amber-50 border-amber-200"
                }`}>
                  <h4 className={`text-sm font-bold mb-2 flex items-center gap-1.5 ${
                    record.conformity_judgment === "符合"
                      ? "text-green-800"
                      : record.conformity_judgment === "不符合"
                      ? "text-red-800"
                      : "text-amber-800"
                  }`}>
                    {judgmentConfig[record.conformity_judgment]?.icon}
                    {t.file.judgmentExplanation}
                  </h4>
                  <p className={`text-sm leading-relaxed ${
                    record.conformity_judgment === "符合"
                      ? "text-green-700"
                      : record.conformity_judgment === "不符合"
                      ? "text-red-700"
                      : "text-amber-700"
                  }`}>{record.judgment_explanation}</p>
                </div>

                {/* 改进建议 */}
                {record.improvement_suggestions && record.improvement_suggestions.length > 0 && (
                  <div className="bg-white border border-slate-200 rounded-xl p-5">
                    <h4 className="text-sm font-bold text-slate-800 mb-3">💡 {t.file.improvementSuggestions}</h4>
                    <ul className="space-y-2">
                      {record.improvement_suggestions.map((suggestion, idx) => (
                        <li key={idx} className="text-sm text-slate-600 flex items-start gap-2">
                          <span className="text-primary-500 font-bold flex-shrink-0">{idx + 1}.</span>
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* ISO 27002 实施指南 */}
                {record.implementation_guidance && (
                  <div className="bg-white border border-slate-200 rounded-xl p-5">
                    <button
                      onClick={() => setGuidanceOpen(!guidanceOpen)}
                      className="flex items-center gap-1.5 text-sm font-medium text-primary-600 hover:text-primary-700"
                    >
                      {guidanceOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      <BookOpen className="w-4 h-4" />
                      {guidanceOpen ? t.file.hideGuidance : t.file.showGuidance}
                    </button>
                    {guidanceOpen && (
                      <div className="mt-3 bg-slate-50 border border-slate-200 rounded-lg p-4 text-sm text-slate-600 whitespace-pre-line leading-relaxed">
                        <p className="font-semibold text-slate-700 mb-2">{t.file.implementationGuidance}</p>
                        {record.implementation_guidance}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
