"""Pydantic 数据模型定义"""
from typing import Optional
from pydantic import BaseModel, Field


# ===== 对话审核 =====
class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色: user / assistant / system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="对话历史")
    audit_context: Optional[str] = Field(None, description="审核上下文（如审核范围、受审核部门等）")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI 回复内容")
    clause_refs: Optional[list[str]] = Field(None, description="引用的 ISO 27001 条款号")


# ===== 条款匹配 =====
class ClauseMatchRequest(BaseModel):
    finding: str = Field(..., description="审核发现描述")
    finding_type: Optional[str] = Field("observation", description="发现类型: observation / nonconformity")


class ClauseMatchResult(BaseModel):
    clause_number: str = Field(..., description="条款号")
    clause_title: str = Field(..., description="条款标题")
    relevance: str = Field(..., description="相关性: high / medium / low")
    judgment: str = Field(..., description="符合性判断: 符合 / 不符合 / 观察项")
    reasoning: str = Field(..., description="判断理由")
    implementation_guidance: Optional[str] = Field(None, description="ISO/IEC 27002:2022 实施指南摘要")


class ClauseMatchResponse(BaseModel):
    results: list[ClauseMatchResult]
    summary: str = Field(..., description="总体判断摘要")


# ===== 文件审核 =====
class FileAuditRequest(BaseModel):
    file_content: str = Field(..., description="文件提取的文本内容")
    file_name: str = Field(..., description="文件名")
    audit_scope: Optional[str] = Field(None, description="审核范围")


class FileAuditFinding(BaseModel):
    clause_number: str = Field(..., description="相关条款号")
    requirement: str = Field(..., description="标准要求")
    current_status: str = Field(..., description="文件中体现的现状")
    gap: str = Field(..., description="差距分析")
    severity: str = Field(..., description="严重程度: major / minor / observation")
    implementation_guidance: Optional[str] = Field(None, description="ISO/IEC 27002:2022 实施指南摘要")


class FileAuditResponse(BaseModel):
    file_summary: str = Field(..., description="文件内容摘要")
    findings: list[FileAuditFinding]
    overall_assessment: str = Field(..., description="总体评估")
    recommendations: list[str] = Field(..., description="改进建议")


# ===== 审核记录（文字输入模式）=====
class AuditRecordTextRequest(BaseModel):
    clause_number: str = Field(..., description="条款号（如 A.5.1 或 5.2）")
    text_content: str = Field(..., description="审核员提供的文字信息（现场观察、文件记录、访谈内容等）")
    audit_scope: Optional[str] = Field(None, description="审核范围（可选）")


class AuditRecordResponse(BaseModel):
    clause_number: str = Field(..., description="条款号")
    clause_title: str = Field(..., description="条款标题")
    standard_requirement: str = Field(..., description="标准要求")
    audit_method: str = Field(..., description="审核方法（文件审查/访谈/观察/抽样等）")
    audit_evidence: str = Field(..., description="审核证据（基于输入信息的客观描述）")
    conformity_judgment: str = Field(..., description="符合性判定: 符合 / 不符合 / 观察项")
    judgment_explanation: str = Field(..., description="判定说明（对照标准要求的分析论证）")
    improvement_suggestions: list[str] = Field(..., description="改进建议")
    implementation_guidance: Optional[str] = Field(None, description="ISO/IEC 27002:2022 实施指南摘要")
