import axios from "axios";
import type {
  ChatMessage,
  ChatResponse,
  ClauseMatchResponse,
  FileAuditResponse,
  ISOClauses,
  AuditRecord,
} from "../types";

const api = axios.create({
  baseURL: "/api",
  timeout: 120000,
});

/** 对话式审核 */
export async function sendChat(
  messages: ChatMessage[],
  auditContext?: string
): Promise<ChatResponse> {
  const { data } = await api.post<ChatResponse>("/chat", {
    messages,
    audit_context: auditContext,
  });
  return data;
}

/** 条款匹配 */
export async function matchClauses(
  finding: string,
  findingType: string = "observation"
): Promise<ClauseMatchResponse> {
  const { data } = await api.post<ClauseMatchResponse>("/clause-match", {
    finding,
    finding_type: findingType,
  });
  return data;
}

/** 文件上传审核 */
export async function uploadAndAudit(
  file: File,
  auditScope?: string
): Promise<FileAuditResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (auditScope) {
    formData.append("audit_scope", auditScope);
  }
  const { data } = await api.post<FileAuditResponse>(
    "/file-audit/upload",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );
  return data;
}

/** 获取所有条款 */
export async function getAllClauses(): Promise<ISOClauses> {
  const { data } = await api.get<ISOClauses>("/clause-match/clauses");
  return data;
}

/** 获取指定 Annex A 控制项的 ISO 27002 实施指南 */
export async function getClauseGuidance(clauseNumber: string): Promise<{
  clause_number: string;
  clause_title: string;
  guidance: string;
}> {
  const { data } = await api.get(`/clause-match/clauses/${clauseNumber}/guidance`);
  return data;
}

/** 生成审核记录（支持文件附件 + 文字描述） */
export async function generateAuditRecord(
  clauseNumber: string,
  textContent: string,
  auditScope?: string,
  file?: File | null
): Promise<AuditRecord> {
  const formData = new FormData();
  formData.append("clause_number", clauseNumber);
  formData.append("text_content", textContent);
  if (auditScope) {
    formData.append("audit_scope", auditScope);
  }
  if (file) {
    formData.append("file", file);
  }
  const { data } = await api.post<AuditRecord>(
    "/file-audit/audit-record",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );
  return data;
}
