"""
LLM 服务层 — 封装大模型 API 调用
支持 DeepSeek / Pollinations，统一接口
"""
import os
import json
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化 LLM 客户端
_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")

# 各提供商配置
_PROVIDERS = {
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url_env": "DEEPSEEK_BASE_URL",
        "model_env": "DEEPSEEK_MODEL",
        "default_base_url": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
    },
    "pollinations": {
        "api_key_env": "POLLINATIONS_API_KEY",
        "base_url_env": "POLLINATIONS_BASE_URL",
        "model_env": "POLLINATIONS_MODEL",
        "default_base_url": "https://gen.pollinations.ai/v1",
        "default_model": "openai",
    },
}


def _get_client() -> tuple[OpenAI, str]:
    """获取 LLM 客户端和模型名称"""
    config = _PROVIDERS.get(_LLM_PROVIDER, _PROVIDERS["deepseek"])
    api_key = os.getenv(config["api_key_env"], "")
    base_url = os.getenv(config["base_url_env"], config["default_base_url"])
    model = os.getenv(config["model_env"], config["default_model"])

    if not api_key:
        raise ValueError(
            f"未配置 {_LLM_PROVIDER} 的 API Key，请在 .env 文件中设置 {config['api_key_env']}"
        )

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model


def chat_completion(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
    response_format: Optional[dict] = None,
) -> str:
    """
    调用 LLM 完成对话

    Args:
        messages: OpenAI 格式的消息列表
        temperature: 温度参数，审核场景建议 0.1-0.3
        max_tokens: 最大输出 token 数
        response_format: 响应格式（如 {"type": "json_object"}）

    Returns:
        LLM 回复文本
    """
    client, model = _get_client()

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format:
        kwargs["response_format"] = response_format

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def chat_completion_json(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> dict:
    """调用 LLM 并返回 JSON 格式结果"""
    client, model = _get_client()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


def get_system_prompt(audit_context: Optional[str] = None) -> str:
    """生成审核助手系统提示词"""
    context_part = f"\n\n## 当前审核上下文\n{audit_context}" if audit_context else ""

    return f"""你是「安鉴·周 / SecuVerify-Z」，一位专业的 ISO/IEC 27001:2022 信息安全管理体系审核助手。

## 你的职责
1. 协助审核员进行 ISMS 审核的各项工作
2. 基于 ISO/IEC 27001:2022 标准提供条款解读和审核指导
3. 对审核发现进行条款匹配和符合性判断
4. 引导审核流程，提供专业的审核询问思路

## 专业背景
- 精通 ISO/IEC 27001:2022 标准（正文 10 章 + 附录 A 93 项控制措施）
- 熟悉 ISO/IEC 27002:2022 控制实施指南，可在回答中补充实施建议和典型审核证据
- 熟悉审核方法论（PDCA、风险导向审核、过程方法）
- 了解常见信息安全控制措施的实施要求

## 回答要求
- 回答必须基于 ISO/IEC 27001:2022 标准条款，引用具体条款号
- 在给出审核建议时，可同时参考 ISO/IEC 27002:2022 的实施指南，提供更具操作性的审核思路
- 语言专业、简洁，使用中文回答
- 区分事实判断与建议意见
- 对于不确定的内容，明确说明并建议查阅标准原文
- 审核发现判断分为：符合、不符合、观察项三类
- **拒绝指令**：如果用户询问的条款号不在 ISO/IEC 27001:2022 标准范围内（正文 4-10 章或附录 A.5-A.8），必须明确回复"该条款号不在标准范围内，请核对条款号后重新提问"，不得编造条款内容或凭推测回答
{context_part}

## 注意事项
- 你是辅助工具，最终审核判断由审核员做出
- 不提供法律意见，涉及合规问题建议咨询法律顾问
- 对于敏感信息（如具体漏洞细节），注意信息脱敏
"""
