"""Error handling functions."""

__all__ = ['dispatch_error', 'dispatch_error_adaptor', 'try_call',
   'run_with_errors', 'default', 'register_handler', 'FailsafeSchema',
   'dispatch_failsafe', 'error_handler', 'exception_handler']

import logging
from inspect import getargspec
from itertools import islice
import sys

import cherrypy
# from peak.rules import abstract, when, around, NoApplicableMethods

from turbogears.util import (inject_args, adapt_call, call_on_stack, has_arg,
    remove_keys, Enum)


log = logging.getLogger(__name__)


# @abstract()
def dispatch_error(controller, tg_source,
        tg_errors, tg_exceptions, *args, **kw):
    """Dispatch error.

    Error handler is a function registered via register_handler or if no
    such decorator was applied, the method triggering the error.

    """

    handler = getattr(tg_source, '_tg_error_handler', None)

    if handler:
        return handler(controller, tg_source, tg_errors, tg_exceptions, *args, **kw)
    if has_arg(tg_source, 'tg_errors'):
        return dispatch_error_adaptor(tg_source)(controller, tg_source, tg_errors, tg_exceptions, *args, **kw)
    else:
        raise NotImplementedError(f'Method {tg_source.__qualname__}() has no '
                                  'applicable error handler.')


# for easier usage and backward compatibility:
# dispatch_error.when = when.__get__(dispatch_error)
# dispatch_error.around = around.__get__(dispatch_error)

# @when(dispatch_error, "tg_errors and has_arg(tg_source, 'tg_errors')")
def _register_implicit_errh(controller, tg_source,
        tg_errors, tg_exceptions, *args, **kw):
    """Register implicitly declared error handler and re-dispatch.

    Any method declaring tg_errors parameter is considered an implicitly
    declared error handler.

    """
    error_handler(tg_source)(tg_source)
    return dispatch_error(controller, tg_source,
        tg_errors, tg_exceptions, *args, **kw)

# @when(dispatch_error, "tg_exceptions and has_arg(tg_source, 'tg_exceptions')")
def _register_implicit_exch(controller, tg_source,
        tg_errors, tg_exceptions, *args, **kw):
    """Register implicitly declared exception handler and re-dispatch.

    Any method declaring tg_exceptions parameter is considered an
    implicitly declared exception handler.

    """
    exception_handler(tg_source)(tg_source)
    return dispatch_error(controller, tg_source,
        tg_errors, tg_exceptions, *args, **kw)

def dispatch_error_adaptor(func):
    """Construct a signature isomorphic to dispatch_error.

    The actual handler will receive only arguments explicitly
    declared, and a possible tg_format parameter.

    """
    def adaptor(controller, tg_source,
            tg_errors, tg_exceptions, *args, **kw):
        tg_format = kw.pop('tg_format', None)
        args, kw = inject_args(func, {'tg_source': tg_source,
            'tg_errors': tg_errors, 'tg_exceptions': tg_exceptions},
                args, kw, 1)
        args, kw = adapt_call(func, args, kw, 1)
        if tg_format is not None:
            kw['tg_format'] = tg_format
        return func(controller, *args, **kw)
    return adaptor

def try_call(func, self, *args, **kw):
    """Call function, catch and dispatch any resulting exception."""

    # turbogears.database import here to avoid circular imports
    from turbogears.database import restart_transaction

    try:
        return func(self, *args, **kw)
    except TypeError as e:
        # cribbed from cherrypy._cpdispatch; see explanation in
        # test_callable_spec.__doc__
        try:
            cherrypy._cpdispatch.test_callable_spec(func, args, kw)
        except cherrypy.HTTPError:
            raise sys.exc_info()[1]
        except Exception:
            log.exception('Could not extract call failure reason for %s', func)

            raise e
        raise
    except Exception as e:
        if (isinstance(e, (cherrypy.HTTPRedirect, cherrypy.InternalRedirect, cherrypy.HTTPError))
                or call_on_stack('dispatch_error',
                    {'tg_source': func, 'tg_exception': e}, 4)):
            raise
        else:
            remove_keys(kw, ('tg_source', 'tg_errors', 'tg_exceptions'))

            if 'tg_format' in cherrypy.request.params:
                kw['tg_format'] = 'json'

            if getattr(cherrypy.request, 'in_transaction', None):
                restart_transaction(1)

            try:
                return dispatch_error(self, func, None, e, *args, **kw)
            except NotImplementedError:
                log.exception('Handler %s has no defined error handler', func)

                raise e


