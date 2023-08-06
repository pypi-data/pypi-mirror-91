import logging

from citibox.profiling import Profiling, GoogleConfig, ProfilerServiceGoogle

from django.conf import settings

logger = logging.getLogger(__name__)


class ProfilingMiddleware:
    _started = False
    CONFIG = settings.PROFILING

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if not self._started and self.CONFIG.get('ACTIVE', False):
            self._start_profiler()
            self._started = True

        return response

    def _start_profiler(self):
        profiling_config = GoogleConfig(
            service_name=self.CONFIG['SERVICE_NAME'],
            service_version=self.CONFIG['SERVICE_VERSION'],
            project_id=self.CONFIG['PROJECT_ID'],
            service_account_json_file=self.CONFIG['SERVICE_ACCOUNT_JSON_FILE'],
        )
        profiling = Profiling(profiler_service=ProfilerServiceGoogle(config=profiling_config))
        profiling.start()
