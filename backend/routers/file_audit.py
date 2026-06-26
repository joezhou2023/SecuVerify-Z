"""文件审核与分析路由"""
import os
import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.file_parser import parse_file
from services.llm_service import chat_completion_json, get_system_prompt
from services.knowledge_manager import km

router = APIRouter()

MAX_SIZE = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20")) * 1024 * 1024


@router.post("/upload")
async def upload_and_audit(
    file: UploadFile = File(...),
    audit_scope: str = Form(default=None),
):
    """
    上传文件并自动进行 ISMS 审核分析
    支持 docx / pdf / xlsx / txt 格式
    """
    # 验证文件大小
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail=f"文件大小超过限制（{MAX_SIZE // 1024 // 1024}MB）")

    # 保存临时文件
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # 解析文件
        file_text = parse_file(tmp_path)
        if not file_text.strip():
            raise HTTPException(status_code=422, detail="文件内容为空或无法提取文本")

        # 截断过长内容（避免超出 LLM token 限制）
        max_chars = 15000
        if len(file_text) > max_chars:
            file_text = file_text[:max_chars] + "\n\n[... 文件内容已截断 ...]"

        # 调用 LLM 进行审核分析
        system_prompt = get_system_prompt(audit_scope)
        knowledge = km.get_summary()

        user_prompt = f"""请对以下文件进行 ISO/IEC 27001:2022 信息安全管理体系审核分析。

## 文件名
{file.filename}

## 文件内容
{file_text}

## 审核范围
{audit_scope or "未指定（请根据文件内容自行判断）"}

## 请按以下 JSON 格式返回分析结果：
{{
    "file_summary": "文件内容摘要（100-200字）",
    "findings": [
        {{
            "clause_number": "相关ISO 27001条款号（如 A.5.1 或 5.2）",
            "requirement": "该条款的标准要求简述",
            "current_status": "文件中体现的当前现状",
            "gap": "与标准要求的差距分析",
            "severity": "严重程度: major / minor / observation"
        }}
    ],
    "overall_assessment": "总体评估（文件与ISMS要求的符合程度）",
    "recommendations": ["改进建议1", "改进建议2", ...]
}}

分析要求：
1. 每个 finding 必须引用具体的 ISO 27001 条款号
2. severity 判断标准：major=严重不符合（缺失关键控制）、minor=一般不符合（存在但不足）、observation=观察项（建议改进）
3. 至少识别 3-5 个 findings
4. 重点关注：信息分类、访问控制、加密、事件管理、供应商管理等控制措施
5. 可参考 ISO/IEC 27002:2022 实施指南提出改进建议"""

        result = chat_completion_json(
            messages=[
                {"role": "system", "content": system_prompt + "\n\n" + knowledge},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
        )

        # 为每个 Annex A 相关发现附加 ISO 27002 实施指南
        if isinstance(result, dict) and "findings" in result:
            km.attach_guidance_to_findings(result["findings"])

        return result

    finally:
        # 清理临时文件
        os.unlink(tmp_path)


@router.post("/audit-record")
async def generate_audit_record(
    clause_number: str = Form(..., description="条款号（如 A.5.1 或 5.2）"),
    text_content: str = Form(..., description="审核员提供的文字信息"),
    audit_scope: str = Form(default=None, description="审核范围（可选）"),
    file: UploadFile = File(default=None, description="可选：受审核方的制度文件/记录等附件"),
):
    """
    生成审核记录 — 支持文件附件 + 文字描述混合输入

    审核员提供条款号 + 现场观察/文件记录/访谈内容等文字信息，
    可选上传受审核方文件作为补充证据，系统综合两者生成标准化审核记录。
    """
    clause_num = clause_number.strip()

    # 查找条款详情
    clause = km.get_clause(clause_num)
    if not clause:
        raise HTTPException(
            status_code=404,
            detail=f"未找到条款: {clause_num}，请输入有效的 ISO 27001 条款号（如 A.5.1 或 5.2）",
        )

    # 获取 ISO 27002 实施指南（仅 Annex A 条款有）
    guidance = km.get_guidance(clause_num.upper())

    # 如果上传了文件，解析文件内容
    file_content_text = ""
    file_name = ""
    if file and file.filename:
        content_bytes = await file.read()
        if len(content_bytes) > MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"文件大小超过限制（{MAX_SIZE // 1024 // 1024}MB）",
            )
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content_bytes)
            tmp_path = tmp.name
        try:
            file_content_text = parse_file(tmp_path)
            if file_content_text.strip():
                # 截断过长内容
                max_chars = 10000
                if len(file_content_text) > max_chars:
                    file_content_text = file_content_text[:max_chars] + "\n\n[... 文件内容已截断 ...]"
                file_name = file.filename
        finally:
            os.unlink(tmp_path)

    # 构建系统提示词
    system_prompt = get_system_prompt(audit_scope)

    # 构建条款知识上下文
    clause_context = f"""## 当前条款信息
- 条款号：{clause['number']}
- 条款标题：{clause['title']}
- 标准要求：{clause['requirement']}
- 所属主题：{clause.get('theme', '')}
"""

    if guidance:
        clause_context += f"\n## ISO/IEC 27002:2022 实施指南\n{guidance}\n"

    # 构建用户提示词，综合文件内容和文字描述
    evidence_section = ""
    if file_content_text and file_name:
        evidence_section = f"""## 审核员上传的文件内容（文件名：{file_name}）
{file_content_text}

## 审核员提供的文字描述
{text_content}"""
    else:
        evidence_section = f"""## 审核员提供的信息
{text_content}"""

    user_prompt = f"""请根据以下审核员提供的信息，为条款 {clause['number']}（{clause['title']}）生成一份标准化的审核记录。

{evidence_section}

## 审核范围
{audit_scope or "未指定"}

## 请按以下 JSON 格式返回审核记录：
{{
    "clause_number": "{clause['number']}",
    "clause_title": "{clause['title']}",
    "standard_requirement": "该条款的标准要求概述（精炼准确，基于标准原文）",
    "audit_method": "审核方法（如：文件审查、现场观察、人员访谈、系统演示、抽样验证等，可组合）",
    "audit_evidence": "审核证据（基于审核员提供的文件和文字信息，客观描述实际观察到的情况，不含主观判断）",
    "conformity_judgment": "符合性判定：符合 / 不符合 / 观察项",
    "judgment_explanation": "判定说明（将审核证据与标准要求逐条对照分析，说明判定理由）",
    "improvement_suggestions": ["改进建议1", "改进建议2", ...]
}}

## 生成要求：
1. audit_evidence 必须基于审核员提供的文件内容和文字描述客观描述，不得编造不存在的证据
2. 如果同时提供了文件和文字描述，应综合两者的信息形成完整的审核证据
3. conformity_judgment 判定标准：
   - 符合：审核证据表明组织已有效实施该条款的所有要求
   - 不符合：审核证据表明组织未实施或实施不满足条款的关键要求
   - 观察项：审核证据表明基本满足要求但存在改进空间，或证据不足以做出确定判断
4. judgment_explanation 必须将审核证据与标准要求逐条对照，逻辑清晰
5. improvement_suggestions 应具有可操作性，参考 ISO 27002 实施指南
6. 如果审核员提供的信息不足以做出判定，应判定为"观察项"并在说明中指明需补充的证据"""

    result = chat_completion_json(
        messages=[
            {"role": "system", "content": system_prompt + "\n\n" + clause_context},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=4096,
    )

    # 确保 clause_number 和 clause_title 使用知识库中的准确值
    if isinstance(result, dict):
        result["clause_number"] = clause["number"]
        result["clause_title"] = clause["title"]
        if guidance:
            result["implementation_guidance"] = guidance

    return result