def run_with_errors(errors, func, self, *args, **kw):
    """Branch execution depending on presence of errors."""
    if errors:
        if hasattr(self, 'validation_error'):
            import warnings
            warnings.warn(
                "Use decorator error_handler() on per-method base "
                "rather than defining a validation_error() method.",
                DeprecationWarning, 2)
            return self.validation_error(func.__name__, kw, errors)
        else:
            remove_keys(kw, ('tg_source', 'tg_errors', 'tg_exceptions'))
            if 'tg_format' in cherrypy.request.params:
                kw['tg_format'] = 'json'

            return dispatch_error(self, func, errors, None, *args, **kw)
    else:
        return func(self, *args, **kw)

def register_handler(handler=None, rules=None):
    """Register handler as an error handler for decorated method.

    If handler is not given, method is considered its own error handler.

    rules can be a string containing an arbitrary logical Python expression
    to be used as dispatch rule allowing multiple error handlers for a
    single method.

    register_handler decorator is an invariant.

    """
    def register(func):
        new_rules = "id(tg_source) == %d" % id(func)
        if rules:
            new_rules += " and (%s)" % rules
        # FIXME: Py3K around(dispatch_error, new_rules)(
            # dispatch_error_adaptor(handler or func))
        return func
    return register

def bind_rules(pre_rules):
    """Prepend rules to error handler specialisation."""
    def registrant(handler=None, rules=None):
        new_rules = pre_rules
        if rules:
            new_rules += " and (%s)" % rules
        return register_handler(handler, new_rules)
    return registrant

# error_handler = bind_rules('tg_errors')
exception_handler = bind_rules('tg_exceptions')


def error_handler(handler):
    def attach_handler(fn):
        fn._tg_error_handler = handler

        return fn

    return attach_handler


FailsafeSchema = Enum('none', 'values', 'map_errors', 'defaults')

def dispatch_failsafe(schema, values, errors, source, kw):
    """Dispatch fail-safe mechanism for failed inputs."""
    return kw

# @when(dispatch_failsafe, "schema is FailsafeSchema.values"
    # " and isinstance(values, dict) and isinstance(errors, dict)")
def _failsafe_values_dict(schema, values, errors, source, kw):
    """Map erroneous inputs to values."""
    for key in errors:
        if key in values:
            kw[key] = values[key]
    return kw

# @when(dispatch_failsafe,
    # "schema is FailsafeSchema.values and isinstance(errors, dict)")
def _failsafe_values_atom(schema, values, errors, source, kw):
    """Map all erroneous inputs to a single value."""
    for key in errors:
        kw[key] = values
    return kw

# @when(dispatch_failsafe,
    # "schema is FailsafeSchema.map_errors and isinstance(errors, dict)")
def _failsafe_map_errors(schema, values, errors, source, kw):
    """Map erroneous inputs to corresponding exceptions."""
    kw.update(errors)
    return kw

# @when(dispatch_failsafe,
    # "schema is FailsafeSchema.defaults and isinstance(errors, dict)")
def _failsafe_defaults(schema, values, errors, source, kw):
    """Map erroneous inputs to method defaults."""
    argnames, defaultvals = getargspec(source)[::3]
    defaults = dict(zip(islice(
        argnames, len(argnames) - len(defaultvals), None), defaultvals))
    for key in errors:
        if key in defaults:
            kw[key] = defaults[key]
    return kw

