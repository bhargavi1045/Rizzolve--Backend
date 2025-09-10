from app.db import SessionLocal, Base, engine
from app import models, schemas


def main():
    print("Resetting DB...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    new_user = models.User(
        name="Test User",
        email="test@example.com",
        role="student",
        hashed_password="not_hashed_password"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("User created:", new_user.id, new_user.email)

    user_schema = schemas.UserOut.model_validate(new_user)
    print("Pydantic Schema:", user_schema.model_dump_json())

    db.close()


if __name__ == "__main__":
    main()
