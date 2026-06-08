from sqlalchemy import distinct, func

from app import db
from app.models import Expense, FDAccount, Goal, Income, SIPInvestment


def to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def currency(value):
    return f"{to_float(value):,.2f}"


def dashboard_summary():
    total_income = to_float(
        db.session.query(func.coalesce(func.sum(Income.amount), 0)).scalar()
    )
    total_expenses = to_float(
        db.session.query(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    )
    monthly_savings = total_income - total_expenses
    savings_rate = (monthly_savings / total_income * 100) if total_income else 0
    total_fd = to_float(
        db.session.query(func.coalesce(func.sum(FDAccount.principal_amount), 0)).scalar()
    )
    total_sip = to_float(
        db.session.query(func.coalesce(func.sum(SIPInvestment.monthly_amount), 0)).scalar()
    )
    total_goal_target = to_float(
        db.session.query(func.coalesce(func.sum(Goal.target_amount), 0)).scalar()
    )
    fd_count = db.session.query(FDAccount.id).count()
    sip_count = db.session.query(SIPInvestment.id).count()
    goal_count = db.session.query(Goal.id).count()
    expense_category_count = db.session.query(distinct(Expense.category)).count()

    score = financial_health_score(
        total_income=total_income,
        total_expenses=total_expenses,
        savings_rate=savings_rate,
        investment_count=fd_count + sip_count,
        goal_count=goal_count,
        expense_category_count=expense_category_count,
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
        "total_fd": total_fd,
        "total_sip": total_sip,
        "total_goal_target": total_goal_target,
        "health_score": score,
    }


def financial_health_score(
    total_income,
    total_expenses,
    savings_rate,
    investment_count,
    goal_count,
    expense_category_count,
):
    score = 0

    if total_income > total_expenses:
        score += 20
    if savings_rate > 20:
        score += 25
    if investment_count > 0:
        score += 20
    if goal_count > 0:
        score += 15
    if expense_category_count > 0:
        score += 20

    return score
