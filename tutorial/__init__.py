from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from .security import groupfinder


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='.resources.Root')
    config.include('pyramid_chameleon')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('login', '/')
    config.add_route('callback', '/login/oauth2/code')
    config.add_route('resource_1', '/resource_1')
    config.add_route('resource_2', '/resource_2')
    config.add_route('mashup', '/mashup.html')

    config.scan('.views')
    return config.make_wsgi_app()