import json
import datetime
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Prepare log entry
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "method": request.method,
            "path": request.get_full_path(),
            "headers": {k: v for k, v in request.headers.items()},
            "GET_params": dict(request.GET),
            "POST_data": {},
        }

        # Try to decode body if present
        try:
            if request.body:
                log_data["POST_data"] = json.loads(request.body.decode("utf-8"))
        except Exception:
            log_data["POST_data"] = request.body.decode("utf-8", errors="ignore")

        # Write log to file
        with open("request_logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(log_data, indent=2))
            log_file.write("\n" + "="*80 + "\n")

        return None
