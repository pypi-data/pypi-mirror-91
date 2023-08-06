=================================================
CenturyLink Cloud ManagedOS Python Utilities [1]_
=================================================

***************
Getting Started
***************

To install the ``clc_msa_utils`` package, use the command below.::

    pip3 install clc_msa_utils

*******
KVStore
*******

This is a utility class that abstracts loading a configuration from Consul or ETCD. This class supports perodically
reloading the configuration from the configured key-value store, and notifying a callback method after reloading.
The following may be passed into the constructor, or pulled from env variables:

+------------------+-----------------------+--------------------------------------------+-----------+
| Constructor Arg  | Environment Variable  | Description                                | Default   |
+==================+=======================+============================================+===========+
| consul_host      | CONSUL_HOST           | Host for Consul                            | None      |
+------------------+-----------------------+--------------------------------------------+-----------+
| consul_port      | CONSUL_PORT           | Port for Consul                            | 8500      |
+------------------+-----------------------+--------------------------------------------+-----------+
| etcd_host        | ETCD_HOST             | Host for etcd                              | localhost |
+------------------+-----------------------+--------------------------------------------+-----------+
| etcd_port        | ETCD_PORT             | Port for etcd                              | 2379      |
+------------------+-----------------------+--------------------------------------------+-----------+
| kv_prefix        | KV_PREFIX             | Prefix for config path                     | ""        |
+------------------+-----------------------+--------------------------------------------+-----------+
| reload_seconds   | RELOAD_CONFIG_PERIOD  | Seconds between config reloads             | 20        |
+------------------+-----------------------+--------------------------------------------+-----------+
| reload_enabled   | RELOAD_ENABLED        | If true, reloads the config periodically.  | False     |
+------------------+-----------------------+--------------------------------------------+-----------+

TODO: Future Features
~~~~~~~~~~~~~~~~~~~~~~
* Nested Configurations: Will enable you specify a list of prefixes to use to overlay configuration values.

Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

      from clc_msa_utils.kv_store import KVStore

        # Create config store
        kv_store = KVStore(
            kv_prefix=os.getenv('CONSUL_PREFIX') or os.getenv('ETCD_PREFIX', '/config/retry-listener'),
            reload_enabled=True
        )

        # Setup on_reload handler
        def initialize():
            kv_store.on_reload(dynamic_configuration)

        # Implement reload handler to check if attributes changed, and then perform some logic.
        def dynamic_configuration(old, new):
            if not old or old.get('exchange_configs') != new.get('exchange_configs') \
                or kv_store.attribute_changed("rabbit_host","rabbit_port","rabbit_user","rabbit_password","rabbit_queue_name"):
            setup_queue()

    # Use kv_store to pull configuration values.
    def setup_queue():
        rabbit_host = kv_store.get('rabbit_host', 'localhost')
        rabbit_port = int(kv_store.get('rabbit_port', 5672))


************
LogManager
************

This is a utility class that uses a KVStore to configure the python logging facility. It uses KVStore's dynamic ability
to reload its configuration to update Python's logging facility.

+------------------+---------------------------------------------+--------------------+
| Constructor Arg  |  Description                                | Default            |
+==================+=============================================+====================+
| kv_store         |  Backing KVStore used to configure logging. | None/Required      |
+------------------+---------------------------------------------+--------------------+

KVStore configurations relative to the kv_prefix

+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| Key                          |  Description                                | Default                                                               |
+==============================+=============================================+=======================================================================+
| logging_filename             |  The file where logs are written.           | None (Std Out)                                                        |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_filemode             |  The file mode if a filename is specified   | None                                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_format               |  The format of the logging line             | [%(threadName)s] %(asctime)s - %(levelname)s - %(name)s - %(message)s |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_datefmt              |  The date format of the date written        | %m/%d/%Y %I:%M:%S %p                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_level                |  Root logging Level                         | INFO                                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_config/log_name_1    |  Logging level for <log_name_1>             | None                                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_config/log_name_2    |  Logging level for <log_name_2>             | None                                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| logging_config/log_name_n    |  Logging level for <log_name_n>             | None                                                                  |
+------------------------------+---------------------------------------------+-----------------------------------------------------------------------+


