# View logger

View Logger is a decorators for Django views. It allows you to collect basic information about the user who made the request and about errors.

## Quick start

1. Add `view_logger` to your INSTALLED_APPS setting like this:
```
INSTALLED_APPS = [
        ...
        'view_logger',
    ]
```
2. Create empty dir `logs` in the root of your project

3. Create `logging` configuration. By default, `view_logger` uses `error_logger` and `info_logger`. These two loggers should be in the logging settings.

```
LOGGING = {
    'version': 1,
    'formatters': {
        ...
    },
    'handlers': {
        ...
    },
    'loggers': {
        'info_logger': {
            ...
        },
        'error_logger': {
            ...
        },
    },
}
```

4. Import from `view_logger` decorators: `log_wrapper` or `http_logger`

`log_wrapper` - Decorator for logging unhandled errors.

`http_logger` - Decorator for logging user`s information and unhandled errors.

## Extra tuning

You can specify additional keys in the settings for additional configuration.

`HTTP_ERROR_LOGGER` - you can set your custom logger name for using. Default is `error_logger`.

`HTTP_INFO_LOGGER` - you can set your custom logger name for using. Default is `info_logger`.

`USER_OBJECT` - for use other then django user object in request. Default is `user`.
If you want to change the object where the user data comes from, you must set user-like object in `request` object.
