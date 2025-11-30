from django.http import StreamingHttpResponse
# libs
# local


class CustomStreamingHttpResponse(StreamingHttpResponse):
    """
    A custom StreamingHttpResponse class with pre-defined headers
    to prevent client-side caching and disable buffering in proxies.
    """

    def __init__(self, streaming_content=(), *args, **kwargs):
        super().__init__(streaming_content, *args, **kwargs)

        self['Cache-Control'] = 'no-cache'
        self['X-Accel-Buffering'] = 'no'
