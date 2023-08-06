'`matflow_demo_extension.__init__.py`'

from functools import partial

from matflow_demo_extension._version import __version__

from matflow.extensions import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
)

SOFTWARE = 'dummy_software'

input_mapper = partial(input_mapper, software=SOFTWARE)
output_mapper = partial(output_mapper, software=SOFTWARE)
cli_format_mapper = partial(cli_format_mapper, software=SOFTWARE)
register_output_file = partial(register_output_file, software=SOFTWARE)
software_versions = partial(software_versions, software=SOFTWARE)

# This import must come after assigning the partial functions:
from matflow_demo_extension import main
