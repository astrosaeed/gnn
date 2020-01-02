
near(A,B,ID) :- near(B,A,ID), object(A), object(B), A!=B.
near(A,B,ID2) :- near(A,C,ID1), near(C,B,ID2), object(A), object(B),object(C), A!=B, B!=C, A!=C.


above(C,A,ID2) :- near(A,B,ID1), above(C,B,ID2), object(A), object(B),object(C), A!=B, B!=C, A!=C.

under(C,A,ID2) :- near(A,B,ID1), under(C,B,ID2), object(A), object(B),object(C), A!=B, B!=C, A!=C.

near(A,C,ID2) :- on(A,B,ID1), near(C,B,ID2), object(A), object(B),object(C), A!=B, B!=C, A!=C.

behind(C,A,ID2) :- near(A,B,ID1), behind(C,B,ID2), object(A), object(B),object(C), A!=B, B!=C, A!=C.
