from typing import Callable, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from fastapi import Request, status

from src.core.logging_config import logger

import time


class LoggingMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as e:
            elapsed_time = time.perf_counter() - start_time

            logger.exception(
                f"시스템 오류: {str(e)} | Time: {elapsed_time:.3f}s",
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status_code": 500,
                    "message": "죄송합니다. 알 수 없는 오류가 발생했습니다.",
                },
            )

        elapsed_time = time.perf_counter() - start_time
        if elapsed_time > 1.0:
            logger.warning(
                f"느린 응답 발견 | Took {elapsed_time:.3f}s for {request.method} {request.url.path}",
            )

        return response
