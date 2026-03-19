from http import HTTPStatus

from fastapi import HTTPException, Request


def get_access_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Access token not found"
        )

    return access_token
