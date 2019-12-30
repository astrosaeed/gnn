
near(A,B) :- near(B,A), object(A), object(B), A!=B.
near(A,B) :- near(A,C), near(C,B), object(A), object(B),object(C), A!=B, B!=C, A!=C.

