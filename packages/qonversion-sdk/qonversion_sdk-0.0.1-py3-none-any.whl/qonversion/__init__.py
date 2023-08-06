# Qonversion Python bindings
# API docs at https://documentation.qonversion.io/reference
# Authors:
# Ilya Solovev <ilya@qonversion.io>

# Configuration variables

api_key = None
api_base = "https://api.qonversion.io/"
max_network_retries = 3

# Set to either 'debug' or 'info', controls console logging
log = None

# API resources
from qonversion.api_resources import User  # noqa
from qonversion.api_resources import Entitlement  # noqa
from qonversion.api_resources import Purchase  # noqa
from qonversion.api_resources import Product  # noqa
from qonversion.api_resources import Subscription  # noqa
from qonversion.api_resources import Identity  # noqa
