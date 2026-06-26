"""条款匹配与符合性判断路由"""
from fastapi import APIRouter, HTTPException
from models.schemas import ClauseMatchRequest, ClauseMatchResponse
from services.llm_service import chat_completion_json, get_system_prompt
from services.knowledge_manager import km

router = APIRouter()


@router.post("", response_model=ClauseMatchResponse)
async def match_clauses(request: ClauseMatchRequest):
    """
    条款匹配与符合性判断 — 输入审核发现，自动匹配 ISO 27001 条款并判断符合性
    """
    system_prompt = get_system_prompt()
    knowledge = km.get_summary()

    user_prompt = f"""请对以下审核发现进行 ISO/IEC 27001:2022 条款匹配和符合性判断。

## 审核发现
{request.finding}

## 发现类型
{request.finding_type}

## 请按以下 JSON 格式返回分析结果：
{{
    "results": [
        {{
            "clause_number": "匹配的ISO 27001条款号",
            "clause_title": "条款标题",
            "relevance": "相关性: high / medium / low",
            "judgment": "符合性判断: 符合 / 不符合 / 观察项",
            "reasoning": "判断理由（引用标准要求进行论证）"
        }}
    ],
    "summary": "总体判断摘要"
}}

匹配规则：
1. 优先匹配附录 A 控制措施（A.5-A.8），其次匹配正文条款（4-10）
2. 可以匹配多个条款，但按相关性排序
3. judgment 判断标准：
   - 符合：审核发现表明组织已有效实施该条款要求
   - 不符合：审核发现表明组织未实施或实施不满足条款要求
   - 观察项：审核发现提示潜在风险，但不构成不符合
4. reasoning 必须引用条款的具体要求进行对比分析"""

    result = chat_completion_json(
        messages=[
            {"role": "system", "content": system_prompt + "\n\n" + knowledge},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=4096,
    )

    # 为每个 Annex A 匹配结果附加 ISO 27002 实施指南
    if isinstance(result, dict) and "results" in result:
        km.attach_guidance_to_matches(result["results"])

    return result


@router.get("/clauses")
async def list_all_clauses():
    """列出所有 ISO 27001 条款（供前端展示和选择）"""
    return {"clauses": km.get_all_clauses()}


@router.get("/clauses/{clause_number}/guidance")
async def get_clause_guidance(clause_number: str):
    """获取指定 Annex A 控制项的 ISO/IEC 27002:2022 实施指南"""
    clause = km.get_clause(clause_number)
    if not clause:
        raise HTTPException(status_code=404, detail=f"未找到条款: {clause_number}")
    guidance = km.get_guidance(clause_number.upper())
    if not guidance:
        raise HTTPException(status_code=404, detail=f"未找到该条款的实施指南: {clause_number}")
    return {
        "clause_number": clause_number.upper(),
        "clause_title": clause.get("title", ""),
        "guidance": guidance,
    }


@router.get("/clauses/{clause_number}")
async def get_clause_detail(clause_number: str):
    """获取指定条款的详情"""
    clause = km.get_clause(clause_number)
    if not clause:
        raise HTTPException(status_code=404, detail=f"未找到条款: {clause_number}")
    return clause
