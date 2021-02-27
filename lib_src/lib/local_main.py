from lib_src.lib.main import lambda_handler, spl_lambda_handler

if __name__ == '__main__':

    thing = spl_lambda_handler('event', 'context')
    print('-  - - - - - - - ')
    print(thing)
    print('-  - - - - - - - ')
