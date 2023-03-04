import configargparse

parser = configargparse.get_argument_parser(
    default_config_files=['config/defaults.ini'],
    description='Parameters for HTTP2Blob service.',
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter
)

parser.add_argument('--log-level', type=str, required=False, env_var='LOG_LEVEL',
                    default='INFO', help='The log level with which to run the application.')

parser.add_argument('--log-file', type=str, required=False, env_var='LOG_FILE',
                    default='app.log', help='The desired log file name.')

parser.add_argument('--listening-port', type=int, required=False, env_var='LISTENING_PORT',
                    default=8084, help='The default port to listen on.')

parser.add_argument('--connection-string', type=str, required=True, env_var='CONNECTION_STRING',
                    help='The Azure storage connection string.')

parser.add_argument('--container-name', type=str, required=True, env_var='CONTAINER_NAME',
                    help='The Azure container to upload data to.')

parser.add_argument('--api-user', type=str, required=True, env_var='API_USER',
                    help='The api username to authenticate against.')

parser.add_argument('--api-pass', type=str, required=True, env_var='API_PASS',
                    help='The api password for basic authentication.')


