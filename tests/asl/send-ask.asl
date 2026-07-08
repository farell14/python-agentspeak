know(john, paris).
know(john, berlin).
know(mary, madrid).

+!test <-
    .my_name(Me);

    .send(Me, askOne, know(john, _), One);
    One = know(john, _);

    .send(Me, askOne, know(nobody, _), NoOne);
    NoOne == false;

    .send(Me, askAll, know(john, _), All);
    .length(All, Len);
    Len == 2.

!test.
