Jason-style AgentSpeak for Python
=================================
.. image:: https://img.shields.io/pypi/v/py-agentspeak.svg
    :target: https://pypi.org/project/py-agentspeak/

.. image:: https://img.shields.io/pypi/pyversions/py-agentspeak.svg
    :target: https://pypi.org/project/py-agentspeak/

.. image:: https://img.shields.io/pypi/l/py-agentspeak
    :target: https://opensource.org/licenses/gpl-3-0
    :alt: GPL 3 License


Origin / Origen
----------------

**English.** This package is a Python interpreter for AgentSpeak, the
agent-oriented programming language used by `Jason <https://jason-lang.github.io/>`_,
a well-known BDI (belief-desire-intention) multi-agent platform written in
Java. It is a fork of `niklasf/python-agentspeak
<https://github.com/niklasf/python-agentspeak>`_ (previously published on
PyPI as ``agentspeak``), maintained at
`farell14/python-agentspeak <https://github.com/farell14/python-agentspeak>`_
and published here as ``py-agentspeak`` while changes make their way back
upstream.

**Español.** Este paquete es un intérprete en Python de AgentSpeak, el
lenguaje de programación orientado a agentes que usa `Jason
<https://jason-lang.github.io/>`_, una conocida plataforma multi-agente BDI
(creencias-deseos-intenciones) escrita en Java. Es un fork de
`niklasf/python-agentspeak <https://github.com/niklasf/python-agentspeak>`_
(publicado antes en PyPI como ``agentspeak``), mantenido en
`farell14/python-agentspeak <https://github.com/farell14/python-agentspeak>`_
y publicado aquí como ``py-agentspeak`` mientras los cambios llegan al
repositorio original.

Key Features
------------
* Jason-style AgentSpeak interpretation
* Easy integration with existing Python code
* Support for complex agent constructions

Setup / Instalación
--------------------

**English:**

.. code::

    pip install py-agentspeak

**Español:**

.. code::

    pip install py-agentspeak

Requirements / Requisitos
--------------------------
* Python 3.8 or higher / Python 3.8 o superior
* Additional dependencies are automatically installed / Las dependencias
  adicionales se instalan automáticamente

Usage example / Ejemplo de uso
--------------------------------

.. code::

    !hello_world.

    +!hello_world <-
      .print("Hello world!").

Usage / Uso
------------

**English.** Run a standalone agent program:

.. code::

    $ python -m agentspeak examples/hello_world.asl

Run an interactive console:

.. code::

    $ python -m agentspeak

See :code:`examples/embedded` for an example that interfaces with custom
Python code.

**Español.** Ejecutar un programa de agente independiente:

.. code::

    $ python -m agentspeak examples/hello_world.asl

Ejecutar una consola interactiva:

.. code::

    $ python -m agentspeak

Revisa :code:`examples/embedded` para un ejemplo de integración con código
Python propio.

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


.. _Jason: https://jason-lang.github.io/
