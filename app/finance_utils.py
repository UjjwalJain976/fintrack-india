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


def dashboard_summary(start_date=None, end_date=None):
    income_query = db.session.query(func.coalesce(func.sum(Income.amount), 0))
    expense_query = db.session.query(func.coalesce(func.sum(Expense.amount), 0))
    category_query = db.session.query(distinct(Expense.category))

    if start_date and end_date:
        income_query = income_query.filter(
            Income.income_date >= start_date,
            Income.income_date <= end_date,
        )
        expense_query = expense_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )
        category_query = category_query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )

    monthly_income = to_float(income_query.scalar())
    monthly_expenses = to_float(expense_query.scalar())
    monthly_savings = monthly_income - monthly_expenses
    savings_rate = (monthly_savings / monthly_income * 100) if monthly_income else 0
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
    expense_category_count = category_query.count()

    score = financial_health_score(
        total_income=monthly_income,
        total_expenses=monthly_expenses,
        savings_rate=savings_rate,
        investment_count=fd_count + sip_count,
        goal_count=goal_count,
        expense_category_count=expense_category_count,
    )

    return {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
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
