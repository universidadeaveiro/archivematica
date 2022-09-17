import os

OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID", "")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_RP_CLIENT_SECRET", "")

OIDC_OP_AUTHORIZATION_ENDPOINT = ""
OIDC_OP_TOKEN_ENDPOINT = ""
OIDC_OP_USER_ENDPOINT = ""
OIDC_OP_JWKS_ENDPOINT = ""

AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID", "")
if AZURE_TENANT_ID:
    OIDC_OP_AUTHORIZATION_ENDPOINT = (
        "https://login.microsoftonline.com/%s/oauth2/v2.0/authorize" % AZURE_TENANT_ID
    )
    OIDC_OP_TOKEN_ENDPOINT = (
        "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % AZURE_TENANT_ID
    )
    OIDC_OP_USER_ENDPOINT = (
        "https://login.microsoftonline.com/%s/openid/userinfo" % AZURE_TENANT_ID
    )
    OIDC_OP_JWKS_ENDPOINT = (
        "https://login.microsoftonline.com/%s/discovery/v2.0/keys" % AZURE_TENANT_ID
    )
else:
    OIDC_OP_AUTHORIZATION_ENDPOINT = os.environ["OIDC_OP_AUTHORIZATION_ENDPOINT"]
    OIDC_OP_TOKEN_ENDPOINT = os.environ["OIDC_OP_TOKEN_ENDPOINT"]
    OIDC_OP_USER_ENDPOINT = os.environ["OIDC_OP_USER_ENDPOINT"]
    OIDC_OP_JWKS_ENDPOINT = os.environ.get("OIDC_OP_JWKS_ENDPOINT", "")

OIDC_TOKEN_USE_BASIC_AUTH = True

OIDC_RP_SIGN_ALGO = os.environ.get("OIDC_RP_SIGN_ALGO", "HS256")

OIDC_RP_SCOPES="openid preferred_username middle_name formatted updated_at email upn sub nMecFunc studentNumber nickname given_name keplerNumber User_Roles locality gender UA_IUPI region family_name email_verified name profile locale phone_number_verified zoneinfo picture postal_code street_address website groups address phone_number birthdate country iss acr"
OIDC_RP_SCOPES="openid email profile phone address"

# Username is email address
OIDC_USERNAME_ALGO = lambda email: email  # noqa

# map attributes from access token
OIDC_ACCESS_ATTRIBUTE_MAP = {"given_name": "first_name", "family_name": "last_name"}

# map attributes from id token
OIDC_ID_ATTRIBUTE_MAP = {"email": "email"}
