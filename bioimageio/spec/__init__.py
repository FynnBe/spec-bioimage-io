from . import v0_1, v0_3
from .build_spec import build_spec

# autogen: start
from bioimageio.spec.shared import fields
from . import nodes, raw_nodes, schema, utils
from .converters import maybe_convert_manifest, maybe_convert_model
from .raw_nodes import FormatVersion

fields = fields


get_nn_instance = utils.get_nn_instance
download_uri_to_local_path = utils.download_uri_to_local_path
load_raw_model = utils.load_raw_model
load_model = utils.load_model

# autogen: stop

# assuming schema will always be part of spec
from . import schema
from .raw_nodes import FormatVersion
__version__ = schema.get_args(FormatVersion)[-1]
