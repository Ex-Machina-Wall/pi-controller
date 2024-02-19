from traceback import print_exc
import logging
from ex_wall_pi_controller.led_panel import Panel

logging.basicConfig(
    # filename='/home/pi/repos/ex-machina-wall/raspberry-pi-controller/log.txt',
    # filemode='a',
    format='%(asctime)s-[%(name)s] [%(levelname)s] | %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
    )

# handler = LogtailHandler(source_token=config("LOGTAIL_TOKEN"))
# handler.setLevel(logging.DEBUG)
# logger = logging.getLogger("")
# logger.addHandler(handler)

suppress_loggers = ["websockets.client", "urllib3.connectionpool"]

for logger in suppress_loggers:
    logging.getLogger(logger).setLevel(logging.CRITICAL)  # propagate = False


def main():
    logging.info("Starting Program..")
    panel = Panel() 
    try:
        panel.run()
    except Exception as e:
        logging.error(e)
        print_exc()
        panel.power_down()


if __name__ == "__main__":
    main()
