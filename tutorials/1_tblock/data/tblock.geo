Point(1) = {-1, -1, 0, 1.0};
Point(2) = {-1, 1, 0, 1.0};
Point(3) = {1, 1, 0, 1.0};
Point(4) = {1, -1, 0, 1.0};
Point(5) = {0.5, 0, 0, 1.0};
Point(6) = {-0.5, 0, 0, 1.0};
Point(7) = {0, 0.5, 0, 1.0};
Point(8) = {0, -0.5, 0, 1.0};
Line(1) = {2, 1};
Line(2) = {1, 4};
Line(3) = {4, 3};
Line(4) = {3, 2};
Point(9) = {0, 0, 0, 1.0};
Circle(5) = {7, 9, 6};
Circle(6) = {6, 9, 8};
Circle(7) = {8, 9, 5};
Circle(8) = {5, 9, 7};
Line Loop(9) = {5, 6, 7, 8};
Plane Surface(10) = {9};
Line Loop(11) = {4, 1, 2, 3};
Plane Surface(12) = {9, 11};
Coherence;
Coherence;
Coherence;
Coherence;
Physical Surface(1) = {10};
Physical Surface(2) = {12};
Physical Line(1) = {2};
Physical Line(2) = {3, 1};
Physical Line(3) = {4};
