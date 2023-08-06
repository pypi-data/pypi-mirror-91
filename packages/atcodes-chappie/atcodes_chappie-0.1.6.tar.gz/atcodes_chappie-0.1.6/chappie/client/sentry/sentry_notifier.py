""" Error reporting """
import os, json


from sentry_sdk import capture_message


class SentryNotifier():
    """
        import sys
        from .utils import SentryNotifier
        # To report non exception Messages, use the following code
        SentryNotifier.publish_message('message', e)
        # To report Exception, use the following code
        try:
            # DO something
        except Exception as e:
            # sentry
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            SentryNotifier.publish_exception(sys.exc_info(), e)
    """

    def publish_exception(cls, exception_info, e, level='info', extra_args={}):    # pragma: no cover
        """ Publish exception details"""
        (exc_type, exc_obj, exc_tb) = exception_info

        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        message = {
            'Error': str(exc_type),
            'Source File': str(fname),
            'Line Number': str(exc_tb.tb_lineno),
            'Details': str(e)
        }

        for index, value in extra_args.items():
            message[index] = str(value)

        if os.environ.get('ENV') != 'local':
            capture_message(json.dumps(message))
        else:
            print(message)

        return True

    def publish_message(cls, message, level='info', extra_args={}):
        """ Send a simple message to sentry """
        message = {
            'message': message
        }
        message.update(extra_args)
        if os.environ.get('ENV') != 'local':
            capture_message(json.dumps(message))
        else:
            print(message)

        return True
