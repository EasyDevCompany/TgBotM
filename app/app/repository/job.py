from .base import RepositoryBase
from app.models.job_application import JobApplication


class RepositoryJobApplication(RepositoryBase[JobApplication]):
    pass
