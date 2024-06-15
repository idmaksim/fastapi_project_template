from repositories.user import UserRepository
from services.user import UserService


def users_service():
    return UserService(UserRepository)
