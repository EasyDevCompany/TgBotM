from app.models.application import Application
from .base import RepositoryBase
from sqlalchemy import or_


class ApplicationRepository(RepositoryBase[Application]):
    pass
    # def check_not_success(self, user_id: int):
    #     return self._session.query(self._model).filter(
    #         or_(
    #             self._model.application_status == Application.ApplicationStatus.pending,
    #             self._model.application_status == Application.ApplicationStatus.return_application,
    #             self._model.application_status == Application.ApplicationStatus.in_work,
    #         )).all()