Example Usage
~~~~~~~~~~~~~
Here are the available configurations for logging provided by KVStore using an example of `/config/local_config`

.. code:: json

    {
      "config" : {
         "local_config" : {
            "logging_level": "INFO",
            "logging_config": {
               "default": "DEBUG",
               "KVStore": "DEBUG",
               "LogManager": "DEBUG"
            }
         }
      }
    }



.. code:: python
   :number-lines: 1

   from clc_msa_utils.kv_store import KVStore
   from clc_msa_utils.log_manager import LogManager

   kv_store = KVStore(
       kv_prefix=os.getenv('CONSUL_PREFIX') or
                 os.getenv('ETCD_PREFIX') or
                 os.getenv('KV_PREFIX', '/config/local_config'),
       reload_enabled=True
   )

   log_manager = LogManager(kv_store=kv_store)


************
QueueFactory
************

This is a utility class that abstracts the creation of Queue Producers and Queue Consumers/Listeners.
The producers and consumers are constructed based on a configuration passed into their respective methods
as a parameter.  The following is an example JSON configuration of a Queue Consumer configuration that
could be stored in a key-value store such as ETCD or Consul. Notice that the `queue_config` attribute is
an array and can be all of the necessary configuration for both your Consumer and Producers.

.. code:: json

    {
      "queue_config": [
        {
          "name": "make_managed_request",
          "type": "consumer",
          "exchange": {
            "name": "managed_server",
            "type": "x-delayed-message",
            "arguments": {"x-delayed-type": "topic"},
            "durable": true
          },
          "queue": "make_managed_mos_cmdb",
          "binding_key": "requested.make_managed",
          "host": "rabbitmq.managed-services-dev.skydns.local",
          "port": "5672",
          "auth": {
            "user": "guest",
            "password": "guest"
          }
        }
      ]
    }

Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

        from clc_msa_utils.queueing import QueueFactory

        # Get config (eg. from kv_store)
        queue_config = kv_store.get('queue-config')

        # Initialize QueueFactory
        q_factory = QueueFactory()

        # Generate Queue Consumers (QueueConsumer)
        consumers = q_factory.create_consumers(queue_config)

        # Generate Queue Producers (QueueProducer)
        producers = q_factory.create_producers(queue_config)

        # Retrieve and use consumer based on name configured
        consumers['make_managed_request'].listen(callback_function)

        # Retrieve and use producer based on name configured
        producers['error'].publish({"error_details": "message about how you messed things up..."})



        def callback_function(ch, method, properties, body):
        ...


Multi-Threaded Example
~~~~~~~~~~~~~~~~~~~~~~
.. code:: python
   :number-lines: 1

      queue_factory = None

      def setup_queue:

         # If the queue_factory was already created, stop_consuming.
         # Clean up the existing connections before creating new ones
         # on a configuration change.
         if queue_factory:
             queue_factory.stop_consuming()

         # Create one configuration per thread, with a unique name for each.
         queue_factory_config = {
             "queue_config": []
         }

         amqp_connections = int(kv_store.get('amqp_connections', '10'))
         x = 0

         while x < amqp_connections:
             queue_config = {
                 "name": "notify_worker_thread_" + str(x),
                 "type": "consumer",
                 "queue": "my_queue",
                 "host": "localhost",
                 "port": "5672",
                 "exchange": {
                     "name": "managed_server",
                     "type": "x-delayed-message",
                     "arguments": {"x-delayed-type": "topic"},
                     "durable": true
                 },
                 "auth": {
                     "user": "guest",
                     "password": "guest"
                 }
             }

             queue_factory_config["queue_config"].append(queue_config)
             x = x + 1

         # Create the QueueFactory, and pass in the configuration and worker function.
         queue_factory = QueueFactory()
         queue_factory.create_consumers(queue_factory_config)
         queue_factory.start_consuming(do_work)

         # Wait for all threads to stop before stopping the main thread.
         for queue_consumer in queue_factory.consumers():
             queue_consumer.thread().join()

      ...

      def do_work(ch, method, properties, body):
         # Worker code goes here
         pass


