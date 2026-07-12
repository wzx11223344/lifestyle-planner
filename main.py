#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活服务工具 - lifestyle-planner
提供10个高级生活算法工具：营养计算器(食物数据库)、BMI健康评估(Deurenberg体脂+Mifflin-St Jeor BMR)、
健身计划生成器(渐进过载+周期化)、预算优化器(50/30/20+线性规划)、餐饮计划器(约束满足+贪心算法)、
习惯追踪分析器(马尔可夫链预测)、睡眠质量分析器(多维评分)、旅行路线优化器(TSP最近邻+2-opt改进)、
购物清单优化器(多店铺比价+贪心)、订阅费用分析器(ROI计算)。

全部使用Python标准库实现，无外部依赖。
"""

import json
import math
import random
from collections import defaultdict
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 1. 营养计算器
# ---------------------------------------------------------------------------
def nutrition_calculator(food_items, daily_targets):
    """
    营养计算器：基于食物数据库计算每日营养摄入，对比目标值，输出分析报告。

    算法原理:
        - 食物数据库: 内置常见食物的营养成分表（每100g）
        - 营养加总: 按食物重量比例计算各营养素摄入量
        - 缺口分析: 计算实际摄入与目标的差值和百分比
        - 评分: 各营养素达标率加权平均 → 0-100营养评分

    参数:
        food_items (list[dict]): 食物列表，每项含:
            - name (str): 食物名称
            - amount (float): 重量(g)
        daily_targets (dict): 每日营养目标，含calories/protein/fat/carbs/fiber等

    返回:
        dict: 营养分析报告，含intake_summary/nutrient_gaps/score/recommendations。
    """
    # 食物营养数据库（每100g营养成分）
    food_db = {
        "米饭": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28.0, "fiber": 0.4, "calcium": 7, "iron": 0.2},
        "面条": {"calories": 280, "protein": 9.0, "fat": 0.6, "carbs": 57.0, "fiber": 2.0, "calcium": 15, "iron": 1.5},
        "鸡蛋": {"calories": 147, "protein": 12.6, "fat": 9.5, "carbs": 1.1, "fiber": 0.0, "calcium": 50, "iron": 1.8},
        "牛奶": {"calories": 54, "protein": 3.0, "fat": 3.2, "carbs": 3.4, "fiber": 0.0, "calcium": 104, "iron": 0.1},
        "鸡胸肉": {"calories": 165, "protein": 31.0, "fat": 3.6, "carbs": 0.0, "fiber": 0.0, "calcium": 15, "iron": 1.0},
        "牛肉": {"calories": 250, "protein": 26.0, "fat": 15.0, "carbs": 0.0, "fiber": 0.0, "calcium": 18, "iron": 2.6},
        "猪肉": {"calories": 395, "protein": 13.0, "fat": 37.0, "carbs": 0.0, "fiber": 0.0, "calcium": 6, "iron": 1.0},
        "鱼": {"calories": 145, "protein": 22.0, "fat": 5.0, "carbs": 0.0, "fiber": 0.0, "calcium": 50, "iron": 0.8},
        "豆腐": {"calories": 76, "protein": 8.1, "fat": 3.7, "carbs": 1.9, "fiber": 0.4, "calcium": 138, "iron": 1.5},
        "西兰花": {"calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 7.0, "fiber": 3.1, "calcium": 40, "iron": 0.5},
        "菠菜": {"calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "fiber": 2.2, "calcium": 99, "iron": 2.7},
        "番茄": {"calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "fiber": 1.2, "calcium": 10, "iron": 0.3},
        "苹果": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14.0, "fiber": 2.4, "calcium": 6, "iron": 0.1},
        "香蕉": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23.0, "fiber": 2.6, "calcium": 5, "iron": 0.3},
        "面包": {"calories": 265, "protein": 9.0, "fat": 3.2, "carbs": 49.0, "fiber": 2.7, "calcium": 107, "iron": 3.6},
        "燕麦": {"calories": 389, "protein": 16.9, "fat": 6.9, "carbs": 66.0, "fiber": 10.6, "calcium": 54, "iron": 4.7},
        "坚果": {"calories": 607, "protein": 20.0, "fat": 54.0, "carbs": 13.0, "fiber": 7.0, "calcium": 100, "iron": 3.0},
        "酸奶": {"calories": 72, "protein": 2.5, "fat": 2.7, "carbs": 9.3, "fiber": 0.0, "calcium": 120, "iron": 0.1},
    }

    # 步骤1: 按食物重量计算营养摄入
    intake = defaultdict(float)
    food_details = []
    unrecognized = []

    for item in food_items:
        name = item.get("name", "")
        amount = item.get("amount", 100)
        # 模糊匹配食物名称
        matched_key = None
        for db_key in food_db:
            if db_key in name or name in db_key:
                matched_key = db_key
                break

        if matched_key:
            ratio = amount / 100.0
            nutrients = food_db[matched_key]
            food_intake = {}
            for nutrient, value in nutrients.items():
                actual = value * ratio
                intake[nutrient] += actual
                food_intake[nutrient] = round(actual, 1)
            food_details.append({
                "name": name, "matched": matched_key, "amount_g": amount,
                "nutrients": food_intake
            })
        else:
            unrecognized.append(name)

    # 步骤2: 计算营养缺口和达标率
    gaps = {}
    achievement_rates = []
    for nutrient, target in daily_targets.items():
        actual = intake.get(nutrient, 0)
        gap = target - actual
        rate = min(actual / target, 1.0) if target > 0 else 1.0
        achievement_rates.append(rate)
        gaps[nutrient] = {
            "target": target,
            "actual": round(actual, 1),
            "gap": round(gap, 1),
            "achievement_rate": round(rate * 100, 1),
            "status": "达标" if rate >= 0.9 else ("接近" if rate >= 0.7 else "不足") if rate >= 0.5 else "严重不足"
        }

    # 步骤3: 营养评分（加权平均达标率）
    # 蛋白质和热量权重更高
    weights = {"calories": 0.25, "protein": 0.25, "fat": 0.15, "carbs": 0.15, "fiber": 0.10, "calcium": 0.05, "iron": 0.05}
    weighted_sum = 0.0
    weight_total = 0.0
    for nutrient, rate in zip(daily_targets.keys(), achievement_rates):
        w = weights.get(nutrient, 0.05)
        weighted_sum += rate * w
        weight_total += w
    score = round((weighted_sum / weight_total * 100) if weight_total > 0 else 0, 1)

    # 步骤4: 生成建议
    recommendations = []
    for nutrient, info in gaps.items():
        if info["status"] == "严重不足":
            recommendations.append(f"严重缺乏{nutrient}！建议增加富含{nutrient}的食物摄入")
        elif info["status"] == "不足":
            recommendations.append(f"{nutrient}摄入不足，还需补充{info['gap']:.1f}{nutrient}")
    if not recommendations:
        recommendations.append("营养摄入均衡，继续保持！")

    return {
        "total_intake": {k: round(v, 1) for k, v in intake.items()},
        "food_details": food_details,
        "unrecognized_foods": unrecognized,
        "nutrient_gaps": gaps,
        "nutrition_score": score,
        "grade": "优秀" if score >= 85 else ("良好" if score >= 70 else ("及格" if score >= 50 else "不及格")),
        "recommendations": recommendations
    }


# ---------------------------------------------------------------------------
# 2. BMI健康评估器
# ---------------------------------------------------------------------------
def bmi_health_assessor(weight, height, age, gender, activity_level):
    """
    BMI健康评估器：计算BMI+体脂率估算+基础代谢率(BMR)+每日总能量消耗(TDEE)。

    算法原理:
        - BMI: BMI = weight(kg) / height(m)^2
        - 体脂率(Deurenberg公式): BF = 1.20*BMI + 0.23*age - 10.8*gender - 5.4
          (gender: male=1, female=0)
        - BMR(Mifflin-St Jeor): 
          男性: BMR = 10*weight + 6.25*height - 5*age + 5
          女性: BMR = 10*weight + 6.25*height - 5*age - 161
        - TDEE: BMR * 活动系数（久坐1.2/轻度1.375/中度1.55/高度1.725/极高1.9）

    参数:
        weight (float): 体重(kg)
        height (float): 身高(cm)
        age (int): 年龄
        gender (str): "male"或"female"
        activity_level (str): 活动等级 "sedentary"/"light"/"moderate"/"active"/"very_active"

    返回:
        dict: 健康评估报告，含bmi/body_fat/bmr/tdee/health_category/recommendations。
    """
    # BMI分类标准
    bmi_categories = [
        (18.5, "偏瘦", "体重偏低，建议适当增加营养摄入"),
        (24.0, "正常", "体重正常，保持健康的生活方式"),
        (28.0, "超重", "体重超标，建议控制饮食并增加运动"),
        (float('inf'), "肥胖", "体重严重超标，建议咨询医生制定减重计划")
    ]

    # 活动系数映射
    activity_factors = {
        "sedentary": 1.2,    # 久坐不动
        "light": 1.375,       # 轻度活动（每周1-3天）
        "moderate": 1.55,     # 中度活动（每周3-5天）
        "active": 1.725,      # 高度活动（每周6-7天）
        "very_active": 1.9    # 极高活动（体力工作者/运动员）
    }

    # 性别数值映射
    gender_value = 1 if gender.lower() == "male" else 0
    gender_label = "男性" if gender_value == 1 else "女性"

    # 步骤1: 计算BMI
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)

    # 步骤2: 计算体脂率（Deurenberg公式）
    # BF = 1.20*BMI + 0.23*age - 10.8*gender - 5.4
    body_fat = 1.20 * bmi + 0.23 * age - 10.8 * gender_value - 5.4

    # 步骤3: 计算基础代谢率BMR（Mifflin-St Jeor公式）
    if gender_value == 1:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 步骤4: 计算每日总能量消耗TDEE
    activity_factor = activity_factors.get(activity_level, 1.375)
    tdee = bmr * activity_factor

    # 步骤5: 确定BMI分类
    bmi_category = None
    for threshold, category, advice in bmi_categories:
        if bmi < threshold:
            bmi_category = (category, advice)
            break

    # 步骤6: 体脂率评估
    if gender_value == 1:
        fat_standards = [(10, "偏低"), (20, "正常"), (25, "偏高"), (float('inf'), "肥胖")]
    else:
        fat_standards = [(18, "偏低"), (28, "正常"), (33, "偏高"), (float('inf'), "肥胖")]

    fat_status = None
    for threshold, status in fat_standards:
        if body_fat < threshold:
            fat_status = status
            break

    # 步骤7: 计算理想体重范围
    ideal_weight_min = 18.5 * (height_m ** 2)
    ideal_weight_max = 24.0 * (height_m ** 2)
    weight_diff = weight - (ideal_weight_min + ideal_weight_max) / 2

    # 步骤8: 生成健康建议
    recommendations = [bmi_category[1]]
    if fat_status in ("偏高", "肥胖"):
        recommendations.append(f"体脂率{body_fat:.1f}%偏高，建议通过有氧运动和饮食控制减脂")
    if bmi >= 28:
        caloric_deficit = min(500, tdee * 0.2)
        recommendations.append(f"建议每日热量赤字{caloric_deficit:.0f}kcal，目标摄入{TDEE - caloric_deficit:.0f}kcal")
    elif bmi < 18.5:
        caloric_surplus = min(300, tdee * 0.15)
        recommendations.append(f"建议每日热量盈余{caloric_surplus:.0f}kcal，目标摄入{TDEE + caloric_surplus:.0f}kcal")
    recommendations.append(f"每日建议蛋白质摄入{weight * 1.2:.0f}g-{weight * 1.6:.0f}g")

    return {
        "bmi": round(bmi, 1),
        "bmi_category": bmi_category[0],
        "body_fat_percentage": round(body_fat, 1),
        "body_fat_status": fat_status,
        "bmr": round(bmr, 0),
        "tdee": round(tdee, 0),
        "ideal_weight_range": [round(ideal_weight_min, 1), round(ideal_weight_max, 1)],
        "weight_status": "偏重" if weight_diff > 0 else "偏轻" if weight_diff < -2 else "理想",
        "weight_difference": round(weight_diff, 1),
        "activity_level": activity_level,
        "gender": gender_label,
        "recommendations": recommendations
    }


# ---------------------------------------------------------------------------
# 3. 健身计划生成器
# ---------------------------------------------------------------------------
def fitness_plan_generator(goal, current_level, days_per_week, equipment):
    """
    健身计划生成器：基于目标+渐进过载原则+肌群分配生成周期化训练计划。

    算法原理:
        - 渐进过载: 每周增加2.5-5%训练量（重量或次数），第4周减载（Deload）
        - 周期化: 4周一个Mesocycle，含渐进期(1-3周)+减载期(第4周)
        - 肌群分配: 按天数分配（3天=推拉腿、4天=上下分化、5天=单肌群）
        - 强度计算: 1RM百分比 × 组数 × 次数 = 训练量(TVL)

    参数:
        goal (str): 训练目标 "fat_loss"/"muscle_gain"/"endurance"/"strength"
        current_level (str): 当前水平 "beginner"/"intermediate"/"advanced"
        days_per_week (int): 每周训练天数
        equipment (list[str]): 可用设备列表

    返回:
        dict: 4周训练计划，含weekly_plans/exercises/progression_chart。
    """
    # 目标配置
    goal_configs = {
        "fat_loss": {"reps": 15, "sets": 3, "rest": 30, "weight_pct": 0.55, "cardio_ratio": 0.4},
        "muscle_gain": {"reps": 10, "sets": 4, "rest": 90, "weight_pct": 0.70, "cardio_ratio": 0.15},
        "endurance": {"reps": 20, "sets": 3, "rest": 45, "weight_pct": 0.45, "cardio_ratio": 0.5},
        "strength": {"reps": 5, "sets": 5, "rest": 180, "weight_pct": 0.85, "cardio_ratio": 0.1}
    }
    config = goal_configs.get(goal, goal_configs["muscle_gain"])

    # 水平系数
    level_modifiers = {"beginner": 0.85, "intermediate": 1.0, "advanced": 1.15}
    level_mod = level_modifiers.get(current_level, 1.0)

    # 训练分割方案
    splits = {
        3: [["胸+三头", "背+二头", "腿+肩"]],
        4: [["胸+三头", "背+二头", "腿", "肩+核心"]],
        5: [["胸", "背", "腿", "肩", "手臂"]],
        6: [["胸", "背", "腿前", "肩", "手臂", "腿后"]],
    }
    split = splits.get(days_per_week, splits[3])[0]

    # 动作数据库
    exercise_db = {
        "胸": [{"name": "杠铃卧推", "compound": True}, {"name": "哑铃飞鸟", "compound": False}, {"name": "俯卧撑", "compound": True}],
        "背": [{"name": "引体向上", "compound": True}, {"name": "杠铃划船", "compound": True}, {"name": "高位下拉", "compound": False}],
        "腿": [{"name": "杠铃深蹲", "compound": True}, {"name": "腿举", "compound": False}, {"name": "罗马尼亚硬拉", "compound": True}],
        "肩": [{"name": "杠铃推举", "compound": True}, {"name": "侧平举", "compound": False}, {"name": "面拉", "compound": False}],
        "手臂": [{"name": "杠铃弯举", "compound": False}, {"name": "绳索下压", "compound": False}, {"name": "锤式弯举", "compound": False}],
        "核心": [{"name": "平板支撑", "compound": True}, {"name": "悬垂举腿", "compound": False}, {"name": "俄罗斯转体", "compound": False}],
        "腿前": [{"name": "杠铃深蹲", "compound": True}, {"name": "前蹲", "compound": True}, {"name": "腿屈伸", "compound": False}],
        "腿后": [{"name": "罗马尼亚硬拉", "compound": True}, {"name": "腿弯举", "compound": False}, {"name": "臀桥", "compound": True}],
        "胸+三头": [{"name": "杠铃卧推", "compound": True}, {"name": "上斜哑铃卧推", "compound": False}, {"name": "绳索下压", "compound": False}],
        "背+二头": [{"name": "引体向上", "compound": True}, {"name": "杠铃划船", "compound": True}, {"name": "杠铃弯举", "compound": False}],
        "腿+肩": [{"name": "杠铃深蹲", "compound": True}, {"name": "罗马尼亚硬拉", "compound": True}, {"name": "杠铃推举", "compound": True}],
    }

    # 步骤1: 生成4周渐进计划
    weekly_plans = []
    progression_chart = []

    for week in range(1, 5):
        # 渐进过载: 每周增加5%训练量，第4周减载
        if week < 4:
            overload = 1.0 + (week - 1) * 0.05  # 第1周100%, 第2周105%, 第3周110%
            is_deload = False
        else:
            overload = 0.6  # 减载周60%训练量
            is_deload = True

        week_plan = {"week": week, "phase": "减载期" if is_deload else "渐进期", "overload_factor": round(overload, 2), "days": []}

        for day_idx in range(days_per_week):
            muscle_group = split[day_idx % len(split)]
            exercises = exercise_db.get(muscle_group, exercise_db["胸"])

            day_exercises = []
            for ex in exercises[:3]:  # 每个部位3个动作
                # 渐进过载: 重量和组数随周递增
                base_sets = config["sets"]
                adjusted_sets = max(2, int(base_sets * overload * level_mod))
                adjusted_reps = max(3, int(config["reps"] * (1.0 - (week - 1) * 0.02))) if goal == "strength" else config["reps"]
                weight_pct = config["weight_pct"] * overload * level_mod

                day_exercises.append({
                    "name": ex["name"],
                    "muscle_group": muscle_group,
                    "sets": adjusted_sets,
                    "reps": adjusted_reps,
                    "rest_seconds": config["rest"],
                    "intensity_pct": round(weight_pct * 100, 1),
                    "estimated_1rm_factor": round(weight_pct, 2)
                })

            # 有氧运动
            if config["cardio_ratio"] > 0:
                cardio_time = int(30 * config["cardio_ratio"] * (1.5 if goal == "fat_loss" else 1.0))
                day_exercises.append({
                    "name": "有氧运动（跑步/椭圆机）",
                    "type": "cardio",
                    "duration_minutes": cardio_time,
                    "intensity": "中等" if goal != "endurance" else "高强度"
                })

            week_plan["days"].append({
                "day": day_idx + 1,
                "focus": muscle_group,
                "exercises": day_exercises
            })

        # 计算周训练量
        total_sets = sum(len([e for e in d["exercises"] if e.get("type") != "cardio"]) for d in week_plan["days"])
        progression_chart.append({
            "week": week, "total_sets": total_sets,
            "intensity_level": round(config["weight_pct"] * overload * 100, 1),
            "phase": "减载" if is_deload else f"渐进{week}"
        })
        weekly_plans.append(week_plan)

    return {
        "goal": goal,
        "level": current_level,
        "days_per_week": days_per_week,
        "split": split,
        "weekly_plans": weekly_plans,
        "progression_chart": progression_chart,
        "principles": [
            "渐进过载: 每周增加5%训练量，第4周减载至60%",
            "周期化: 4周一个Mesocycle，含3周渐进+1周减载",
            f"强度区间: {config['weight_pct']*100:.0f}% 1RM × {config['sets']}组 × {config['reps']}次",
            f"组间休息: {config['rest']}秒"
        ]
    }


# ---------------------------------------------------------------------------
# 4. 预算优化器
# ---------------------------------------------------------------------------
def budget_optimizer(income, expenses, savings_goal, categories):
    """
    预算优化器：基于50/30/20规则+零基预算+线性规划优化最大化储蓄。

    算法原理:
        - 50/30/20规则: 需求50% / 想要30% / 储蓄20%
        - 零基预算: 收入 = 支出 + 储蓄，每分钱都有去处
        - 线性规划: 在约束条件下最大化储蓄 S = income - Σ(expenses')
          约束: 基本需求 ≥ 50% * income (下限), 储蓄 ≥ savings_goal (下限)
        - 支出分析: 各类目占比 + 超支预警

    参数:
        income (float): 月收入
        expenses (list[dict]): 支出列表，每项含category/amount/essential(是否必要支出)
        savings_goal (float): 储蓄目标
        categories (dict): 预算分类上限，如{"housing": 0.3, "food": 0.15, "entertainment": 0.1}

    返回:
        dict: 预算优化方案，含allocation/analysis/optimizations/alerts。
    """
    total_expenses = sum(e["amount"] for e in expenses)
    current_savings = income - total_expenses

    # 步骤1: 50/30/20规则分析
    rule_50 = income * 0.5  # 需求
    rule_30 = income * 0.3  # 想要
    rule_20 = income * 0.2  # 储蓄

    # 步骤2: 分类支出统计
    category_spending = defaultdict(float)
    category_essential = {}
    for e in expenses:
        cat = e.get("category", "other")
        category_spending[cat] += e["amount"]
        category_essential[cat] = e.get("essential", False)

    # 步骤3: 必要支出 vs 非必要支出
    essential_total = sum(e["amount"] for e in expenses if e.get("essential", False))
    non_essential_total = total_expenses - essential_total

    # 步骤4: 线性规划优化 - 最大化储蓄
    # 变量: 每个非必要支出类目的缩减比例 (0 ~ 0.5)
    # 目标: 最大化 S = income - essential - Σ(non_essential_i * (1 - reduction_i))
    # 约束1: 各类目支出 >= 类目下限
    # 约束2: 储蓄 >= savings_goal
    # 约束3: 缩减比例 ∈ [0, 0.5]

    optimizations = []
    optimized_expenses = {}

    for cat, amount in category_spending.items():
        limit_ratio = categories.get(cat, 0.1)
        limit = income * limit_ratio
        is_essential = category_essential.get(cat, False)

        if is_essential:
            # 必要支出不缩减
            optimized_expenses[cat] = amount
        else:
            # 非必要支出: 缩减至上限或保持
            if amount > limit:
                reduction = amount - limit
                optimized_expenses[cat] = limit
                optimizations.append({
                    "category": cat,
                    "original": amount,
                    "optimized": limit,
                    "reduction": round(reduction, 2),
                    "reduction_pct": round(reduction / amount * 100, 1)
                })
            else:
                optimized_expenses[cat] = amount

    optimized_total = sum(optimized_expenses.values())
    optimized_savings = income - optimized_total

    # 步骤5: 如果优化后仍达不到储蓄目标，进一步缩减非必要支出
    if optimized_savings < savings_goal:
        deficit = savings_goal - optimized_savings
        # 按非必要支出占比分配缩减
        non_essential_cats = {c: a for c, a in optimized_expenses.items() if not category_essential.get(c, False)}
        non_essential_sum = sum(non_essential_cats.values())
        if non_essential_sum > 0:
            for cat, amount in non_essential_cats.items():
                cut_ratio = amount / non_essential_sum
                cut = min(deficit * cut_ratio, amount * 0.3)  # 最多削减30%
                optimized_expenses[cat] -= cut
                optimizations.append({
                    "category": cat,
                    "original": amount,
                    "optimized": round(optimized_expenses[cat], 2),
                    "reduction": round(cut, 2),
                    "reduction_pct": round(cut / amount * 100, 1),
                    "reason": "为达成储蓄目标进一步缩减"
                })
            optimized_total = sum(optimized_expenses.values())
            optimized_savings = income - optimized_total

    # 步骤6: 支出分析
    analysis = []
    for cat, amount in sorted(category_spending.items(), key=lambda x: -x[1]):
        pct = amount / income * 100
        limit_ratio = categories.get(cat, 0.1)
        status = "正常" if pct <= limit_ratio * 100 * 1.1 else ("偏高" if pct <= limit_ratio * 100 * 1.5 else "超支")
        analysis.append({
            "category": cat,
            "amount": round(amount, 2),
            "percentage": round(pct, 1),
            "budget_limit": round(income * limit_ratio, 2),
            "limit_ratio": f"{limit_ratio*100:.0f}%",
            "status": status,
            "essential": category_essential.get(cat, False)
        })

    # 步骤7: 预警
    alerts = []
    if essential_total > rule_50:
        alerts.append(f"必要支出占比{essential_total/income*100:.0f}%超过50%阈值，收入偏低或支出结构不合理")
    if current_savings < 0:
        alerts.append(f"当前入不敷出，赤字{abs(current_savings):.0f}元，需立即削减支出")
    if optimized_savings < savings_goal:
        alerts.append(f"即使优化后储蓄仍低于目标，建议增加收入来源")
    if non_essential_total > rule_30:
        alerts.append(f"非必要支出占比{non_essential_total/income*100:.0f}%超过30%阈值")

    return {
        "income": income,
        "current_expenses": round(total_expenses, 2),
        "current_savings": round(current_savings, 2),
        "optimized_expenses": {k: round(v, 2) for k, v in optimized_expenses.items()},
        "optimized_total": round(optimized_total, 2),
        "optimized_savings": round(optimized_savings, 2),
        "savings_goal": savings_goal,
        "goal_achieved": optimized_savings >= savings_goal,
        "rule_50_30_20": {
            "needs_50": round(rule_50, 2),
            "wants_30": round(rule_30, 2),
            "savings_20": round(rule_20, 2),
            "actual_needs": round(essential_total, 2),
            "actual_wants": round(non_essential_total, 2),
            "actual_savings": round(current_savings, 2)
        },
        "category_analysis": analysis,
        "optimizations": optimizations,
        "total_savings_increase": round(optimized_savings - current_savings, 2),
        "alerts": alerts
    }


# ---------------------------------------------------------------------------
# 5. 餐饮计划器
# ---------------------------------------------------------------------------
def meal_planner(calorie_target, meals_per_day, food_database, restrictions):
    """
    餐饮计划器：基于营养目标+约束满足+贪心算法生成每日餐食方案。

    算法原理:
        - 约束满足: 每餐热量 ≈ calorie_target / meals_per_day，宏量营养素比例约束
        - 贪心算法: 优先选择营养密度高的食物（营养/热量比）
        - 随机化: 从候选食物中随机选择以增加多样性
        - 迭代调整: 超出/不足热量时增减食物份量

    参数:
        calorie_target (int): 每日热量目标
        meals_per_day (int): 每日餐数
        food_database (list[dict]): 食物数据库，每项含name/calories/protein/fat/carbs/serving_size
        restrictions (list[str]): 饮食限制列表

    返回:
        dict: 每日餐食方案，含meals/nutrition_summary/variety_score。
    """
    # 宏量营养素目标比例
    macro_ratios = {"protein": 0.30, "fat": 0.25, "carbs": 0.45}

    # 过滤受限食物
    available_foods = []
    for food in food_database:
        is_restricted = False
        for restriction in restrictions:
            if restriction.lower() in food.get("name", "").lower():
                is_restricted = True
                break
        if not is_restricted:
            available_foods.append(food)

    if not available_foods:
        available_foods = food_database  # 如果全部受限则不过滤

    # 步骤1: 计算营养密度（蛋白质/热量比）
    for food in available_foods:
        cal = food.get("calories", 100)
        protein = food.get("protein", 0)
        food["nutrition_density"] = protein / cal if cal > 0 else 0

    # 按营养密度排序
    sorted_foods = sorted(available_foods, key=lambda x: x.get("nutrition_density", 0), reverse=True)

    # 步骤2: 每餐热量分配
    calories_per_meal = calorie_target / meals_per_day
    protein_per_meal = (calorie_target * macro_ratios["protein"] / 4) / meals_per_day  # 蛋白质4kcal/g
    carbs_per_meal = (calorie_target * macro_ratios["carbs"] / 4) / meals_per_day
    fat_per_meal = (calorie_target * macro_ratios["fat"] / 9) / meals_per_day

    meals = []
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    used_foods = set()

    for meal_idx in range(meals_per_day):
        meal_name = ["早餐", "午餐", "晚餐", "加餐"][meal_idx % 4]
        meal_calories = 0
        meal_foods = []
        meal_protein = 0
        meal_fat = 0
        meal_carbs = 0

        # 步骤3: 贪心选择食物
        # 分高密度和低密度，按2:1比例选择
        high_density = [f for f in sorted_foods if f.get("nutrition_density", 0) > 0.05]
        low_density = [f for f in sorted_foods if f.get("nutrition_density", 0) <= 0.05]

        # 每餐选择3-5个食物
        num_items = random.randint(3, min(5, len(available_foods)))

        for _ in range(num_items):
            # 80%概率选高密度食物，20%选低密度
            if random.random() < 0.7 and high_density:
                food = random.choice(high_density)
            elif low_density:
                food = random.choice(low_density)
            else:
                food = random.choice(available_foods)

            # 计算份量以达到每餐热量目标
            remaining = calories_per_meal - meal_calories
            if remaining <= 0:
                break

            serving_cal = food.get("calories", 100)
            # 份量比例: 目标热量的30-50%
            target_cal = remaining * random.uniform(0.25, 0.45)
            servings = max(0.5, target_cal / serving_cal if serving_cal > 0 else 1)

            actual_cal = serving_cal * servings
            actual_protein = food.get("protein", 0) * servings
            actual_fat = food.get("fat", 0) * servings
            actual_carbs = food.get("carbs", 0) * servings

            meal_foods.append({
                "name": food.get("name", "未知食物"),
                "servings": round(servings, 2),
                "serving_size": food.get("serving_size", "100g"),
                "calories": round(actual_cal, 0),
                "protein": round(actual_protein, 1),
                "fat": round(actual_fat, 1),
                "carbs": round(actual_carbs, 1)
            })

            meal_calories += actual_cal
            meal_protein += actual_protein
            meal_fat += actual_fat
            meal_carbs += actual_carbs
            used_foods.add(food.get("name", ""))

        # 步骤4: 微调份量使总热量接近目标
        calorie_diff = calories_per_meal - meal_calories
        if abs(calorie_diff) > 50 and meal_foods:
            # 等比例调整所有食物份量
            adjust_ratio = calories_per_meal / meal_calories if meal_calories > 0 else 1
            for mf in meal_foods:
                mf["servings"] = round(mf["servings"] * adjust_ratio, 2)
                mf["calories"] = round(mf["calories"] * adjust_ratio, 0)
                mf["protein"] = round(mf["protein"] * adjust_ratio, 1)
                mf["fat"] = round(mf["fat"] * adjust_ratio, 1)
                mf["carbs"] = round(mf["carbs"] * adjust_ratio, 1)
            meal_calories *= adjust_ratio
            meal_protein *= adjust_ratio
            meal_fat *= adjust_ratio
            meal_carbs *= adjust_ratio

        meals.append({
            "meal": meal_name,
            "foods": meal_foods,
            "total_calories": round(meal_calories, 0),
            "total_protein": round(meal_protein, 1),
            "total_fat": round(meal_fat, 1),
            "total_carbs": round(meal_carbs, 1)
        })

        total_calories += meal_calories
        total_protein += meal_protein
        total_fat += meal_fat
        total_carbs += meal_carbs

    # 步骤5: 多样性评分（使用的不同食物数/总食物数）
    variety_score = round(len(used_foods) / max(len(available_foods), 1) * 100, 1)

    # 步骤6: 营养达标分析
    target_protein = calorie_target * macro_ratios["protein"] / 4
    target_carbs = calorie_target * macro_ratios["carbs"] / 4
    target_fat = calorie_target * macro_ratios["fat"] / 9

    return {
        "meals": meals,
        "nutrition_summary": {
            "total_calories": round(total_calories, 0),
            "calorie_target": calorie_target,
            "calorie_diff": round(total_calories - calorie_target, 0),
            "total_protein": round(total_protein, 1),
            "total_fat": round(total_fat, 1),
            "total_carbs": round(total_carbs, 1),
            "macro_ratios": {
                "protein_pct": round(total_protein * 4 / total_calories * 100, 1) if total_calories > 0 else 0,
                "fat_pct": round(total_fat * 9 / total_calories * 100, 1) if total_calories > 0 else 0,
                "carbs_pct": round(total_carbs * 4 / total_calories * 100, 1) if total_calories > 0 else 0
            }
        },
        "variety_score": variety_score,
        "foods_used": len(used_foods),
        "restrictions_applied": restrictions
    }


# ---------------------------------------------------------------------------
# 6. 习惯追踪分析器
# ---------------------------------------------------------------------------
def habit_tracker_streak_analyzer(habit_data):
    """
    习惯追踪分析器：计算连续天数/完成率/趋势预测（马尔可夫链）。

    算法原理:
        - 连续天数: 从最后一天往前计算连续完成的天数
        - 完成率: 完成天数 / 总天数
        - 马尔可夫链预测: 构建2状态转移矩阵（完成↔未完成），
          P(next_done) = P(done|done)*P(current_done) + P(done|not_done)*P(current_not_done)
        - 趋势分析: 滑动窗口完成率变化趋势

    参数:
        habit_data (dict): 习惯追踪数据，含:
            - habit_name (str): 习惯名称
            - records (list[dict]): 每日记录，含date和completed(bool)

    返回:
        dict: 习惯分析报告，含streak/completion_rate/prediction/trend。
    """
    records = habit_data.get("records", [])
    if not records:
        return {"error": "无记录数据"}

    habit_name = habit_data.get("habit_name", "习惯")
    total_days = len(records)

    # 步骤1: 计算当前连续天数（从最后一天往前）
    current_streak = 0
    for record in reversed(records):
        if record.get("completed", False):
            current_streak += 1
        else:
            break

    # 步骤2: 计算最长连续记录
    longest_streak = 0
    temp_streak = 0
    for record in records:
        if record.get("completed", False):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0

    # 步骤3: 计算完成率
    completed_days = sum(1 for r in records if r.get("completed", False))
    completion_rate = completed_days / total_days if total_days > 0 else 0

    # 步骤4: 构建马尔可夫链转移矩阵
    # 状态: 0=未完成, 1=完成
    transitions = {"00": 0, "01": 0, "10": 0, "11": 0}
    for i in range(len(records) - 1):
        curr = 1 if records[i].get("completed", False) else 0
        next_d = 1 if records[i + 1].get("completed", False) else 0
        key = str(curr) + str(next_d)
        transitions[key] += 1

    # 计算转移概率
    from_done = transitions["11"] + transitions["10"]
    from_not = transitions["01"] + transitions["00"]

    p_done_given_done = transitions["11"] / from_done if from_done > 0 else 0.5
    p_done_given_not = transitions["01"] / from_not if from_not > 0 else 0.5

    # 步骤5: 预测未来7天完成概率
    current_state_prob = 1.0 if records[-1].get("completed", False) else 0.0
    predictions = []
    for day in range(7):
        # P(next_done) = P(done|done)*P(current_done) + P(done|not_done)*P(current_not_done)
        p_next_done = (p_done_given_done * current_state_prob +
                       p_done_given_not * (1 - current_state_prob))
        predictions.append({
            "day": day + 1,
            "predicted_completion_prob": round(p_next_done * 100, 1)
        })
        current_state_prob = p_next_done

    # 步骤6: 趋势分析（7天滑动窗口）
    window_size = min(7, total_days)
    weekly_rates = []
    for i in range(0, total_days - window_size + 1):
        window = records[i:i + window_size]
        rate = sum(1 for r in window if r.get("completed", False)) / window_size
        weekly_rates.append(rate)

    trend_direction = "上升" if len(weekly_rates) >= 2 and weekly_rates[-1] > weekly_rates[0] + 0.05 else \
                       "下降" if len(weekly_rates) >= 2 and weekly_rates[-1] < weekly_rates[0] - 0.05 else "稳定"

    # 步骤7: 习惯等级评定
    if completion_rate >= 0.9:
        grade = "钻石级"
    elif completion_rate >= 0.75:
        grade = "黄金级"
    elif completion_rate >= 0.5:
        grade = "白银级"
    elif completion_rate >= 0.25:
        grade = "青铜级"
    else:
        grade = "新手级"

    # 步骤8: 周内模式分析
    weekday_completion = [0] * 7
    weekday_total = [0] * 7
    for record in records:
        date_str = record.get("date", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = dt.weekday()
            weekday_total[weekday] += 1
            if record.get("completed", False):
                weekday_completion[weekday] += 1
        except (ValueError, TypeError):
            pass

    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_analysis = []
    for i in range(7):
        rate = weekday_completion[i] / weekday_total[i] if weekday_total[i] > 0 else 0
        weekday_analysis.append({
            "weekday": weekday_names[i],
            "completion_rate": round(rate * 100, 1),
            "total_days": weekday_total[i]
        })

    return {
        "habit_name": habit_name,
        "total_days": total_days,
        "completed_days": completed_days,
        "completion_rate": round(completion_rate * 100, 1),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "grade": grade,
        "markov_chain": {
            "transition_matrix": {
                "P(done|done)": round(p_done_given_done, 3),
                "P(not_done|done)": round(1 - p_done_given_done, 3),
                "P(done|not_done)": round(p_done_given_not, 3),
                "P(not_done|not_done)": round(1 - p_done_given_not, 3)
            },
            "predictions": predictions
        },
        "trend": {
            "direction": trend_direction,
            "recent_rate": round(weekly_rates[-1] * 100, 1) if weekly_rates else 0,
            "earliest_rate": round(weekly_rates[0] * 100, 1) if weekly_rates else 0
        },
        "weekday_pattern": weekday_analysis,
        "insights": [
            f"当前连续{current_streak}天，历史最长{longest_streak}天",
            f"完成率{completion_rate*100:.1f}%，等级：{grade}",
            f"趋势：{trend_direction}",
            f"马尔可夫预测明日完成概率：{predictions[0]['predicted_completion_prob']}%" if predictions else ""
        ]
    }


# ---------------------------------------------------------------------------
# 7. 睡眠质量分析器
# ---------------------------------------------------------------------------
def sleep_quality_analyzer(sleep_records):
    """
    睡眠质量分析器：计算睡眠时长/入睡效率/规律性/质量评分。

    算法原理:
        - 平均睡眠时长: Σ(duration) / n
        - 入睡效率: actual_sleep_time / time_in_bed * 100%
        - 睡眠规律性: 睡眠时长标准差（越小越规律）
        - 质量评分: 加权综合(时长40% + 效率30% + 规律性20% + 深睡比例10%)
        - 理想睡眠: 7-9小时，效率>85%，标准差<1小时

    参数:
        sleep_records (list[dict]): 睡眠记录列表，每项含:
            - date (str): 日期
            - bedtime (str): 就寝时间
            - wakeup (str): 起床时间
            - sleep_duration (float): 实际睡眠时长(小时)
            - time_in_bed (float): 在床时间(小时)
            - deep_sleep (float): 深睡时间(小时)
            - awakenings (int): 夜间醒来次数

    返回:
        dict: 睡眠分析报告，含averages/quality_score/grade/recommendations。
    """
    if not sleep_records:
        return {"error": "无睡眠记录"}

    n = len(sleep_records)

    # 步骤1: 计算平均值
    avg_duration = sum(r.get("sleep_duration", 0) for r in sleep_records) / n
    avg_time_in_bed = sum(r.get("time_in_bed", 0) for r in sleep_records) / n
    avg_deep_sleep = sum(r.get("deep_sleep", 0) for r in sleep_records) / n
    avg_awakenings = sum(r.get("awakenings", 0) for r in sleep_records) / n

    # 步骤2: 计算入睡效率
    avg_efficiency = (avg_duration / avg_time_in_bed * 100) if avg_time_in_bed > 0 else 0

    # 步骤3: 计算睡眠时长标准差（规律性指标）
    variance = sum((r.get("sleep_duration", 0) - avg_duration) ** 2 for r in sleep_records) / n
    std_dev = math.sqrt(variance)

    # 步骤4: 计算深睡比例
    deep_sleep_ratio = (avg_deep_sleep / avg_duration * 100) if avg_duration > 0 else 0

    # 步骤5: 质量评分（0-100，加权综合）
    # 时长得分（7-9小时为满分）
    if 7 <= avg_duration <= 9:
        duration_score = 100
    elif 6 <= avg_duration < 7 or 9 < avg_duration <= 10:
        duration_score = 75
    elif 5 <= avg_duration < 6 or 10 < avg_duration <= 11:
        duration_score = 50
    else:
        duration_score = 25

    # 效率得分（>85%为满分）
    if avg_efficiency >= 85:
        efficiency_score = 100
    elif avg_efficiency >= 75:
        efficiency_score = 80
    elif avg_efficiency >= 65:
        efficiency_score = 60
    else:
        efficiency_score = 30

    # 规律性得分（标准差<0.5h为满分）
    if std_dev < 0.5:
        regularity_score = 100
    elif std_dev < 1.0:
        regularity_score = 75
    elif std_dev < 1.5:
        regularity_score = 50
    else:
        regularity_score = 25

    # 深睡比例得分（>20%为满分）
    if deep_sleep_ratio >= 20:
        deep_score = 100
    elif deep_sleep_ratio >= 15:
        deep_score = 75
    elif deep_sleep_ratio >= 10:
        deep_score = 50
    else:
        deep_score = 25

    # 加权综合评分
    quality_score = round(
        duration_score * 0.40 +
        efficiency_score * 0.30 +
        regularity_score * 0.20 +
        deep_score * 0.10
    )

    # 步骤6: 等级评定
    if quality_score >= 85:
        grade = "优秀"
    elif quality_score >= 70:
        grade = "良好"
    elif quality_score >= 55:
        grade = "一般"
    elif quality_score >= 40:
        grade = "较差"
    else:
        grade = "很差"

    # 步骤7: 趋势分析
    first_half = sleep_records[:n // 2]
    second_half = sleep_records[n // 2:]
    first_avg = sum(r.get("sleep_duration", 0) for r in first_half) / len(first_half) if first_half else 0
    second_avg = sum(r.get("sleep_duration", 0) for r in second_half) / len(second_half) if second_half else 0
    trend = "改善" if second_avg > first_avg + 0.3 else ("恶化" if second_avg < first_avg - 0.3 else "稳定")

    # 步骤8: 生成改善建议
    recommendations = []
    if avg_duration < 7:
        recommendations.append(f"平均睡眠{avg_duration:.1f}小时偏短，建议每天睡7-9小时")
    elif avg_duration > 9:
        recommendations.append(f"平均睡眠{avg_duration:.1f}小时偏长，过长的睡眠可能影响精神状态")

    if avg_efficiency < 85:
        recommendations.append(f"入睡效率{avg_efficiency:.0f}%偏低，建议减少睡前屏幕使用时间")

    if std_dev > 1.0:
        recommendations.append(f"睡眠规律性差（标准差{std_dev:.1f}h），建议固定作息时间")

    if deep_sleep_ratio < 15:
        recommendations.append(f"深睡比例{deep_sleep_ratio:.0f}%偏低，建议增加白天运动量以提高深睡")

    if avg_awakenings > 2:
        recommendations.append(f"平均夜间醒来{avg_awakenings:.1f}次偏多，检查睡眠环境")

    if not recommendations:
        recommendations.append("睡眠质量良好，请继续保持当前的睡眠习惯！")

    return {
        "total_records": n,
        "averages": {
            "sleep_duration_hours": round(avg_duration, 2),
            "time_in_bed_hours": round(avg_time_in_bed, 2),
            "deep_sleep_hours": round(avg_deep_sleep, 2),
            "deep_sleep_ratio": round(deep_sleep_ratio, 1),
            "sleep_efficiency": round(avg_efficiency, 1),
            "nighttime_awakenings": round(avg_awakenings, 1)
        },
        "regularity": {
            "std_deviation_hours": round(std_dev, 2),
            "min_duration": round(min(r.get("sleep_duration", 0) for r in sleep_records), 2),
            "max_duration": round(max(r.get("sleep_duration", 0) for r in sleep_records), 2)
        },
        "quality_score": quality_score,
        "grade": grade,
        "score_breakdown": {
            "duration_score": duration_score,
            "efficiency_score": efficiency_score,
            "regularity_score": regularity_score,
            "deep_sleep_score": deep_score
        },
        "trend": trend,
        "recommendations": recommendations
    }


# ---------------------------------------------------------------------------
# 8. 旅行路线优化器
# ---------------------------------------------------------------------------
def travel_itinerary_optimizer(destinations, days, preferences, constraints):
    """
    旅行路线优化器：TSP旅行商问题简化版（最近邻贪心+2-opt改进）。

    算法原理:
        - TSP问题: 寻找访问所有目的地的最短路径
        - 最近邻贪心: 从起点出发，每次选择最近未访问的目的地
        - 2-opt改进: 遍历所有边对(i,j)，若交换后路径更短则交换
        - 时间分配: 按目的地吸引力评分分配游览时间

    参数:
        destinations (list[dict]): 目的地列表，每项含:
            - name (str): 名称
            - lat (float): 纬度
            - lon (float): 经度
            - attraction_score (int): 景点吸引力评分(1-10)
            - recommended_hours (float): 建议游览时长(小时)
        days (int): 旅行天数
        preferences (dict): 偏好设置，如{"pace": "relaxed", "start": "酒店"}
        constraints (dict): 约束条件，如{"max_daily_hours": 8, "travel_speed": 80}

    返回:
        dict: 优化后的旅行路线，含route/daily_plans/statistics。
    """
    n = len(destinations)
    if n == 0:
        return {"error": "无目的地"}

    max_daily_hours = constraints.get("max_daily_hours", 8)
    travel_speed = constraints.get("travel_speed", 80)  # km/h

    # 步骤1: 计算距离矩阵（Haversine公式）
    def haversine(lat1, lon1, lat2, lon2):
        """Haversine公式计算两点间球面距离(km)"""
        R = 6371  # 地球半径(km)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    dist_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = haversine(
                    destinations[i]["lat"], destinations[i]["lon"],
                    destinations[j]["lat"], destinations[j]["lon"]
                )

    # 步骤2: 最近邻贪心算法构建初始路径
    visited = [False] * n
    route = [0]  # 从第一个目的地出发
    visited[0] = True
    total_distance = 0

    for _ in range(n - 1):
        current = route[-1]
        nearest = -1
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and dist_matrix[current][j] < min_dist:
                min_dist = dist_matrix[current][j]
                nearest = j
        if nearest >= 0:
            route.append(nearest)
            visited[nearest] = True
            total_distance += min_dist

    # 回到起点
    total_distance += dist_matrix[route[-1]][route[0]]

    # 步骤3: 2-opt改进算法
    def calculate_route_distance(r):
        """计算路径总距离"""
        dist = 0
        for i in range(len(r) - 1):
            dist += dist_matrix[r[i]][r[i + 1]]
        dist += dist_matrix[r[-1]][r[0]]
        return dist

    improved = True
    iterations = 0
    max_iterations = 100

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # 计算交换前后的距离差
                before = (dist_matrix[route[i - 1]][route[i]] +
                         dist_matrix[route[j]][route[(j + 1) % n]])
                after = (dist_matrix[route[i - 1]][route[j]] +
                        dist_matrix[route[i]][route[(j + 1) % n]])
                if after < before - 0.1:
                    # 执行2-opt交换（反转i到j之间的路径段）
                    route[i:j + 1] = route[i:j + 1][::-1]
                    improved = True

    total_distance = calculate_route_distance(route)

    # 步骤4: 按天数分配游览计划
    total_hours_available = days * max_daily_hours
    total_recommended = sum(d.get("recommended_hours", 4) for d in destinations)
    total_travel_time = total_distance / travel_speed  # 旅行总时间(小时)

    # 按吸引力比例分配时间
    daily_plans = []
    current_day = 1
    current_day_hours = 0
    current_day_destinations = []

    for idx in route:
        dest = destinations[idx]
        attraction = dest.get("attraction_score", 5)
        recommended = dest.get("recommended_hours", 4)
        # 按比例调整游览时间
        time_ratio = total_hours_available / max(total_recommended, 1)
        adjusted_hours = recommended * min(time_ratio, 1.2)

        # 加上到下一个目的地的旅行时间
        next_idx = route[route.index(idx) + 1] if route.index(idx) < len(route) - 1 else route[0]
        travel_dist = dist_matrix[idx][next_idx]
        travel_time = travel_dist / travel_speed

        if current_day_hours + adjusted_hours + travel_time > max_daily_hours:
            # 新的一天
            daily_plans.append({
                "day": current_day,
                "destinations": current_day_destinations,
                "total_hours": round(current_day_hours, 1)
            })
            current_day += 1
            current_day_hours = 0
            current_day_destinations = []

        current_day_destinations.append({
            "name": dest["name"],
            "attraction_score": attraction,
            "visit_hours": round(adjusted_hours, 1),
            "next_destination": destinations[next_idx]["name"],
            "travel_distance_km": round(travel_dist, 1),
            "travel_time_hours": round(travel_time, 1)
        })
        current_day_hours += adjusted_hours + travel_time

    # 添加最后一天
    if current_day_destinations:
        daily_plans.append({
            "day": current_day,
            "destinations": current_day_destinations,
            "total_hours": round(current_day_hours, 1)
        })

    # 步骤5: 统计信息
    optimized_route_names = [destinations[i]["name"] for i in route]

    return {
        "optimized_route": optimized_route_names,
        "route_indices": route,
        "total_distance_km": round(total_distance, 1),
        "total_travel_time_hours": round(total_distance / travel_speed, 1),
        "algorithm": "最近邻贪心 + 2-opt改进",
        "iterations": iterations,
        "daily_plans": daily_plans[:days],
        "statistics": {
            "destinations_count": n,
            "days_planned": len(daily_plans[:days]),
            "avg_distance_per_day": round(total_distance / days, 1),
            "total_visit_hours": round(sum(d.get("recommended_hours", 4) for d in destinations), 1),
            "preference": preferences.get("pace", "normal")
        }
    }


# ---------------------------------------------------------------------------
# 9. 购物清单优化器
# ---------------------------------------------------------------------------
def shopping_list_optimizer(items, stores, budget, constraints):
    """
    购物清单优化器：多店铺比价+预算约束+贪心算法最大化购买数量/满意度。

    算法原理:
        - 多店铺比价: 对每个物品找到最低价格店铺
        - 贪心算法: 按性价比（需求度/价格）排序，优先购买性价比高的
        - 预算约束: 累计花费不超过预算
        - 店铺合并: 尽量减少购物店铺数量（减少出行成本）

    参数:
        items (list[dict]): 购物清单，每项含name/quantity/priority(1-5)
        stores (list[dict]): 店铺列表，每项含name和price_map(物品名→价格)
        budget (float): 总预算
        constraints (dict): 约束条件，如{"min_stores": 1, "prefer_single_store": True}

    返回:
        dict: 优化后的采购方案，含purchases/store_assignments/total_cost/savings。
    """
    # 步骤1: 为每个物品找到最低价店铺
    best_prices = {}  # item_name -> (store, price)
    for item in items:
        item_name = item["name"]
        quantity = item.get("quantity", 1)
        best_store = None
        best_price = float('inf')
        store_prices = []

        for store in stores:
            price = store.get("price_map", {}).get(item_name, None)
            if price is not None:
                store_prices.append({"store": store["name"], "price": price})
                total_cost = price * quantity
                if total_cost < best_price:
                    best_price = total_cost
                    best_store = store["name"]

        best_prices[item_name] = {
            "store": best_store,
            "unit_price": best_price / quantity if best_price < float('inf') and quantity > 0 else 0,
            "total_price": best_price,
            "quantity": quantity,
            "all_prices": store_prices
        }

    # 步骤2: 计算性价比（优先级/价格比）
    item_values = []
    for item in items:
        name = item["name"]
        priority = item.get("priority", 3)
        price_info = best_prices.get(name, {})
        total_price = price_info.get("total_price", float('inf'))
        if total_price > 0 and total_price < float('inf'):
            value_ratio = priority / total_price  # 性价比 = 优先级 / 总价
            item_values.append({
                "name": name,
                "quantity": item.get("quantity", 1),
                "priority": priority,
                "best_store": price_info["store"],
                "unit_price": round(price_info["unit_price"], 2),
                "total_price": round(total_price, 2),
                "value_ratio": value_ratio,
                "all_prices": price_info.get("all_prices", [])
            })

    # 步骤3: 贪心选择 - 按性价比排序，优先购买高性价比物品
    sorted_items = sorted(item_values, key=lambda x: (-x["value_ratio"], -x["priority"]))

    # 步骤4: 预算约束下的购买
    purchases = []
    total_cost = 0
    remaining_budget = budget

    for item in sorted_items:
        if item["total_price"] <= remaining_budget:
            purchases.append(item)
            total_cost += item["total_price"]
            remaining_budget -= item["total_price"]
        else:
            # 预算不足，记录为未购买
            item["status"] = "预算不足"
            purchases.append(item)

    # 步骤5: 店铺分配优化
    # 尽量合并到少数店铺以减少出行成本
    store_groups = defaultdict(list)
    for p in purchases:
        if p.get("status") != "预算不足":
            store_groups[p["best_store"]].append(p)

    # 步骤6: 如果偏好单店购买，计算每个店铺的全覆盖成本
    prefer_single = constraints.get("prefer_single_store", False)
    single_store_option = None
    if prefer_single:
        for store in stores:
            store_total = 0
            can_fulfill = True
            for item in items:
                price = store.get("price_map", {}).get(item["name"], None)
                if price is None:
                    can_fulfill = False
                    break
                store_total += price * item.get("quantity", 1)
            if can_fulfill and store_total <= budget:
                if single_store_option is None or store_total < single_store_option["total_cost"]:
                    single_store_option = {
                        "store": store["name"],
                        "total_cost": round(store_total, 2),
                        "items": len(items)
                    }

    # 步骤7: 计算节省
    # 节省 = 各物品在最高价店铺购买的总价 - 优化后总价
    max_total = 0
    for item in items:
        name = item["name"]
        quantity = item.get("quantity", 1)
        max_price = 0
        for store in stores:
            price = store.get("price_map", {}).get(name, 0)
            if price > max_price:
                max_price = price
        max_total += max_price * quantity

    savings = max_total - total_cost

    # 步骤8: 店铺汇总
    store_assignments = []
    for store_name, store_items in store_groups.items():
        store_total = sum(item["total_price"] for item in store_items)
        store_assignments.append({
            "store": store_name,
            "item_count": len(store_items),
            "items": [item["name"] for item in store_items],
            "subtotal": round(store_total, 2)
        })

    store_assignments.sort(key=lambda x: -x["subtotal"])

    purchased_names = [p["name"] for p in purchases if p.get("status") != "预算不足"]
    unpurchased = [p for p in purchases if p.get("status") == "预算不足"]

    return {
        "purchases": [{"name": p["name"], "store": p["best_store"],
                       "quantity": p["quantity"], "unit_price": p["unit_price"],
                       "total_price": p["total_price"],
                       "status": p.get("status", "已购买")} for p in purchases],
        "store_assignments": store_assignments,
        "total_cost": round(total_cost, 2),
        "budget": budget,
        "remaining_budget": round(remaining_budget, 2),
        "budget_utilization": round(total_cost / budget * 100, 1) if budget > 0 else 0,
        "savings_vs_max": round(savings, 2),
        "items_purchased": len(purchased_names),
        "items_unpurchased": len(unpurchased),
        "unpurchased_items": [{"name": p["name"], "reason": p.get("status", "")} for p in unpurchased],
        "single_store_option": single_store_option,
        "stores_used": len(store_groups),
        "algorithm": "贪心性价比排序 + 多店铺比价优化"
    }


# ---------------------------------------------------------------------------
# 10. 订阅费用分析器
# ---------------------------------------------------------------------------
def subscription_cost_analyzer(subscriptions, usage_data):
    """
    订阅费用分析器：计算总费用+使用率分析(ROI)+取消建议+替代方案。

    算法原理:
        - 月/年费用汇总: 按计费周期换算统一费用
        - ROI计算: ROI = 使用次数 / 月费用（每次使用成本）
        - 取消建议: 使用率低于阈值（月使用<3次且ROI<1.0）建议取消
        - 替代方案: 为高费用低使用率的订阅推荐更经济的替代品
        - 年度节省: 计算取消低效订阅后的预计节省金额

    参数:
        subscriptions (list[dict]): 订阅列表，每项含:
            - name (str): 订阅名称
            - monthly_cost (float): 月费用
            - billing_cycle (str): "monthly"/"yearly"
            - category (str): 类别
        usage_data (list[dict]): 使用数据，每项含:
            - subscription_name (str): 订阅名称
            - monthly_usage_count (int): 月使用次数
            - last_used_days (int): 最后一次使用距今天数

    返回:
        dict: 订阅分析报告，含cost_summary/roi_analysis/cancellation_suggestions/alternatives。
    """
    # 步骤1: 费用换算（统一为月费用）
    subscription_details = []
    total_monthly = 0
    total_yearly = 0

    # 构建使用数据查找表
    usage_map = {}
    for u in usage_data:
        usage_map[u["subscription_name"]] = u

    for sub in subscriptions:
        name = sub["name"]
        monthly_cost = sub.get("monthly_cost", 0)
        cycle = sub.get("billing_cycle", "monthly")
        category = sub.get("category", "其他")

        # 换算月费用
        if cycle == "yearly":
            actual_monthly = monthly_cost / 12
        else:
            actual_monthly = monthly_cost

        yearly_cost = actual_monthly * 12
        total_monthly += actual_monthly
        total_yearly += yearly_cost

        # 获取使用数据
        usage = usage_map.get(name, {})
        usage_count = usage.get("monthly_usage_count", 0)
        last_used = usage.get("last_used_days", 999)

        # 步骤2: 计算ROI（每次使用成本）
        cost_per_use = actual_monthly / usage_count if usage_count > 0 else actual_monthly
        roi_score = usage_count / actual_monthly if actual_monthly > 0 else 0

        # 步骤3: 使用率评级
        if usage_count >= 20:
            usage_level = "高频"
        elif usage_count >= 10:
            usage_level = "中频"
        elif usage_count >= 3:
            usage_level = "低频"
        else:
            usage_level = "极低频"

        # 步骤4: 取消建议判定
        should_cancel = False
        cancel_reason = None
        if usage_count < 3 and last_used > 14:
            should_cancel = True
            cancel_reason = "使用频率极低且超过14天未使用"
        elif cost_per_use > actual_monthly:  # 每次使用成本高于月费（不合理）
            should_cancel = True
            cancel_reason = f"每次使用成本{cost_per_use:.1f}元过高"
        elif roi_score < 0.5 and last_used > 7:
            should_cancel = True
            cancel_reason = "ROI过低（使用次数/费用比<0.5）"

        subscription_details.append({
            "name": name,
            "category": category,
            "monthly_cost": round(actual_monthly, 2),
            "yearly_cost": round(yearly_cost, 2),
            "billing_cycle": cycle,
            "monthly_usage_count": usage_count,
            "last_used_days_ago": last_used,
            "cost_per_use": round(cost_per_use, 2),
            "roi_score": round(roi_score, 2),
            "usage_level": usage_level,
            "should_cancel": should_cancel,
            "cancel_reason": cancel_reason
        })

    # 步骤5: 分类汇总
    category_summary = defaultdict(lambda: {"monthly": 0, "yearly": 0, "count": 0})
    for sub in subscription_details:
        cat = sub["category"]
        category_summary[cat]["monthly"] += sub["monthly_cost"]
        category_summary[cat]["yearly"] += sub["yearly_cost"]
        category_summary[cat]["count"] += 1

    # 步骤6: 取消建议和节省计算
    cancel_suggestions = []
    potential_monthly_savings = 0
    for sub in subscription_details:
        if sub["should_cancel"]:
            cancel_suggestions.append({
                "name": sub["name"],
                "monthly_cost": sub["monthly_cost"],
                "yearly_cost": sub["yearly_cost"],
                "reason": sub["cancel_reason"],
                "usage_level": sub["usage_level"],
                "last_used": f"{sub['last_used_days_ago']}天前"
            })
            potential_monthly_savings += sub["monthly_cost"]

    # 步骤7: 替代方案推荐
    alternatives_db = {
        "Netflix": {"name": "多平台组合", "cost": 15, "note": "B站+爱奇艺+腾讯视频组合更便宜"},
        "Spotify": {"name": "免费版+广告", "cost": 0, "note": "免费版功能足够日常使用"},
        "iCloud": {"name": "Google Drive免费版", "cost": 0, "note": "15GB免费存储空间"},
        "Adobe CC": {"name": "GIMP+Inkscape", "cost": 0, "note": "开源替代方案，功能接近"},
        "Microsoft 365": {"name": "Google Docs", "cost": 0, "note": "免费在线办公套件"},
    }

    alternatives = []
    for sub in cancel_suggestions:
        alt = alternatives_db.get(sub["name"])
        if alt:
            alternatives.append({
                "original": sub["name"],
                "original_cost": sub["monthly_cost"],
                "alternative": alt["name"],
                "alternative_cost": alt["cost"],
                "monthly_savings": round(sub["monthly_cost"] - alt["cost"], 2),
                "note": alt["note"]
            })

    # 步骤8: 使用率排名
    usage_ranking = sorted(subscription_details, key=lambda x: x["roi_score"], reverse=True)

    return {
        "cost_summary": {
            "total_monthly": round(total_monthly, 2),
            "total_yearly": round(total_yearly, 2),
            "subscription_count": len(subscriptions),
            "avg_monthly_per_sub": round(total_monthly / len(subscriptions), 2) if subscriptions else 0
        },
        "category_breakdown": [
            {"category": cat, "monthly_cost": round(data["monthly"], 2),
             "yearly_cost": round(data["yearly"], 2), "count": data["count"]}
            for cat, data in sorted(category_summary.items(), key=lambda x: -x[1]["monthly"])
        ],
        "subscription_details": subscription_details,
        "usage_ranking": [
            {"rank": i + 1, "name": s["name"], "roi_score": s["roi_score"],
             "usage_level": s["usage_level"], "cost_per_use": s["cost_per_use"]}
            for i, s in enumerate(usage_ranking)
        ],
        "cancellation_suggestions": cancel_suggestions,
        "potential_savings": {
            "monthly": round(potential_monthly_savings, 2),
            "yearly": round(potential_monthly_savings * 12, 2),
            "cancel_count": len(cancel_suggestions)
        },
        "alternatives": alternatives,
        "recommendations": [
            f"总订阅费用{total_monthly:.0f}元/月（{total_yearly:.0f}元/年）",
            f"可取消{len(cancel_suggestions)}个低效订阅，年节省{potential_monthly_savings*12:.0f}元" if cancel_suggestions else "所有订阅使用率良好",
            f"最划算的订阅: {usage_ranking[0]['name']}（ROI={usage_ranking[0]['roi_score']}）" if usage_ranking else ""
        ]
    }


# ---------------------------------------------------------------------------
# 主程序测试
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 70)
    print("生活服务工具 - lifestyle-planner 测试")
    print("=" * 70)

    # 测试1: 营养计算器
    print("\n1. 营养计算器测试")
    print("-" * 40)
    food_items = [
        {"name": "米饭", "amount": 200},
        {"name": "鸡胸肉", "amount": 150},
        {"name": "西兰花", "amount": 100},
        {"name": "苹果", "amount": 150}
    ]
    targets = {"calories": 2000, "protein": 60, "fat": 50, "carbs": 250, "fiber": 25}
    nutrition = nutrition_calculator(food_items, targets)
    print(f"营养评分: {nutrition['nutrition_score']} ({nutrition['grade']})")
    print(f"总热量: {nutrition['total_intake'].get('calories', 0):.0f} kcal")
    print(f"建议: {'; '.join(nutrition['recommendations'][:2])}")

    # 测试2: BMI健康评估
    print("\n2. BMI健康评估测试")
    print("-" * 40)
    health = bmi_health_assessor(75, 175, 28, "male", "moderate")
    print(f"BMI: {health['bmi']} ({health['bmi_category']})")
    print(f"体脂率: {health['body_fat_percentage']}% ({health['body_fat_status']})")
    print(f"BMR: {health['bmr']:.0f} kcal, TDEE: {health['tdee']:.0f} kcal")
    print(f"理想体重: {health['ideal_weight_range']} kg")

    # 测试3: 健身计划生成
    print("\n3. 健身计划生成测试")
    print("-" * 40)
    plan = fitness_plan_generator("muscle_gain", "intermediate", 4, ["dumbbell", "barbell"])
    print(f"目标: {plan['goal']}, 水平: {plan['level']}")
    print(f"分割: {plan['split']}")
    w1 = plan['weekly_plans'][0]
    print(f"第1周({w1['phase']}): {len(w1['days'])}天")
    d1 = w1['days'][0]
    print(f"  Day1({d1['focus']}): {[e['name'] for e in d1['exercises'][:3]]}")

    # 测试4: 预算优化器
    print("\n4. 预算优化器测试")
    print("-" * 40)
    expenses = [
        {"category": "housing", "amount": 3000, "essential": True},
        {"category": "food", "amount": 1500, "essential": True},
        {"category": "transport", "amount": 500, "essential": True},
        {"category": "entertainment", "amount": 1200, "essential": False},
        {"category": "shopping", "amount": 800, "essential": False},
        {"category": "subscription", "amount": 300, "essential": False}
    ]
    budget = budget_optimizer(10000, expenses, 2000, {"housing": 0.3, "food": 0.15, "entertainment": 0.08, "shopping": 0.06})
    print(f"当前储蓄: {budget['current_savings']}元")
    print(f"优化后储蓄: {budget['optimized_savings']}元 (目标: {budget['savings_goal']}元)")
    print(f"储蓄增加: {budget['total_savings_increase']}元")
    print(f"预警: {budget['alerts'][:1]}")

    # 测试5: 餐饮计划器
    print("\n5. 餐饮计划器测试")
    print("-" * 40)
    food_db = [
        {"name": "鸡胸肉", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "serving_size": "100g"},
        {"name": "米饭", "calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28, "serving_size": "100g"},
        {"name": "西兰花", "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 7, "serving_size": "100g"},
        {"name": "鸡蛋", "calories": 147, "protein": 12.6, "fat": 9.5, "carbs": 1.1, "serving_size": "1个"},
        {"name": "燕麦", "calories": 389, "protein": 16.9, "fat": 6.9, "carbs": 66, "serving_size": "100g"},
        {"name": "牛奶", "calories": 54, "protein": 3.0, "fat": 3.2, "carbs": 3.4, "serving_size": "100ml"},
        {"name": "香蕉", "calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "serving_size": "1根"},
    ]
    meal_plan = meal_planner(2000, 3, food_db, [])
    print(f"餐数: {len(meal_plan['meals'])}")
    print(f"总热量: {meal_plan['nutrition_summary']['total_calories']:.0f} kcal (目标: {meal_plan['nutrition_summary']['calorie_target']})")
    print(f"多样性评分: {meal_plan['variety_score']}")

    # 测试6: 习惯追踪分析
    print("\n6. 习惯追踪分析测试")
    print("-" * 40)
    habit_records = []
    base_date = datetime(2025, 1, 1)
    for i in range(30):
        date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        completed = random.random() > 0.25  # 75%完成率
        habit_records.append({"date": date, "completed": completed})
    # 确保最近5天连续完成
    for i in range(5):
        habit_records[-(i+1)]["completed"] = True
    habit_data = {"habit_name": "每日阅读", "records": habit_records}
    habit_analysis = habit_tracker_streak_analyzer(habit_data)
    print(f"当前连续: {habit_analysis['current_streak']}天")
    print(f"最长连续: {habit_analysis['longest_streak']}天")
    print(f"完成率: {habit_analysis['completion_rate']}% ({habit_analysis['grade']})")
    print(f"明日完成概率: {habit_analysis['markov_chain']['predictions'][0]['predicted_completion_prob']}%")

    # 测试7: 睡眠质量分析
    print("\n7. 睡眠质量分析测试")
    print("-" * 40)
    sleep_records = []
    for i in range(14):
        sleep_records.append({
            "date": f"2025-01-{i+1:02d}",
            "bedtime": "23:00",
            "wakeup": "07:00",
            "sleep_duration": 7.5 + random.uniform(-0.5, 0.5),
            "time_in_bed": 8.0 + random.uniform(-0.2, 0.2),
            "deep_sleep": 1.5 + random.uniform(-0.3, 0.3),
            "awakenings": random.randint(0, 2)
        })
    sleep_analysis = sleep_quality_analyzer(sleep_records)
    print(f"睡眠评分: {sleep_analysis['quality_score']} ({sleep_analysis['grade']})")
    print(f"平均时长: {sleep_analysis['averages']['sleep_duration_hours']}h")
    print(f"入睡效率: {sleep_analysis['averages']['sleep_efficiency']}%")
    print(f"规律性(σ): {sleep_analysis['regularity']['std_deviation_hours']}h")

    # 测试8: 旅行路线优化
    print("\n8. 旅行路线优化测试")
    print("-" * 40)
    destinations = [
        {"name": "北京", "lat": 39.9042, "lon": 116.4074, "attraction_score": 9, "recommended_hours": 8},
        {"name": "上海", "lat": 31.2304, "lon": 121.4737, "attraction_score": 8, "recommended_hours": 6},
        {"name": "西安", "lat": 34.3416, "lon": 108.9398, "attraction_score": 9, "recommended_hours": 7},
        {"name": "成都", "lat": 30.5728, "lon": 104.0668, "attraction_score": 8, "recommended_hours": 6},
        {"name": "杭州", "lat": 30.2741, "lon": 120.1551, "attraction_score": 7, "recommended_hours": 5},
    ]
    travel = travel_itinerary_optimizer(destinations, 5, {"pace": "normal"}, {"max_daily_hours": 8})
    print(f"优化路线: {' → '.join(travel['optimized_route'])}")
    print(f"总距离: {travel['total_distance_km']} km")
    print(f"算法: {travel['algorithm']}, 迭代{travel['iterations']}次")
    print(f"天数: {len(travel['daily_plans'])}天")

    # 测试9: 购物清单优化
    print("\n9. 购物清单优化测试")
    print("-" * 40)
    shop_items = [
        {"name": "苹果", "quantity": 2, "priority": 4},
        {"name": "牛奶", "quantity": 3, "priority": 5},
        {"name": "面包", "quantity": 1, "priority": 3},
        {"name": "鸡蛋", "quantity": 2, "priority": 5},
        {"name": "坚果", "quantity": 1, "priority": 2},
    ]
    stores_data = [
        {"name": "超市A", "price_map": {"苹果": 5, "牛奶": 8, "面包": 6, "鸡蛋": 7, "坚果": 25}},
        {"name": "超市B", "price_map": {"苹果": 4, "牛奶": 9, "面包": 5, "鸡蛋": 6, "坚果": 22}},
        {"name": "超市C", "price_map": {"苹果": 6, "牛奶": 7, "面包": 7, "鸡蛋": 8, "坚果": 20}},
    ]
    shopping = shopping_list_optimizer(shop_items, stores_data, 100, {"prefer_single_store": True})
    print(f"总花费: {shopping['total_cost']}元 (预算: {shopping['budget']}元)")
    print(f"已购: {shopping['items_purchased']}/{len(shop_items)}件")
    print(f"店铺数: {shopping['stores_used']}")
    print(f"比最高价节省: {shopping['savings_vs_max']}元")
    for sa in shopping['store_assignments']:
        print(f"  {sa['store']}: {sa['item_count']}件, {sa['subtotal']}元")

    # 测试10: 订阅费用分析
    print("\n10. 订阅费用分析测试")
    print("-" * 40)
    subs = [
        {"name": "Netflix", "monthly_cost": 45, "billing_cycle": "monthly", "category": "娱乐"},
        {"name": "Spotify", "monthly_cost": 15, "billing_cycle": "monthly", "category": "音乐"},
        {"name": "iCloud", "monthly_cost": 21, "billing_cycle": "monthly", "category": "存储"},
        {"name": "Adobe CC", "monthly_cost": 68, "billing_cycle": "monthly", "category": "工具"},
        {"name": "Gym", "monthly_cost": 200, "billing_cycle": "monthly", "category": "健康"},
    ]
    usage = [
        {"subscription_name": "Netflix", "monthly_usage_count": 15, "last_used_days": 1},
        {"subscription_name": "Spotify", "monthly_usage_count": 30, "last_used_days": 0},
        {"subscription_name": "iCloud", "monthly_usage_count": 5, "last_used_days": 2},
        {"subscription_name": "Adobe CC", "monthly_usage_count": 1, "last_used_days": 20},
        {"subscription_name": "Gym", "monthly_usage_count": 8, "last_used_days": 3},
    ]
    sub_analysis = subscription_cost_analyzer(subs, usage)
    print(f"总月费: {sub_analysis['cost_summary']['total_monthly']}元")
    print(f"总年费: {sub_analysis['cost_summary']['total_yearly']}元")
    print(f"建议取消: {sub_analysis['potential_savings']['cancel_count']}个")
    print(f"年节省: {sub_analysis['potential_savings']['yearly']}元")
    for r in sub_analysis['usage_ranking'][:3]:
        print(f"  #{r['rank']} {r['name']}: ROI={r['roi_score']}, {r['usage_level']}")

    print("\n" + "=" * 70)
    print("所有测试完成！")
    print("=" * 70)
