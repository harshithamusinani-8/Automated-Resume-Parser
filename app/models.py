
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(150), unique=True)
    password_hash = Column(String(255))
    role = Column(String(30))


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    raw_text = Column(Text)


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))

    name = Column(String(100))
    email = Column(String(150))
    phone = Column(String(50))

    education = Column(Text)
    experience = Column(Text)