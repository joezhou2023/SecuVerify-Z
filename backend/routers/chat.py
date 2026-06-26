"""对话式审核引导路由"""
from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.llm_service import chat_completion, get_system_prompt
from services.knowledge_manager import km

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    对话式审核引导 — 基于审核上下文提供专业的审核指导
    """
    system_prompt = get_system_prompt(request.audit_context)
    system_prompt += f"\n\n{km.get_summary()}"

    # 如果用户消息中提到具体 Annex A 控制项，注入对应的 ISO 27002 实施指南
    user_text = " ".join(m.content for m in request.messages if m.role == "user")
    system_prompt = km.inject_guidance(user_text, system_prompt)

    messages = [{"role": "system", "content": system_prompt}]
    for msg in request.messages:
        messages.append({"role": msg.role, "content": msg.content})

    reply = chat_completion(messages, temperature=0.3, max_tokens=4096)

    # 提取回复中引用的条款号
    clause_refs = km.extract_clause_refs(reply)
    clause_refs = clause_refs if clause_refs else None

    return ChatResponse(reply=reply, clause_refs=clause_refs)
