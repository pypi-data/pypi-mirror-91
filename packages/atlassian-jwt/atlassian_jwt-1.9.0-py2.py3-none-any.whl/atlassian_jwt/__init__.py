"""JSON Web Token (JWT) encoding and decoding library for Python 2 and 3.
Extends pyjwt to include Atlassian's custom query string hash (qsh) claim.
"""

from .encode import encode_token
from .authenticate import Authenticator, DecodeError
