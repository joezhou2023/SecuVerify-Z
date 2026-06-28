"""
LLM 服务层 — 封装大模型 API 调用
支持 DeepSeek / Pollinations / Agnes，统一接口，自动故障切换
"""

import os
import json
import logging
from typing import Optional
from openai import OpenAI, APIError
from dotenv import load_dotenv

load_dotenv()

# 日志记录器
logger = logging.getLogger("secuverify.llm")

# 各提供商配置
_PROVIDERS = {
    "deepseek": {
        "name": "DeepSeek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url_env": "DEEPSEEK_BASE_URL",
        "model_env": "DEEPSEEK_MODEL",
        "default_base_url": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
    },
    "pollinations": {
        "name": "Pollinations",
        "api_key_env": "POLLINATIONS_API_KEY",
        "base_url_env": "POLLINATIONS_BASE_URL",
        "model_env": "POLLINATIONS_MODEL",
        "default_base_url": "https://gen.pollinations.ai/v1",
        "default_model": "openai",
    },
    "agnes": {
        "name": "Agnes",
        "api_key_env": "AGNES_API_KEY",
        "base_url_env": "AGNES_BASE_URL",
        "model_env": "AGNES_MODEL",
        "default_base_url": "https://apihub.agnes-ai.com/v1",
        "default_model": "agnes-2.0-flash",
    },
}


def _get_provider_list() -> list[str]:
    """获取提供商优先级列表（逗号分隔），自动过滤未配置 API Key 的提供商"""
    raw = os.getenv("LLM_PROVIDER", "deepseek")
    # 解析逗号分隔列表
    candidates = [p.strip() for p in raw.split(",") if p.strip()]
    # 过滤：只保留有 API Key 且配置存在的提供商
    valid = []
    for name in candidates:
        config = _PROVIDERS.get(name)
        if not config:
            logger.warning("未知的 LLM 提供商: %s，已跳过", name)
            continue
        api_key = os.getenv(config["api_key_env"], "")
        if not api_key:
            logger.warning("提供商 %s 未配置 API Key（%s），已跳过", name, config["api_key_env"])
            continue
        valid.append(name)

    if not valid:
        # 如果全都不可用，回退到 deepseek（可能也会失败但给出明确错误）
        fallback = "deepseek"
        if fallback in _PROVIDERS:
            valid.append(fallback)
    return valid


def _try_provider(provider_name: str, **kwargs) -> Optional[tuple]:
    """尝试用指定提供商调用 LLM，成功返回 (client, model)，失败返回 None"""
    config = _PROVIDERS[provider_name]
    api_key = os.getenv(config["api_key_env"], "")
    base_url = os.getenv(config["base_url_env"], config["default_base_url"])
    model = os.getenv(config["model_env"], config["default_model"])

    try:
        client = OpenAI(api_key=api_key, base_url=base_url, timeout=60)
        # 发一个轻量请求验证连通性（messages 必须有内容）
        test_resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
            temperature=0,
        )
        _ = test_resp.choices[0].message.content
        logger.info("提供商 %s 连通成功（%s）", provider_name, config.get("name", provider_name))
        return client, model
    except Exception as e:
        logger.warning("提供商 %s 不可用（%s）: %s", provider_name, config.get("name", provider_name), str(e))
        return None


def _get_client() -> tuple[OpenAI, str, str]:
    """获取第一个可用的 LLM 客户端和模型名称，带自动故障切换"""
    providers = _get_provider_list()
    errors = []

    for pname in providers:
        result = _try_provider(pname)
        if result is not None:
            client, model = result
            config = _PROVIDERS[pname]
            logger.info("当前使用提供商: %s，模型: %s", config.get("name", pname), model)
            return (client, model, pname)  # 返回三元组，第三个是提供商名

        config = _PROVIDERS.get(pname, {})
        errors.append(f"{config.get('name', pname)}: 不可用")

    # 全部失败
    raise ConnectionError(
        f"所有 LLM 提供商均不可用（{' → '.join(errors)}）。"
        "请检查 API Key 配置和网络连接。"
    )


def _try_call_with_failover(
    call_fn, messages, temperature, max_tokens, response_format=None
):
    """带故障切换的 LLM 调用：按优先级依次尝试每个提供商"""
    providers = _get_provider_list()
    errors = []

    for pname in providers:
        config = _PROVIDERS[pname]
        api_key = os.getenv(config["api_key_env"], "")
        base_url = os.getenv(config["base_url_env"], config["default_base_url"])
        model = os.getenv(config["model_env"], config["default_model"])

        try:
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=120)
            logger.info("尝试调用 %s（%s），模型: %s", pname, config.get("name", pname), model)

            result = call_fn(client, model, messages, temperature, max_tokens, response_format)
            logger.info("提供商 %s 调用成功", config.get("name", pname))
            return result

        except Exception as e:
            err_msg = f"{config.get('name', pname)}: {str(e)}"
            logger.warning("提供商 %s 调用失败: %s", config.get("name", pname), str(e))
            errors.append(err_msg)
            continue

    # 全部失败
    raise ConnectionError(
        f"所有 LLM 提供商调用均失败:\n" + "\n".join(f"  - {e}" for e in errors)
    )


def _chat_call(
    client: OpenAI, model: str, messages: list, temperature: float,
    max_tokens: int, response_format: Optional[dict]
) -> str:
    """执行一次 chat.completions.create 调用"""
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


def chat_completion(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
    response_format: Optional[dict] = None,
) -> str:
    """
    调用 LLM 完成对话（自动故障切换）

    Args:
        messages: OpenAI 格式的消息列表
        temperature: 温度参数，审核场景建议 0.1-0.3
        max_tokens: 最大输出 token 数
        response_format: 响应格式（如 {"type": "json_object"}）

    Returns:
        LLM 回复文本
    """
    return _try_call_with_failover(
        _chat_call, messages, temperature, max_tokens, response_format
    )


def _chat_json_call(
    client: OpenAI, model: str, messages: list, temperature: float,
    max_tokens: int, response_format: Optional[dict]
) -> dict:
    """执行一次 JSON 格式的 chat.completions.create 调用"""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


def chat_completion_json(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> dict:
    """调用 LLM 并返回 JSON 格式结果（自动故障切换）"""
    return _try_call_with_failover(
        _chat_json_call, messages, temperature, max_tokens
    )


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
