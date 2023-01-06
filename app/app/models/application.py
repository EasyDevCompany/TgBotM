import enum

from app.db.base_class import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship


class Application(Base):
    __tablename__ = "application"

    class Role(str, enum.Enum):
        accountant = "accountant"  # Бухгалтер
        storekeeper = "storekeeper"   # Кладовщик
        supervisor = "supervisor"  # Супервайзер
        foreman = "foreman"  # Прораб
        section_chief = "section_chief"  # Начальник участка
        curator = "curator"  # Куратор
        department_head = "department_head"  # Начальник отдела
        head_of_dec_department = "head_of_dec_department"  # Начальник управления ДИК
        supply_officer = "supply_officer"  # Сотрудник снабжения
        supply_pto = "supply_pto"  # Сотрудник ПТО
        account_approve = "account_approve"  # Утверждающий счета
        project_manager = "project_manager"  # Руководитель оотдела
        head_of_the_administrative_and_economic_department = "head_of_the_administrative_and_economic_department"
        # ачальник Административно Хозяйственного управления

    class RequestAnswered(str, enum.Enum):
        admin = "administrator"
        moderator = "moderator"

    class RequestType(str, enum.Enum):
        change_status_application = "change_status_application"  # смена статуса заявки
        conversion_factor = "conversion_factor"  # добавление коэффицента пересчета
        warehouse_adjustments = "warehouse adjustments"  # корректировки склада в заявке
        add_naming = "add_naming"  # добавление наименований
        edit_view_job = "edit_view_job"  # добавление видов работ
        add_view_job = "add_view_job"  # добавление видов работ
        edit_subobject = "edit_subobject"  # редактирование подобъектов
        editing_some_movement = "editing_some_movement"  # Редактирование некорректного перемещения
        add_subobject = "add_subobject"  # добавление подобъектов
        add_material = "add_material"  # Добавление материалов на свободный остаток
        add_edo = "add_edo"  # Добавление объекта в ЭДО
        open_edo = "open_edo"  # Открытие доступов Эдо для сотрудников
        edit_some_moving = "edit_some_moving"  # Редактирование некорректного перемещения
        adjustment_of_supplies = "adjustment_of_supplies"  # Корректировка поставок

    class ApplicationStatus(str, enum.Enum):
        pending = "pending"
        success = "success"
        return_application = "return_application"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("telegramuser.id"),
        index=True,
        nullable=True
    )
    date = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(Role))
    application_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.pending)
    request_answered = Column(Enum(RequestAnswered))
    request_type = Column(Enum(RequestType))
    field_one = Column(String(300))
    field_two = Column(String(300))
    field_three = Column(String(300))
    field_four = Column(String(300))
    field_five = Column(String(300), nullable=True)
    field_six = Column(String(300), nullable=True)
    field_seven = Column(String(300), nullable=True)
    field_eight = Column(String(300), nullable=True)
    field_nine = Column(String(300), nullable=True)
    user = relationship("TelegramUser")

    def repr(self) -> str:
        return f"{self.role}"