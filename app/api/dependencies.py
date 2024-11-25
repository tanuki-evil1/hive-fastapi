from typing import Annotated

DocsDEP = Annotated[UserService, Depends(get_service(UserService))]