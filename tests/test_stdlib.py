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

    def test_abolish_matches_beliefs_regardless_of_extra_annotations(self):
        # .abolish(b(X, X)) has no annotation filter, so it must remove
        # matching beliefs no matter what annotations they actually carry.
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()

        source_percept = agentspeak.Literal("source", (agentspeak.Literal("percept"), ))
        b22 = agentspeak.Literal("b", (2, 2), frozenset([source_percept]))
        b34 = agentspeak.Literal("b", (3, 4), frozenset([source_percept]))
        agent.beliefs[("b", 2)].add(b22)
        agent.beliefs[("b", 2)].add(b34)

        X = agentspeak.Var()
        term = agentspeak.Literal(".abolish", (agentspeak.Literal("b", (X, X)), ))
        next(agentspeak.stdlib._abolish(agent, term, intention))

        self.assertEqual(agent.beliefs[("b", 2)], {b34})

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

    def test_add_plan(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()

        term = agentspeak.Literal(".add_plan", ('+!greet <- .print("hi").', ))
        next(agentspeak.stdlib._add_plan(agent, term, intention))

        key = (agentspeak.Trigger.addition, agentspeak.GoalType.achievement, "greet", 0)
        self.assertEqual(len(agent.plans[key]), 1)

    def test_remove_plan(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()

        add_term = agentspeak.Literal(".add_plan", ('@my_label +!greet <- .print("hi").', ))
        next(agentspeak.stdlib._add_plan(agent, add_term, intention))

        key = (agentspeak.Trigger.addition, agentspeak.GoalType.achievement, "greet", 0)
        self.assertEqual(len(agent.plans[key]), 1)

        remove_term = agentspeak.Literal(".remove_plan", ("@my_label", ))
        next(agentspeak.stdlib._remove_plan(agent, remove_term, intention))

        self.assertEqual(len(agent.plans[key]), 0)

    def test_relevant_plans(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()

        add_term = agentspeak.Literal(".add_plan", ('+!greet(X) <- .print(X).', ))
        next(agentspeak.stdlib._add_plan(agent, add_term, intention))

        LP = agentspeak.Var()
        term = agentspeak.Literal(".relevant_plans", ("+!greet(_)", LP))
        next(agentspeak.stdlib._relevant_plans(agent, term, intention))

        plans = LP.grounded(intention.scope)
        self.assertEqual(len(plans), 1)
        self.assertIn("greet", plans[0])

        # Calling it again must not blow up (plan_to_str used to mutate
        # plan.args, breaking on a second call for the same plan).
        intention2 = agentspeak.runtime.Intention()
        LP2 = agentspeak.Var()
        term2 = agentspeak.Literal(".relevant_plans", ("+!greet(_)", LP2))
        next(agentspeak.stdlib._relevant_plans(agent, term2, intention2))
        self.assertEqual(LP2.grounded(intention2.scope), plans)

    def test_plan_label(self):
        env = agentspeak.runtime.Environment()
        agent = agentspeak.runtime.Agent(env, "agent")
        intention = agentspeak.runtime.Intention()

        Label = agentspeak.Var()
        term = agentspeak.Literal(".plan_label", ('@my_label +!greet <- .print("hi").', Label))
        next(agentspeak.stdlib._plan_label(agent, term, intention))

        self.assertEqual(Label.grounded(intention.scope), agentspeak.Literal("my_label"))

        # An unlabeled plan yields nothing.
        intention2 = agentspeak.runtime.Intention()
        Label2 = agentspeak.Var()
        term2 = agentspeak.Literal(".plan_label", ('+!greet <- .print("hi").', Label2))
        with self.assertRaises(StopIteration):
            next(agentspeak.stdlib._plan_label(agent, term2, intention2))


if __name__ == "__main__":
    unittest.main()
