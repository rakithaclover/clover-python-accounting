"""
PostgreSQL checks of the Clover distribution's settings, run by CI with a PostgreSQL service.

Run: python tests/postgresql/smoke.py postgresql+psycopg2://user:password@host:port/database
The database is emptied first. Not collected by pytest, because the amount precision must be set
before the models are imported, which pytest's conftest has already done.
"""

import sys
from datetime import datetime
from decimal import Decimal

from python_accounting.config import config

config.database["amount_precision"] = 28
config.configure_hashing(salt="smoke test salt", chain="entity")

# pylint: disable=wrong-import-position
from sqlalchemy import String, create_engine, select, text, update
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from python_accounting.database.session import get_session
from python_accounting.models import Account, Base, Currency, Entity, Ledger, LineItem
from python_accounting.transactions import JournalEntry


class OtherBase(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """A model base unrelated to accounting."""


class Note(OtherBase):  # pylint: disable=too-few-public-methods
    """A model of another part of an application."""

    __tablename__ = "smoke_note"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(50))


def _journal(session, entity, debit, credit, amount):
    journal = JournalEntry(
        narration="Smoke journal",
        transaction_date=datetime.now(),
        account_id=debit.id,
        entity_id=entity.id,
    )
    session.add(journal)
    session.flush()
    line = LineItem(
        narration="Smoke line", account_id=credit.id, amount=Decimal(amount), entity_id=entity.id
    )
    session.add(line)
    session.flush()
    journal.line_items.add(line)
    session.flush()
    journal.post(session)
    return journal


def main(url: str) -> None:
    """Runs the checks, raising AssertionError on the first failure."""
    engine = create_engine(url)
    with engine.begin() as connection:
        # A fresh public schema: drop_all cannot drop the library's unnamed use_alter keys.
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    OtherBase.metadata.create_all(engine)

    with get_session(engine) as session:
        entity = Entity(name="Smoke Entity")
        session.add(entity)
        session.commit()
        currency = Currency(name="Euro", code="EUR", entity_id=entity.id)
        session.add(currency)
        session.commit()
        bank = Account(name="Bank", account_type=Account.AccountType.BANK,
                       currency_id=currency.id, entity_id=entity.id)
        revenue = Account(name="Revenue", account_type=Account.AccountType.OPERATING_REVENUE,
                          currency_id=currency.id, entity_id=entity.id)
        session.add_all([bank, revenue])
        session.commit()

        # D4: amounts of a billion and more are stored exactly.
        big = _journal(session, entity, bank, revenue, "12500000000.1234")
        session.commit()
        stored = session.scalars(select(Ledger.amount).where(Ledger.transaction_id == big.id)).all()
        assert stored and all(a == Decimal("12500000000.1234") for a in stored), stored
        print("D4 ok: 12500000000.1234 stored exactly")

        # D3: the entity chain detects a changed predecessor.
        second = _journal(session, entity, bank, revenue, "50")
        session.commit()
        assert big.is_secure(session) and second.is_secure(session)
        last_of_big = max(ledger.id for ledger in big.ledgers)
        session.connection().execute(update(Ledger).where(Ledger.id == last_of_big).values(hash="x"))
        session.expire_all()
        assert not second.is_secure(session)
        session.rollback()
        print("D3 ok: a changed hash breaks the next transaction's verification")

        # D2: timestamps are taken when saving.
        assert second.created_at > big.created_at
        print("D2 ok: created_at is the time of saving")

    # D0: a plain session works beside the accounting session.
    with Session(engine) as plain:
        plain.add(Note(text="not accounting"))
        plain.commit()
        assert plain.scalars(select(Note.text)).one() == "not accounting"
    print("D0 ok: plain Session unaffected")
    print("PostgreSQL smoke checks passed")


if __name__ == "__main__":
    main(sys.argv[1])
