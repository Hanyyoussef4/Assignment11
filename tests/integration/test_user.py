# ======================================================================================
# tests/integration/test_user.py
# ======================================================================================
# Purpose: Demonstrate user model interactions with the database using pytest fixtures.
#          Relies on 'conftest.py' for database session management and test isolation.
# ======================================================================================

import pytest
import logging
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.user import User
from tests.conftest import create_fake_user, managed_db_session

# Use the logger configured in conftest.py
logger = logging.getLogger(__name__)

# ======================================================================================
# Basic Connection & Session Tests
# ======================================================================================

def test_database_connection(db_session):
    """
    Verify that the database connection is working.
    
    Uses the db_session fixture from conftest.py, which truncates tables after each test.
    """
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    logger.info("Database connection test passed")


def test_managed_session():
    """
    Test the managed_db_session context manager for one-off queries and rollbacks.
    Demonstrates how a manual session context can work alongside the fixture-based approach.
    """
    with managed_db_session() as session:
        # Simple query
        session.execute(text("SELECT 1"))
        
        # Generate an error to trigger rollback
        try:
            session.execute(text("SELECT * FROM nonexistent_table"))
        except Exception as e:
            assert "nonexistent_table" in str(e)

# ======================================================================================
# Session Handling & Partial Commits
# ======================================================================================

def test_session_handling(db_session):
    """
    Demonstrate partial commits:
      - user1 is committed
      - user2 fails (duplicate email), triggers rollback, user1 remains
      - user3 is committed
      - final check ensures we only have user1 and user3
    """
    initial_count = db_session.query(User).count()
    logger.info(f"Initial user count before test_session_handling: {initial_count}")
    assert initial_count == 0, f"Expected 0 users before test, found {initial_count}"
    
    user1 = User(
        first_name="Test",
        last_name="User",
        email="test1@example.com",
        username="testuser1",
        password="password123"
    )
    db_session.add(user1)
    db_session.commit()
    logger.info(f"Added user1: {user1.email}")
    
    current_count = db_session.query(User).count()
    logger.info(f"User count after adding user1: {current_count}")
    assert current_count == 1, f"Expected 1 user after adding user1, found {current_count}"
    
    try:
        user2 = User(
            first_name="Test",
            last_name="User",
            email="test1@example.com",  # Duplicate
            username="testuser2",
            password="password456"
        )
        db_session.add(user2)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        logger.info("IntegrityError caught and rolled back for user2.")
    
    found_user1 = db_session.query(User).filter_by(email="test1@example.com").first()
    assert found_user1 is not None, "User1 should still exist after rollback"
    assert found_user1.username == "testuser1"
    logger.info(f"Found user1 after rollback: {found_user1.email}")
    
    user3 = User(
        first_name="Test",
        last_name="User",
        email="test3@example.com",
        username="testuser3",
        password="password789"
    )
    db_session.add(user3)
    db_session.commit()
    logger.info(f"Added user3: {user3.email}")
    
    users = db_session.query(User).order_by(User.email).all()
    current_count = len(users)
    emails = {user.email for user in users}
    logger.info(f"Final user count: {current_count}, Emails: {emails}")
    
    assert current_count == 2, f"Should have exactly user1 and user3, found {current_count}"
    assert "test1@example.com" in emails, "User1 must remain"
    assert "test3@example.com" in emails, "User3 must exist"



# ======================================================================================
# User Creation Tests
# ======================================================================================

def test_create_user_with_faker(db_session):
    """
    Create a single user using Faker-generated data and verify it was saved.
    """
    user_data = create_fake_user()
    logger.info(f"Creating user with data: {user_data}")
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # Refresh populates fields like user.id
    
    assert user.id is not None
    assert user.email == user_data["email"]
    logger.info(f"Successfully created user with ID: {user.id}")


def test_create_multiple_users(db_session):
    """
    Create multiple users in a loop and verify they are all saved.
    """
    users = []
    for _ in range(3):
        user_data = create_fake_user()
        user = User(**user_data)
        users.append(user)
        db_session.add(user)
    
    db_session.commit()
    assert len(users) == 3
    logger.info(f"Successfully created {len(users)} users")

# ======================================================================================
# Query Tests
# ======================================================================================

def test_query_methods(db_session, seed_users):
    """
    Illustrate various query methods using seeded users.
    
    - Counting all users
    - Filtering by email
    - Ordering by email
    """
    user_count = db_session.query(User).count()
    assert user_count >= len(seed_users), "The user table should have at least the seeded users"
    
    first_user = seed_users[0]
    found = db_session.query(User).filter_by(email=first_user.email).first()
    assert found is not None, "Should find the seeded user by email"
    
    users_by_email = db_session.query(User).order_by(User.email).all()
    assert len(users_by_email) >= len(seed_users), "Query should return at least the seeded users"

