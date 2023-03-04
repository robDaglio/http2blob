# --------------------------------------------------------------------------------------
# Application Name: http2blob
# Author: Rob Daglio
# Contact: saasteam@kitchenbrains.com
# Application Description: This application exposes an HTTP endpoint which will forward
# a posted JSON payload to an Azure Storage Blob container defined within it's configuration.
# --------------------------------------------------------------------------------------

import json
import sys
import uvicorn
from logger.logger import Logger
from config import parser
from fastapi import FastAPI


cfg = parser.parse_known_args()[0]
log = Logger(
    name=__name__,
    log_to_file=True,
    log_level=cfg.log_level,
    log_file_name=cfg.log_file,
).get_logger()


def read_version_properties(properties_file: str) -> str:
    try:
        with open(properties_file, 'r') as f:
            version = f.read()
            return version.split('=')[-1] if '=' in version else version
    except (FileNotFoundError, IOError) as e:
        log.exception(f'Unable to read properties file:\n{e}')
        return 'na'


if __name__ == '__main__':
    log.info(f'HTTP2Blob Service version: {read_version_properties("version.properties")}')
    log.debug(f'Configuration: {json.dumps(vars(cfg), indent=4)}')

    try:
        from endpoints import router

        app = FastAPI()
        app.include_router(router)


        uvicorn.run(
            app,
            host='0.0.0.0',
            port=8084,
            log_config=None
        )
    except KeyboardInterrupt:
        log.info('Process interrupted by the user. Exiting.')
        sys.exit(0)