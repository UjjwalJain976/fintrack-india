from calendar import month_name, monthrange
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import func

from app import db
from app.finance_utils import currency, dashboard_summary, to_float
from app.models import Expense, FDAccount, Goal, Income, SIPInvestment


main = Blueprint("main", __name__)
EXPENSE_CATEGORIES = [
    "Food",
    "Rent",
    "Travel",
    "Shopping",
    "Bills",
    "Family",
    "Investment",
    "Other",
]


def parse_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


def parse_decimal(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def delete_record(model, row_id):
    record = db.session.get(model, int(row_id))
    if record:
        db.session.delete(record)
        db.session.commit()


def parse_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def selected_month_range(month, year):
    last_day = monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def dashboard_year_options(selected_year, current_year):
    years = list(range(current_year - 5, current_year + 2))
    if selected_year not in years:
        years.append(selected_year)
    return sorted(years, reverse=True)


@main.route("/")
def dashboard():
    today = date.today()
    selected_month = parse_int(request.args.get("month"), today.month)
    selected_year = parse_int(request.args.get("year"), today.year)

    if selected_month < 1 or selected_month > 12:
        selected_month = today.month
    if selected_year < 2000 or selected_year > today.year + 10:
        selected_year = today.year

    start_date, end_date = selected_month_range(selected_month, selected_year)

    category_totals = (
        db.session.query(
            Expense.category,
            func.coalesce(func.sum(Expense.amount), 0).label("total"),
        )
        .filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )
        .group_by(Expense.category)
        .order_by(func.coalesce(func.sum(Expense.amount), 0).desc())
        .all()
    )
    recent_income = (
        Income.query.filter(
            Income.income_date >= start_date,
            Income.income_date <= end_date,
        )
        .order_by(Income.income_date.desc(), Income.created_at.desc(), Income.id.desc())
        .limit(5)
        .all()
    )
    recent_expenses = (
        Expense.query.filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date,
        )
        .order_by(
            Expense.expense_date.desc(),
            Expense.created_at.desc(),
            Expense.id.desc(),
        )
        .limit(5)
        .all()
    )

    summary = dashboard_summary(start_date=start_date, end_date=end_date)
    income_expense_chart = {
        "labels": ["Income", "Expenses"],
        "values": [summary["monthly_income"], summary["monthly_expenses"]],
    }
    category_chart = {
        "labels": [category for category, _total in category_totals],
        "values": [to_float(total) for _category, total in category_totals],
    }

    return render_template(
        "dashboard.html",
        summary=summary,
        selected_month=selected_month,
        selected_month_name=month_name[selected_month],
        selected_year=selected_year,
        month_options=[(month, month_name[month]) for month in range(1, 13)],
        year_options=dashboard_year_options(selected_year, today.year),
        income_expense_chart=income_expense_chart,
        category_chart=category_chart,
        recent_income=recent_income,
        recent_expenses=recent_expenses,
        currency=currency,
    )


@main.route("/income", methods=["GET", "POST"])
def income():
    if request.method == "POST":
        entry = Income(
            source=request.form.get("source"),
            amount=parse_decimal(request.form.get("amount")),
            income_date=parse_date(request.form.get("date")),
            notes=request.form.get("notes"),
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.income"))

    entries = Income.query.all()
    return render_template("income.html", entries=entries)


@main.post("/income/delete/<row_id>")
def delete_income(row_id):
    delete_record(Income, row_id)
    return redirect(url_for("main.income"))


@main.route("/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "POST":
        entry = Expense(
            category=request.form.get("category"),
            amount=parse_decimal(request.form.get("amount")),
            expense_date=parse_date(request.form.get("date")),
            payment_mode=request.form.get("payment_mode"),
            notes=request.form.get("notes"),
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.expenses"))

    entries = Expense.query.all()
    return render_template(
        "expenses.html",
        entries=entries,
        categories=EXPENSE_CATEGORIES,
    )


@main.post("/expenses/delete/<row_id>")
def delete_expense(row_id):
    delete_record(Expense, row_id)
    return redirect(url_for("main.expenses"))


@main.route("/fd", methods=["GET", "POST"])
def fd():
    if request.method == "POST":
        entry = FDAccount(
            bank_name=request.form.get("bank_name"),
            principal_amount=parse_decimal(request.form.get("principal_amount")),
            interest_rate=parse_decimal(request.form.get("interest_rate")),
            start_date=parse_date(request.form.get("start_date")),
            maturity_date=parse_date(request.form.get("maturity_date")),
            maturity_amount=parse_decimal(request.form.get("maturity_amount")),
            status=request.form.get("status") or "Active",
            notes=request.form.get("notes"),
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.fd"))

    entries = FDAccount.query.all()
    return render_template("fd.html", entries=entries)


@main.post("/fd/delete/<row_id>")
def delete_fd(row_id):
    delete_record(FDAccount, row_id)
    return redirect(url_for("main.fd"))


@main.route("/sip", methods=["GET", "POST"])
def sip():
    if request.method == "POST":
        entry = SIPInvestment(
            fund_name=request.form.get("fund_name"),
            monthly_amount=parse_decimal(request.form.get("monthly_amount")),
            start_date=parse_date(request.form.get("start_date")),
            category=request.form.get("category"),
            current_value=parse_decimal(request.form.get("current_value")),
            notes=request.form.get("notes"),
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.sip"))

    entries = SIPInvestment.query.all()
    return render_template("sip.html", entries=entries)


@main.post("/sip/delete/<row_id>")
def delete_sip(row_id):
    delete_record(SIPInvestment, row_id)
    return redirect(url_for("main.sip"))


@main.route("/goals", methods=["GET", "POST"])
def goals():
    if request.method == "POST":
        entry = Goal(
            goal_name=request.form.get("goal_name"),
            target_amount=parse_decimal(request.form.get("target_amount")),
            current_amount=parse_decimal(request.form.get("current_amount")),
            target_date=parse_date(request.form.get("target_date")),
            priority=request.form.get("priority"),
            notes=request.form.get("notes"),
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.goals"))

    entries = Goal.query.all()
    return render_template("goals.html", entries=entries)


@main.post("/goals/delete/<row_id>")
def delete_goal(row_id):
    delete_record(Goal, row_id)
    return redirect(url_for("main.goals"))
