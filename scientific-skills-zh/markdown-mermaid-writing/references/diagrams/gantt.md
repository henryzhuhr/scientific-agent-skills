<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 甘特图

> **返回[样式指南](../mermaid_style_guide.md)** — 首先阅读样式指南以了解表情符号、颜色和可访问性规则。

* *语法关键字：** `gantt`
* *最适合：**项目时间表、路线图、阶段规划、里程碑跟踪、任务依赖性
* *何时不使用：**简单的时间顺序事件（使用[时间轴](timeline.md)）、流程逻辑（使用[流程图](flowchart.md)）

- --

## 示例图

```mermaid
gantt
    accTitle: Q1 Product Launch Roadmap
    accDescr: Eight-week project timeline across discovery, design, build, and launch phases with milestones for design review and go/no-go decision

    title 🚀 Q1 Product Launch Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section 📋 Discovery
        User research          :done, research, 2026-01-05, 7d
        Competitive analysis   :done, compete, 2026-01-05, 5d
        Requirements doc       :done, reqs, after compete, 3d

    section 🎨 Design
        Wireframes             :done, wire, after reqs, 5d
        Visual design          :active, visual, after wire, 7d
        🏁 Design review       :milestone, review, after visual, 0d

    section 🔧 Build
        Core features          :crit, core, after visual, 10d
        API integration        :api, after visual, 8d
        Testing                :test, after core, 5d

    section 🚀 Launch
        Staging deploy         :staging, after test, 3d
        🏁 Go / no-go          :milestone, decision, after staging, 0d
        Production release     :crit, release, after staging, 2d
```

- --

## 提示

- 使用带有表情符号前缀的`section`按阶段或团队进行分组
- 用`:milestone`和`0d`标记里程碑持续时间-前缀为🏁
- 状态标签：`:done`、`:active`、`:crit`（关键路径，突出显示）
- 使用 `after taskId` 作为依赖项
- 保持总时间线**低于 3 个月**以提高可读性
- 使用 `axisFormat`控制日期显示(`%b %d` = "Jan 05", `%m/%d` = "01/05")

- --

## 模板

```mermaid
gantt
    accTitle: Your Title Here
    accDescr: Describe the timeline scope and key milestones

    title 📋 Your Roadmap Title
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section 📋 Phase 1
        Task one       :done, t1, 2026-01-01, 5d
        Task two       :active, t2, after t1, 3d

    section 🔧 Phase 2
        Task three     :crit, t3, after t2, 7d
        🏁 Milestone   :milestone, m1, after t3, 0d
```

- --

## 复杂示例

A跨团队平台迁移历时 4 个月，包含 6 个部分、24 项任务和 3 个里程碑。显示团队之间的依赖关系（后端迁移阻止前端迁移）、关键路径项以及从规划到启动监控的完整生命周期。

```mermaid
gantt
    accTitle: Multi-Team Platform Migration Roadmap
    accDescr: Four-month migration project across planning, backend, frontend, data, QA, and launch teams with cross-team dependencies, critical path items, and three milestone gates

    title 🚀 Platform Migration — Q1/Q2 2026
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section 📋 Planning
        Kickoff meeting               :done, plan1, 2026-01-05, 2d
        Architecture review            :done, plan2, after plan1, 5d
        Migration plan document        :done, plan3, after plan2, 5d
        Risk assessment                :done, plan4, after plan2, 3d
        🏁 Planning complete           :milestone, m_plan, after plan3, 0d

    section 🔧 Backend Team
        API redesign                   :crit, be1, after m_plan, 12d
        Data migration scripts         :be2, after m_plan, 10d
        New service deployment         :crit, be3, after be1, 8d
        Backward compatibility layer   :be4, after be1, 6d

    section 🎨 Frontend Team
        Component library update       :fe1, after m_plan, 10d
        Page migration                 :crit, fe2, after be3, 12d
        A/B testing setup              :fe3, after fe2, 5d
        Feature parity validation      :fe4, after fe2, 4d

    section 🗄️ Data Team
        Schema migration               :crit, de1, after be2, 8d
        ETL pipeline update            :de2, after de1, 7d
        Data validation suite          :de3, after de2, 5d
        Rollback scripts               :de4, after de1, 4d

    section 🧪 QA Team
        Test plan creation             :qa1, after m_plan, 7d
        Regression suite               :qa2, after be3, 10d
        Performance testing            :crit, qa3, after qa2, 7d
        UAT coordination               :qa4, after qa3, 5d
        🏁 QA sign-off                 :milestone, m_qa, after qa4, 0d

    section 🚀 Launch
        Staging deploy                 :crit, l1, after m_qa, 3d
        🏁 Go / no-go decision         :milestone, m_go, after l1, 0d
        Production cutover             :crit, l2, after m_go, 2d
        Post-launch monitoring         :l3, after l2, 10d
        Legacy system decommission     :l4, after l3, 5d
```

### 为什么有效

- **6 个部分映射到真实团队** — 每个团队一目了然地看到他们的工作流程。跨团队依赖关系（前端等待后端 API，QA 等待后端部署）通过 `after taskId`.
 明确 - **`:crit` 标记关键路径** - 决定总项目持续时间的任务链。如果任何关键任务出现延误，启动日期就会发生变化。 Mermaid 以红色突出显示这些内容。
- **3 个里程碑是决策门** - 计划完成、QA 签核和进行/不进行。这些是利益相关者做出决策的点，而不仅仅是状态更新。
- **4 个月内的 24 项任务** 是可读的，因为部分按团队分组。如果没有部分，这将是一堵无法阅读的酒吧墙。
