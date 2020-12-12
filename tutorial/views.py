from pyramid.view import forbidden_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPSeeOther
from pyramid.security import NO_PERMISSION_REQUIRED, Everyone, remember, authenticated_userid, unauthenticated_userid

# from .oauth import OAuth
from .utils import redirect_path
from pyramid.view import (
    view_config,

    )
import requests
import logging
import json

log = logging.getLogger(__name__)

@view_config(route_name='login')
def login(request):

    print('login **** start')

    sm_user = request.headers.get('sm_user')
    userid = request.cookies.get('userid')

    print('sm_user - {0}'.format(sm_user))
    print('userid - {0}'.format(userid))

    if not sm_user and not userid:
        return HTTPFound(request.route_url('callback'))

    login_url = request.route_url('login')

    redirect_to = redirect_path(request)

    response = Response(json.dumps({'note': 'testing'}))
    return response


@view_config(route_name='callback')
def callback(request):

    log.debug('********* callback **********')
    print_requests(request)

    code = request.params.get('code')

    # userid, name = OAuth(code).get_user_info()
    userid ='lak'
    name = 'test'
    headers = remember(request, userid)
    login_url = request.route_url('login')
    print('login_url - ', login_url)

    response = HTTPSeeOther(location=login_url, headers=headers)
    response.set_cookie('name', name)
    response.set_cookie('userid', userid)

    return response


@view_config(route_name='resource_1', permission='edit')
# @view_config(route_name='resource_1')
def resource_1(request):
    print('u - ',unauthenticated_userid(request))
    print('a -', authenticated_userid(request))
    r = {'test': 'resource_1'}
    return Response(json.dumps(r))


@forbidden_view_config()
def resource_2(request):
    return Response('You are not allowed', status='403 Forbidden')

@view_config(route_name='mashup')
def mashup(request):
    print('mashup')

    r = {'Note': 'Undergoing test'}

    return Response(json.dumps(r))


def print_requests(request):
    pass
