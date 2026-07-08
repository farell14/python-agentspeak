#!/usr/bin/env python

import collections
import unittest

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib


class StdlibTest(unittest.TestCase):

    def test_concat_strings(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()
        X = agentspeak.Var()

        term = agentspeak.Literal(".concat", ("hello", " ", "world", X))
        next(agentspeak.stdlib._concat(agent, term, intention))

        self.assertEqual(X.grounded(intention.scope), "hello world")

    def test_concat_lists(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()
        X = agentspeak.Var()

        term = agentspeak.Literal(".concat", ((1, 2), (3, ), X))
        next(agentspeak.stdlib._concat(agent, term, intention))

        self.assertEqual(X.grounded(intention.scope), (1, 2, 3))

    def test_current_intention(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()
        intention.head_term = agentspeak.Literal("goal", (1, 2))
        X = agentspeak.Var()

        term = agentspeak.Literal(".current_intention", (X, ))
        next(agentspeak.stdlib._current_intention(agent, term, intention))

        self.assertEqual(X.grounded(intention.scope), agentspeak.Literal("goal", (1, 2)))

    def test_intend(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")

        running = agentspeak.runtime.Intention()
        running.head_term = agentspeak.Literal("goal", (1, 2))
        agent.intentions.append(collections.deque([running]))

        caller = agentspeak.runtime.Intention()
        X = agentspeak.Var()
        term = agentspeak.Literal(".intend", (agentspeak.Literal("goal", (1, X)), ))
        next(agentspeak.stdlib._intend(agent, term, caller))

        self.assertEqual(X.grounded(caller.scope), 2)

    def test_drop_intention(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")

        running = agentspeak.runtime.Intention()
        running.head_term = agentspeak.Literal("goal", (1, 2))
        stack = collections.deque([running])
        agent.intentions.append(stack)

        caller = agentspeak.runtime.Intention()
        term = agentspeak.Literal(".drop_intention", (agentspeak.Literal("goal", (1, 2)), ))
        next(agentspeak.stdlib._drop_intention(agent, term, caller))

        self.assertEqual(len(stack), 0)

    def test_succeed_goal(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")

        running = agentspeak.runtime.Intention()
        running.head_term = agentspeak.Literal("goal", (1, 2))
        running.instr = agentspeak.runtime.Instruction(agentspeak.runtime.noop)
        agent.intentions.append(collections.deque([running]))

        caller = agentspeak.runtime.Intention()
        term = agentspeak.Literal(".succeed_goal", (agentspeak.Literal("goal", (1, 2)), ))
        next(agentspeak.stdlib._succeed_goal(agent, term, caller))

        self.assertIsNone(running.instr)

    def test_drop_all_intentions(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        agent.intentions.append(collections.deque([agentspeak.runtime.Intention()]))

        caller = agentspeak.runtime.Intention()
        term = agentspeak.Literal(".drop_all_intentions", ())
        next(agentspeak.stdlib._drop_all_intentions(agent, term, caller))

        self.assertEqual(len(agent.intentions), 0)


if __name__ == "__main__":
    unittest.main()
