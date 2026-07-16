"""Auto-generated tests for lifestyle-planner."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main


class TestMain:
    """Tests for lifestyle-planner module."""

    def test_module_import(self):
        """Test that main module imports correctly."""
        assert main is not None
        assert hasattr(main, "nutrition_calculator")


    def test_nutrition_calculator_basic(self):
        """Test nutrition calculator."""
        foods = [{"name": "米饭", "amount": 200}, {"name": "鸡蛋", "amount": 100}]
        targets = {"calories": 2000, "protein": 60, "fat": 65, "carbs": 300, "fiber": 25}
        result = main.nutrition_calculator(foods, targets)
        assert "intake_summary" in result or "nutrient_gaps" in result

    def test_nutrition_calculator_empty(self):
        """Test nutrition calculator with empty foods."""
        targets = {"calories": 2000}
        result = main.nutrition_calculator([], targets)
        assert result is not None

    def test_nutrition_missing_food(self):
        """Test with unrecognized food."""
        foods = [{"name": "火星食物", "amount": 100}]
        result = main.nutrition_calculator(foods, {"calories": 2000})
        assert "unrecognized" in result or "intake_summary" in result

    def test_bmi_health_assessor_exists(self):
        """Test that bmi_health_assessor function is callable."""
        assert callable(main.bmi_health_assessor)
        assert main.bmi_health_assessor.__doc__ is not None

    def test_fitness_plan_generator_exists(self):
        """Test that fitness_plan_generator function is callable."""
        assert callable(main.fitness_plan_generator)
        assert main.fitness_plan_generator.__doc__ is not None

    def test_budget_optimizer_exists(self):
        """Test that budget_optimizer function is callable."""
        assert callable(main.budget_optimizer)
        assert main.budget_optimizer.__doc__ is not None

    def test_meal_planner_exists(self):
        """Test that meal_planner function is callable."""
        assert callable(main.meal_planner)
        assert main.meal_planner.__doc__ is not None
