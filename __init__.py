from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from .security import groupfinder


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('login', '/')
    # config.add_view(login, route_name='login')

    config.add_route('callback', '/login/oauth2/code/nih')
    # config.add_view(callback, route_name='callback')

    config.add_route('resource_1', '/resource_1')
    # config.add_view(resource_1, route_name='resource_1', permission='edit')
    # config.add_view(resource_1, route_name='resource_1', permission='')

    config.add_route('resource_2', '/resource_2')
    # config.add_view(resource_2, route_name='resource_2')

    config.add_route('mashup', '/mashup.html')
    # config.add_view(mashup, route_name='mashup')

    # config.add_route('home', '/')
    # config.add_route('hello', '/howdy')
    # config.add_route('login', '/login')
    # config.add_route('logout', '/logout')
    config.scan('.app')
    return config.make_wsgi_app()