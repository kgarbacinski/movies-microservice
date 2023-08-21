from src.core import config

keycloak_admin_config = dict(
    server_url=config.KEYCLOAK_SERVER_URL,
    username=config.KEYCLOAK_ADMIN_USER,
    password=config.KEYCLOAK_ADMIN_PASSWORD,
    client_id=config.KEYCLOAK_ADMIN_CLIENT_ID,
    realm_name=config.KEYCLOAK_REALM_NAME,
    client_secret_key=config.KEYCLOAK_ADMIN_CLIENT_SECRET_KEY,
    verify=True,
)

keycloak_openid_config = dict(
    server_url=config.KEYCLOAK_SERVER_URL,
    client_id=config.KEYCLOAK_OPENID_CLIENT_ID,
    realm_name=config.KEYCLOAK_REALM_NAME,
    client_secret_key=config.KEYCLOAK_OPENID_CLIENT_SECRET_KEY,
)