# ======================================================================================
# Transaction / Rollback Tests
# ======================================================================================

def test_transaction_rollback(db_session):
    """
    Demonstrate how a partial transaction fails and triggers rollback.
    - We add a user and force an error
    - We catch the error and rollback
    - Verify the user was not committed
    """
    initial_count = db_session.query(User).count()
    
    try:
        user_data = create_fake_user()
        user = User(**user_data)
        db_session.add(user)
        # Force an error to trigger rollback
        db_session.execute(text("SELECT * FROM nonexistent_table"))
        db_session.commit()
    except Exception:
        db_session.rollback()
    
    final_count = db_session.query(User).count()
    assert final_count == initial_count, "The new user should not have been committed"

# ======================================================================================
# Update Tests
# ======================================================================================

def test_update_with_refresh(db_session, test_user):
    """
    Update a user's email and refresh the session to see updated fields.
    """
    original_email = test_user.email
    original_update_time = test_user.updated_at
    
    new_email = f"new_{original_email}"
    test_user.email = new_email
    db_session.commit()
    db_session.refresh(test_user)  # Refresh to populate any updated_at or other fields
    
    assert test_user.email == new_email, "Email should have been updated"
    assert test_user.updated_at > original_update_time, "Updated time should be newer"
    logger.info(f"Successfully updated user {test_user.id}")

# ======================================================================================
# Bulk Operation Tests
# ======================================================================================

@pytest.mark.slow
def test_bulk_operations(db_session):
    """
    Test bulk inserting multiple users at once (marked slow).
    Use --run-slow to enable this test.
    """
    users_data = [create_fake_user() for _ in range(10)]
    users = [User(**data) for data in users_data]
    db_session.bulk_save_objects(users)
    db_session.commit()
    
    count = db_session.query(User).count()
    assert count >= 10, "At least 10 users should now be in the database"
    logger.info(f"Successfully performed bulk operation with {len(users)} users")

# ======================================================================================
# Uniqueness Constraint Tests
# ======================================================================================

def test_unique_email_constraint(db_session):
    """
    Create two users with the same email and expect an IntegrityError.
    """
    first_user_data = create_fake_user()
    first_user = User(**first_user_data)
    db_session.add(first_user)
    db_session.commit()
    
    second_user_data = create_fake_user()
    second_user_data["email"] = first_user_data["email"]  # Force a duplicate email
    second_user = User(**second_user_data)
    db_session.add(second_user)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_unique_username_constraint(db_session):
    """
    Create two users with the same username and expect an IntegrityError.
    """
    first_user_data = create_fake_user()
    first_user = User(**first_user_data)
    db_session.add(first_user)
    db_session.commit()
    
    second_user_data = create_fake_user()
    second_user_data["username"] = first_user_data["username"]  # Force a duplicate username
    second_user = User(**second_user_data)
    db_session.add(second_user)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

# ======================================================================================
# Persistence after Constraint Violation
# ======================================================================================

def test_user_persistence_after_constraint(db_session):
    """
    - Create and commit a valid user
    - Attempt to create a duplicate user (same email) -> fails
    - Confirm the original user still exists
    """
    initial_user_data = {
        "first_name": "First",
        "last_name": "User",
        "email": "first@example.com",
        "username": "firstuser",
        "password": "password123"
    }
    initial_user = User(**initial_user_data)
    db_session.add(initial_user)
    db_session.commit()
    saved_id = initial_user.id
    
    try:
        duplicate_user = User(
            first_name="Second",
            last_name="User",
            email="first@example.com",  # Duplicate
            username="seconduser",
            password="password456"
        )
        db_session.add(duplicate_user)
        db_session.commit()
        assert False, "Should have raised IntegrityError"
    except IntegrityError:
        db_session.rollback()
    
    found_user = db_session.query(User).filter_by(id=saved_id).first()
    assert found_user is not None, "Original user should exist"
    assert found_user.id == saved_id, "Should find original user by ID"
    assert found_user.email == "first@example.com", "Email should be unchanged"
    assert found_user.username == "firstuser", "Username should be unchanged"

# ======================================================================================
# Error Handling Test
# ======================================================================================

def test_error_handling():
    """
    Verify that a manual managed_db_session can capture and log invalid SQL errors.
    """
    with pytest.raises(Exception) as exc_info:
        with managed_db_session() as session:
            session.execute(text("INVALID SQL"))
    assert "INVALID SQL" in str(exc_info.value)

