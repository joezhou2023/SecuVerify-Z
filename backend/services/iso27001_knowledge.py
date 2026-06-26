"""
ISO/IEC 27001:2022 知识库
包含标准正文条款（第 4-10 章）和附录 A 控制措施（93 项）
"""

# ===== 正文条款（可审核条款 4-10）=====
MAIN_CLAUSES = [
    {
        "number": "4",
        "title": "组织环境",
        "sub_clauses": [
            {"number": "4.1", "title": "理解组织及其环境", "requirement": "组织应确定与其信息安全管理体系相关的内外部环境问题，包括可能影响 ISMS 实现预期结果的能力的因素。"},
            {"number": "4.2", "title": "理解相关方的需求和期望", "requirement": "组织应确定 ISMS 相关方的需求，以及哪些需求将通过 ISMS 解决。"},
            {"number": "4.3", "title": "确定信息安全管理体系的范围", "requirement": "组织应确定 ISMS 的边界和适用性，以建立其范围。范围应作为成文信息可获得。"},
            {"number": "4.4", "title": "信息安全管理体系", "requirement": "组织应按照标准要求建立、实施、保持和持续改进 ISMS，包括所需的过程及其相互作用。"},
        ],
    },
    {
        "number": "5",
        "title": "领导作用",
        "sub_clauses": [
            {"number": "5.1", "title": "领导作用和承诺", "requirement": "最高管理者应通过以下方式证实对 ISMS 的领导作用和承诺：确保信息安全方针和目标制定、与战略方向一致、融入业务过程、提供资源、传达重要性、确保达成预期结果、支持其他管理者、推动持续改进。"},
            {"number": "5.2", "title": "方针", "requirement": "最高管理者应建立信息安全方针，方针应：包含对满足适用要求和持续改进 ISMS 有效性的承诺、提供建立和评审信息安全目标的框架、包含满足适用安全相关要求和义务的承诺。方针应作为成文信息可获得、在组织内传达、适当时可为相关方获取。"},
            {"number": "5.3", "title": "组织的角色、职责和权限", "requirement": "最高管理者应确保相关角色的职责和权限得到分配和传达。应分配职责和权限以：确保 ISMS 符合标准要求、向最高管理者报告 ISMS 绩效、确保信息安全风险评估和处置过程得到执行、向最高管理者报告 ISMS 改进需求。"},
        ],
    },
    {
        "number": "6",
        "title": "策划",
        "sub_clauses": [
            {"number": "6.1", "title": "应对风险和机会的措施", "requirement": "组织应策划 ISMS 以：应对风险和机会、实现信息安全目标、预防或减少不良影响、实现持续改进。包括信息安全风险评估过程和信息风险处置过程。"},
            {"number": "6.2", "title": "信息安全目标及其实现策划", "requirement": "组织应在相关职能和层次上建立信息安全目标，目标应：与方针一致、可测量、考虑适用要求和风险评估结果、得到传达、适当时更新。"},
            {"number": "6.3", "title": "变更策划", "requirement": "当组织确定需要对 ISMS 进行变更时，变更应按策划的方式进行。"},
        ],
    },
    {
        "number": "7",
        "title": "支持",
        "sub_clauses": [
            {"number": "7.1", "title": "资源", "requirement": "组织应确定并提供建立、实施、保持和持续改进 ISMS 所需的资源。"},
            {"number": "7.2", "title": "能力", "requirement": "组织应确定必要的胜任能力，确保人员具备适当的教育、培训或经验，并保留适当的成文信息作为证据。"},
            {"number": "7.3", "title": "意识", "requirement": "组织应确保在组织控制下工作的人员知晓信息安全方针、他们对 ISMS 有效性的贡献、改进 ISMS 绩效的益处、不符合 ISMS 要求的后果。"},
            {"number": "7.4", "title": "沟通", "requirement": "组织应确定与 ISMS 相关的内部和外部沟通需求，包括沟通什么、何时沟通、与谁沟通、如何沟通、由谁沟通。"},
            {"number": "7.5", "title": "成文信息", "requirement": "组织的 ISMS 应包括标准要求的成文信息、组织确定的实现 ISMS 有效性所需的成文信息。应控制成文信息的创建和更新、分发、访问、检索和使用、存储和保护、变更控制、保留和处置。"},
        ],
    },
    {
        "number": "8",
        "title": "运行",
        "sub_clauses": [
            {"number": "8.1", "title": "运行的策划和控制", "requirement": "组织应策划、实施和控制满足 ISMS 要求所需的过程，并实施风险处置计划中确定的措施。"},
            {"number": "8.2", "title": "信息安全风险评估", "requirement": "组织应在策划的时间间隔或重大变更发生时执行信息安全风险评估，保留风险评估结果的成文信息。"},
            {"number": "8.3", "title": "信息安全风险处置", "requirement": "组织应实施信息安全风险处置计划，保留风险处置结果的成文信息。"},
        ],
    },
    {
        "number": "9",
        "title": "绩效评价",
        "sub_clauses": [
            {"number": "9.1", "title": "监视、测量、分析和评价", "requirement": "组织应评价信息安全绩效和 ISMS 的有效性。组织应确定需要监视和测量什么、方法、何时执行、何时分析和评价、由谁执行。"},
            {"number": "9.2", "title": "内部审核", "requirement": "组织应按策划的时间间隔进行内部审核，以提供 ISMS 是否符合标准和自身要求的信息、是否得到有效实施和维护的信息。"},
            {"number": "9.3", "title": "管理评审", "requirement": "最高管理者应按策划的时间间隔评审组织的 ISMS，以确保其持续的适宜性、充分性和有效性。"},
        ],
    },
    {
        "number": "10",
        "title": "改进",
        "sub_clauses": [
            {"number": "10.1", "title": "持续改进", "requirement": "组织应持续改进 ISMS 的适宜性、充分性和有效性。"},
            {"number": "10.2", "title": "不符合和纠正措施", "requirement": "当发生不符合时，组织应：对不符合做出反应并适用时采取措施控制和纠正、评价消除不符合原因的措施需求、评审纠正措施的有效性、必要时变更 ISMS。"},
        ],
    },
]


