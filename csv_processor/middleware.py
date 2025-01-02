from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
import time

class RateLimitMiddleware(MiddlewareMixin):
    RATE_LIMIT = 100  # Maximum requests allowed
    TIME_WINDOW = 300  # 5 minutes in seconds

    def get_client_ip(self, request):
        """Extract the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        """Handle the rate-limiting logic."""
        client_ip = self.get_client_ip(request)
        current_time = time.time()

        # Generate a cache key for the client IP
        cache_key = f"rate_limit:{client_ip}"
        request_data = cache.get(cache_key, [])

        # Filter out timestamps outside the time window
        request_data = [timestamp for timestamp in request_data if current_time - timestamp < self.TIME_WINDOW]

        if len(request_data) >= self.RATE_LIMIT:
            # Block the request if the rate limit is exceeded
            return JsonResponse(
                {"error": "Too many requests. Please try again later."},
                status=429,
                headers={"Retry-After": str(self.TIME_WINDOW)}
            )

        # Add the current request timestamp
        request_data.append(current_time)
        cache.set(cache_key, request_data, timeout=self.TIME_WINDOW)

        # Add remaining requests to the response header
        request.remaining_requests = self.RATE_LIMIT - len(request_data)

    def process_response(self, request, response):
        """Add rate-limiting headers to the response."""
        if hasattr(request, 'remaining_requests'):
            response['X-RateLimit-Limit'] = self.RATE_LIMIT
            response['X-RateLimit-Remaining'] = request.remaining_requests
        return response