************
QueueWorker
************

This is a utility class that creates a KVStore, LogManager, configures exchanges and queues, and starts consuming. This
class also supports multi-threaded queue consumers, specified by the amqp connections. It also provides convenience
methods to publish success messages, error messages, and will handle catching and reporting exceptionswithout writing
code in the callback method, and acknowldge the message when done.

Here are the parameters available when creating a QueueWorker

+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| Parameter                    |  Description                                                                                                 | Default              |
+==============================+==============================================================================================================+======================+
| consul_host                  |  Consul host used to initialize the KVStore.                                                                 | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| consul_port                  |  Consul port used to initialize the KVStore.                                                                 | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| etcd_host                    |  Etcd host used to initialize the KVStore.                                                                   | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| etcd_port                    |  Etcd port used to initialize the KVStore.                                                                   | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| kv_prefix                    |  The prefix used to initialize the KVStore.                                                                  | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_host_key              |  The key in the kv store that contains the RabbitMQ Host.                                                    | rabbit_host          |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_port_key              |  The key in the kv store that contains the RabbitMQ Port                                                     | rabbit_port          |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_user_key              |  The key in the kv store that contains the RabbitMQ User                                                     | rabbit_user          |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_password_key          |  The key in the kv store that contains the RabbitMQ Password                                                 | rabbit_password      |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| amqp_connection_key          |  The key in the kv store that contains the number of connections to RabbitMQ                                 | amqp_connections     |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| listen_exchange_key          |  The key in the kv store that contains the exchange to publish to listen on when consuming messages          | exchange             |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| listen_routing_key_key       |  The key in the kv store that contains the routing key to bind to when consuming messages.                   | listen_routing_key   |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| queue_name_key               |  The key in the kv store that contains the queue name to listen on when consuming messages                   | queue                |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| done_exchange_key            |  The key in the kv store that contains the exchange to publish to on success                                 | done_exchange        |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| done_routing_key_key         |  The key in the kv store that contains the routing key to publish to on success.                             | done_routing_key     |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| error_exchange_key           |  The key in the kv store that contains the exchange to publish to on error                                   | error_exchange       |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| error_routing_key_key        |  The key in the kv store that contains the routing key to publish to on error.                               | error_routing_key    |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| data_key_on_error_payload    |  The key in the kv store that contains the key in the error payload when publishing  to the error exchange.  | data                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| initialize_log_manager       |  When true, creates a LogManager using the kv store created or specified                                     | True                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| kv_store                     |  When specigfied, this kv_store is used instead of creating a new one.                                       | None                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_host_default          |  The default value of the RabbitMQ Host.                                                                     | localhost            |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_port_default          |  The default value of the RabbitMQ Port                                                                      | 5672                 |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_user_default          |  The default value of the RabbitMQ User                                                                      | guest                |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| rabbit_password_default      |  The default value of the RabbitMQ Password                                                                  | guest                |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| amqp_connection_default      |  The default value of the number of connections to RabbitMQ                                                  | 10                   |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| listen_exchange_default      |  The default value of the exchange to publish to listen on when consuming messages                           | main_exchange        |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| listen_routing_key_default   |  The default value of the routing key to bind to when consuming messages.                                    | listen.key           |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| queue_name_default           |  The default value of the queue name to listen on when consuming messages                                    | default_queue        |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| done_exchange_default        |  The default value of the exchange to publish to on success                                                  | main_exchange        |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| done_routing_key_default     |  The default value of the routing key to publish to on success.                                              | done.key             |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| error_exchange_default       |  The default value ofthe exchange to publish to on error                                                     | error_exchange       |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+
| error_routing_key_default    |  The default value of the routing key to publish to on error.                                                | error.key            |
+------------------------------+--------------------------------------------------------------------------------------------------------------+----------------------+


