+!test <-
    .add_plan("@greet_label +!greet(N) <- .print(\"hi \", N).");
    !greet(world);

    .relevant_plans("+!greet(_)", LP);
    .length(LP, Len);
    Len == 1;

    .plan_label("@x_label +!foo <- true.", Label);
    Label == x_label;

    .remove_plan("@greet_label");
    .relevant_plans("+!greet(_)", LP2);
    .length(LP2, Len2);
    Len2 == 0.

!test.
