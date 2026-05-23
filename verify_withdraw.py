
import sys
import os
from sqlalchemy import create_mock_engine
from sqlalchemy.orm import Session, sessionmaker

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.database import Base
from backend.models.models import User, Transaction, TransactionType, TransactionStatus
from backend.services.wallet_service import wallet_service
from sqlalchemy import create_engine

# Use in-memory sqlite for testing
engine = create_engine('sqlite:///:memory:')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_withdrawal_logic():
    db = TestingSessionLocal()
    try:
        # 1. Create a user with 100 balance
        user = User(
            full_name="Test User",
            username="testuser",
            email="test@example.com",
            hashed_password="password",
            balance=100.0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Initial balance: {user.balance}")

        # 2. Attempt withdrawal of 150 (Insufficient)
        print("Testing insufficient balance...")
        try:
            wallet_service.create_transaction(db, user.id, TransactionType.WITHDRAWAL, 150.0, "Bank")
            print("ERROR: Allowed withdrawal with insufficient balance")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        # 3. Successful withdrawal of 40
        print("Testing successful withdrawal creation...")
        tx = wallet_service.create_transaction(db, user.id, TransactionType.WITHDRAWAL, 40.0, "Bank")
        db.refresh(user)
        print(f"Balance after withdrawal creation: {user.balance}")
        if user.balance == 60.0:
            print("SUCCESS: Balance deducted correctly")
        else:
            print(f"FAILURE: Balance is {user.balance}, expected 60.0")

        # 4. Reject the withdrawal (Refund)
        print("Testing withdrawal rejection (refund)...")
        wallet_service.reject_transaction(db, tx.id)
        db.refresh(user)
        db.refresh(tx)
        print(f"Balance after rejection: {user.balance}")
        print(f"Transaction status: {tx.status}")
        if user.balance == 100.0 and tx.status == TransactionStatus.REJECTED:
            print("SUCCESS: Balance refunded correctly")
        else:
            print("FAILURE: Rejection logic failed")

        # 5. Create another and approve it
        print("Testing withdrawal approval...")
        tx2 = wallet_service.create_transaction(db, user.id, TransactionType.WITHDRAWAL, 50.0, "Bank")
        wallet_service.approve_transaction(db, tx2.id)
        db.refresh(user)
        db.refresh(tx2)
        print(f"Balance after approval: {user.balance}")
        print(f"Transaction status: {tx2.status}")
        if user.balance == 50.0 and tx2.status == TransactionStatus.APPROVED:
            print("SUCCESS: Approval logic correct")
        else:
            print("FAILURE: Approval logic failed")

    finally:
        db.close()

if __name__ == "__main__":
    test_withdrawal_logic()