Example Usage
~~~~~~~~~~~~~

*worker.py*

.. code:: python
   :number-lines: 1

   import logging
   import time

   from clc_msa_utils.queueing import QueueWorker

   logger = logging.getLogger("default")

   unregister_queue_worker = QueueWorker(
       kv_prefix=os.getenv("ETCD_PREFIX", "/config/billing-listener"),

       # Rabbit Connection Info
       rabbit_host_key="rabbit_host", rabbit_host_default="rabbitmq.rabbitmq",
       rabbit_port_key="rabbit_port", rabbit_port_default=15672,
       rabbit_user_key="rabbit_user", rabbit_user_default="guest",
       rabbit_password_key="rabbit_password", rabbit_password_default="guest",
       amqp_connection_key="amqp_connection_count", amqp_connection_default=10,

       # Listen Config
       listen_exchange_key="main_exchange", listen_exchange_default="managed_server",
       listen_routing_key_key="main_exchange_stop_billing_routing_key", listen_routing_default="requested.make_unmanaged",
       queue_name_key="rabbit_stop_billing_queue_name", queue_name_default="stop_billing",

       # Done Config
       done_exchange_key="main_exchange", done_exchange_default="managed_server",
       done_routing_key_key="main_exchange_done_stop_billing_routing_key",
       done_routing_key_default="billing.make_unmanaged",

       # Error Config
       error_exchange_key="dead_letter_exchange", error_exchange_default="managed_server_error",
       error_routing_key_key="dead_letter_exchange_stop_billing_routing_key",
       error_routing_key_default="monitoring_config.make_managed",
       data_key_on_error_payload="server")

   # Use the same kv_store as above, and don't initialize another log_manager
   register_queue_worker = QueueWorker(
       # Rabbit Connection Info
       rabbit_host_key="rabbit_host", rabbit_host_default="rabbitmq.rabbitmq",
       rabbit_port_key="rabbit_port", rabbit_port_default=15672,
       rabbit_user_key="rabbit_user", rabbit_user_default="guest",
       rabbit_password_key="rabbit_password", rabbit_password_default="guest",
       amqp_connection_key="amqp_connection_count", amqp_connection_default=10,

       # Listen Config
       listen_exchange_key="main_exchange", listen_exchange_default="managed_server",
       listen_routing_key_key="main_exchange_routing_key", listen_routing_default="requested.make_managed",
       queue_name_key="rabbit_queue_name", queue_name_default="start_billing",

       # Done Config
       done_exchange_key="main_exchange", done_exchange_default="managed_server",
       done_routing_key_key="main_exchange_done_routing_key", done_routing_key_default="billing.make_managed",

       # Error Config
       error_exchange_key="dead_letter_exchange", error_exchange_default="managed_server_error",
       error_routing_key_key="dead_letter_exchange_routing_key", error_routing_key_default="billing.make_managed",
       data_key_on_error_payload="server",

       # Reuse configs
       initialize_log_manager=False, kv_store=unregister_queue_worker.kv_store())

   # Use the same kv_store for my configurations.
   kv_store=unregister_queue_worker.kv_store()

   # Use all defaults.
   all_defaults_queue_worker = QueueWorker(rabbit_host_default="rabbitmq.rabbitmq")


   # Initializes the listener
   def initialize():
       logger.debug("Initializing worker...")

       # Register the callbacks with the queue workers, this initializes the worker and starts consuming.
       register_queue_worker.set_callback(register_listener)
       unregister_queue_worker.set_callback(unregister_listener)
       all_defaults_queue_worker.set_callback(all_defaults_listener)

       logger.debug("Done Initializing worker")


   def register_listener(ch, method, properties, body):
       _do_work(ch, method, properties, body, "register", register_queue_worker)


   def unregister_listener(ch, method, properties, body):
       _do_work(ch, method, properties, body, "unregister", unregister_queue_worker)


   def all_defaults_listener(ch, method, properties, body):
       _do_work(ch, method, properties, body, "all_defaults", all_defaults_queue_worker)


   def _do_work(ch, method, properties, body, task_name, queue_worker, sleep_seconds=8):
       logger.info("[{0}] Received the following message: {1}".format(task_name, body.decode("utf-8")))
       logger.info("[{0}] Pretending to do something for {1} seconds...".format(task_name, str(sleep_seconds)))

       time.sleep(sleep_seconds)

       logger.info("[{0}] Done pretending to do something. ".format(task_name, str(sleep_seconds)))

       payload = {
           "task_name": task_name,
           "sleep_seconds": sleep_seconds,
           "original_message": body.decode("utf-8"),
           "properties": properties,
           "method": method
       }

    # No need to catch an error, the QueueWorker will publish the error for you.
    # The error message will contain 'Exception: Raising an error.', the error_details and
    # errorDetails will contain the stack trace, and the `data_key_on_error_payload` property will contain the
    # original payload.
    if "error" in str(body.decode("utf-8")):
        raise Exception("Raising an error.")

    # Publish a success message, propagating the properties
    queue_worker.publish_success(payload, properties)

    # If I need to manually publish an error message, there is a method to do so.
    queue_worker.publish_error(payload)

    # Queue worker acknowledges the message, so need to do is here!
    logger.info("[{0}] Acknowledged that I am done pretending to do something.".format(task_name))


   if __name__ == '__main__':
       initialize()


