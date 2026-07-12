---
name: lifestyle-planner-zx
displayName: 生活服务工具
summary: 10个生活算法工具：营养计算(食物数据库)/BMI评估(Deurenberg+Mifflin-St Jeor)/健身计划(渐进过载)/预算优化(50-30-20+LP)/餐饮计划(贪心)/习惯追踪(马尔可夫链)/睡眠分析(多维评分)/旅行优化(TSP+2-opt+Haversine)/购物优化(多店铺比价)/订阅分析(ROI)
tags:
  - lifestyle
  - health
  - travel
  - budget
  - fitness
  - nutrition
version: 2.0.0
language: python
---

# 生活服务工具 (lifestyle-planner-zx)

## 描述

提供10个包含真实算法实现的生活服务工具，覆盖营养计算、BMI健康评估、健身计划生成、预算优化、餐饮计划、习惯追踪分析、睡眠质量分析、旅行路线优化(TSP)、购物清单优化、订阅费用分析等日常生活场景。每个工具均包含完整数学公式实现，非简单函数调用。

## 功能

1. **营养计算器** - 食物数据库+加权评分+缺口分析（18种食物营养表）
2. **BMI健康评估器** - Deurenberg体脂公式+Mifflin-St Jeor BMR+TDEE计算
3. **健身计划生成器** - 渐进过载原则+4周周期化(Mesocycle)+肌群分配
4. **预算优化器** - 50/30/20规则+线性规划优化最大化储蓄+支出分析
5. **餐饮计划器** - 贪心算法+营养密度排序+约束满足(卡路里/宏量营养素)
6. **习惯追踪分析器** - 连续天数统计+马尔可夫链2状态转移矩阵预测
7. **睡眠质量分析器** - 4维加权评分(时长/效率/规律性/深度比例)+改善建议
8. **旅行路线优化器** - TSP最近邻贪心+2-opt局部搜索+Haversine球面距离
9. **购物清单优化器** - 多店铺比价+贪心算法(最大化购买数量或满意度)
10. **订阅费用分析器** - ROI计算+使用率分析+取消建议+替代方案推荐

## 使用

```python
from main import nutrition_calculator, bmi_health_assessor, travel_itinerary_optimizer

# 营养计算
result = nutrition_calculator(
    [{"name": "米饭", "amount": 200}, {"name": "鸡蛋", "amount": 60}],
    {"calories": 2000, "protein": 60, "fat": 60, "carbs": 300, "fiber": 25}
)

# BMI健康评估
health = bmi_health_assessor(weight=70, height=175, age=25, gender=1, activity_level="moderate")

# 旅行路线优化（TSP + 2-opt）
route = travel_itinerary_optimizer(
    destinations=[
        {"name": "故宫", "lat": 39.9163, "lon": 116.3972, "attraction_score": 9, "visit_time": 4},
        {"name": "天坛", "lat": 39.8822, "lon": 116.4066, "attraction_score": 8, "visit_time": 2},
    ],
    days=1, preferences={"culture": 0.6, "nature": 0.4}, constraints={}
)
```

## 依赖

无外部依赖，仅使用Python标准库（math, random, datetime, collections, json）。
