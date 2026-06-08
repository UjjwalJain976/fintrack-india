from sqlalchemy import func

from app import db


class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    income_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    payment_mode = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class FDAccount(db.Model):
    __tablename__ = "fd_accounts"

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(120), nullable=False)
    principal_amount = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    maturity_date = db.Column(db.Date, nullable=False)
    maturity_amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Active")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class SIPInvestment(db.Model):
    __tablename__ = "sip_investments"

    id = db.Column(db.Integer, primary_key=True)
    fund_name = db.Column(db.String(160), nullable=False)
    monthly_amount = db.Column(db.Numeric(12, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    current_value = db.Column(db.Numeric(12, 2), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(160), nullable=False)
    target_amount = db.Column(db.Numeric(12, 2), nullable=False)
    current_amount = db.Column(db.Numeric(12, 2), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(40), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
