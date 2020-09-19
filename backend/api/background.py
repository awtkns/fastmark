import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
broker = RabbitmqBroker(host=config.RABBITMQ_HOST, middleware=[CurrentMessage()])
dramatiq.set_broker(broker)


@dramatiq.actor
def identity(x):
    return x


@dramatiq.actor
def print_result(message_data, result):
    print(f"The result of message {message_data['message_id']} was {result}.")


if __name__ == '__main__':
    identity.send_with_options(args=(42,), on_success=print_result)
