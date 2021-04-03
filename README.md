# Path-Planning-Algorithms
All python programs can be directly run individually.

All the obstacles, goal and number of sample points and all variables can be changed by looking under "#Variables" in all the programs

Sample obstacles, goal points have been already set.

Specific things for individual programs, things that may not be explained in comments

Note: bounds_of_plane is a rectangular region which has two of it's diagonal vertices as origin (0, 0) and the tuple bounds_of_plane

1)RRT - For RRT, most variables can be found under "#variables" (line - 61). However, Obstacles, start point and goal cannot be found under "#variables",  they can be changed in the function called test_rrt() (line - 135).

2)RRT* - "#variables can be found on (line - 91)

3)PRM + Astar - "#variables can be found on (line - 92)

Also please note that the PRM code has not been cleaned up yet, there is a lot of redundant code, would not recommend reading through it.
