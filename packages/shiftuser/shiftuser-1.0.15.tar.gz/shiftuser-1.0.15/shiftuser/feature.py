import os
from flask import session, current_app, abort
from jinja2 import ChoiceLoader, FileSystemLoader
from flask_login import current_user
from flask_principal import identity_loaded
from flask_principal import Identity
from flask_principal import AnonymousIdentity
import logging

from shiftuser import exceptions as x
from shiftuser.session_interface import SessionInterface
from shiftuser.services import login_manager, oauth, principal
from shiftuser.services import user_service
from shiftuser.util.oauth_providers import OauthProviders


def user_feature(app):
    """
    Add user feature
    Allows to register users and assign groups, instantiates flask login,
    flask principal and oauth integration
    """

    # check we have jwt secret configures
    if not app.config.get('USER_JWT_SECRET', None):
        raise x.JwtSecretMissing('Please set USER_JWT_SECRET in config')

    # set path to default user templates
    if not isinstance(app.jinja_loader, ChoiceLoader):
        app.jinja_loader = ChoiceLoader([app.jinja_loader])
    user_templates = os.path.realpath(os.path.dirname(__file__) + '/templates')
    app.jinja_loader.loaders.append(FileSystemLoader([user_templates]))

    # use custom session interface
    app.session_interface = SessionInterface()

    # init user service
    user_service.init(app)

    # init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(id):
        return user_service.get(id)

    # init OAuth
    oauth.init_app(app)
    registry = OauthProviders(app)
    providers = registry.get_providers()
    with app.app_context():
        for provider in providers:
            if provider not in oauth.remote_apps:
                oauth.remote_app(provider, **providers[provider])
                registry.register_token_getter(provider)

    # init principal
    principal.init_app(app)

    @principal.identity_loader
    def load_identity():
        if current_user.is_authenticated:
            return Identity(current_user.id)
        session.pop('identity.name', None)
        session.pop('identity.auth_type', None)
        return AnonymousIdentity()

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if not current_user.is_authenticated:
            return

        # add needs provided by the user
        for need in current_user.provide_principal_needs():
            identity.provides.add(need)


def enable_request_loader():
    """
    Enable request loader
    Optional user loader based on incomin request object. This is useful to
    enable on top of default user loader if you want to authenticate API
    requests via bearer token header.
    :return:
    """
    @login_manager.request_loader
    def load_user_from_request(request):
        user = None
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Bearer'):
            try:
                token = auth[7:]
                user = user_service.get_user_by_token(token)
            except x.UserException as exception:
                msg = 'JWT token login failed for [{ip}] with message: [{msg}]'
                msg = msg.format(
                    ip=request.environ['REMOTE_ADDR'],
                    msg=str(exception)
                )
                current_app.logger.log(msg=msg, level=logging.INFO)
                abort(401, description=str(exception))

        return user