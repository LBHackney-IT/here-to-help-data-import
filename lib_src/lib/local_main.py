from lib_src.lib.main import self_isolation_lambda_handler
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    self_isolation_lambda_handler('event', 'context')