# ===== 附录 A 控制措施（93 项，按 4 大主题组织）=====
# 条款标题和控制描述均依据 GB/T 22080-2025 / ISO/IEC 27001:2022 附录 A
ANNEX_A_CONTROLS = [
    # ===== A.5 组织控制（37 项）=====
    {"number": "A.5.1", "theme": "组织控制", "title": "信息安全策略", "attribute": "预防", "description": "应定义信息安全方针和特定主题策略，由管理层批准后发布，传达并让相关工作人员和相关方知悉，按计划的时间间隔以及在发生重大变更时对其进行评审。"},
    {"number": "A.5.2", "theme": "组织控制", "title": "信息安全角色和责任", "attribute": "预防", "description": "信息安全角色和责任应根据组织需求进行定义和分配。"},
    {"number": "A.5.3", "theme": "组织控制", "title": "职责分离", "attribute": "预防", "description": "应分离相互冲突的职责和责任范围。"},
    {"number": "A.5.4", "theme": "组织控制", "title": "管理责任", "attribute": "预防", "description": "管理层应要求所有工作人员根据组织已建立的信息安全方针、特定主题策略和规程，履行信息安全责任。"},
    {"number": "A.5.5", "theme": "组织控制", "title": "与职能机构的联系", "attribute": "纠正", "description": "组织应建立并维护与相关职能机构的联系。"},
    {"number": "A.5.6", "theme": "组织控制", "title": "与特定相关方的联系", "attribute": "检测", "description": "组织应建立并维护与特定相关方或其他专业安全论坛和专业协会的联系。"},
    {"number": "A.5.7", "theme": "组织控制", "title": "威胁情报", "attribute": "检测", "description": "应收集并分析信息安全威胁相关的信息，以生成威胁情报。"},
    {"number": "A.5.8", "theme": "组织控制", "title": "项目管理中的信息安全", "attribute": "预防", "description": "应将信息安全整合到项目管理中。"},
    {"number": "A.5.9", "theme": "组织控制", "title": "信息及其他相关资产的清单", "attribute": "预防", "description": "应编制和维护信息及其他相关资产（包括资产拥有者）的清单。"},
    {"number": "A.5.10", "theme": "组织控制", "title": "信息及其他相关资产的可接受使用", "attribute": "预防", "description": "应识别、文件化并实施信息及其他相关资产的可接受使用规则和处理规程。"},
    {"number": "A.5.11", "theme": "组织控制", "title": "资产归还", "attribute": "纠正", "description": "适宜时，工作人员和其他相关方在任用、合同或协议变更及终止时，应归还其拥有的所有组织资产。"},
    {"number": "A.5.12", "theme": "组织控制", "title": "信息分级", "attribute": "预防", "description": "应根据组织基于保密性、完整性、可用性的信息安全需求以及相关方的要求，对信息进行分级。"},
    {"number": "A.5.13", "theme": "组织控制", "title": "信息标记", "attribute": "预防", "description": "应按组织采用的信息分级方案，制定并实施适当的信息标记规程。"},
    {"number": "A.5.14", "theme": "组织控制", "title": "信息传输", "attribute": "预防", "description": "应为组织内部以及组织与其他各方之间所有类型的传输设施，制定信息传输规则、规程或协议。"},
    {"number": "A.5.15", "theme": "组织控制", "title": "访问控制", "attribute": "预防", "description": "应基于业务和信息安全要求，建立和实施信息及其他相关资产的物理和逻辑访问控制规则。"},
    {"number": "A.5.16", "theme": "组织控制", "title": "身份管理", "attribute": "预防", "description": "应管理身份的全生存周期。"},
    {"number": "A.5.17", "theme": "组织控制", "title": "鉴别信息", "attribute": "预防", "description": "应通过管理过程控制鉴别信息的分配和管理，包括向工作人员提供鉴别信息的适当处理建议。"},
    {"number": "A.5.18", "theme": "组织控制", "title": "访问权限", "attribute": "预防", "description": "应根据组织访问控制的特定主题策略和规则来提供、评审、修改和删除信息及其他相关资产的访问权限。"},
    {"number": "A.5.19", "theme": "组织控制", "title": "供应商关系中的信息安全", "attribute": "预防", "description": "应定义并实施过程和规程，以管理供应商产品或服务使用相关的信息安全风险。"},
    {"number": "A.5.20", "theme": "组织控制", "title": "解决ICT供应链中的信息安全问题", "attribute": "预防", "description": "应根据供应商关系的类型建立相关的信息安全要求，并与每个供应商达成一致。"},
    {"number": "A.5.21", "theme": "组织控制", "title": "管理信息通信技术供应链中的信息安全", "attribute": "预防", "description": "应定义并实施过程和规程，以管理与信息通信技术（ICT）产品和服务供应链相关的信息安全风险。"},
    {"number": "A.5.22", "theme": "组织控制", "title": "供应商服务的监视、评审和变更管理", "attribute": "检测", "description": "组织应定期监视、评审、评价和管理供应商信息安全实践和服务交付的变更。"},
    {"number": "A.5.23", "theme": "组织控制", "title": "云服务使用的信息安全", "attribute": "预防", "description": "应根据组织的信息安全要求，建立云服务的获取、使用、管理和退出过程。"},
    {"number": "A.5.24", "theme": "组织控制", "title": "信息安全事件管理规划和准备", "attribute": "预防", "description": "组织应通过定义、建立和传达信息安全事件管理过程、角色和责任，为管理信息安全事件做出规划和准备。"},
    {"number": "A.5.25", "theme": "组织控制", "title": "信息安全事态的评估和决策", "attribute": "检测", "description": "组织应评估信息安全事态，并决定是否将其归类为信息安全事件。"},
    {"number": "A.5.26", "theme": "组织控制", "title": "信息安全事件的响应", "attribute": "纠正", "description": "应按文件化的规程响应信息安全事件。"},
    {"number": "A.5.27", "theme": "组织控制", "title": "从信息安全事件中学习", "attribute": "纠正", "description": "应使用从信息安全事件中得到的知识来加强和改进信息安全控制。"},
    {"number": "A.5.28", "theme": "组织控制", "title": "证据收集", "attribute": "检测", "description": "组织应建立并实施包括识别、收集、获取和保存信息安全事态相关证据的规程。"},
    {"number": "A.5.29", "theme": "组织控制", "title": "中断期间的信息安全", "attribute": "纠正", "description": "组织应制定在中断期间将信息安全维持在适当级别的计划。"},
    {"number": "A.5.30", "theme": "组织控制", "title": "业务连续性的信息通信技术就绪", "attribute": "预防", "description": "应根据业务连续性目标和信息通信技术（ICT）连续性要求，策划、实施、维护和测试ICT的就绪。"},
    {"number": "A.5.31", "theme": "组织控制", "title": "法律、法规、规章和合同要求", "attribute": "预防", "description": "应识别与信息安全相关的法律、法规、规章和合同要求，以及组织满足这些要求的方法，并将其文件化且保持更新。"},
    {"number": "A.5.32", "theme": "组织控制", "title": "知识产权", "attribute": "预防", "description": "组织应实施适当的规程来保护知识产权。"},
    {"number": "A.5.33", "theme": "组织控制", "title": "记录的保护", "attribute": "预防", "description": "应保护记录不被丢失、破坏、篡改、未经授权的访问和未经授权的发布。"},
    {"number": "A.5.34", "theme": "组织控制", "title": "隐私和个人可识别信息保护", "attribute": "预防", "description": "组织应根据适用的法律、法规和合同要求，识别并满足有关隐私保护和个人可识别信息（PII）保护的要求。"},
    {"number": "A.5.35", "theme": "组织控制", "title": "信息安全的独立评审", "attribute": "检测", "description": "组织管理信息安全的方法及其实现，包括人员、过程和技术，应在计划的时间间隔内或发生重大变化时进行独立评审。"},
    {"number": "A.5.36", "theme": "组织控制", "title": "符合信息安全的策略、规则和标准", "attribute": "检测", "description": "应定期评审与组织信息安全方针、特定主题策略、规则和标准的符合性。"},
    {"number": "A.5.37", "theme": "组织控制", "title": "文件化的操作规程", "attribute": "预防", "description": "信息处理设施的操作规程应形成文件，并对有需要的工作人员可用。"},

    # ===== A.6 人员控制（8 项）=====
    {"number": "A.6.1", "theme": "人员控制", "title": "审查", "attribute": "预防", "description": "加入组织前，应对所有拟录用工作人员的候选人进行背景审查，并在入职后持续进行，同时考虑适用的法律、法规和道德规范，与业务要求、访问信息的级别和感知到的风险相适宜。"},
    {"number": "A.6.2", "theme": "人员控制", "title": "任用条款和条件", "attribute": "预防", "description": "应在任用合同协议中规定工作人员和组织对信息安全的责任。"},
    {"number": "A.6.3", "theme": "人员控制", "title": "信息安全意识、教育和培训", "attribute": "预防", "description": "组织工作人员和相关方应接受适宜的信息安全意识、教育和培训，并获得与其工作职能相关的组织信息安全方针、特定主题策略和规程的定期更新信息。"},
    {"number": "A.6.4", "theme": "人员控制", "title": "违规处理过程", "attribute": "纠正", "description": "应正式制定违规处理过程并将之传达给工作人员和相关方，以便对违反信息安全策略的工作人员和其他相关方采取措施。"},
    {"number": "A.6.5", "theme": "人员控制", "title": "任用终止或变更后的责任", "attribute": "纠正", "description": "应确定任用终止或变更后仍有效的信息安全责任及其义务，传达至相关人员和其他相关方并执行。"},
    {"number": "A.6.6", "theme": "人员控制", "title": "保密或不泄露协议", "attribute": "预防", "description": "应识别、文件化、定期评审反映组织信息保护需求的保密或不泄露协议，并与工作人员和其他相关方签署。"},
    {"number": "A.6.7", "theme": "人员控制", "title": "远程工作", "attribute": "预防", "description": "应在工作人员远程工作时实施安全措施，以保护在组织场所外所访问的、处理的或存储的信息。"},
    {"number": "A.6.8", "theme": "人员控制", "title": "信息安全事态的报告", "attribute": "检测", "description": "组织应提供机制，使工作人员通过适当渠道及时报告观察到的或可疑的信息安全事态。"},

    # ===== A.7 物理控制（14 项）=====
    {"number": "A.7.1", "theme": "物理控制", "title": "物理安全边界", "attribute": "预防", "description": "应定义并使用安全边界来保护包含信息及其他相关资产的区域。"},
    {"number": "A.7.2", "theme": "物理控制", "title": "物理入口", "attribute": "预防", "description": "安全区域应由适当的入口控制和访问点保护。"},
    {"number": "A.7.3", "theme": "物理控制", "title": "办公室、房间和设施的安全保护", "attribute": "预防", "description": "应对办公室、房间和设施的物理安全进行设计，并予以实施。"},
    {"number": "A.7.4", "theme": "物理控制", "title": "物理安全监视", "attribute": "检测", "description": "应持续监视场所，以防止发生未经授权的物理访问。"},
    {"number": "A.7.5", "theme": "物理控制", "title": "物理和环境威胁防范", "attribute": "预防", "description": "应对物理和环境威胁的防范进行设计并予以实施，例如，自然灾害和其他对基础设施有意或无意的物理威胁。"},
    {"number": "A.7.6", "theme": "物理控制", "title": "在安全区域工作", "attribute": "预防", "description": "应设计并实施在安全区域工作的安全措施。"},
    {"number": "A.7.7", "theme": "物理控制", "title": "清理桌面和屏幕", "attribute": "预防", "description": "应定义并适当地执行纸质和可移动存储媒体的桌面清理规则和信息处理设施的屏幕清理规则。"},
    {"number": "A.7.8", "theme": "物理控制", "title": "设备安置和保护", "attribute": "预防", "description": "应安全地安置并保护设备。"},
    {"number": "A.7.9", "theme": "物理控制", "title": "组织场所外的资产安全", "attribute": "预防", "description": "应保护组织场所外的资产。"},
    {"number": "A.7.10", "theme": "物理控制", "title": "存储媒体", "attribute": "预防", "description": "存储媒体应在其获取、使用、运输和处置的整个生存周期内，按组织的分级方案和处理要求进行管理。"},
    {"number": "A.7.11", "theme": "物理控制", "title": "支持性设施", "attribute": "预防", "description": "应保护信息处理设施使其免于由支持性设施的故障而引起的电源故障和其他中断。"},
    {"number": "A.7.12", "theme": "物理控制", "title": "布缆安全", "attribute": "预防", "description": "应保护传输电力、数据或支持信息服务的电缆免受窃听、干扰或损坏。"},
    {"number": "A.7.13", "theme": "物理控制", "title": "设备维护", "attribute": "预防", "description": "设备应予以正确的维护，以确保信息的可用性、完整性和保密性。"},
    {"number": "A.7.14", "theme": "物理控制", "title": "设备的安全处置或重复使用", "attribute": "纠正", "description": "应对包含存储媒体的设备的所有部分进行核查，以确保在处置或重复使用之前，任何敏感数据和获得许可的软件已被删除或安全地覆写。"},

    # ===== A.8 技术控制（34 项）=====
    {"number": "A.8.1", "theme": "技术控制", "title": "用户终端设备", "attribute": "预防", "description": "应保护用户终端设备所存储或处理的，或通过其访问的信息。"},
    {"number": "A.8.2", "theme": "技术控制", "title": "特许访问权限", "attribute": "预防", "description": "应限制和管理特许访问权限的分配和使用。"},
    {"number": "A.8.3", "theme": "技术控制", "title": "信息访问限制", "attribute": "预防", "description": "应按已建立的访问控制特定主题策略，限制对信息及其他相关资产的访问。"},
    {"number": "A.8.4", "theme": "技术控制", "title": "源代码的访问", "attribute": "预防", "description": "对源代码、开发工具和软件库的读写访问进行适当的管理。"},
    {"number": "A.8.5", "theme": "技术控制", "title": "安全鉴别", "attribute": "预防", "description": "应当基于信息访问限制和访问控制的特定主题策略实施安全的鉴别技术和规程。"},
    {"number": "A.8.6", "theme": "技术控制", "title": "容量管理", "attribute": "预防", "description": "应根据当前和预期的容量需求，监视和调整资源的使用。"},
    {"number": "A.8.7", "theme": "技术控制", "title": "恶意软件防范", "attribute": "预防", "description": "应实施恶意软件防范，并通过适当的用户意识教育予以支持。"},
    {"number": "A.8.8", "theme": "技术控制", "title": "技术脆弱性管理", "attribute": "检测", "description": "应获取有关使用中的信息系统的技术脆弱性的信息，评价组织暴露于此类脆弱性的风险，并采取适当措施。"},
    {"number": "A.8.9", "theme": "技术控制", "title": "配置管理", "attribute": "预防", "description": "应建立、记录、实施、监视和评审硬件、软件、服务和网络的配置，包括安全配置。"},
    {"number": "A.8.10", "theme": "技术控制", "title": "信息删除", "attribute": "纠正", "description": "当不再需要时，应删除存储在信息系统、设备或任何其他存储媒体中的信息。"},
    {"number": "A.8.11", "theme": "技术控制", "title": "数据脱敏", "attribute": "预防", "description": "应根据组织关于访问控制的特定主题策略和其他相关的特定主题策略以及业务要求使用数据脱敏，并考虑到适用的法律法规。"},
    {"number": "A.8.12", "theme": "技术控制", "title": "数据防泄露", "attribute": "检测", "description": "数据防泄露措施应用于处理、存储或传输敏感信息的系统、网络和任何其他设备。"},
    {"number": "A.8.13", "theme": "技术控制", "title": "信息备份", "attribute": "纠正", "description": "信息、软件和系统的备份副本应按商定的备份特定主题策略进行维护和定期测试。"},
    {"number": "A.8.14", "theme": "技术控制", "title": "信息处理设施的冗余", "attribute": "预防", "description": "信息处理设施应具有足够的冗余以满足可用性要求。"},
    {"number": "A.8.15", "theme": "技术控制", "title": "日志", "attribute": "检测", "description": "应生成、存储、保护和分析用于记录活动、异常、故障及其他相关事态的日志。"},
    {"number": "A.8.16", "theme": "技术控制", "title": "监视活动", "attribute": "检测", "description": "应监视网络、系统和应用程序，以发现异常行为，并采取适当措施评价潜在的信息安全事件。"},
    {"number": "A.8.17", "theme": "技术控制", "title": "时钟同步", "attribute": "预防", "description": "组织使用的信息处理系统的时钟应与批准的时间源同步。"},
    {"number": "A.8.18", "theme": "技术控制", "title": "特权实用程序的使用", "attribute": "预防", "description": "应限制并严格控制可能超越系统和应用程序控制的实用程序的使用。"},
    {"number": "A.8.19", "theme": "技术控制", "title": "运行系统软件的安装", "attribute": "预防", "description": "应实施规程和措施以安全地管理运行系统上的软件安装。"},
    {"number": "A.8.20", "theme": "技术控制", "title": "网络安全", "attribute": "预防", "description": "应保护、管理和控制网络和网络设备以保护系统和应用程序中的信息。"},
    {"number": "A.8.21", "theme": "技术控制", "title": "网络服务的安全", "attribute": "预防", "description": "应识别、实施和监视网络服务的安全机制、服务级别和服务要求。"},
    {"number": "A.8.22", "theme": "技术控制", "title": "网络隔离", "attribute": "预防", "description": "应在组织的网络中隔离信息服务组、用户组和信息系统组。"},
    {"number": "A.8.23", "theme": "技术控制", "title": "网页过滤", "attribute": "预防", "description": "应管理对外部网站的访问，以减少对恶意内容的暴露。"},
    {"number": "A.8.24", "theme": "技术控制", "title": "密码技术的使用", "attribute": "预防", "description": "应定义并实施有效使用密码技术的规则，包括密钥管理。"},
    {"number": "A.8.25", "theme": "技术控制", "title": "安全开发生存周期", "attribute": "预防", "description": "应建立并应用软件和系统安全开发规则。"},
    {"number": "A.8.26", "theme": "技术控制", "title": "应用程序安全要求", "attribute": "预防", "description": "在开发或获取应用程序时，应识别、规定和批准信息安全要求。"},
    {"number": "A.8.27", "theme": "技术控制", "title": "系统安全架构和工程原则", "attribute": "预防", "description": "应建立、文件化、维护系统安全工程的原则，并将其应用于所有的信息系统开发活动。"},
    {"number": "A.8.28", "theme": "技术控制", "title": "安全编码", "attribute": "预防", "description": "软件开发中应应用安全编码原则。"},
    {"number": "A.8.29", "theme": "技术控制", "title": "开发和验收中的安全测试", "attribute": "预防", "description": "应在开发生存周期中定义和实施安全测试过程。"},
    {"number": "A.8.30", "theme": "技术控制", "title": "开发外包", "attribute": "预防", "description": "组织应指导、监视和评审系统开发外包相关的活动。"},
    {"number": "A.8.31", "theme": "技术控制", "title": "开发、测试和生产环境的隔离", "attribute": "预防", "description": "应隔离并保护开发、测试和生产环境。"},
    {"number": "A.8.32", "theme": "技术控制", "title": "变更管理", "attribute": "预防", "description": "信息处理设施和信息系统的变更应遵循变更管理规程。"},
    {"number": "A.8.33", "theme": "技术控制", "title": "测试信息", "attribute": "预防", "description": "应适当地选择、保护和管理测试信息。"},
    {"number": "A.8.34", "theme": "技术控制", "title": "在审计测试中保护信息系统", "attribute": "预防", "description": "应对涉及运行系统评估的审计测试和其他保障活动进行规划，并在测试人员和适合的管理人员之间达成一致。"},
]


