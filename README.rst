Jason-style AgentSpeak for Python
=================================
.. image:: https://img.shields.io/pypi/v/agentspeak.svg
    :target: https://pypi.python.org/pypi/agentspeak

.. image:: https://img.shields.io/pypi/pyversions/agentspeak.svg
    :target: https://pypi.python.org/pypi/agentspeak

.. image:: https://img.shields.io/pypi/l/agentspeak
    :target: https://opensource.org/licenses/gpl-3-0
    :alt: GPL 3 License

.. image:: https://pepy.tech/badge/agentspeak
    :target: https://pepy.tech/project/agentspeak
    :alt: Downloads

.. image:: https://img.shields.io/pypi/format/agentspeak.svg
    :target: https://pypi.python.org/pypi/agentspeak



A Python-based interpreter for the agent-oriented programming language JASON.

`python-agentspeak` is a Python-based interpreter for the agent-oriented programming language JASON. This library makes it easy to create and manage intelligent agents, offering syntax and functionalities similar to JASON in a Python environment.

Key Features
------------
* Jason-style AgentSpeak interpretation
* Easy integration with existing Python code
* Support for complex agent constructions

Setup
-----

.. code::

    pip install agentspeak

Requirements
------------
* Python 3.6 or higher
* Additional dependencies are automatically installed

Usage example
-------------

.. code::

    !hello_world.

    +!hello_world <-
      .print("Hello world!").

Usage
-----

Run a standalone agent program:

.. code::

    $ python -m agentspeak examples/hello_world.asl

Run an interactive console:

.. code::

    $ python -m agentspeak

See :code:`examples/embedded` for an example that interfaces with custom
Python code.

Jason compability
-----------------

python-agentspeak should be mostly equivalent to Jason_.

* Plan annotations are parsed and used as plan labels (e.g. for
  :code:`.untellHow`), but behavior annotations such as
  :code:`atomic` or :code:`breakpoint` are not interpreted.
* Standard library does not yet contain syntactic transformations with
  :code:`{begin ...}` and :code:`{end}`.
* Standard library contains some, but not all, introspective and
  plan-manipulation actions. Implemented: :code:`.current_intention`,
  :code:`.intend`, :code:`.drop_intention`, :code:`.succeed_goal`,
  :code:`.drop_all_intentions`, :code:`.add_plan`, :code:`.remove_plan`,
  :code:`.relevant_plans`, :code:`.plan_label`. Not yet implemented:
  :code:`.fail_goal`, event/desire introspection (:code:`.desire`,
  :code:`.drop_event`, :code:`.drop_all_events`, :code:`.drop_desire`,
  :code:`.drop_all_desires`), and agent lifecycle actions
  (:code:`.create_agent`, :code:`.kill_agent`, :code:`.at`,
  :code:`.perceive`).
* :code:`.send(Receiver, askOne, Query, Answer)` and
  :code:`.send(Receiver, askAll, Query, Answer)` query the receiver's
  belief base directly and bind the answer in the same reasoning
  step, rather than actually dispatching an asynchronous message and
  suspending the sender until a reply arrives.
* Jason 2.0 fork join operators are tokenized by the lexer but not yet
  parsed/supported.
* Literals are only comparable if they have the same signature.


.. _Jason: http://jason.sourceforge.net/
