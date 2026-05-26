from app.src.core.models.user import (
    UserDTO,
    UserInputModel,
    UserResponseModel,
    UserUpdateModel,
)
from app.src.infracstructure.db.models.user import Users


class UserMapper:
    @staticmethod
    def to_dto(user: UserInputModel) -> UserDTO:
        return UserDTO.from_input(user.username, user.email, user.password)

    @staticmethod
    def to_response(user: Users) -> UserResponseModel:
        return UserResponseModel.model_validate(user)

    @staticmethod
    def to_dict(user) -> dict:
        return user.model_dump()

    @staticmethod
    def update_to_dict(user: UserUpdateModel) -> dict:
        return user.model_dump(exclude_unset=True)
