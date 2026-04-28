import pandas as pd
import pytest
from metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5, 6],
        "department": ["Sales", "Sales", "HR", "HR", "IT", "IT"],
        "overtime": ["Yes", "Yes", "No", "No", "Yes", "No"],
        "job_satisfaction": [1, 2, 3, 4, 1, 2],
        "monthly_income": [4000.0, 5000.0, 6000.0, 7000.0, 4500.0, 5500.0],
        "attrition": ["Yes", "Yes", "No", "No", "Yes", "No"],
    })


# --- attrition_rate ---

def test_attrition_rate_fifty_percent(sample_df):
    assert attrition_rate(sample_df) == 50.0


def test_attrition_rate_zero(sample_df):
    sample_df["attrition"] = "No"
    assert attrition_rate(sample_df) == 0.0


def test_attrition_rate_hundred_percent(sample_df):
    sample_df["attrition"] = "Yes"
    assert attrition_rate(sample_df) == 100.0


# --- attrition_by_department ---

def test_attrition_by_department_columns(sample_df):
    result = attrition_by_department(sample_df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_rates(sample_df):
    result = attrition_by_department(sample_df)
    rates = dict(zip(result["department"], result["attrition_rate"]))
    assert rates["Sales"] == 100.0
    assert rates["IT"] == 50.0
    assert rates["HR"] == 0.0


def test_attrition_by_department_sorted_descending(sample_df):
    result = attrition_by_department(sample_df)
    assert list(result["department"]) == ["Sales", "IT", "HR"]


# --- attrition_by_overtime ---

def test_attrition_by_overtime_columns(sample_df):
    result = attrition_by_overtime(sample_df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_rates(sample_df):
    # All 3 overtime=Yes employees left; all 3 overtime=No employees stayed
    result = attrition_by_overtime(sample_df)
    rates = dict(zip(result["overtime"], result["attrition_rate"]))
    assert rates["Yes"] == 100.0
    assert rates["No"] == 0.0


# --- average_income_by_attrition ---

def test_average_income_by_attrition_columns(sample_df):
    result = average_income_by_attrition(sample_df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_values(sample_df):
    # Leavers: 4000, 5000, 4500 → mean 4500.0
    # Stayers: 6000, 7000, 5500 → mean 6166.67
    result = average_income_by_attrition(sample_df)
    income = dict(zip(result["attrition"], result["avg_monthly_income"]))
    assert income["Yes"] == 4500.0
    assert income["No"] == 6166.67


# --- satisfaction_summary ---

def test_satisfaction_summary_columns(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_rates(sample_df):
    # sat=1: 2 employees, 2 leavers → 100%
    # sat=2: 2 employees, 1 leaver  → 50%
    # sat=3: 1 employee,  0 leavers → 0%
    # sat=4: 1 employee,  0 leavers → 0%
    result = satisfaction_summary(sample_df)
    rates = dict(zip(result["job_satisfaction"], result["attrition_rate"]))
    assert rates[1] == 100.0
    assert rates[2] == 50.0
    assert rates[3] == 0.0
    assert rates[4] == 0.0


def test_satisfaction_summary_sorted_by_satisfaction(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result["job_satisfaction"]) == [1, 2, 3, 4]