def get_all_clauses() -> list[dict]:
    """获取所有条款（正文 + 附录 A）"""
    all_clauses = []
    for clause_group in MAIN_CLAUSES:
        for sub in clause_group["sub_clauses"]:
            all_clauses.append({
                "number": sub["number"],
                "title": sub["title"],
                "requirement": sub["requirement"],
                "source": "正文",
                "theme": clause_group["title"],
            })
    for control in ANNEX_A_CONTROLS:
        all_clauses.append({
            "number": control["number"],
            "title": control["title"],
            "requirement": control["description"],
            "source": "附录A",
            "theme": control["theme"],
            "attribute": control.get("attribute", ""),
        })
    return all_clauses


def get_clause_by_number(number: str) -> dict | None:
    """根据条款号获取条款详情"""
    for clause in get_all_clauses():
        if clause["number"] == number:
            return clause
    return None


def get_clause_with_guidance(number: str) -> dict | None:
    """根据条款号获取条款详情及其 ISO 27002 实施指南"""
    clause = get_clause_by_number(number)
    if not clause:
        return None
    from services.iso27002_knowledge import get_guidance_by_number
    guidance = get_guidance_by_number(number)
    return {**clause, "guidance": guidance}


def get_knowledge_summary() -> str:
    """生成知识库摘要文本，用于注入 LLM 提示词"""
    lines = ["## ISO/IEC 27001:2022 标准条款知识库\n"]
    lines.append("### 正文条款（第 4-10 章）")
    for group in MAIN_CLAUSES:
        lines.append(f"\n**第 {group['number']} 章 {group['title']}**")
        for sub in group["sub_clauses"]:
            lines.append(f"  - {sub['number']} {sub['title']}: {sub['requirement'][:80]}...")

    lines.append("\n### 附录 A 控制措施（93 项）")
    for theme in ["组织控制", "人员控制", "物理控制", "技术控制"]:
        controls = [c for c in ANNEX_A_CONTROLS if c["theme"] == theme]
        section = theme[0] if theme == "组织控制" else theme[0]
        theme_map = {"组织控制": "A.5", "人员控制": "A.6", "物理控制": "A.7", "技术控制": "A.8"}
        lines.append(f"\n**{theme_map[theme]} {theme}（{len(controls)} 项）**")
        for c in controls:
            lines.append(f"  - {c['number']} {c['title']}")

    return "\n".join(lines)