*worker_UT.py*

.. code:: python
   :number-lines: 1

   import unittest
   import worker


   class WorkerTests(unittest.TestCase):

       def setUp(self):
           pass

       def tearDown(self):
           # Stop reloading so the test will end.
           worker.kv_store.disable_reloading()

       def test_something(self):
           pass


**********************************
utils.dict_replace_empty_values()
**********************************

This utility method removes or replaces empty strings in a dictionary. Optionally, you may also replace None values.

**positional parameters**

#. The dictionary to process

**arguments**

- *process_none_values*: When true, replace or remove attributes that have a value of None/Null, default=False
- *clone_dict*: When true clones the input dictionary, processes it, and returns the clone leaving the original untouched, default=False
- *remove_values*: When true, removes attributes that are empty or optionally None, default=False
- *replace_with*: The replacement value, default=None
- *replace_float_with_decimal*: The replacement value, default=None


Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

          from utils import dict_replace_empty_values

          def process_dict(my_dict):
              # Return a clone of my_dict removing None values and empty strings.
              dict_a = dict_replace_empty_values(my_dict,
                                                 process_none_values=True,
                                                 clone_dict=True,
                                                 remove_values=True)

               # Return a clone of my_dict replacing None values and empty strings with "EMPTY".
               dict_b = dict_replace_empty_values(my_dict,
                                                  process_none_values=True,
                                                  clone_dict=True,
                                                  replace_with="EMPTY")

               # Return a clone of my_dict replacing None values and empty strings with "EMPTY", and replace floats with decimal.
               dict_c = dict_replace_empty_values(my_dict,
                                                  process_none_values=True,
                                                  clone_dict=True,
                                                  replace_with="EMPTY",
                                                  replace_float_with_decimal=True)

**********************************
utils.log_dict_types()
**********************************
Logs the type for every attribute in the specified dictionary.


**positional parameters**

#. The dictionary for which to log types

**arguments**

- *types*: Which types to show, else show all, default=None,
- *use_logger*: The logger uto use, default=logger

**********************************
utils.dig()
**********************************
Safely retrieves the value of a deeply nested dictionary property. If the path doesn't exist, `None` is returned.
If no keys are specified, `obj` is returned. No exception will be thrown if any key doesn't exist.

**positional parameters**

#. The dictionary for which to log types
#. list of keys

Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

    # For countries={"USA":{"MO":"Missouri"}} returns Missouri
    # For countries={"USA":{"KS":"Kansas"}} returns None
    dig(countries, "USA", "MO")

    # Returns 1
    dig(1)

    # Returns None
    dig(1, "a", "b")



----


.. [1] This document is formatted using `reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_,
   with `reStructuredText directives <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_.
