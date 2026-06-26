export interface ChangelogEntry {
  version: string;
  date: string;
  changes: string[];
}

/**
 * 版本修订历史
 * 最新版本放在数组最前面，按时间倒序排列
 */
export const changelog: ChangelogEntry[] = [
  {
    version: "1.4.0",
    date: "2026-06-26",
    changes: [
      "文件审核模块新增「审核记录」模式：支持文件附件 + 文字描述混合输入，综合生成标准化审核记录",
      "审核员输入条款号 + 可选上传附件 + 必填文字描述，AI 综合两者生成完整审核记录",
      "审核记录包含：标准要求、审核方法、审核证据、符合性判定、判定说明、改进建议",
      "审核记录自动附加 ISO/IEC 27002:2022 实施指南（Annex A 条款）",
      "符合性判定结果以彩色徽章直观展示（符合-绿色 / 不符合-红色 / 观察项-橙色）",
      "后端新增 POST /api/file-audit/audit-record 接口（multipart/form-data，支持文件+文字）",
      "删除通义千问/文心一言大模型配置，仅保留 DeepSeek + Pollinations",
    ],
  },
  {
    version: "1.3.0",
    date: "2026-06-26",
    changes: [
      "架构演进 Phase 1：创建 KnowledgeManager 统一知识库入口，三层分离（Router → KM → 知识源）",
      "对话审核、条款匹配、文件审核三大模块统一通过 km 调用知识库，不再直接 import 知识源",
      "新增知识源时只需在 KM 注册方法，Router 无需改动，为 Phase 2（案例库）/ Phase 3（向量检索）铺路",
    ],
  },
  {
    version: "1.2.0",
    date: "2026-06-26",
    changes: [
      "新增 ISO/IEC 27002:2022 实施指南知识库，覆盖全部 93 项 Annex A 控制措施",
      "对话审核在询问具体 Annex A 条款时自动注入 27002 实施指南与审核关注点",
      "条款匹配结果新增「ISO 27002 实施指南」可展开查看",
      "文件审核发现项新增「ISO 27002 实施指南」可展开查看",
      "后端新增 GET /api/clause-match/clauses/{clause_number}/guidance 接口",
    ],
  },
  {
    version: "1.1.0",
    date: "2026-06-26",
    changes: [
      "前端新增中英文语言切换按钮（侧边栏底部 / EN）",
      "所有界面文案支持中英文双语（对话审核、文件审核、条款匹配、版本历史）",
      "语言偏好自动保存到 localStorage",
      "项目根目录添加 MIT License",
    ],
  },
  {
    version: "1.0.0",
    date: "2026-06-26",
    changes: [
      "项目初始化，完成 ISO 27001 AI 审核助手基础功能",
      "支持对话审核、文件审核、条款匹配三大模块",
      "接入 Pollinations.ai 作为默认大模型",
      "左下角版本号可点击查看版本修订历史",
      "页面底部「Powered by Joezhou」链接到 https://www.joezhou.top",
    ],
  },
];
