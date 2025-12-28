from repository_infrastructure_example.containers.repositories import Repositories
from repository_infrastructure_example.services.organisation import OrganisationService
from repository_infrastructure_example.services.user import UserService


class Services:
    _repositories: Repositories

    def __init__(self, repositories: Repositories):
        self._repositories = repositories

    @property
    def organisation(self) -> OrganisationService:
        return OrganisationService(self._repositories.organisation)

    @property
    def user(self) -> UserService:
        return UserService(
            organisation_service=self.organisation,
            user_repository=self._repositories.user,
        )
