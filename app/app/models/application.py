# -*- coding: utf-8 -*-

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
        accountant = "Бухгалтер"  # Бухгалтер
        storekeeper = "Кладовщик"   # Кладовщик
        supervisor = "Супервайзер"  # Супервайзер
        foreman = "Прораб"  # Прораб
        section_chief = "Начальник участка"  # Начальник участка
        curator = "Куратор"  # Куратор
        department_head = "Начальник отдела"  # Начальник отдела
        head_of_dec_department = "Начальник управления"  # Начальник управления ДИК
        supply_officer = "Сотрудник снабжения"  # Сотрудник снабжения
        supply_pto = "Сотрудник ПТО"  # Сотрудник ПТО
        account_approve = "Утверждающий счета"  # Утверждающий счета
        project_manager = "Руководитель отдела"  # Руководитель оотдела
        head_of_the_administrative_and_economic_department = "Начальник Адм.Хоз Упр."
        # ачальник Административно Хозяйственного управления

    class RequestAnswered(str, enum.Enum):
        admin = "admin"
        moderator = "moderator"

    class RequestType(str, enum.Enum):
        change_status_application = "Смена статуса заявки"  # смена статуса заявки
        conversion_factor = "Добавление коэффицента пересчета"  # добавление коэффицента пересчета
        warehouse_adjustments = "Корректировки склада в заявке"  # корректировки склада в заявке
        add_naming = "Добавление наименований"  # добавление наименований
        edit_view_job = "Редактирование видов работ"  # добавление видов работ
        add_view_job = "Добавление видов работ"  # добавление видов работ
        edit_subobject = "Редактирование подобъектов"  # редактирование подобъектов
        adjustment_invoice = 'Корректировка оформленной накладной'  # Корректировка оформленной накладной
        add_subobject = "Добавление подобъектов"  # добавление подобъектов
        add_material = "Добавление материалов на свободный остаток"  # Добавление материалов на свободный остаток
        add_edo = "Добавление объекта в ЭДО"  # Добавление объекта в ЭДО
        open_edo = "Открытие доступов Эдо для сотрудников"  # Открытие доступов Эдо для сотрудников
        edit_some_moving = "Редактирование некорректного перемещения"  # Редактирование некорректного перемещения
        adjustment_of_supplies = "Корректировка поставок"  # Корректировка поставок

    class ApplicationStatus(str, enum.Enum):
        pending = "Ожидание взятия в работу"
        success = "Выполнен"
        return_application = "Запрос возвращен для корректировки"
        in_work = "Запрос в работе"

    id = Column(Integer, primary_key=True, index=True)
    sender_user_id = Column(
        Integer,
        ForeignKey("telegramuser.id"),
        nullable=True
    )
    recipient_user_id = Column(
        Integer,
        ForeignKey("telegramuser.id"),
        nullable=True
    )
    date = Column(DateTime, default=datetime.utcnow)
    name = Column(String(300))
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
    field_seven = Column(String(1000), nullable=True)
    field_eight = Column(String(300), nullable=True)
    field_nine = Column(String(300), nullable=True)
    sender_user = relationship('TelegramUser', foreign_keys=[sender_user_id])
    recipient_user = relationship("TelegramUser", foreign_keys=[recipient_user_id])

    def repr(self) -> str:
        return f"{self.role}"
