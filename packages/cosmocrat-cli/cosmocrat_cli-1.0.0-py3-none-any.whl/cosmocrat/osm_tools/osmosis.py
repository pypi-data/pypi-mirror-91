import os
import cosmocrat.definitions as definitions

from cosmocrat.helper_functions import deconstruct_file_path, get_compression_method, run_command_wrapper

SUBPROCESS_NAME='osmosis'

def clip_polygon(input_path, polygon_path, input_timestamp, base_output_path, exist_ok=False):
    (_, input_name, _, _) = deconstruct_file_path(input_path)
    (_, polygon_name, _, _) = deconstruct_file_path(polygon_path)

    output_format = definitions.FORMATS_MAP['OSM_PBF']
    output_name = f'{input_name}.{polygon_name}.{input_timestamp}.{output_format}'
    output_path = os.path.join(base_output_path, output_name)

    if not exist_ok or not os.path.isfile(output_path):
        run_command_wrapper(command=f'{definitions.OSMOSIS_PATH} \
                        --read-pbf-fast file={input_path} outPipe.0=1 \
                        --bounding-polygon file={polygon_path} \
                        completeWays=true completeRelations=true inPipe.0=1 outPipe.0=2 \
                        --write-pbf file={output_path} inPipe.0=2 \
                        -v',
                        subprocess_name=SUBPROCESS_NAME)
    return output_path

def apply_changes_by_polygon(base_output_path, input_path, change_path, polygon_path):
    (_, input_name, _, _) = deconstruct_file_path(input_path)
    (_, _, changes_timestamps, changes_format) = deconstruct_file_path(change_path)

    compression_type = definitions.COMPRESSION_METHOD_MAP[changes_format]

    output_format = definitions.FORMATS_MAP['OSM_PBF']
    output_path = os.path.join(base_output_path, f'{input_name}.{changes_timestamps}.{output_format}')

    run_command_wrapper(command=f'{definitions.OSMOSIS_PATH} \
                    --read-pbf-fast file={input_path} outPipe.0=1 \
                    --read-xml-change compressionMethod={compression_type} file={change_path} outPipe.0=2 \
                    --apply-change inPipe.0=1 inPipe.1=2 outPipe.0=3 \
                    --bounding-polygon file={polygon_path} inPipe.0=3 outPipe.0=4 \
                    --write-pbf file={output_path} inPipe.0=4 \
                    -v',
                    subprocess_name=SUBPROCESS_NAME)
    return output_path

def create_delta(delta_path, delta_name, first_input_pbf_path, second_input_pbf_path, should_compress=False):
    (compression_type, output_format) = get_compression_method(compression=should_compress, base_format=definitions.FORMATS_MAP['OSC'])
    output_name = f'{delta_name}.{output_format}'
    output_path = os.path.join(delta_path, output_name)
    run_command_wrapper(command=f'{definitions.OSMOSIS_PATH} \
                    --read-pbf-fast file={first_input_pbf_path} outPipe.0=1 \
                    --read-pbf-fast file={second_input_pbf_path} outPipe.0=2 \
                    --derive-change inPipe.0=1 inPipe.1=2 outPipe.0=3 \
                    --write-xml-change compressionMethod={compression_type} file={output_path} inPipe.0=3 \
                    -v',
                    subprocess_name=SUBPROCESS_NAME)
    return output_path