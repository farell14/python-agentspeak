+!test <-
    .current_intention(test);

    !!sibling(1);
    .intend(sibling(1));
    .drop_intention(sibling(1));

    !!other(2);
    .succeed_goal(other(2));

    .drop_all_intentions.

+!sibling(N) <-
    .print("sibling should not run: ", N).

+!other(N) <-
    .print("other should not run: ", N).

!test.
