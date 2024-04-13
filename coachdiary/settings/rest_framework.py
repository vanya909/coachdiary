REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'EXCEPTION_HANDLER': (
        'coachdiary.api.utils.exception_handler.custom_exception_handler'
    ),
}
