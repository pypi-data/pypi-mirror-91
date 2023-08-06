from ..production import *

{% include "discovery/apps/settings/partials/common.py" %}

# The following urls should be accessible from the outside by a discovery web user in
# order to use the /login endpoint
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = SOCIAL_AUTH_EDX_OIDC_URL_ROOT
SOCIAL_AUTH_EDX_OIDC_KEY = "{{ DISCOVERY_OAUTH2_KEY }}"

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
