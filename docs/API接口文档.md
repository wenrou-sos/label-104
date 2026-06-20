# 美容连锁门店经营分析看板系统 - API 接口文档

## 1. 概述

本文档描述了美容连锁门店经营分析看板系统的后端 API 接口规范。所有接口遵循 RESTful 设计风格，返回 JSON 格式数据。

## 2. 接口规范

### 2.1 基础信息

| 项目 | 说明 |
|------|------|
| 基础路径 | `/api/v1` |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |
| 请求方式 | GET |

### 2.2 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，200表示成功 |
| message | string | 状态信息 |
| data | object/array | 响应数据 |

### 2.3 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 2.4 通用查询参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| startDate | string | 否 | 开始日期 (YYYY-MM-DD 或 YYYY-MM) | 2024-01-01 |
| endDate | string | 否 | 结束日期 (YYYY-MM-DD 或 YYYY-MM) | 2024-12-31 |
| storeIds | string | 否 | 门店ID，多个用逗号分隔 | S001,S002,S003 |
| sortBy | string | 否 | 排序字段 | revenue |
| sortOrder | string | 否 | 排序方向 (asc/desc) | desc |

## 3. 门店分析接口

### 3.1 获取门店核心指标

**接口地址**: `GET /api/v1/stores/metrics`

**功能说明**: 获取各门店的核心经营指标数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "store_id": "S001",
      "store_name": "朝阳旗舰店",
      "city": "北京",
      "area": "朝阳区",
      "revenue": 856230.50,
      "customer_price": 398.50,
      "visit_frequency": 3.25,
      "new_customers": 885,
      "repeat_rate": 0.6776
    }
  ]
}
```

### 3.2 获取门店排名对比

**接口地址**: `GET /api/v1/stores/ranking`

**功能说明**: 获取门店排名数据，支持按不同指标排序

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |
| sortBy | string | 否 | 排序字段 (revenue/customer_price/visit_frequency/new_customers/repeat_rate) |
| sortOrder | string | 否 | 排序方向 (asc/desc) |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "rank": 1,
      "store_id": "S003",
      "store_name": "浦东中心店",
      "city": "上海",
      "revenue": 925680.00,
      "customer_price": 425.80,
      "visit_frequency": 3.45,
      "new_customers": 920,
      "repeat_rate": 0.7025
    }
  ]
}
```

### 3.3 获取门店趋势数据

**接口地址**: `GET /api/v1/stores/trend`

**功能说明**: 获取门店指标随时间变化的趋势数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "store_id": "S001",
      "store_name": "朝阳旗舰店",
      "months": ["2024-01", "2024-02", "2024-03"],
      "revenue": [780000, 820000, 856000],
      "customer_price": [380, 390, 398.5],
      "visit_frequency": [3.0, 3.1, 3.25],
      "new_customers": [75, 78, 85],
      "repeat_rate": [0.65, 0.66, 0.6776]
    }
  ]
}
```

## 4. 项目分析接口

### 4.1 获取项目销售占比

**接口地址**: `GET /api/v1/projects/sales`

**功能说明**: 获取各项目的销售额和销售占比

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "project_id": "P001",
      "project_name": "面部清洁护理",
      "category": "皮肤管理",
      "sales_amount": 456200.00,
      "sales_count": 1560,
      "percentage": 0.1525
    }
  ]
}
```

### 4.2 获取项目毛利率

**接口地址**: `GET /api/v1/projects/margin`

**功能说明**: 获取各项目的毛利率数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "project_id": "P001",
      "project_name": "面部清洁护理",
      "category": "皮肤管理",
      "sales_amount": 456200.00,
      "cost_amount": 129800.00,
      "gross_profit": 326400.00,
      "gross_margin": 0.7155
    }
  ]
}
```

### 4.3 获取项目四象限矩阵数据

**接口地址**: `GET /api/v1/projects/matrix`

**功能说明**: 获取项目四象限分析数据（销售额 vs 毛利率）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "avg_sales": 280000,
    "avg_margin": 0.65,
    "projects": [
      {
        "project_id": "P001",
        "project_name": "面部清洁护理",
        "category": "皮肤管理",
        "sales_amount": 456200.00,
        "gross_margin": 0.7155,
        "quadrant": "star"
      }
    ]
  }
}
```

**象限说明**:
- `star`: 明星项目（高销售额、高毛利率）
- `question`: 问题项目（低销售额、高毛利率）
- `cash_cow`: 现金牛项目（高销售额、低毛利率）
- `dog`: 瘦狗项目（低销售额、低毛利率）

## 5. 员工分析接口

### 5.1 获取员工业绩排行

**接口地址**: `GET /api/v1/employees/ranking`

