# 美容连锁门店经营分析看板系统 技术架构文档

## 1. 架构设计

```mermaid
graph TB
    subgraph "前端层"
        FE["Vue 3 + TypeScript"]
        AntD["Ant Design Vue"]
        Plotly["Plotly.js (vue-plotly)"]
        Router["Vue Router"]
    end
    
    subgraph "后端层"
        Flask["Python Flask"]
        API["RESTful API"]
        CORS["CORS 跨域处理"]
    end
    
    subgraph "数据层"
        CSV["CSV 模拟数据"]
        Pandas["Pandas 数据处理"]
    end
    
    FE --> AntD
    FE --> Plotly
    FE --> Router
    FE -- "HTTP请求" --> Flask
    Flask --> API
    Flask --> CORS
    API --> Pandas
    Pandas --> CSV
```

## 2. 技术栈说明

| 层级 | 技术选型 | 版本 | 说明 |
|------|----------|------|------|
| 前端框架 | Vue 3 | ^3.4.0 | Composition API + TypeScript |
| UI组件库 | Ant Design Vue | ^4.1.0 | 企业级UI组件库 |
| 图表库 | Plotly.js | ^2.27.0 | 交互式科学图表 |
| 路由 | Vue Router | ^4.2.0 | SPA路由管理 |
| 构建工具 | Vite | ^5.0.0 | 快速开发构建 |
| 后端框架 | Flask | ^3.0.0 | Python轻量Web框架 |
| 数据处理 | Pandas | ^2.0.0 | CSV数据处理分析 |
| 编程语言 | Python | 3.10+ | 后端开发语言 |
| 数据格式 | CSV | - | 模拟数据存储格式 |

## 3. 路由定义

| 路由路径 | 页面名称 | 说明 |
|----------|----------|------|
| / | 重定向到门店分析 | 默认首页重定向 |
| /store-analysis | 门店核心指标分析 | 门店KPI、排名对比、趋势图 |
| /project-analysis | 项目分析 | 项目占比、毛利率、四象限 |
| /employee-analysis | 员工产出分析 | 业绩排行、客单对比 |
| /member-lifecycle | 会员生命周期管理 | 充值周期、复充率、流失预警 |
| /channel-analysis | 渠道获客分析 | 渠道转化、客单价对比 |

## 4. API 接口定义

### 4.1 接口规范

- 协议：HTTP/HTTPS
- 数据格式：JSON
- 基础路径：`/api/v1`
- 响应格式：

```typescript
interface ApiResponse<T> {
  code: number;       // 200: 成功, 400: 参数错误, 500: 服务器错误
  message: string;    // 状态信息
  data: T;            // 响应数据
}
```

### 4.2 接口列表

| 接口路径 | 方法 | 说明 |
|----------|------|------|
| /stores/metrics | GET | 获取门店核心指标数据 |
| /stores/ranking | GET | 获取门店排名对比数据 |
| /stores/trend | GET | 获取门店指标趋势数据 |
| /projects/sales | GET | 获取项目销售占比数据 |
| /projects/margin | GET | 获取项目毛利率数据 |
| /projects/matrix | GET | 获取项目四象限矩阵数据 |
| /employees/ranking | GET | 获取员工业绩排行数据 |
| /employees/orders | GET | 获取员工客单数与客单价数据 |
| /members/cycle | GET | 获取会员充值周期数据 |
| /members/recharge | GET | 获取会员复充率数据 |
| /members/churn | GET | 获取流失预警会员列表 |
| /channels/conversion | GET | 获取渠道转化率数据 |
| /channels/aov | GET | 获取渠道客单价对比数据 |
| /channels/evaluation | GET | 获取渠道效果评估数据 |
| /export/{module} | GET | 导出指定模块数据 |

### 4.3 通用查询参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始日期 (YYYY-MM-DD) |
| endDate | string | 否 | 结束日期 (YYYY-MM-DD) |
| storeIds | string | 否 | 门店ID，逗号分隔 |
| sortBy | string | 否 | 排序字段 |
| sortOrder | string | 否 | 排序方向 (asc/desc) |

## 5. 后端架构图

```mermaid
graph TB
    subgraph "Flask 应用层"
        App["Flask App"]
        Routes["路由层 (routes/)"]
        Cors["CORS 中间件"]
    end
    
    subgraph "业务逻辑层"
        StoreService["门店服务"]
        ProjectService["项目服务"]
        EmployeeService["员工服务"]
        MemberService["会员服务"]
        ChannelService["渠道服务"]
    end
    
    subgraph "数据访问层"
        CsvLoader["CSV 数据加载器"]
        DataProcessor["数据处理器 (Pandas)"]
    end
    
    subgraph "数据层"
        StoreCSV["stores.csv"]
        ProjectCSV["projects.csv"]
        EmployeeCSV["employees.csv"]
        MemberCSV["members.csv"]
        ChannelCSV["channels.csv"]
    end
    
    App --> Routes
    App --> Cors
    Routes --> StoreService
    Routes --> ProjectService
    Routes --> EmployeeService
    Routes --> MemberService
    Routes --> ChannelService
    StoreService --> CsvLoader
    ProjectService --> CsvLoader
    EmployeeService --> CsvLoader
    MemberService --> CsvLoader
    ChannelService --> CsvLoader
    CsvLoader --> DataProcessor
    DataProcessor --> StoreCSV
    DataProcessor --> ProjectCSV
    DataProcessor --> EmployeeCSV
    DataProcessor --> MemberCSV
    DataProcessor --> ChannelCSV
```

