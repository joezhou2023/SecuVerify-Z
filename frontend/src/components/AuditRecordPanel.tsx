import { useState } from "react";
import { useI18n } from "../i18n/I18nContext";
import { generateAuditRecord } from "../services/api";
import type { AuditRecord } from "../types";

export default function AuditRecordPanel() {
  const { t } = useI18n();
  const [clauseNumber, setClauseNumber] = useState("");
  const [textContent, setTextContent] = useState("");
  const [auditScope, setAuditScope] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AuditRecord | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) setFile(f);
  };

  const removeFile = () => setFile(null);

  const handleGenerate = async () => {
    if (!clauseNumber.trim()) return;
    if (!textContent.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await generateAuditRecord(
        clauseNumber.trim(),
        textContent.trim(),
        auditScope.trim() || undefined,
        file
      );
      setResult(data);
    } catch {
      setError(t.file.recordError);
    } finally {
      setLoading(false);
    }
  };

  const judgmentColor = (judgment: string) => {
    switch (judgment) {
      case "符合":
        return "bg-green-100 text-green-800 border-green-300";
      case "不符合":
        return "bg-red-100 text-red-800 border-red-300";
      default:
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* 输入区域 */}
      <div className="bg-white border-b px-6 py-4">
        <h2 className="text-lg font-bold text-slate-800">
          {t.auditRecord?.title || "审核记录"}
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          {t.auditRecord?.description || "输入条款号和审核信息，AI 按标准格式自动生成审核记录"}
        </p>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="p-6 space-y-4">
          {/* 条款号 */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {t.file.clauseNumberLabel}
            </label>
            <input
              type="text"
              value={clauseNumber}
              onChange={(e) => setClauseNumber(e.target.value)}
              placeholder={t.file.clauseNumberPlaceholder}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
            <p className="text-xs text-slate-400 mt-1">{t.file.clauseNumberHint}</p>
          </div>

          {/* 审核范围 */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {t.file.scopeLabel}
            </label>
            <input
              type="text"
              value={auditScope}
              onChange={(e) => setAuditScope(e.target.value)}
              placeholder={t.file.scopePlaceholder}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          {/* 审核信息描述 */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {t.file.textContentLabel}
            </label>
            <textarea
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              placeholder={t.file.textContentPlaceholder}
              rows={6}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-y"
            />
            <p className="text-xs text-slate-400 mt-1">{t.file.textContentHint}</p>
          </div>

          {/* 附件上传 */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {t.file.attachmentLabel}
              <span className="text-xs text-slate-400 ml-1">({t.file.optional})</span>
            </label>
            {!file ? (
              <label className="flex flex-col items-center justify-center h-24 border-2 border-dashed border-slate-300 rounded-lg cursor-pointer hover:border-primary-400 transition-colors">
                <svg className="w-6 h-6 text-slate-400 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span className="text-xs text-slate-400">{t.file.attachmentText}</span>
                <input type="file" accept=".docx,.pdf,.xlsx,.txt" className="hidden" onChange={handleFileChange} />
              </label>
            ) : (
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 rounded-lg border border-slate-200">
                <svg className="w-4 h-4 text-slate-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm text-slate-600 truncate flex-1">{file.name}</span>
                <span className="text-xs text-slate-400">({(file.size / 1024).toFixed(0)} KB)</span>
                <button onClick={removeFile} className="text-slate-400 hover:text-red-500 text-sm ml-1">&times;</button>
              </div>
            )}
            <p className="text-xs text-slate-400 mt-1">{t.file.attachmentHint}</p>
          </div>

          {/* 生成按钮 */}
          <button
            onClick={handleGenerate}
            disabled={loading || !clauseNumber.trim() || !textContent.trim()}
            className="w-full py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? t.file.generatingRecord : t.file.generateRecord}
          </button>

          {/* 默认判定提示 */}
          <div className="flex items-start gap-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-700">
            <svg className="w-4 h-4 text-blue-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{t.auditRecord?.defaultHint || "默认输出为符合性判定。如需输出观察项或不符合项，请在审核信息描述中明确指出。"}</span>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {error}
            </div>
          )}

          {/* 结果 — 核心：可直接使用的审核记录 */}
          {result && (
            <div className="space-y-3">
              {/* ====== 可直接复制的审核记录 ====== */}
              <div className="border border-primary-300 rounded-lg overflow-hidden">
                {/* 审核依据头：条款号 + 标题 + 判定 */}
                <div className="flex items-center gap-3 px-4 py-3 bg-primary-700 text-white">
                  <span className="text-xs font-bold uppercase tracking-wider text-primary-200">
                    {t.auditRecord?.clause || "审核依据"}
                  </span>
                  <span className="font-mono font-bold text-base">{result.clause_number}</span>
                  <span className="text-sm text-primary-100 flex-1 truncate">{result.clause_title}</span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${judgmentColor(result.conformity_judgment)}`}>
                    {result.conformity_judgment}
                  </span>
                </div>

                {/* 检查或跟踪记录 — 核心证据 */}
                <div className="px-4 py-3 bg-white border-b border-slate-200">
                  <div className="text-xs text-slate-500 font-bold mb-1.5">
                    {t.auditRecord?.colRecord || "检查或跟踪记录"}
                  </div>
                  <div className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">
                    {result.audit_evidence}
                  </div>
                </div>

                {/* 判定说明 */}
                <div className={`px-4 py-3 border-b border-slate-200 ${
                  result.conformity_judgment === "符合"
                    ? "bg-green-50"
                    : result.conformity_judgment === "不符合"
                    ? "bg-red-50"
                    : "bg-amber-50"
                }`}>
                  <div className={`text-xs font-bold mb-1 ${
                    result.conformity_judgment === "符合"
                      ? "text-green-800"
                      : result.conformity_judgment === "不符合"
                      ? "text-red-800"
                      : "text-amber-800"
                  }`}>
                    {t.auditRecord?.judgmentLabel || "判定说明"}
                  </div>
                  <div className={`text-sm leading-relaxed whitespace-pre-wrap ${
                    result.conformity_judgment === "符合"
                      ? "text-green-700"
                      : result.conformity_judgment === "不符合"
                      ? "text-red-700"
                      : "text-amber-700"
                  }`}>
                    {result.judgment_explanation}
                  </div>
                </div>

                {/* 改进建议 */}
                {result.improvement_suggestions && result.improvement_suggestions.length > 0 && (
                  <div className="px-4 py-3 bg-white">
                    <div className="text-xs text-slate-500 font-bold mb-1.5">
                      {t.auditRecord?.improveLabel || "改进建议"}
                    </div>
                    <ul className="list-disc pl-4 text-sm text-slate-700 space-y-0.5">
                      {result.improvement_suggestions.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* ====== 参考信息（折叠放置） ====== */}
              <details className="group border border-slate-200 rounded-lg">
                <summary className="flex items-center gap-2 px-4 py-2.5 bg-slate-50 cursor-pointer text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg">
                  <svg className={`w-4 h-4 transition-transform group-open:rotate-90`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  参考信息（标准要求、审核方法、27002 指南）
                </summary>
                <div className="px-4 py-3 space-y-3 border-t border-slate-200">
                  {/* 标准要求 */}
                  <div>
                    <div className="text-xs text-slate-500 font-bold mb-1">{t.file.standardRequirement}</div>
                    <div className="text-sm text-slate-600 whitespace-pre-wrap leading-relaxed">{result.standard_requirement}</div>
                  </div>
                  {/* 审核方法 */}
                  <div className="pt-2 border-t border-slate-100">
                    <div className="text-xs text-slate-500 font-bold mb-1">{t.auditRecord?.methodLabel || "审核方法"}</div>
                    <div className="text-sm text-slate-600">{result.audit_method}</div>
                  </div>
                  {/* 27002 指南 */}
                  {result.implementation_guidance && (
                    <div className="pt-2 border-t border-slate-100">
                      <div className="text-xs text-slate-500 font-bold mb-1">{t.file.implementationGuidance}</div>
                      <div className="text-sm text-slate-600 whitespace-pre-wrap leading-relaxed">{result.implementation_guidance}</div>
                    </div>
                  )}
                </div>
              </details>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
