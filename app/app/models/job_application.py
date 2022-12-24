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


class JobApplication(Base):
    __tablename__ = "job_application"

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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("telegram_user.id"))
    user = relationship("TelegramUser")
    date = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(Role))
    request_answered = Column(Enum(RequestAnswered))
    request_type = Column(Enum(RequestType))
    field_one = Column(String)
    field_two = Column(String)
    field_four = Column(String)
    field_five = Column(String, nullable=True)
    six_field = Column(String, nullable=True)
    seven_field = Column(String, nullable=True)
    eight_field = Column(String, nullable=True)
    nine_field = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"{self.user_id} {self.role}"
