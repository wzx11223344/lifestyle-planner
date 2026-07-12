#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活服务工具 - lifestyle-planner
提供10个生活服务工具：食谱推荐、健身计划、预算追踪、旅行规划、餐饮计划、
习惯追踪、睡眠分析、购物清单、穿搭推荐、订阅管理。

无外部依赖，仅使用Python标准库。
"""

import json
import random
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 1. 食谱推荐
# ---------------------------------------------------------------------------
def recipe_recommender(ingredients, cuisine="中餐", dietary=None, num_results=5):
    """
    食谱推荐：根据可用食材、菜系和饮食偏好推荐食谱。

    参数:
        ingredients (list[str]): 可用食材列表，如 ["鸡肉", "番茄", "鸡蛋"]。
        cuisine (str): 菜系偏好，如 "中餐"/"西餐"/"日料"/"韩餐"，默认 "中餐"。
        dietary (str): 饮食限制，如 "素食"/"低脂"/"无麸质"/"低碳水"，为None时无限制。
        num_results (int): 返回食谱数量，默认5。

    返回:
        list[dict]: 推荐食谱列表，每个食谱含名称、食材、步骤和营养信息。
    """
    recipe_db = {
        "中餐": [
            {"name": "番茄炒鸡蛋", "ingredients": ["番茄", "鸡蛋", "葱", "盐", "糖"],
             "difficulty": "简单", "time_minutes": 15, "calories": 200,
             "tags": ["家常菜", "快手菜"]},
            {"name": "红烧鸡块", "ingredients": ["鸡肉", "酱油", "糖", "姜", "蒜", "料酒"],
             "difficulty": "中等", "time_minutes": 40, "calories": 350,
             "tags": ["家常菜", "下饭菜"]},
            {"name": "清蒸鱼", "ingredients": ["鱼", "葱", "姜", "蒸鱼豉油", "料酒"],
             "difficulty": "中等", "time_minutes": 25, "calories": 180,
             "tags": ["健康", "低脂"]},
            {"name": "麻婆豆腐", "ingredients": ["豆腐", "猪肉末", "豆瓣酱", "花椒", "蒜"],
             "difficulty": "中等", "time_minutes": 30, "calories": 280,
             "tags": ["川菜", "下饭菜"]},
            {"name": "青菜豆腐汤", "ingredients": ["青菜", "豆腐", "盐", "香油"],
             "difficulty": "简单", "time_minutes": 15, "calories": 120,
             "tags": ["素食", "低脂", "汤品"]},
            {"name": "土豆炖牛肉", "ingredients": ["牛肉", "土豆", "胡萝卜", "酱油", "八角"],
             "difficulty": "中等", "time_minutes": 60, "calories": 400,
             "tags": ["炖菜", "高蛋白"]},
            {"name": "凉拌黄瓜", "ingredients": ["黄瓜", "蒜", "醋", "辣椒油", "盐"],
             "difficulty": "简单", "time_minutes": 10, "calories": 80,
             "tags": ["素食", "凉菜", "低脂"]},
            {"name": "蛋炒饭", "ingredients": ["鸡蛋", "米饭", "葱", "盐", "酱油"],
             "difficulty": "简单", "time_minutes": 15, "calories": 300,
             "tags": ["主食", "快手菜"]}
        ],
        "西餐": [
            {"name": "意大利面", "ingredients": ["意面", "番茄酱", "橄榄油", "蒜", "罗勒"],
             "difficulty": "简单", "time_minutes": 25, "calories": 400,
             "tags": ["主食", "素食"]},
            {"name": "凯撒沙拉", "ingredients": ["生菜", "面包丁", "帕玛森芝士", "凯撒酱"],
             "difficulty": "简单", "time_minutes": 15, "calories": 250,
             "tags": ["沙拉", "低脂"]},
            {"name": "牛排", "ingredients": ["牛排", "盐", "黑胡椒", "黄油", "蒜"],
             "difficulty": "中等", "time_minutes": 20, "calories": 500,
             "tags": ["高蛋白", "主菜"]},
            {"name": "奶油蘑菇汤", "ingredients": ["蘑菇", "奶油", "洋葱", "面粉", "鸡汤"],
             "difficulty": "中等", "time_minutes": 30, "calories": 300,
             "tags": ["汤品", "西式"]}
        ],
        "日料": [
            {"name": "寿司", "ingredients": ["米饭", "海苔", "三文鱼", "黄瓜", "醋"],
             "difficulty": "中等", "time_minutes": 40, "calories": 300,
             "tags": ["主食", "日式"]},
            {"name": "味噌汤", "ingredients": ["味噌", "豆腐", "海带", "葱"],
             "difficulty": "简单", "time_minutes": 10, "calories": 80,
             "tags": ["汤品", "低脂", "日式"]}
        ],
        "韩餐": [
            {"name": "泡菜炒饭", "ingredients": ["米饭", "泡菜", "鸡蛋", "葱", "香油"],
             "difficulty": "简单", "time_minutes": 15, "calories": 350,
             "tags": ["主食", "韩式"]},
            {"name": "韩式拌饭", "ingredients": ["米饭", "菠菜", "胡萝卜", "牛肉", "鸡蛋", "辣酱"],
             "difficulty": "中等", "time_minutes": 30, "calories": 400,
             "tags": ["主食", "韩式"]}
        ]
    }

    # 获取菜系食谱
    recipes = recipe_db.get(cuisine, recipe_db["中餐"])

    # 饮食偏好过滤
    if dietary:
        dietary_lower = dietary.lower()
        if "素食" in dietary or "vegetarian" in dietary_lower:
            recipes = [r for r in recipes if "素食" in r.get("tags", []) or not any(
                meat in str(r.get("ingredients", [])) for meat in ["猪肉", "牛肉", "鸡肉", "鱼", "三文鱼"]
            )]
        if "低脂" in dietary:
            recipes = [r for r in recipes if "低脂" in r.get("tags", []) or r.get("calories", 999) < 250]
        if "低碳水" in dietary:
            recipes = [r for r in recipes if "主食" not in r.get("tags", [])]

    # 食材匹配评分
    scored = []
    for recipe in recipes:
        recipe_ingredients = recipe.get("ingredients", [])
        user_has = set(ingredients)
        recipe_needs = set(recipe_ingredients)

        matched = user_has & recipe_needs
        missing = recipe_needs - user_has
        match_score = len(matched) / len(recipe_needs) if recipe_needs else 0

        scored.append({
            "name": recipe["name"],
            "cuisine": cuisine,
            "difficulty": recipe["difficulty"],
            "time_minutes": recipe["time_minutes"],
            "calories": recipe["calories"],
            "tags": recipe.get("tags", []),
            "ingredients_needed": recipe_ingredients,
            "ingredients_matched": list(matched),
            "ingredients_missing": list(missing),
            "match_score": round(match_score * 100, 1),
            "can_cook": len(missing) <= 2  # 缺2种以内可以烹饪
        })

    # 按匹配度排序
    scored.sort(key=lambda x: x["match_score"], reverse=True)

    return scored[:num_results]


# ---------------------------------------------------------------------------
# 2. 健身计划
# ---------------------------------------------------------------------------
def workout_planner(fitness_level="beginner", goal="general_fitness", days_per_week=3, equipment=None):
    """
    健身计划：根据健身水平、目标和设备生成训练计划。

    参数:
        fitness_level (str): 健身水平，可选 "beginner"（初级）、"intermediate"（中级）、
            "advanced"（高级），默认 "beginner"。
        goal (str): 健身目标，如 "general_fitness"（通用健身）、"muscle_gain"（增肌）、
            "weight_loss"（减脂）、"endurance"（耐力），默认 "general_fitness"。
        days_per_week (int): 每周训练天数，默认3。
        equipment (list[str]): 可用设备列表，如 ["哑铃", "杠铃", "跑步机"]，为None时使用徒手训练。

    返回:
        dict: 健身计划，含每周训练安排和各动作详情。
    """
    if equipment is None:
        equipment = ["徒手"]

    # 训练动作库
    exercise_db = {
        "徒手": {
            "beginner": [
                {"name": "俯卧撑", "sets": 3, "reps": "8-12", "rest": "60秒", "muscle": "胸/三头"},
                {"name": "深蹲", "sets": 3, "reps": "12-15", "rest": "60秒", "muscle": "腿/臀"},
                {"name": "平板支撑", "sets": 3, "reps": "20-30秒", "rest": "45秒", "muscle": "核心"},
                {"name": "弓步蹲", "sets": 3, "reps": "10每侧", "rest": "60秒", "muscle": "腿/臀"},
                {"name": "仰卧卷腹", "sets": 3, "reps": "15-20", "rest": "45秒", "muscle": "腹"},
                {"name": "开合跳", "sets": 3, "reps": "30秒", "rest": "30秒", "muscle": "全身/有氧"}
            ],
            "intermediate": [
                {"name": "钻石俯卧撑", "sets": 4, "reps": "10-15", "rest": "60秒", "muscle": "三头/胸"},
                {"name": "保加利亚深蹲", "sets": 4, "reps": "12每侧", "rest": "60秒", "muscle": "腿/臀"},
                {"name": "侧平板支撑", "sets": 3, "reps": "30秒每侧", "rest": "45秒", "muscle": "核心"},
                {"name": "登山者", "sets": 4, "reps": "30秒", "rest": "30秒", "muscle": "核心/有氧"},
                {"name": "波比跳", "sets": 4, "reps": "10-15", "rest": "60秒", "muscle": "全身"}
            ],
            "advanced": [
                {"name": "单臂俯卧撑", "sets": 4, "reps": "8-10每侧", "rest": "90秒", "muscle": "胸/三头"},
                {"name": "手枪深蹲", "sets": 4, "reps": "8-10每侧", "rest": "90秒", "muscle": "腿"},
                {"name": "前臂支撑", "sets": 3, "reps": "60秒", "rest": "45秒", "muscle": "核心"},
                {"name": "倒立俯卧撑", "sets": 4, "reps": "6-10", "rest": "90秒", "muscle": "肩/三头"}
            ]
        },
        "哑铃": [
            {"name": "哑铃卧推", "sets": 4, "reps": "8-12", "rest": "90秒", "muscle": "胸"},
            {"name": "哑铃弯举", "sets": 3, "reps": "10-15", "rest": "60秒", "muscle": "二头"},
            {"name": "哑铃肩推", "sets": 4, "reps": "8-12", "rest": "90秒", "muscle": "肩"},
            {"name": "哑铃硬拉", "sets": 4, "reps": "10-12", "rest": "90秒", "muscle": "背/腿"},
            {"name": "哑铃飞鸟", "sets": 3, "reps": "12-15", "rest": "60秒", "muscle": "胸"}
        ]
    }

    # 收集可用动作
    available_exercises = []
    for eq in equipment:
        if eq in exercise_db:
            eq_exercises = exercise_db[eq]
            if isinstance(eq_exercises, dict):
                available_exercises.extend(eq_exercises.get(fitness_level, eq_exercises.get("beginner", [])))
            else:
                available_exercises.extend(eq_exercises)

    if not available_exercises:
        available_exercises = exercise_db["徒手"]["beginner"]

    # 根据目标调整
    goal_config = {
        "muscle_gain": {"sets_multiplier": 1.5, "rest": "90-120秒", "cardio": False},
        "weight_loss": {"sets_multiplier": 1.0, "rest": "30-45秒", "cardio": True},
        "endurance": {"sets_multiplier": 1.0, "rest": "30秒", "cardio": True, "reps_multiplier": 1.5},
        "general_fitness": {"sets_multiplier": 1.0, "rest": "60秒", "cardio": True}
    }
    config = goal_config.get(goal, goal_config["general_fitness"])

    # 生成每周计划
    split_types = {
        3: ["全身训练A", "全身训练B", "全身训练C"],
        4: ["上半身", "下半身", "上半身", "下半身"],
        5: ["胸", "背", "腿", "肩/臂", "核心/有氧"],
        6: ["胸/三头", "背/二头", "腿", "肩", "手臂", "全身HIIT"]
    }

    day_names = split_types.get(days_per_week, split_types[3])
    weekly_plan = []

    for day_idx in range(days_per_week):
        day_name = day_names[day_idx]
        # 选择4-6个动作
        num_exercises = min(6, max(4, len(available_exercises) // days_per_week + 2))
        start = (day_idx * num_exercises) % len(available_exercises)
        day_exercises = []

        for i in range(num_exercises):
            ex = available_exercises[(start + i) % len(available_exercises)]
            adjusted_sets = max(3, int(ex["sets"] * config["sets_multiplier"]))
            day_exercises.append({
                "name": ex["name"],
                "sets": adjusted_sets,
                "reps": ex["reps"],
                "rest": config["rest"],
                "muscle_group": ex["muscle"]
            })

        day_plan = {
            "day": day_idx + 1,
            "type": day_name,
            "exercises": day_exercises,
            "estimated_duration": f"{num_exercises * 10 + 15}分钟"
        }

        # 减脂/耐力目标增加有氧
        if config.get("cardio") and day_idx % 2 == 0:
            day_plan["cardio"] = {
                "type": "HIIT" if goal == "weight_loss" else "慢跑",
                "duration": "15-20分钟",
                "intensity": "中高" if goal == "weight_loss" else "中等"
            }

        weekly_plan.append(day_plan)

    return {
        "fitness_level": fitness_level,
        "goal": goal,
        "days_per_week": days_per_week,
        "equipment": equipment,
        "weekly_plan": weekly_plan,
        "rest_days": 7 - days_per_week,
        "tips": [
            "训练前进行5-10分钟热身",
            "训练后进行拉伸放松",
            "保持充足的水分摄入",
            "确保每周至少1-2天完全休息",
            "根据身体反馈调整训练强度"
        ]
    }


# ---------------------------------------------------------------------------
# 3. 预算追踪
# ---------------------------------------------------------------------------
def budget_tracker(income, expenses, savings_goal, period="monthly"):
    """
    预算追踪：根据收入、支出和储蓄目标追踪预算。

    参数:
        income (float): 总收入金额。
        expenses (list[dict]): 支出列表，每项含 category、amount、description。
        savings_goal (float): 储蓄目标金额。
        period (str): 周期，可选 "weekly"/"monthly"/"yearly"，默认 "monthly"。

    返回:
        dict: 预算报告，含支出分析、储蓄进度和建议。
    """
    total_expenses = sum(e.get("amount", 0) for e in expenses)
    net_savings = income - total_expenses

    # 按类别分组
    category_totals = {}
    for exp in expenses:
        cat = exp.get("category", "其他")
        category_totals[cat] = category_totals.get(cat, 0) + exp.get("amount", 0)

    # 支出占比
    category_breakdown = []
    for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = round(amount / total_expenses * 100, 1) if total_expenses > 0 else 0
        category_breakdown.append({
            "category": cat,
            "amount": round(amount, 2),
            "percentage": percentage,
            "vs_income": round(amount / income * 100, 1) if income > 0 else 0
        })

    # 储蓄进度
    savings_rate = round(net_savings / income * 100, 1) if income > 0 else 0
    goal_progress = round(net_savings / savings_goal * 100, 1) if savings_goal > 0 else 0

    # 50/30/20法则分析
    needs = sum(v for k, v in category_totals.items() if k in ["房租", "房贷", "水电", "交通", "保险", "餐饮"])
    wants = sum(v for k, v in category_totals.items() if k in ["娱乐", "购物", "外出", "订阅", "旅行"])
    savings = net_savings

    needs_pct = round(needs / income * 100, 1) if income > 0 else 0
    wants_pct = round(wants / income * 100, 1) if income > 0 else 0
    savings_pct = round(savings / income * 100, 1) if income > 0 else 0

    # 健康度评估
    issues = []
    if needs_pct > 50:
        issues.append(f"必要支出占比{needs_pct}%，超过50%的建议上限")
    if wants_pct > 30:
        issues.append(f"非必要支出占比{wants_pct}%，超过30%的建议上限")
    if savings_rate < 20 and savings_rate > 0:
        issues.append(f"储蓄率{savings_rate}%，低于20%的建议下限")
    if net_savings < 0:
        issues.append("支出超过收入，存在预算赤字")

    return {
        "period": period,
        "income": round(income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate": savings_rate,
        "savings_goal": savings_goal,
        "goal_progress": min(goal_progress, 100),
        "goal_achieved": net_savings >= savings_goal,
        "category_breakdown": category_breakdown,
        "rule_50_30_20": {
            "needs": {"amount": round(needs, 2), "percentage": needs_pct, "ideal": "50%"},
            "wants": {"amount": round(wants, 2), "percentage": wants_pct, "ideal": "30%"},
            "savings": {"amount": round(savings, 2), "percentage": savings_pct, "ideal": "20%"}
        },
        "issues": issues,
        "recommendations": _get_budget_recommendations(savings_rate, needs_pct, wants_pct, net_savings),
        "status": "健康" if savings_rate >= 20 and net_savings > 0 else ("需改善" if net_savings > 0 else "赤字")
    }


def _get_budget_recommendations(savings_rate, needs_pct, wants_pct, net_savings):
    """根据预算分析生成建议。"""
    recs = []
    if net_savings < 0:
        recs.append("当前支出超过收入，建议立即削减非必要支出。")
    if needs_pct > 50:
        recs.append("必要支出过高，建议考虑降低住房成本或优化固定支出。")
    if wants_pct > 30:
        recs.append("非必要支出偏多，建议设定每月娱乐购物预算上限。")
    if savings_rate < 20 and savings_rate > 0:
        recs.append("储蓄率偏低，建议将储蓄率逐步提升至20%以上。")
    if savings_rate >= 20:
        recs.append("储蓄率良好，建议考虑将储蓄用于投资增值。")
    if not recs:
        recs.append("预算管理良好，继续保持。")
    return recs


# ---------------------------------------------------------------------------
# 4. 旅行规划
# ---------------------------------------------------------------------------
def travel_planner(destination, duration, budget, preferences=None):
    """
    旅行规划：根据目的地、天数、预算和偏好生成旅行计划。

    参数:
        destination (str): 目的地名称。
        duration (int): 旅行天数。
        budget (float): 总预算金额。
        preferences (dict): 偏好设置，含 travel_style（旅行风格）、
            interests（兴趣列表）、pace（节奏），为None时使用默认值。

    返回:
        dict: 旅行计划，含日程安排、预算分配和建议。
    """
    if preferences is None:
        preferences = {"travel_style": "经济", "interests": ["自然风光", "美食"], "pace": "适中"}

    travel_style = preferences.get("travel_style", "经济")
    interests = preferences.get("interests", ["自然风光"])
    pace = preferences.get("pace", "适中")

    # 预算分配
    style_multiplier = {"经济": 1.0, "舒适": 1.5, "豪华": 2.5}.get(travel_style, 1.0)
    adjusted_budget = budget / style_multiplier

    budget_allocation = {
        "住宿": adjusted_budget * 0.35,
        "餐饮": adjusted_budget * 0.25,
        "交通": adjusted_budget * 0.20,
        "景点门票": adjusted_budget * 0.10,
        "购物纪念": adjusted_budget * 0.05,
        "应急储备": adjusted_budget * 0.05
    }

    # 每日安排
    daily_plan = []
    activities_by_interest = {
        "自然风光": ["游览国家公园", "登山徒步", "湖边漫步", "日出日落观景"],
        "历史文化": ["参观博物馆", "古城游览", "历史遗迹探访", "文化表演"],
        "美食": ["当地特色餐厅", "街头小吃探索", "美食市场", "烹饪体验课"],
        "购物": ["商业街购物", "当地市场", "手工艺品店", "免税店"],
        "冒险": ["户外探险", "水上运动", "骑行游览", "跳伞/蹦极"],
        "休闲": ["温泉SPA", "海滩日光浴", "咖啡厅休闲", "公园散步"]
    }

    pace_config = {"紧凑": 4, "适中": 3, "轻松": 2}
    activities_per_day = pace_config.get(pace, 3)

    for day in range(1, duration + 1):
        day_activities = []
        for i in range(activities_per_day):
            interest = interests[i % len(interests)] if interests else "自然风光"
            activities = activities_by_interest.get(interest, ["自由活动"])
            activity = activities[(day + i) % len(activities)]
            day_activities.append({
                "time": _get_activity_time(i),
                "activity": activity,
                "interest": interest,
                "estimated_cost": round(adjusted_budget / duration / activities_per_day * 0.8, 0)
            })

        daily_plan.append({
            "day": day,
            "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
            "activities": day_activities,
            "daily_budget": round(adjusted_budget / duration, 2),
            "pace": pace
        })

    return {
        "destination": destination,
        "duration_days": duration,
        "total_budget": budget,
        "travel_style": travel_style,
        "interests": interests,
        "pace": pace,
        "budget_allocation": {k: round(v, 2) for k, v in budget_allocation.items()},
        "daily_budget": round(adjusted_budget / duration, 2),
        "itinerary": daily_plan,
        "packing_list": _generate_packing_list(destination, duration, travel_style),
        "tips": [
            f"提前预订{destination}的住宿以获得更好价格",
            "了解当地天气并准备相应衣物",
            "保存重要联系方式和紧急联系电话",
            "购买旅行保险以防意外",
            "兑换适量当地货币"
        ]
    }


def _get_activity_time(slot):
    """根据时段索引返回时间。"""
    times = ["上午 09:00-12:00", "下午 14:00-17:00", "傍晚 17:00-20:00", "晚上 20:00-22:00"]
    return times[slot % len(times)]


def _generate_packing_list(destination, duration, style):
    """生成行李清单。"""
    essentials = ["身份证/护照", "手机充电器", "现金/银行卡", "常用药品", "雨伞"]
    clothing = [f"内衣 {duration}套", f"袜子 {duration}双", "外套 1件",
                f"上衣 {min(duration, 5)}件", f"裤子 {min(duration // 2 + 1, 4)}条"]
    toiletries = ["牙刷/牙膏", "洗发水", "沐浴露", "毛巾", "防晒霜"]

    if style == "豪华":
        clothing.append("正装 1套")

    return {
        "必需品": essentials,
        "衣物": clothing,
        "洗漱用品": toiletries,
        "电子产品": ["手机", "充电宝", "耳机", "转换插头"]
    }


# ---------------------------------------------------------------------------
# 5. 一周餐饮计划
# ---------------------------------------------------------------------------
def meal_planner(week=None, dietary_prefs=None, calorie_target=2000):
    """
    一周餐饮计划：根据饮食偏好和热量目标生成一周三餐计划。

    参数:
        week (str): 目标周次，如 "2025-W01"，为None时使用当前周。
        dietary_prefs (str): 饮食偏好，如 "均衡"/"素食"/"高蛋白"/"低碳水"，为None时为"均衡"。
        calorie_target (int): 每日热量目标（千卡），默认2000。

    返回:
        dict: 一周餐饮计划，含每日三餐和营养统计。
    """
    if week is None:
        week = datetime.now().strftime("%Y-W%W")

    if dietary_prefs is None:
        dietary_prefs = "均衡"

    # 餐食数据库
    meal_db = {
        "均衡": {
            "breakfast": [
                {"name": "全麦吐司+鸡蛋+牛奶", "calories": 400, "protein": 20, "carbs": 45, "fat": 15},
                {"name": "燕麦粥+坚果+水果", "calories": 380, "protein": 12, "carbs": 55, "fat": 12},
                {"name": "包子+豆浆+鸡蛋", "calories": 420, "protein": 18, "carbs": 50, "fat": 14},
                {"name": "三明治+牛奶+水果", "calories": 410, "protein": 16, "carbs": 48, "fat": 14}
            ],
            "lunch": [
                {"name": "米饭+鸡胸肉+蔬菜", "calories": 650, "protein": 35, "carbs": 70, "fat": 18},
                {"name": "面条+牛肉+青菜", "calories": 680, "protein": 32, "carbs": 75, "fat": 20},
                {"name": "杂粮饭+鱼+豆腐+蔬菜", "calories": 620, "protein": 38, "carbs": 65, "fat": 15},
                {"name": "炒饭+虾仁+蔬菜", "calories": 660, "protein": 30, "carbs": 72, "fat": 20}
            ],
            "dinner": [
                {"name": "杂粮粥+蒸鱼+蔬菜", "calories": 550, "protein": 30, "carbs": 55, "fat": 15},
                {"name": "汤面+鸡蛋+青菜", "calories": 520, "protein": 22, "carbs": 60, "fat": 16},
                {"name": "红薯+鸡胸肉沙拉", "calories": 500, "protein": 28, "carbs": 50, "fat": 14},
                {"name": "蔬菜炒饭+豆腐汤", "calories": 530, "protein": 20, "carbs": 62, "fat": 15}
            ]
        },
        "素食": {
            "breakfast": [
                {"name": "豆浆+全麦馒头+水果", "calories": 380, "protein": 14, "carbs": 52, "fat": 10},
                {"name": "燕麦粥+坚果+蓝莓", "calories": 360, "protein": 11, "carbs": 55, "fat": 11}
            ],
            "lunch": [
                {"name": "杂粮饭+麻婆豆腐+蔬菜", "calories": 600, "protein": 25, "carbs": 70, "fat": 18},
                {"name": "蔬菜意面+沙拉", "calories": 580, "protein": 18, "carbs": 75, "fat": 16}
            ],
            "dinner": [
                {"name": "蔬菜粥+蒸南瓜+凉拌菜", "calories": 480, "protein": 15, "carbs": 55, "fat": 12},
                {"name": "豆腐蔬菜汤+杂粮饭", "calories": 500, "protein": 22, "carbs": 58, "fat": 14}
            ]
        },
        "高蛋白": {
            "breakfast": [
                {"name": "蛋白煎蛋+鸡胸肉+全麦面包", "calories": 450, "protein": 40, "carbs": 35, "fat": 15},
                {"name": "希腊酸奶+蛋白粉+坚果", "calories": 420, "protein": 35, "carbs": 30, "fat": 16}
            ],
            "lunch": [
                {"name": "鸡胸肉+糙米+西兰花", "calories": 700, "protein": 50, "carbs": 60, "fat": 18},
                {"name": "牛肉+红薯+蔬菜", "calories": 720, "protein": 45, "carbs": 55, "fat": 22}
            ],
            "dinner": [
                {"name": "三文鱼+蔬菜沙拉", "calories": 550, "protein": 38, "carbs": 25, "fat": 28},
                {"name": "蛋白+鸡胸肉+蔬菜", "calories": 520, "protein": 42, "carbs": 30, "fat": 16}
            ]
        }
    }

    prefs_meals = meal_db.get(dietary_prefs, meal_db["均衡"])
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    weekly_meals = []
    total_calories_week = 0

    for i, day_name in enumerate(weekdays):
        random.seed(hash(week + day_name) % 10000)

        breakfast = random.choice(prefs_meals["breakfast"])
        lunch = random.choice(prefs_meals["lunch"])
        dinner = random.choice(prefs_meals["dinner"])

        day_calories = breakfast["calories"] + lunch["calories"] + dinner["calories"]
        day_protein = breakfast["protein"] + lunch["protein"] + dinner["protein"]
        day_carbs = breakfast["carbs"] + lunch["carbs"] + dinner["carbs"]
        day_fat = breakfast["fat"] + lunch["fat"] + dinner["fat"]

        total_calories_week += day_calories

        weekly_meals.append({
            "day": day_name,
            "meals": {
                "早餐": breakfast,
                "午餐": lunch,
                "晚餐": dinner
            },
            "daily_nutrition": {
                "total_calories": day_calories,
                "calorie_target": calorie_target,
                "target_met": abs(day_calories - calorie_target) <= 200,
                "protein_g": day_protein,
                "carbs_g": day_carbs,
                "fat_g": day_fat,
                "protein_ratio": round(day_protein * 4 / day_calories * 100, 1),
                "carbs_ratio": round(day_carbs * 4 / day_calories * 100, 1),
                "fat_ratio": round(day_fat * 9 / day_calories * 100, 1)
            }
        })

    return {
        "week": week,
        "dietary_prefs": dietary_prefs,
        "calorie_target": calorie_target,
        "weekly_meals": weekly_meals,
        "weekly_summary": {
            "avg_daily_calories": round(total_calories_week / 7),
            "total_calories": total_calories_week,
            "target_variance": round(total_calories_week / 7 - calorie_target, 0),
            "assessment": "热量摄入达标" if abs(total_calories_week / 7 - calorie_target) <= 200 else "热量偏差较大，建议调整"
        }
    }


# ---------------------------------------------------------------------------
# 6. 习惯追踪器
# ---------------------------------------------------------------------------
def habit_tracker(habits, frequency="daily", streak_data=None):
    """
    习惯追踪器：追踪习惯养成情况和连续天数。

    参数:
        habits (list[dict]): 习惯列表，每项含 name、target_count、description。
        frequency (str): 追踪频率，如 "daily"/"weekly"/"monthly"，默认 "daily"。
        streak_data (dict): 历史连续记录，键为习惯名，值为连续天数。为None时初始化。

    返回:
        dict: 习惯追踪报告，含连续天数、完成率和建议。
    """
    if streak_data is None:
        streak_data = {}

    today = datetime.now()
    tracked = []
    best_streak = 0
    completed_count = 0

    for habit in habits:
        name = habit.get("name", "未知习惯")
        target = habit.get("target_count", 1)
        current_streak = streak_data.get(name, {}).get("streak", 0)
        best = streak_data.get(name, {}).get("best", 0)
        last_done = streak_data.get(name, {}).get("last_done", "")
        today_done = streak_data.get(name, {}).get("today_done", False)

        if today_done:
            completed_count += 1

        if current_streak > best:
            best = current_streak
        if best > best_streak:
            best_streak = best

        # 生成里程碑
        milestones = []
        for ms in [7, 21, 30, 66, 100, 365]:
            if current_streak >= ms:
                milestones.append({"days": ms, "achieved": True})
            elif current_streak >= ms * 0.7:
                milestones.append({"days": ms, "achieved": False, "progress": f"{current_streak}/{ms}天", "days_remaining": ms - current_streak})

        tracked.append({
            "name": name,
            "description": habit.get("description", ""),
            "frequency": frequency,
            "target_count": target,
            "current_streak": current_streak,
            "best_streak": best,
            "today_completed": today_done,
            "last_done": last_done,
            "milestones": milestones,
            "status": "进行中" if current_streak > 0 else "未开始",
            "motivation": _get_habit_motivation(current_streak)
        })

    return {
        "date": today.strftime("%Y-%m-%d"),
        "frequency": frequency,
        "total_habits": len(habits),
        "completed_today": completed_count,
        "completion_rate": round(completed_count / len(habits) * 100, 1) if habits else 0,
        "best_overall_streak": best_streak,
        "tracked_habits": tracked,
        "summary": _get_habit_summary(completed_count, len(habits), best_streak),
        "tips": [
            "从小目标开始，逐步增加难度",
            "将新习惯与已有习惯关联（习惯叠加）",
            "记录每日完成情况，可视化进度",
            "中断不超过2天，保持连续性",
            "给自己适当的奖励作为正向反馈"
        ]
    }


def _get_habit_motivation(streak):
    """根据连续天数返回激励语。"""
    if streak == 0:
        return "今天开始第一步！"
    elif streak < 7:
        return f"已坚持{streak}天，正在养成习惯！"
    elif streak < 21:
        return f"已坚持{streak}天，习惯正在形成！"
    elif streak < 66:
        return f"已坚持{streak}天，习惯已基本养成！"
    elif streak < 100:
        return f"已坚持{streak}天，非常出色！"
    else:
        return f"已坚持{streak}天，令人敬佩的毅力！"


def _get_habit_summary(completed, total, best):
    """生成习惯总结。"""
    rate = completed / total * 100 if total > 0 else 0
    if rate == 100:
        return f"完美的一天！今日{completed}/{total}个习惯全部完成。"
    elif rate >= 75:
        return f"表现优秀！今日完成{completed}/{total}个习惯。"
    elif rate >= 50:
        return f"还不错，今日完成{completed}/{total}个习惯，继续努力。"
    else:
        return f"今天完成了{completed}/{total}个习惯，明天加油！"


# ---------------------------------------------------------------------------
# 7. 睡眠分析
# ---------------------------------------------------------------------------
def sleep_analyzer(sleep_records, period="weekly"):
    """
    睡眠分析：分析睡眠记录的质量和趋势。

    参数:
        sleep_records (list[dict]): 睡眠记录列表，每项含 date、bedtime、wakeup_time、
            duration_hours、quality(1-5)、deep_sleep_hours、rem_sleep_hours。
        period (str): 分析周期，如 "weekly"/"monthly"，默认 "weekly"。

    返回:
        dict: 睡眠分析报告，含平均时长、质量评分和趋势。
    """
    if not sleep_records:
        return {"error": "无睡眠记录数据"}

    total_duration = sum(r.get("duration_hours", 0) for r in sleep_records)
    avg_duration = total_duration / len(sleep_records)
    total_deep = sum(r.get("deep_sleep_hours", 0) for r in sleep_records)
    avg_deep = total_deep / len(sleep_records)
    total_rem = sum(r.get("rem_sleep_hours", 0) for r in sleep_records)
    avg_rem = total_rem / len(sleep_records)
    avg_quality = sum(r.get("quality", 3) for r in sleep_records) / len(sleep_records)

    # 睡眠质量分级
    if avg_quality >= 4.5:
        quality_level = "优秀"
    elif avg_quality >= 3.5:
        quality_level = "良好"
    elif avg_quality >= 2.5:
        quality_level = "一般"
    else:
        quality_level = "较差"

    # 深度睡眠比例
    deep_ratio = avg_deep / avg_duration * 100 if avg_duration > 0 else 0
    rem_ratio = avg_rem / avg_duration * 100 if avg_duration > 0 else 0

    # 按日期排序分析趋势
    sorted_records = sorted(sleep_records, key=lambda x: x.get("date", ""))

    # 检测异常
    issues = []
    if avg_duration < 6:
        issues.append("平均睡眠时长不足6小时，严重睡眠不足")
    elif avg_duration < 7:
        issues.append("平均睡眠时长不足7小时，建议增加睡眠时间")

    if avg_duration > 10:
        issues.append("平均睡眠时长超过10小时，可能存在嗜睡问题")

    if deep_ratio < 15:
        issues.append(f"深度睡眠比例仅{deep_ratio:.1f}%，低于推荐值15-25%")

    if avg_quality < 3:
        issues.append("睡眠质量评分偏低，建议改善睡眠环境")

    # 一致性分析
    durations = [r.get("duration_hours", 0) for r in sleep_records]
    if durations:
        avg_d = sum(durations) / len(durations)
        variance = sum((d - avg_d) ** 2 for d in durations) / len(durations)
        std_dev = variance ** 0.5
        consistency = "高" if std_dev < 0.5 else ("中" if std_dev < 1.0 else "低")
    else:
        std_dev = 0
        consistency = "未知"

    # 日级别详情
    daily_details = []
    for r in sorted_records:
        duration = r.get("duration_hours", 0)
        quality = r.get("quality", 3)
        daily_details.append({
            "date": r.get("date", ""),
            "bedtime": r.get("bedtime", ""),
            "wakeup_time": r.get("wakeup_time", ""),
            "duration_hours": round(duration, 1),
            "quality": quality,
            "quality_label": {1: "很差", 2: "差", 3: "一般", 4: "好", 5: "很好"}.get(quality, "一般"),
            "deep_sleep_hours": r.get("deep_sleep_hours", 0),
            "rem_sleep_hours": r.get("rem_sleep_hours", 0),
            "status": "充足" if duration >= 7 else ("不足" if duration < 6 else "适中")
        })

    return {
        "period": period,
        "total_records": len(sleep_records),
        "averages": {
            "duration_hours": round(avg_duration, 1),
            "deep_sleep_hours": round(avg_deep, 1),
            "rem_sleep_hours": round(avg_rem, 1),
            "quality_score": round(avg_quality, 1),
            "quality_level": quality_level
        },
        "sleep_composition": {
            "deep_sleep_ratio": round(deep_ratio, 1),
            "rem_sleep_ratio": round(rem_ratio, 1),
            "light_sleep_ratio": round(100 - deep_ratio - rem_ratio, 1),
            "deep_ideal": "15-25%",
            "rem_ideal": "20-25%",
            "light_ideal": "50-60%"
        },
        "consistency": {
            "level": consistency,
            "std_deviation": round(std_dev, 2),
            "recommendation": "睡眠时间规律" if consistency == "高" else "建议固定作息时间，提高睡眠规律性"
        },
        "issues": issues,
        "daily_details": daily_details,
        "recommendations": _get_sleep_recommendations(avg_duration, avg_quality, deep_ratio, consistency)
    }


def _get_sleep_recommendations(avg_dur, avg_qual, deep_ratio, consistency):
    """生成睡眠建议。"""
    recs = []
    if avg_dur < 7:
        recs.append("建议每晚保证7-9小时睡眠时间")
    if avg_dur > 9:
        recs.append("睡眠时间偏长，建议调整至7-9小时")
    if avg_qual < 3.5:
        recs.append("改善睡眠环境：保持安静、适宜温度和黑暗环境")
    if deep_ratio < 15:
        recs.append("增加深度睡眠：避免睡前使用电子设备、减少咖啡因摄入")
    if consistency != "高":
        recs.append("建立规律作息：每天固定时间入睡和起床")
    recs.append("睡前1小时避免剧烈运动和强光刺激")
    recs.append("保持卧室温度在18-22°C最为适宜")
    return recs


# ---------------------------------------------------------------------------
# 8. 购物清单生成
# ---------------------------------------------------------------------------
def shopping_list_generator(meals, pantry=None, store_aisles=None):
    """
    购物清单生成：根据餐食计划和现有库存生成购物清单。

    参数:
        meals (list[dict]): 餐食计划列表，每项含 name、ingredients (list)。
        pantry (dict): 现有库存，键为食材名，值为数量。为None时视为空库存。
        store_aisles (dict): 超市区域映射，键为区域名，值为食材类别列表。
            为None时使用默认分区。

    返回:
        dict: 购物清单，按超市区域组织。
    """
    if pantry is None:
        pantry = {}
    if store_aisles is None:
        store_aisles = {
            "蔬菜区": ["番茄", "黄瓜", "青菜", "白菜", "胡萝卜", "洋葱", "土豆", "菠菜",
                      "西兰花", "生菜", "茄子", "青椒", "蘑菇", "姜", "蒜", "葱"],
            "肉类区": ["鸡肉", "猪肉", "牛肉", "鱼", "虾", "鸡蛋", "排骨", "三文鱼", "猪肉末"],
            "主食区": ["米饭", "面条", "面包", "燕麦", "面粉", "意面", "馒头", "杂粮", "全麦面包"],
            "调味区": ["盐", "糖", "酱油", "醋", "料酒", "橄榄油", "香油", "豆瓣酱",
                      "黑胡椒", "蒸鱼豉油", "辣酱", "味噌", "辣椒油", "八角"],
            "乳制品区": ["牛奶", "奶酪", "酸奶", "黄油", "奶油", "希腊酸奶"],
            "其他": ["坚果", "蓝莓", "水果", "海苔", "泡菜", "面包丁", "帕玛森芝士",
                    "凯撒酱", "蛋白粉", "面粉", "蜂蜜", "茶叶"]
        }

    # 汇总所需食材
    needed = {}
    for meal in meals:
        ingredients = meal.get("ingredients", [])
        if isinstance(ingredients, str):
            ingredients = [ingredients]
        for ing in ingredients:
            if ing in needed:
                needed[ing] += 1
            else:
                needed[ing] = 1

    # 减去已有库存
    to_buy = {}
    for item, qty in needed.items():
        have = pantry.get(item, 0)
        if qty > have:
            to_buy[item] = qty - have

    # 按超市区域分组
    organized = {}
    unclassified = []

    for item, qty in to_buy.items():
        placed = False
        for aisle, categories in store_aisles.items():
            if item in categories:
                if aisle not in organized:
                    organized[aisle] = []
                organized[aisle].append({
                    "item": item,
                    "quantity": qty,
                    "unit": "份/个"
                })
                placed = True
                break
        if not placed:
            unclassified.append({"item": item, "quantity": qty, "unit": "份/个"})

    # 计算总项数
    total_items = sum(len(items) for items in organized.values()) + len(unclassified)

    return {
        "total_items": total_items,
        "meals_planned": len(meals),
        "items_in_pantry": len(pantry),
        "items_to_buy": len(to_buy),
        "organized_list": organized,
        "unclassified": unclassified,
        "shopping_tips": [
            "按区域顺序购物可节省时间",
            "生鲜食品最后购买",
            "检查保质期，选择新鲜产品",
            "使用购物袋减少塑料使用",
            "对比价格选择性价比最高的商品"
        ]
    }


# ---------------------------------------------------------------------------
# 9. 穿搭推荐
# ---------------------------------------------------------------------------
def weather_outfit_planner(temperature, weather, occasion="casual"):
    """
    穿搭推荐：根据天气和场合推荐穿搭。

    参数:
        temperature (float): 温度（摄氏度）。
        weather (str): 天气状况，如 "晴"/"多云"/"雨"/"雪"/"风"。
        occasion (str): 场合，如 "casual"（休闲）、"formal"（正式）、
            "sport"（运动）、"work"（工作），默认 "casual"。

    返回:
        dict: 穿搭建议，含上装、下装、鞋子和配饰。
    """
    # 温度区间
    if temperature >= 30:
        temp_level = "炎热"
    elif temperature >= 25:
        temp_level = "温暖"
    elif temperature >= 18:
        temp_level = "舒适"
    elif temperature >= 10:
        temp_level = "凉爽"
    elif temperature >= 0:
        temp_level = "寒冷"
    else:
        temp_level = "严寒"

    # 穿搭数据库
    outfit_db = {
        "炎热": {
            "casual": {"top": "短袖T恤/背心", "bottom": "短裤/短裙", "shoes": "凉鞋/帆布鞋",
                       "accessories": ["遮阳帽", "太阳镜", "防晒霜"]},
            "formal": {"top": "短袖衬衫", "bottom": "轻薄西裤/半裙", "shoes": "透气皮鞋",
                        "accessories": ["太阳镜", "手帕"]},
            "work": {"top": "短袖衬衫/Polo衫", "bottom": "轻薄西裤", "shoes": "乐福鞋",
                      "accessories": ["太阳镜"]},
            "sport": {"top": "速干短袖", "bottom": "运动短裤", "shoes": "运动凉鞋",
                       "accessories": ["遮阳帽", "运动水壶"]}
        },
        "温暖": {
            "casual": {"top": "短袖/T恤", "bottom": "薄长裤/牛仔裤", "shoes": "帆布鞋/运动鞋",
                       "accessories": ["太阳镜"]},
            "formal": {"top": "薄衬衫", "bottom": "西裤", "shoes": "皮鞋",
                        "accessories": ["手表"]},
            "work": {"top": "衬衫", "bottom": "西裤/半裙", "shoes": "皮鞋",
                      "accessories": ["手表"]},
            "sport": {"top": "速干T恤", "bottom": "运动裤", "shoes": "跑步鞋",
                       "accessories": ["运动水壶"]}
        },
        "舒适": {
            "casual": {"top": "长袖T恤/薄卫衣", "bottom": "牛仔裤/休闲裤", "shoes": "运动鞋/休闲鞋",
                       "accessories": ["薄外套"]},
            "formal": {"top": "衬衫+薄外套", "bottom": "西裤", "shoes": "皮鞋",
                        "accessories": ["围巾(可选)"]},
            "work": {"top": "衬衫+薄针织衫", "bottom": "西裤/半裙", "shoes": "皮鞋",
                      "accessories": ["手表"]},
            "sport": {"top": "长袖运动衣", "bottom": "运动长裤", "shoes": "跑步鞋",
                       "accessories": ["运动水壶"]}
        },
        "凉爽": {
            "casual": {"top": "卫衣/毛衣", "bottom": "厚牛仔裤/休闲裤", "shoes": "运动鞋/靴子",
                       "accessories": ["围巾", "薄外套"]},
            "formal": {"top": "衬衫+毛衣+外套", "bottom": "西裤", "shoes": "皮鞋",
                        "accessories": ["围巾", "手套"]},
            "work": {"top": "衬衫+针织衫+外套", "bottom": "西裤/半裙+打底裤", "shoes": "皮鞋/短靴",
                      "accessories": ["围巾"]},
            "sport": {"top": "保暖运动衣", "bottom": "运动长裤", "shoes": "跑步鞋",
                       "accessories": ["运动手套", "保暖帽"]}
        },
        "寒冷": {
            "casual": {"top": "厚毛衣/羽绒内胆", "bottom": "加绒裤", "shoes": "雪地靴/厚底鞋",
                       "accessories": ["羽绒服", "围巾", "手套", "毛线帽"]},
            "formal": {"top": "衬衫+毛衣+厚外套", "bottom": "加厚西裤", "shoes": "皮靴",
                        "accessories": ["围巾", "手套", "毛线帽"]},
            "work": {"top": "衬衫+毛衣+羽绒服", "bottom": "加绒西裤", "shoes": "短靴",
                      "accessories": ["围巾", "手套"]},
            "sport": {"top": "保暖运动套装", "bottom": "加绒运动裤", "shoes": "防滑运动鞋",
                       "accessories": ["运动手套", "保暖帽", "面罩"]}
        },
        "严寒": {
            "casual": {"top": "厚羽绒+毛衣", "bottom": "加绒裤+秋裤", "shoes": "雪地靴",
                       "accessories": ["厚围巾", "厚手套", "毛线帽", "暖宝宝"]},
            "formal": {"top": "衬衫+厚毛衣+羽绒服", "bottom": "加厚西裤+秋裤", "shoes": "厚皮靴",
                        "accessories": ["厚围巾", "厚手套", "毛线帽"]},
            "work": {"top": "保暖内衣+衬衫+毛衣+羽绒服", "bottom": "加绒西裤+秋裤", "shoes": "厚靴子",
                      "accessories": ["围巾", "手套", "帽子"]},
            "sport": {"top": "保暖内衣+抓绒+防风外套", "bottom": "加绒运动裤", "shoes": "防滑雪地鞋",
                       "accessories": ["运动手套", "面罩", "保暖帽", "暖宝宝"]}
        }
    }

    # 获取基础穿搭
    temp_outfits = outfit_db.get(temp_level, outfit_db["舒适"])
    outfit = temp_outfits.get(occasion, temp_outfits.get("casual")).copy()

    # 根据天气调整
    weather_adjustments = {
        "雨": {"extra": "雨伞/雨衣", "shoes_override": "防水鞋/雨靴",
               "note": "雨天出行，注意防滑和防水"},
        "雪": {"extra": "防水面料外套", "shoes_override": "防滑雪地靴",
               "note": "雪天出行，注意保暖和防滑"},
        "风": {"extra": "防风外套", "note": "大风天气，注意防风保暖"},
        "晴": {"extra": "太阳镜" if temperature > 20 else None,
               "note": "晴天出行，注意防晒" if temperature > 20 else "天气晴好"},
        "多云": {"note": "天气适中，穿搭灵活"}
    }

    adjustment = weather_adjustments.get(weather, {"note": "注意查看实时天气预报"})
    if adjustment.get("shoes_override"):
        outfit["shoes"] = adjustment["shoes_override"]
    if adjustment.get("extra"):
        outfit["accessories"] = outfit.get("accessories", []) + [adjustment["extra"]]

    return {
        "temperature": temperature,
        "temperature_level": temp_level,
        "weather": weather,
        "occasion": occasion,
        "outfit": {
            "top": outfit.get("top", ""),
            "bottom": outfit.get("bottom", ""),
            "shoes": outfit.get("shoes", ""),
            "accessories": outfit.get("accessories", []),
            "outerwear": outfit.get("outerwear", "根据体感选择")
        },
        "weather_note": adjustment.get("note", ""),
        "tips": [
            "采用洋葱式穿搭法，方便增减衣物",
            "选择透气面料避免闷热",
            "注意保护易受寒部位（颈、手、脚）",
            "深色衣物吸热，浅色衣物反射阳光"
        ]
    }


# ---------------------------------------------------------------------------
# 10. 订阅管理追踪
# ---------------------------------------------------------------------------
def subscription_tracker(subscriptions, billing_cycle="monthly"):
    """
    订阅管理追踪：追踪各类订阅服务的费用和使用情况。

    参数:
        subscriptions (list[dict]): 订阅列表，每项含 name、category、price、
            billing_cycle、start_date、last_used、status。
        billing_cycle (str): 默认计费周期筛选，如 "monthly"/"yearly"/"weekly"，
            默认 "monthly"。

    返回:
        dict: 订阅管理报告，含总费用、分类统计和使用建议。
    """
    now = datetime.now()
    active_subs = [s for s in subscriptions if s.get("status", "active") == "active"]
    total_monthly_cost = 0
    total_yearly_cost = 0
    category_costs = {}
    unused_subs = []
    expiring_soon = []

    for sub in subscriptions:
        name = sub.get("name", "未知")
        category = sub.get("category", "其他")
        price = sub.get("price", 0)
        cycle = sub.get("billing_cycle", "monthly")

        # 转换为月费
        if cycle == "yearly":
            monthly_cost = price / 12
        elif cycle == "weekly":
            monthly_cost = price * 4.33
        elif cycle == "quarterly":
            monthly_cost = price / 3
        else:
            monthly_cost = price

        yearly_cost = monthly_cost * 12
        total_monthly_cost += monthly_cost
        total_yearly_cost += yearly_cost

        # 分类统计
        if category not in category_costs:
            category_costs[category] = {"monthly": 0, "count": 0, "items": []}
        category_costs[category]["monthly"] += monthly_cost
        category_costs[category]["count"] += 1
        category_costs[category]["items"].append(name)

        # 检查使用情况
        last_used = sub.get("last_used", "")
        if last_used:
            try:
                last_used_dt = datetime.strptime(last_used, "%Y-%m-%d")
                days_unused = (now - last_used_dt).days
                sub["days_since_last_use"] = days_unused
                if days_unused > 30:
                    unused_subs.append({
                        "name": name,
                        "category": category,
                        "monthly_cost": round(monthly_cost, 2),
                        "days_unused": days_unused,
                        "recommendation": "已超过30天未使用，建议考虑取消订阅"
                    })
            except (ValueError, TypeError):
                pass

        # 检查即将到期
        start_date = sub.get("start_date", "")
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                if cycle == "yearly":
                    renewal_date = start_dt + timedelta(days=365)
                else:
                    renewal_date = start_dt + timedelta(days=30)

                while renewal_date < now:
                    if cycle == "yearly":
                        renewal_date += timedelta(days=365)
                    else:
                        renewal_date += timedelta(days=30)

                days_until_renewal = (renewal_date - now).days
                sub["next_renewal_date"] = renewal_date.strftime("%Y-%m-%d")
                sub["days_until_renewal"] = days_until_renewal

                if days_until_renewal <= 7:
                    expiring_soon.append({
                        "name": name,
                        "renewal_date": renewal_date.strftime("%Y-%m-%d"),
                        "days_until_renewal": days_until_renewal,
                        "cost": price
                    })
            except (ValueError, TypeError):
                pass

    # 分类统计排序
    sorted_categories = sorted(category_costs.items(), key=lambda x: x[1]["monthly"], reverse=True)
    category_summary = []
    for cat, data in sorted_categories:
        category_summary.append({
            "category": cat,
            "monthly_cost": round(data["monthly"], 2),
            "yearly_cost": round(data["monthly"] * 12, 2),
            "percentage": round(data["monthly"] / total_monthly_cost * 100, 1) if total_monthly_cost > 0 else 0,
            "subscription_count": data["count"],
            "subscriptions": data["items"]
        })

    # 节省建议
    savings_potential = sum(u["monthly_cost"] for u in unused_subs)

    return {
        "report_date": now.strftime("%Y-%m-%d"),
        "billing_cycle_filter": billing_cycle,
        "total_subscriptions": len(subscriptions),
        "active_subscriptions": len(active_subs),
        "total_monthly_cost": round(total_monthly_cost, 2),
        "total_yearly_cost": round(total_yearly_cost, 2),
        "average_per_subscription": round(total_monthly_cost / len(subscriptions), 2) if subscriptions else 0,
        "category_breakdown": category_summary,
        "unused_subscriptions": unused_subs,
        "expiring_soon": expiring_soon,
        "potential_monthly_savings": round(savings_potential, 2),
        "potential_yearly_savings": round(savings_potential * 12, 2),
        "recommendations": _get_subscription_recommendations(unused_subs, total_monthly_cost, savings_potential),
        "status": "需优化" if len(unused_subs) > 2 else ("良好" if total_monthly_cost < 200 else "偏高")
    }


def _get_subscription_recommendations(unused, total_cost, savings):
    """生成订阅管理建议。"""
    recs = []
    if unused:
        recs.append(f"发现{len(unused)}个未使用的订阅，取消后每月可节省{savings:.2f}元。")
    if total_cost > 500:
        recs.append("月度订阅费用偏高，建议审视各订阅的必要性。")
    if total_cost > 200:
        recs.append("考虑家庭共享计划或年付优惠来降低成本。")
    recs.append("定期（每季度）审查订阅使用情况，及时取消不需要的服务。")
    recs.append("关注各平台的优惠活动，适时切换到更优惠的套餐。")
    return recs


# ---------------------------------------------------------------------------
# 主程序入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("生活服务工具 - lifestyle-planner")
    print("=" * 60)

    # 演示：食谱推荐
    print("\n[1] 食谱推荐示例:")
    recipes = recipe_recommender(["鸡蛋", "番茄", "鸡肉"], "中餐", None, 3)
    print(json.dumps(recipes, ensure_ascii=False, indent=2))

    # 演示：健身计划
    print("\n[2] 健身计划示例:")
    workout = workout_planner("beginner", "general_fitness", 3, ["徒手"])
    print(json.dumps(workout, ensure_ascii=False, indent=2))

    # 演示：穿搭推荐
    print("\n[3] 穿搭推荐示例:")
    outfit = weather_outfit_planner(15, "多云", "casual")
    print(json.dumps(outfit, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("所有工具已就绪，可通过导入 main 模块使用。")