**功能说明**: 获取员工业绩排行榜

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |
| serviceType | string | 否 | 服务类型筛选 |
| sortBy | string | 否 | 排序字段 (card_amount/order_count/avg_price) |
| sortOrder | string | 否 | 排序方向 (asc/desc) |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "rank": 1,
      "emp_id": "E001",
      "emp_name": "张美丽",
      "store_id": "S001",
      "store_name": "朝阳旗舰店",
      "position": "高级美容师",
      "service_type": "皮肤管理",
      "card_amount": 58620.00,
      "order_count": 128,
      "avg_price": 457.97
    }
  ]
}
```

### 5.2 获取员工客单对比

**接口地址**: `GET /api/v1/employees/orders`

**功能说明**: 获取员工客单数与客单价对比数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |
| serviceType | string | 否 | 服务类型筛选 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "emp_id": "E001",
      "emp_name": "张美丽",
      "order_count": 128,
      "avg_price": 457.97,
      "card_amount": 58620.00
    }
  ]
}
```

## 6. 会员分析接口

### 6.1 获取会员充值周期

**接口地址**: `GET /api/v1/members/cycle`

**功能说明**: 获取会员平均充值周期统计数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "avg_cycle_days": 95,
    "median_cycle_days": 88,
    "cycle_distribution": [
      {"range": "0-30天", "count": 150, "percentage": 0.068},
      {"range": "31-60天", "count": 380, "percentage": 0.172},
      {"range": "61-90天", "count": 520, "percentage": 0.235},
      {"range": "91-120天", "count": 480, "percentage": 0.217},
      {"range": "121-180天", "count": 420, "percentage": 0.190},
      {"range": "180天以上", "count": 260, "percentage": 0.118}
    ]
  }
}
```

### 6.2 获取会员复充率

**接口地址**: `GET /api/v1/members/recharge`

**功能说明**: 获取会员复充率统计数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_members": 2210,
    "recharged_members": 1326,
    "recharge_rate": 0.60,
    "store_data": [
      {
        "store_id": "S001",
        "store_name": "朝阳旗舰店",
        "total_members": 320,
        "recharged_members": 205,
        "recharge_rate": 0.6406
      }
    ]
  }
}
```

### 6.3 获取流失预警会员

**接口地址**: `GET /api/v1/members/churn`

**功能说明**: 获取流失预警会员列表（连续60天未到店）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| storeIds | string | 否 | 门店ID列表 |
| daysThreshold | int | 否 | 流失天数阈值，默认60天 |
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页条数，默认20 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 350,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "member_id": "M00001",
        "store_id": "S001",
        "store_name": "朝阳旗舰店",
        "total_recharge": 15800.00,
        "last_visit_date": "2024-10-15",
        "days_since_visit": 75,
        "total_visits": 45,
        "risk_level": "warning"
      }
    ]
  }
}
```

**风险等级**:
- `active`: 活跃（30天内到店）
- `warning`: 预警（31-60天未到店）
- `risk`: 风险（61-90天未到店）
- `churned`: 流失（90天以上未到店）

## 7. 渠道分析接口

### 7.1 获取渠道转化率

**接口地址**: `GET /api/v1/channels/conversion`

**功能说明**: 获取各渠道的转化漏斗数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "channel_id": "C001",
      "channel_name": "美团",
      "channel_type": "本地生活",
      "exposure_count": 85000,
      "click_count": 8500,
      "arrival_count": 320,
      "click_rate": 0.10,
      "conversion_rate": 0.0376
    }
  ]
}
```

### 7.2 获取渠道客单价

**接口地址**: `GET /api/v1/channels/aov`

**功能说明**: 获取各渠道的客单价对比数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "channel_id": "C001",
      "channel_name": "美团",
      "channel_type": "本地生活",
      "arrival_count": 320,
      "avg_price": 420.50,
      "total_revenue": 134560.00
    }
  ]
}
```

### 7.3 获取渠道效果评估

**接口地址**: `GET /api/v1/channels/evaluation`

**功能说明**: 获取各渠道的综合效果评估和优化建议

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| startDate | string | 否 | 开始月份 |
| endDate | string | 否 | 结束月份 |
| storeIds | string | 否 | 门店ID列表 |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "channel_id": "C001",
      "channel_name": "美团",
      "channel_type": "本地生活",
      "conversion_rate": 0.0376,
      "avg_price": 420.50,
      "total_revenue": 134560.00,
      "arrival_count": 320,
      "score": 85,
      "grade": "A",
      "suggestion": "转化效果优秀，建议加大投放力度，可尝试拓展更多服务品类"
    }
  ]
}
```

## 8. 数据导出接口

### 8.1 导出数据

**接口地址**: `GET /api/v1/export/{module}`

**功能说明**: 导出指定模块的数据为 CSV 文件

**路径参数**:

| 参数名 | 说明 |
|--------|------|
| module | 模块名称 |

**支持的模块**:
- `stores/metrics` - 门店指标
- `stores/ranking` - 门店排名
- `projects/sales` - 项目销售
- `projects/margin` - 项目毛利
- `employees/ranking` - 员工排行
- `employees/orders` - 员工客单
- `members/cycle` - 会员周期
- `members/recharge` - 会员复充
- `members/churn` - 会员流失
- `channels/conversion` - 渠道转化
- `channels/aov` - 渠道客单
- `channels/evaluation` - 渠道评估

**请求参数**: 同对应模块的查询参数

**响应**: CSV 文件下载

## 9. 健康检查

### 9.1 健康检查接口

**接口地址**: `GET /api/v1/health`

**功能说明**: 检查服务是否正常运行

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "ok"
  }
}
```
