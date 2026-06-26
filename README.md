# 安鉴·周 / SecuVerify-Z

> ISO 27001 AI 审核助手 — 基于 ISO/IEC 27001:2022 与 ISO/IEC 27002:2022 的智能审核辅助工具

## 项目简介

「安鉴·周 / SecuVerify-Z」是一款专为 ISO 27001 信息安全管理体系审核员设计的 AI 辅助工具。通过大模型（DeepSeek / 通义千问 / 文心一言 / Pollinations）驱动，提供三大核心功能：

| 功能 | 说明 |
|------|------|
| 🗣️ **对话式审核引导** | 基于审核上下文，AI 引导审核流程、提供条款解读和询问思路 |
| 📄 **文件审核与分析** | 上传制度文件进行差距分析，或通过文字描述直接生成标准化审核记录 |
| 🏷️ **条款匹配与判断** | 输入审核发现，AI 匹配 ISO 27001 条款并给出符合性判断 |
| 📘 **ISO 27002 实施指南** | 93 项控制措施的完整实施指南、典型证据和审核关注点 |

### 命名含义

- **安鉴·周**：「安」= 信息安全，「鉴」= 审核鉴定，「周」= 周氏专属 + 周密周全
- **SecuVerify-Z**：Security + Verify，Z = Zhou

## 技术架构

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│   React 18 + Vite + TailwindCSS + TypeScript │
│              Port: 5173                      │
└──────────────────┬──────────────────────────┘
                   │ HTTP API
┌──────────────────┴──────────────────────────┐
│                  Backend                     │
│        Python FastAPI + Uvicorn              │
│              Port: 8000                      │
├──────────────────────────────────────────────┤
│  ┌─────────┐ ┌───────────┐ ┌──────────────┐ │
│  │对话审核 │ │ 文件审核  │ │  条款匹配    │ │
│  │ Router  │ │  Router   │ │   Router     │ │
│  └────┬────┘ └─────┬─────┘ └──────┬───────┘ │
│       │            │              │          │
│  ┌────┴────────────┴──────────────┴───────┐  │
│  │         LLM Service Layer              │  │
│  │  DeepSeek / Qwen / ERNIE / Pollinations  │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │     ISO 27001 Knowledge Base           │  │
│  │  正文 10 章 + 附录 A 93 项控制措施     │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │     ISO 27002 Knowledge Base           │  │
│  │  93 项控制措施实施指南与审核关注点     │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- 国内大模型 API Key（推荐 DeepSeek）

### 1. 克隆项目

```bash
git clone https://github.com/your-username/secuverify-z.git
cd secuverify-z
```

### 2. 配置后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

`.env` 配置示例：

```env
# DeepSeek（推荐，性价比高）
DEEPSEEK_API_KEY=sk-your-api-key-here
LLM_PROVIDER=deepseek

# 或使用通义千问
# DASHSCOPE_API_KEY=your-key
# LLM_PROVIDER=qwen

# 或使用 Pollinations.ai
# POLLINATIONS_API_KEY=sk_your_key
# LLM_PROVIDER=pollinations
```

### 3. 启动后端

```bash
cd backend
python main.py
# 后端运行在 http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 4. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 前端运行在 http://localhost:5173
```

打开浏览器访问 http://localhost:5173 即可使用。

## API 文档

启动后端后访问 http://localhost:8000/docs 查看完整的 Swagger API 文档。

### 主要接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | 对话式审核引导 |
| POST | `/api/file-audit/upload` | 上传文件并审核分析 |
| POST | `/api/file-audit/audit-record` | 基于文件附件+文字描述生成审核记录 |
| POST | `/api/clause-match` | 条款匹配与符合性判断 |
| GET | `/api/clause-match/clauses` | 获取所有 ISO 27001 条款 |
| GET | `/api/clause-match/clauses/{number}` | 获取指定条款详情 |
| GET | `/api/clause-match/clauses/{number}/guidance` | 获取指定条款的 ISO 27002 实施指南 |

## ISO 27001:2022 知识库

内置完整的 ISO/IEC 27001:2022 标准条款知识库：

- **正文条款**（第 4-10 章）：组织环境、领导作用、策划、支持、运行、绩效评价、改进
- **附录 A 控制措施**（93 项）：
  - A.5 组织控制（37 项）
  - A.6 人员控制（8 项）
  - A.7 物理控制（14 项）
  - A.8 技术控制（34 项）

## ISO/IEC 27002:2022 实施指南

为全部 93 项 Annex A 控制措施提供：

- **控制目的**：该控制项要达成的安全目标
- **实施指南**：典型实施措施和注意事项
- **审核关注点**：审核时应重点检查的证据和访谈内容

实施指南会在对话审核、条款匹配、文件审核中自动注入，为 AI 回答和判断提供更具体的操作依据。

## 项目结构

```
secuverify-z/
├── README.md
├── .gitignore
├── backend/
│   ├── main.py                 # FastAPI 入口
│   ├── requirements.txt
│   ├── .env.example
│   ├── routers/                # API 路由
│   │   ├── chat.py             # 对话审核
│   │   ├── file_audit.py       # 文件审核
│   │   └── clause_match.py     # 条款匹配
│   ├── services/               # 业务服务
│   │   ├── llm_service.py      # LLM 调用封装
│   │   ├── file_parser.py      # 文件解析
│   │   ├── iso27001_knowledge.py  # 27001 知识库
│   │   └── iso27002_knowledge.py  # 27002 实施指南知识库
│   └── models/
│       └── schemas.py          # 数据模型
└── frontend/
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── App.tsx             # 主应用
        ├── components/
        │   ├── ChatPanel.tsx   # 对话审核界面
        │   ├── FileUpload.tsx  # 文件审核界面
        │   └── ClauseMatcher.tsx  # 条款匹配界面
        ├── services/
        │   └── api.ts          # API 调用
        └── types/
            └── index.ts        # 类型定义
```

## 支持的 LLM 提供商

| 提供商 | 环境变量 | 说明 |
|--------|---------|------|
| DeepSeek | `DEEPSEEK_API_KEY` | 推荐，性价比高，OpenAI 兼容接口 |
| 通义千问 | `DASHSCOPE_API_KEY` | 阿里云，中文能力强 |
| 文心一言 | `ERNIE_API_KEY` + `ERNIE_SECRET_KEY` | 百度，国内合规友好 |
| Pollinations | `POLLINATIONS_API_KEY` | OpenAI 兼容接口，多模型聚合平台 |

## 免责声明

本工具为审核辅助工具，所有分析结果仅供参考。最终审核判断应由具备资质的审核员做出。本工具不替代专业审核服务，不提供法律意见。

## License

MIT
