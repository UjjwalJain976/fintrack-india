from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.finance_utils import currency, dashboard_summary
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


@main.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        summary=dashboard_summary(),
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