## 6. 数据模型

### 6.1 数据模型定义

```mermaid
erDiagram
    STORE {
        string store_id PK "门店ID"
        string store_name "门店名称"
        string city "城市"
        string area "区域"
        date open_date "开业日期"
    }
    
    STORE_METRICS {
        string metric_id PK "指标ID"
        string store_id FK "门店ID"
        date stat_date "统计日期"
        float revenue "营收"
        float customer_price "客单价"
        float visit_frequency "到店频次"
        int new_customers "新客数"
        float repeat_rate "复购率"
    }
    
    PROJECT {
        string project_id PK "项目ID"
        string project_name "项目名称"
        string category "项目分类"
        float price "项目定价"
        float cost "项目成本"
    }
    
    PROJECT_SALES {
        string sales_id PK "销售ID"
        string store_id FK "门店ID"
        string project_id FK "项目ID"
        date stat_date "统计日期"
        int sales_count "销售数量"
        float sales_amount "销售金额"
    }
    
    EMPLOYEE {
        string emp_id PK "员工ID"
        string emp_name "员工姓名"
        string store_id FK "门店ID"
        string position "职位"
        string service_type "服务类型"
    }
    
    EMPLOYEE_PERFORMANCE {
        string perf_id PK "绩效ID"
        string emp_id FK "员工ID"
        date stat_date "统计日期"
        float card_amount "划卡总额"
        int order_count "客单数"
        float avg_price "客单价"
    }
    
    MEMBER {
        string member_id PK "会员ID"
        string store_id FK "门店ID"
        date register_date "注册日期"
        float total_recharge "累计充值"
        date last_visit_date "最后到店日期"
        int total_visits "到店次数"
    }
    
    CHANNEL {
        string channel_id PK "渠道ID"
        string channel_name "渠道名称"
        string channel_type "渠道类型"
    }
    
    CHANNEL_DATA {
        string data_id PK "数据ID"
        string store_id FK "门店ID"
        string channel_id FK "渠道ID"
        date stat_date "统计日期"
        int exposure_count "曝光数"
        int click_count "点击数"
        int arrival_count "到店数"
        float avg_price "客单价"
    }
    
    STORE ||--o{ STORE_METRICS : has
    STORE ||--o{ PROJECT_SALES : has
    PROJECT ||--o{ PROJECT_SALES : has
    STORE ||--o{ EMPLOYEE : has
    EMPLOYEE ||--o{ EMPLOYEE_PERFORMANCE : has
    STORE ||--o{ MEMBER : has
    STORE ||--o{ CHANNEL_DATA : has
    CHANNEL ||--o{ CHANNEL_DATA : has
```

### 6.2 CSV 文件结构

| 文件名 | 说明 | 主要字段 |
|--------|------|----------|
| stores.csv | 门店主数据 | store_id, store_name, city, area, open_date |
| store_metrics.csv | 门店月度指标 | store_id, stat_month, revenue, customer_price, visit_frequency, new_customers, repeat_rate |
| projects.csv | 项目主数据 | project_id, project_name, category, price, cost |
| project_sales.csv | 项目销售数据 | store_id, project_id, stat_month, sales_count, sales_amount |
| employees.csv | 员工主数据 | emp_id, emp_name, store_id, position, service_type |
| employee_performance.csv | 员工绩效数据 | emp_id, store_id, stat_month, card_amount, order_count, avg_price |
| members.csv | 会员数据 | member_id, store_id, register_date, total_recharge, last_visit_date, total_visits, recharge_cycle_days, recharged_in_90d |
| channels.csv | 渠道主数据 | channel_id, channel_name, channel_type |
| channel_data.csv | 渠道数据 | store_id, channel_id, stat_month, exposure_count, click_count, arrival_count, avg_price |

## 7. 前端目录结构

```
src/
├── components/          # 公共组件
│   ├── charts/         # 图表组件
│   ├── layout/         # 布局组件
│   └── common/         # 通用组件
├── pages/              # 页面组件
│   ├── StoreAnalysis.vue
│   ├── ProjectAnalysis.vue
│   ├── EmployeeAnalysis.vue
│   ├── MemberLifecycle.vue
│   └── ChannelAnalysis.vue
├── api/                # API 接口
│   ├── request.ts      # 请求封装
│   ├── store.ts
│   ├── project.ts
│   ├── employee.ts
│   ├── member.ts
│   └── channel.ts
├── types/              # TypeScript 类型定义
├── utils/              # 工具函数
├── router/             # 路由配置
├── assets/             # 静态资源
└── App.vue
```

## 8. 后端目录结构

```
backend/
├── app.py              # Flask 应用入口
├── requirements.txt    # Python 依赖
├── routes/             # 路由模块
│   ├── __init__.py
│   ├── store_routes.py
│   ├── project_routes.py
│   ├── employee_routes.py
│   ├── member_routes.py
│   └── channel_routes.py
├── services/           # 业务逻辑层
│   ├── __init__.py
│   ├── store_service.py
│   ├── project_service.py
│   ├── employee_service.py
│   ├── member_service.py
│   └── channel_service.py
├── data/               # CSV 数据目录
│   ├── stores.csv
│   ├── store_metrics.csv
│   ├── projects.csv
│   ├── project_sales.csv
│   ├── employees.csv
│   ├── employee_performance.csv
│   ├── members.csv
│   ├── channels.csv
│   └── channel_data.csv
└── utils/              # 工具模块
    ├── __init__.py
    ├── csv_loader.py
    └── data_processor.py
```
