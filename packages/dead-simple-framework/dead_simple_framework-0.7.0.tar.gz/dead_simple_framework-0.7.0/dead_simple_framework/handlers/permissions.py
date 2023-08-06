''' Builtin handler for routes with permissions '''

# Clients
import os

# Base class
from .default import DefaultRouteHandler, RouteHandler

# Helper method
from ..api import JsonResponse

# Settings
from ..config import App_Settings



# Typing
from typing import Callable, Union


class Permissions:
    ''' Class that stores allowed permissions for each method '''

    DEFAULT_PERMISSIONS_LIST = os.environ.get('DEFAULT_PERMISSIONS_LIST', ['ADMIN', 'USER']) # TODO - Move to Config

    def __init__(self, GET:list=None, POST:list=None, DELETE:list=None, PUT:list=None, PATCH:list=None, OPTIONS:list=None):
        self.GET = GET
        self.POST = POST
        self.DELETE = DELETE
        self.PUT = PUT
        self.PATCH = PATCH
        self.OPTIONS = OPTIONS


class PermissionsRouteHandler(RouteHandler):
    ''' Route that only allows access for specific user permissions '''

    PERMISSIONS = None

    @staticmethod
    def hasPermission(current_user:dict, method_permissions:list) -> bool:
        ''' Checks if the current user has permission to access the resource '''

        if not current_user or not current_user.get('permissions'): 
            return False
        if 'ADMIN' in current_user.get('permissions'): 
            return True # TODO - Dynamic admin
        if any(role in method_permissions for role in current_user.get('permissions')):
            return True

        return False


    def permission_verifier_decorator(self, verifier:Callable, permissions:Permissions):

        def verifier_wrapper(method, payload, identity):
            method_permissions = getattr(permissions, method, None)
            if isinstance(method_permissions, str):
                method_permissions = [method_permissions]
                
            if method_permissions and App_Settings.APP_USE_JWT:
                if identity and self.hasPermission(identity, method_permissions):
                    return verifier(method, payload, identity)
                return False
            return True

        return verifier_wrapper
    

    def __init__(self, permissions:Permissions, GET:Callable=None, POST:Callable=None, DELETE:Callable=None, PUT:Callable=None, PATCH:Callable=None, OPTIONS:Callable=None, verifier:Callable=None, schema:dict=None):
        self.permissions = permissions
        self.verifier = self.permission_verifier_decorator(verifier or self.verifier, permissions)

        super().__init__(GET=GET, POST=POST, DELETE=DELETE, PUT=PUT, PATCH=PATCH, OPTIONS=OPTIONS, schema=schema)



class DefaultPermissionsRouteHandler(PermissionsRouteHandler, DefaultRouteHandler):
    ''' Route that only allows access for specific user permissions '''

    def __init__(self, permissions:Permissions, GET:Callable=None, POST:Callable=None, DELETE:Callable=None, PUT:Callable=None, PATCH:Callable=None, OPTIONS:Callable=None, verifier:Callable=None, schema:dict=None):
        self.permissions = permissions
        self.verifier = self.permission_verifier_decorator(verifier or self.verifier, permissions)
        
        super(DefaultRouteHandler, self).__init__(GET=GET, POST=POST, DELETE=DELETE, PUT=PUT, PATCH=PATCH, OPTIONS=OPTIONS, schema=schema)
