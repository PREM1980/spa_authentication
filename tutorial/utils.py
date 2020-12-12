import marshmallow as ma
from urllib.parse import urlparse, urlsplit, parse_qs
from urllib.parse import urlencode, urlunsplit, urlsplit, parse_qs
import json

class PathSchema(ma.Schema):
    path = ma.fields.String(required=True)

    class Meta:
        unknown = ma.EXCLUDE

    @ma.validates('path')
    def validate_path(self, path):
        parsed_result = urlparse(path)
        if parsed_result.netloc or parsed_result.scheme:
            raise ma.ValidationError(
                "The path must not contain a scheme (protocol) or a netloc (host)"
            )
        return '?'.join([parsed_result.path, parsed_result.query])


def validate_redirect_path(path):
    """
    Validate redirect parameters making sure they are not pointing to an external URL.

    Raise ValidationError if invalid or None.
    """
    data = PathSchema().load({'path': path})
    redirect = data.get('path')
    return redirect


def add_path_params(path, params, doseq=True, **kwargs):
    """
    Add GET params to provided path.

    Args:
        path (str): string of target path
        params: dict containing requested params to be added
            or iterable of (key, value) pairs. Passing an iterable
            guarantees the order of the query parameters in the URL.
            This function is compatible with multiple query string keys with the same name.
        doseq (bool): Optional. Passed verbatim to :func:`urlencode`. Exposed here because
            it changes the default value: In :func:`urlencode`, `doseq` is by default `False`,
            here, by the contrary, is by default `True`.
        **kwargs: Additional keyword arguments to be passed verbatim to :func:`urlencode`.

    Return:
        Updated path string
    """
    # The path url may already contain params
    base = urlsplit(path)
    if base.query:
        params.update(parse_qs(base.query))
    qs = urlencode(params, doseq=doseq, **kwargs)
    return urlunsplit((base.scheme, base.netloc, base.path, qs, base.fragment))


def redirect_path(request):
    """Return the relevant redirect path/url."""
    # If we have an explicit redirect query param, use that. Else, get the origin query parameter
    # that the FE gives us through the Login link.
    # Note that redirect is path and origin a full URI.
    uri = request.params.get('redirect') or request.params.get('origin')

    if uri:
        base = urlsplit(uri)
        path = add_path_params(base.path or '/', parse_qs(base.query))
        validate_redirect_path(path)
        return path

    return request.route_path('login')