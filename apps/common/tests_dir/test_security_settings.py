from django.conf import settings


def test_request_size_limit_is_configured():
    assert settings.DATA_UPLOAD_MAX_MEMORY_SIZE <= (
        2 * 1024 * 1024
    )


def test_file_upload_size_limit_is_configured():
    assert settings.FILE_UPLOAD_MAX_MEMORY_SIZE <= (
        2 * 1024 * 1024
    )