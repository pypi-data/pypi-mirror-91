import logging


def main():
    # logger creation and config
    logging.basicConfig(filename='bookcut.log', format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger
