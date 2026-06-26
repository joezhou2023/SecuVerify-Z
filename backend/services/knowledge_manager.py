"""
知识库统一管理器 — 所有 Router 的唯一知识库调用入口

架构三层分离：
  Router 层  →  KnowledgeManager（本模块）  →  知识源（iso27001 / iso27002 / 未来扩展）

新增知识源时只需在本模块注册方法，Router 无需任何改动。
Phase 2（案例库）、Phase 3（向量检索）在此模块内部扩展即可。
"""

import re
from services.iso27001_knowledge import (
    get_knowledge_summary,
    get_all_clauses,
    get_clause_by_number,
    get_clause_with_guidance,
)
from services.iso27002_knowledge import (
    get_guidance_summary,
    get_guidance_by_number,
    get_all_guidance_numbers,
)


class KnowledgeManager:
    """统一知识库入口，封装所有知识源的查询与注入逻辑。

    对外提供三类能力：
    1. 条款号提取（extract_*）
    2. 知识查询（get_*）
    3. 上下文注入与结果增强（inject_* / attach_*）
    """

    # ========================================
    # 1. 条款号提取（统一正则，消除 Router 重复代码）
    # ========================================

    @staticmethod
    def extract_annex_a_numbers(text: str) -> list[str]:
        """从文本中提取 Annex A 控制项编号，归一化为 A.x.y 格式。

        支持格式：A.5.1 / A 5.1 / 附录A 5.1 / Annex A.5.1
        """
        raw = re.findall(
            r"(?:附录|Annex\s*)?[Aa]\.?\s*(\d{1,2})\.(\d{1,2})",
            text or "",
            re.IGNORECASE,
        )
        return [f"A.{m}.{n}" for m, n in raw]

    @staticmethod
    def extract_clause_refs(text: str) -> list[str]:
        """从文本中提取所有 ISO 27001 条款号（正文 4-10 + 附录 A）。

        用于 chat 路由：从用户消息或 AI 回复中提取引用的条款号。
        """
        refs = re.findall(
            r"[Aa]\.\d+\.\d+|(?<!\d)[4-9]\.\d+(?:\.\d+)?|10\.\d+",
            text or "",
        )
        return sorted(set(refs)) if refs else []

    # ========================================
    # 2. 知识查询（委托到底层知识源模块）
    # ========================================

    @staticmethod
    def get_summary() -> str:
        """获取 ISO 27001 知识库摘要文本（注入 LLM 系统提示词用）"""
        return get_knowledge_summary()

    @staticmethod
    def get_all_clauses() -> list[dict]:
        """获取所有条款列表（正文 + 附录 A）"""
        return get_all_clauses()

    @staticmethod
    def get_clause(number: str) -> dict | None:
        """按条款号查询条款详情"""
        return get_clause_by_number(number)

    @staticmethod
    def get_clause_detail(number: str) -> dict | None:
        """按条款号查询条款详情（含 ISO 27002 指南）"""
        return get_clause_with_guidance(number)

    @staticmethod
    def get_guidance(clause_number: str) -> str | None:
        """获取 Annex A 控制项的 ISO 27002 实施指南摘要文本"""
        return get_guidance_summary(clause_number.upper())

    @staticmethod
    def get_guidance_detail(clause_number: str) -> dict | None:
        """获取 Annex A 控制项的 ISO 27002 实施指南完整结构"""
        return get_guidance_by_number(clause_number.upper())

    @staticmethod
    def get_all_guidance_numbers() -> list[str]:
        """获取所有有实施指南的 Annex A 条款号"""
        return get_all_guidance_numbers()

    # ========================================
    # 3. 上下文注入（选择性注入策略）
    # ========================================

    @classmethod
    def inject_guidance(cls, text: str, system_prompt: str) -> str:
        """从 text 中提取 Annex A 条款号，将对应 27002 指南注入 system_prompt。

        用于 chat 路由：用户消息提及条款号时自动注入相关指南。
        若 text 中无 Annex A 条款号，原样返回 system_prompt。
        """
        refs = cls.extract_annex_a_numbers(text)
        if not refs:
            return system_prompt

        guidance_parts = []
        seen = set()
        for ref in refs:
            ref_key = ref.upper()
            if ref_key in seen:
                continue
            seen.add(ref_key)
            guidance = cls.get_guidance(ref_key)
            if guidance:
                guidance_parts.append(guidance)

        if guidance_parts:
            system_prompt += (
                "\n\n## 以下是与用户问题相关的 ISO/IEC 27002:2022 实施指南\n\n"
                + "\n\n".join(guidance_parts)
            )

        return system_prompt

    # ========================================
    # 4. 结果增强（为 LLM 输出附加实施指南）
    # ========================================

    @classmethod
    def attach_guidance_to_matches(cls, results: list[dict]) -> list[dict]:
        """为条款匹配结果列表中的每项附加 implementation_guidance。

        用于 clause_match 路由：LLM 返回匹配结果后调用。
        仅对包含 Annex A 条款号的结果项附加指南。
        """
        for item in results:
            refs = cls.extract_annex_a_numbers(item.get("clause_number", ""))
            if refs:
                guidance = cls.get_guidance(refs[0].upper())
                if guidance:
                    item["implementation_guidance"] = guidance
        return results

    @classmethod
    def attach_guidance_to_findings(cls, findings: list[dict]) -> list[dict]:
        """为文件审核发现列表中的每项附加 implementation_guidance。

        用于 file_audit 路由：LLM 返回分析结果后调用。
        仅对包含 Annex A 条款号的发现项附加指南。
        """
        for finding in findings:
            refs = cls.extract_annex_a_numbers(finding.get("clause_number", ""))
            if refs:
                guidance = cls.get_guidance(refs[0].upper())
                if guidance:
                    finding["implementation_guidance"] = guidance
        return findings


# 全局单例 — Router 直接 import 使用
km = KnowledgeManager()
