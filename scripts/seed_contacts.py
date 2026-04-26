from sqlalchemy import select

from app.db.models import Base, Contact
from app.db.session import SessionLocal, engine


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.scalar(select(Contact.id).limit(1))
        if existing:
            print("Contacts already seeded.")
            return

        contacts = [
            Contact(email="artist1@example.com", artist_name="Artist One"),
            Contact(email="artist2@example.com", artist_name="Artist Two"),
            Contact(email="artist3@example.com", artist_name="Artist Three"),
        ]
        db.add_all(contacts)
        db.commit()
        print("Seeded sample contacts.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
