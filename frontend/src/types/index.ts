/** 类型定义 */

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatResponse {
  reply: string;
  clause_refs?: string[];
}

export interface ClauseMatchResult {
  clause_number: string;
  clause_title: string;
  relevance: "high" | "medium" | "low";
  judgment: "符合" | "不符合" | "观察项";
  reasoning: string;
  implementation_guidance?: string;
}

export interface ClauseMatchResponse {
  results: ClauseMatchResult[];
  summary: string;
}

export interface FileAuditFinding {
  clause_number: string;
  requirement: string;
  current_status: string;
  gap: string;
  severity: "major" | "minor" | "observation";
  implementation_guidance?: string;
}

export interface FileAuditResponse {
  file_summary: string;
  findings: FileAuditFinding[];
  overall_assessment: string;
  recommendations: string[];
}

/** 审核记录（文字输入模式） */
export interface AuditRecord {
  clause_number: string;
  clause_title: string;
  standard_requirement: string;
  audit_method: string;
  audit_evidence: string;
  conformity_judgment: "符合" | "不符合" | "观察项";
  judgment_explanation: string;
  improvement_suggestions: string[];
  implementation_guidance?: string;
}

export interface ISOClauses {
  clauses: ClauseInfo[];
}

export interface ClauseInfo {
  number: string;
  title: string;
  requirement: string;
  source: string;
  theme: string;
  attribute?: string;
}
