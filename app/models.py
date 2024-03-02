from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base



class Role(Base):
    __tablename__= "role"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

class District(Base):
    __tablename__= "district"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

class Upazilla(Base):
    __tablename__= "upazilla"

    id = Column(Integer, primary_key=True, nullable=False)
    district = Column(String, ForeignKey("district.name", ondelete="CASCADE"), nullable=False, unique=False)
    name = Column(String, nullable=False, unique=True)


class Mouza(Base):
    __tablename__= "mouza"

    id = Column(Integer, primary_key=True, nullable=False)
    upazilla = Column(String, ForeignKey("upazilla.name", ondelete="CASCADE"), nullable=False, unique=False)
    name = Column(String, nullable=False, unique=True)

class Leasee(Base):
    __tablename__ = "leasee"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    f_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    district = Column(String, ForeignKey("district.name", ondelete="CASCADE"),
                              nullable=False, unique=False)
    upazilla = Column(String, ForeignKey("upazilla.name", ondelete="CASCADE"),
                              nullable=False, unique=False)
    remarks = Column(String, nullable=True)
    nid_number = Column(String, nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    alt_phone_number = Column(String, nullable=True)
    sex = Column(String, nullable=False)
    profile = Column(String, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class VPcase(Base):
    __tablename__ = "vpcase"

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String, nullable=False, unique=True)
    mouza = Column(String, ForeignKey("mouza.name", ondelete="CASCADE"),
                              nullable=False, unique=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class LSchedule(Base):
    __tablename__ = "lschedule"

    id = Column(Integer, primary_key=True, nullable=False)
    land_id =Column(Integer, nullable=False, unique=True)
    vpcase = Column(String, ForeignKey("vpcase.number", ondelete="CASCADE"),
                              nullable=False, unique=False)
    mutation_number_past = Column(String, nullable=False)
    plot_number_past = Column(String, nullable=False)
    mutation_number_new = Column(String, nullable=False)
    plot_number_new = Column(String, nullable=False)
    land_area = Column(Float, nullable=False)
    land_class = Column(String, nullable=False)
    is_shop = Column(Boolean, nullable=False, default=False)
    shop_sqf = Column(Float, nullable=False, default=0)
    renewed_upto = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Users(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, ForeignKey("role.name", ondelete="CASCADE"),
                              nullable=False, default=None, unique=False)


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, nullable=False)
    vpcase = Column(String, ForeignKey("vpcase.number", ondelete="CASCADE"), nullable=False, unique=False)
    leasee = Column(String, nullable=True)
    nid_number = Column(String, ForeignKey("leasee.nid_number", ondelete="CASCADE"),
                        nullable=False, unique=False)
    application_date = Column(Date, nullable=False)
    leasee_type = Column(String, nullable=False)
    applicant_type = Column(String, nullable=False)
    representative_name = Column(String, nullable=True)
    rep_phone_number = Column(String, nullable=True)
    user = Column(String, ForeignKey('users.role', ondelete="CASCADE"), nullable=False, unique=False)
    user_by = Column(String, ForeignKey('users.role', ondelete="CASCADE"), nullable=False, unique=False)
    application_status = Column(String, nullable=False)
    applied_for = Column(String, nullable=False)
    fee = Column(Integer, nullable=False)
    application_for = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, nullable=False)
    application_id = Column(Integer, ForeignKey("application.id", ondelete="CASCADE"), nullable=False, unique=False)
    vpcase = Column(String, ForeignKey("vpcase.number", ondelete="CASCADE"),
                    nullable=False, unique=False)
    execution_date = Column(Date, nullable=False)
    execution_type = Column(String, nullable=False)
    application_date = Column(Date, nullable=False) #application.application_date
    user = Column(String, ForeignKey('users.username', ondelete="CASCADE"), nullable=False, unique=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, nullable=False)
    application_id = Column(Integer, ForeignKey("application.id", ondelete="CASCADE"),
                            nullable=False, unique=False)
    order_no = Column(Integer, nullable=False)
    order_date = Column(Date, nullable=False)
    last_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)

    sent_from = Column(String, ForeignKey('users.username', ondelete="CASCADE"), nullable=False, unique=False)
    sent_to = Column(String, ForeignKey('users.username', ondelete="CASCADE"), nullable=False, unique=False)

    actions_taken = Column(String, nullable=True)

    sent_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, nullable=False)
    application_id = Column(Integer, ForeignKey("application.id", ondelete="CASCADE"),
                            nullable=False, unique=False)
    order_no = Column(Integer, nullable=False)

    report_no = Column(Integer, nullable=False)
    report_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    actions_taken = Column(String, nullable=True)

    sent_from = Column(String, ForeignKey('users.username', ondelete="CASCADE"), nullable=False, unique=False)
    sent_to = Column(String, ForeignKey('users.username', ondelete="CASCADE"), nullable=False, unique=False)

    sent_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class DCR(Base):
    __tablename__ = "dcr"

    id = Column(Integer, primary_key=True, nullable=False)
    application_id = Column(Integer, ForeignKey("application.id", ondelete="CASCADE"),
                            nullable=False, unique=True)
    dcr_date = Column(Date, nullable=False)
    signature_by = Column(String, nullable=True)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

