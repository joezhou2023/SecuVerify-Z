import { useState } from "react";
import { Search, Loader2, Tag, CheckCircle, XCircle, AlertCircle, BookOpen } from "lucide-react";
import { matchClauses } from "../services/api";
import { useI18n } from "../i18n/I18nContext";
import type { ClauseMatchResponse, ClauseMatchResult } from "../types";

export default function ClauseMatcher() {
  const { t } = useI18n();
  const [finding, setFinding] = useState("");
  const [findingType, setFindingType] = useState("observation");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ClauseMatchResponse | null>(null);
  const [error, setError] = useState("");

  const handleMatch = async () => {
    if (!finding.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await matchClauses(finding, findingType);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : t.clause.matchError);
    } finally {
      setLoading(false);
    }
  };

  const judgmentConfig = {
    [t.clause.conforming]: { color: "bg-green-100 text-green-700 border-green-200", icon: <CheckCircle className="w-4 h-4" /> },
    [t.clause.nonConforming]: { color: "bg-red-100 text-red-700 border-red-200", icon: <XCircle className="w-4 h-4" /> },
    [t.clause.observationItem]: { color: "bg-blue-100 text-blue-700 border-blue-200", icon: <AlertCircle className="w-4 h-4" /> },
  };

  const relevanceConfig = {
    high: "bg-red-50 text-red-600",
    medium: "bg-amber-50 text-amber-600",
    low: "bg-slate-50 text-slate-500",
  };

  const relevanceText: Record<string, string> = {
    high: t.clause.highRelevance,
    medium: t.clause.mediumRelevance,
    low: t.clause.lowRelevance,
  };

  const examples = [
    "组织已制定信息安全方针，但方针未包含持续改进的承诺",
    "员工离职后其系统访问权限未及时收回，存在未授权访问风险",
    "机房未安装温湿度监控设备，无法及时发现环境异常",
    "组织未定期进行信息安全风险评估，上次评估为两年前",
  ];

  /** 单条匹配结果中的 27002 指南展开组件 */
  function GuidancePanel({ item }: { item: ClauseMatchResult }) {
    const [open, setOpen] = useState(false);
    if (!item.implementation_guidance) return null;
    return (
      <div className="mt-2">
        <button
          onClick={() => setOpen(!open)}
          className="flex items-center gap-1 text-xs text-primary-600 hover:text-primary-700 font-medium"
        >
          <BookOpen className="w-3.5 h-3.5" />
          {open ? t.clause.hideGuidance : t.clause.showGuidance}
        </button>
        {open && (
          <div className="mt-2 bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-600 whitespace-pre-line leading-relaxed">
            <p className="font-semibold text-slate-700 mb-1">{t.clause.implementationGuidance}</p>
            {item.implementation_guidance}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* 标题 */}
        <div>
          <h2 className="text-xl font-bold text-slate-800">{t.clause.title}</h2>
          <p className="text-sm text-slate-500 mt-1">{t.clause.description}</p>
        </div>

        {/* 输入区 */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-4">
          <div>
            <label className="text-sm font-medium text-slate-700 block mb-2">
              {t.clause.findingLabel}
            </label>
            <textarea
              value={finding}
              onChange={(e) => setFinding(e.target.value)}
              placeholder={t.clause.findingPlaceholder}
              rows={4}
              className="w-full px-4 py-3 text-sm border border-slate-200 rounded-lg resize-none focus:outline-none focus:border-primary-400"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 block mb-2">
              {t.clause.typeLabel}
            </label>
            <div className="flex gap-2">
              {[
                { value: "observation", label: t.clause.observation },
                { value: "nonconformity", label: t.clause.nonconformity },
              ].map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setFindingType(opt.value)}
                  className={`px-4 py-2 text-sm rounded-lg border transition-colors ${
                    findingType === opt.value
                      ? "bg-primary-600 text-white border-primary-600"
                      : "bg-white text-slate-600 border-slate-200 hover:border-primary-300"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleMatch}
            disabled={!finding.trim() || loading}
            className="w-full py-2.5 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                {t.clause.analyzing}
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                {t.clause.match}
              </>
            )}
          </button>
        </div>

        {/* 示例 */}
        {!result && !loading && (
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-2">💡 {t.clause.examplesTitle}</p>
            <div className="space-y-1">
              {examples.map((ex, idx) => (
                <button
                  key={idx}
                  onClick={() => setFinding(ex)}
                  className="block w-full text-left text-sm text-slate-600 hover:text-primary-600 px-3 py-1.5 rounded hover:bg-white transition-colors"
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-600">
            ⚠️ {error}
          </div>
        )}

        {/* 匹配结果 */}
        {result && (
          <div className="space-y-4 fade-in">
            {/* 总体摘要 */}
            <div className="bg-primary-50 border border-primary-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-primary-800 mb-1">📋 {t.clause.summary}</h3>
              <p className="text-sm text-primary-700">{result.summary}</p>
            </div>

            {/* 逐条结果 */}
            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <h3 className="text-sm font-bold text-slate-800 mb-3">
                {t.clause.details}（{result.results.length} {t.clause.itemCount}）
              </h3>
              <div className="space-y-3">
                {result.results.map((item, idx) => {
                  const judg = judgmentConfig[item.judgment] || judgmentConfig[t.clause.observationItem];
                  const rel = relevanceConfig[item.relevance] || relevanceConfig.low;
                  return (
                    <div key={idx} className="border border-slate-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Tag className="w-4 h-4 text-slate-400" />
                        <span className="px-2 py-0.5 bg-slate-100 text-slate-600 text-xs font-mono rounded">
                          {item.clause_number}
                        </span>
                        <span className="text-sm font-medium text-slate-700 flex-1">
                          {item.clause_title}
                        </span>
                        <span className={`px-2 py-0.5 text-xs rounded ${rel}`}>
                          {relevanceText[item.relevance] || relevanceText.low}
                        </span>
                        <span className={`flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded border ${judg.color}`}>
                          {judg.icon}
                          {item.judgment}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 leading-relaxed">
                        {item.reasoning}
                      </p>
                      <GuidancePanel item={item} />
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
