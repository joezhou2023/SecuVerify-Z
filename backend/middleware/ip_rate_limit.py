import datetime
import threading
from collections import defaultdict
from typing import Callable

from fastapi.responses import JSONResponse


class IPRateLimitMiddleware:
    """匿名按 IP 限流 + 自然日配额。

    FastAPI/Starlette 期望的中间件模式：
    - middleware 类实现 __call__(request, call_next)
    - 或者由 app.middleware("http") 闭包调用。

    - 限流：每分钟最多 requests_per_minute 次（超出返回 429）
    - 配额：自然日最多 requests_per_day 次（超出返回 403）

    注意：该实现是进程内内存版；多进程/多实例需要 Redis 版本。
    """

    def __init__(
        self,
        app,
        route_key_rules,
    ):
        self.app = app
        self.route_key_rules = route_key_rules
        

        self._lock = threading.Lock()

        # 每分钟计数：{ip: {minute_key: {route_key: count}}}
        self._minute_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # 每日配额计数：{ip: {day_key: {route_key: count}}}
        self._day_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    async def __call__(self, request, call_next: Callable):
        client_ip = self._get_client_ip(request)
        if not client_ip:
            return JSONResponse({"detail": "Forbidden"}, status_code=403)

        route_key = self._match_route_key(request.url.path)
        if not route_key:
            return await call_next(request)

        policy = self.route_key_rules[route_key]
        now = datetime.datetime.now()

        minute_key = f"{now.year:04d}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}"
        day_key = f"{now.year:04d}-{now.month:02d}-{now.day:02d}"

        with self._lock:
            minute_count = self._minute_counts[client_ip][minute_key][route_key]
            if minute_count >= policy["requests_per_minute"]:
                return JSONResponse({"detail": "Too Many Requests"}, status_code=429)

            day_count = self._day_counts[client_ip][day_key][route_key]
            if day_count >= policy["requests_per_day"]:
                return JSONResponse({"detail": "Forbidden"}, status_code=403)

            # 通过后再计数
            self._minute_counts[client_ip][minute_key][route_key] += 1
            self._day_counts[client_ip][day_key][route_key] += 1

        return await call_next(request)

    def _match_route_key(self, path: str):
        # 精确匹配到已知 API 前缀/路由
        # 例如：/api/chat、/api/file-audit/upload、/api/clause-match
        if path.startswith("/api/chat"):
            return "chat"
        if path.startswith("/api/file-audit/upload"):
            return "file_audit_upload"
        if path.startswith("/api/clause-match"):
            return "clause_match"
        return None

    def _get_client_ip(self, request):
        # 优先取 X-Forwarded-For（反代场景）
        xff = request.headers.get("x-forwarded-for")
        if xff:
            # 取最左边客户端 IP
            return xff.split(",")[0].strip()
        return request.client.host if request.client else None
