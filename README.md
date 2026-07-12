# lifestyle-planner 生活服务工具

## 概述

生活服务工具是一个纯Python标准库实现的生活辅助工具集合，提供10个工具来帮助管理日常生活的各个方面。

## 功能列表

| 序号 | 函数名 | 功能说明 |
|------|--------|----------|
| 1 | `recipe_recommender` | 食谱推荐 |
| 2 | `workout_planner` | 健身计划 |
| 3 | `budget_tracker` | 预算追踪 |
| 4 | `travel_planner` | 旅行规划 |
| 5 | `meal_planner` | 一周餐饮计划 |
| 6 | `habit_tracker` | 习惯追踪器 |
| 7 | `sleep_analyzer` | 睡眠分析 |
| 8 | `shopping_list_generator` | 购物清单生成 |
| 9 | `weather_outfit_planner` | 穿搭推荐 |
| 10 | `subscription_tracker` | 订阅管理追踪 |

## 安装

无需安装外部依赖，仅使用Python标准库。

## 使用方法

```python
from main import recipe_recommender, workout_planner, budget_tracker

# 食谱推荐
recipes = recipe_recommender(["鸡蛋", "番茄", "鸡肉"], "中餐", None, 5)

# 健身计划
plan = workout_planner("beginner", "weight_loss", 4, ["徒手"])

# 预算追踪
budget = budget_tracker(10000, [{"category": "房租", "amount": 3000}], 2000, "monthly")
```

## 运行

```bash
python main.py
```

## 技术特点

- 零外部依赖，仅使用Python标准库
- 所有函数均有详细的中文docstring
- 内置食谱、运动、穿搭等知识库
- 50/30/20预算法则分析
- 睡眠质量分级和趋势分析
- 订阅费用节省建议
