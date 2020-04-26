# Periscope system: statement of the problem 

## General statement of the problem:  
There is a system in 3d space from a *laser installation*, a periscope (2 *mirrors*), a *target*, and a *server* (*camera*).
![***Result:***](https://github.com/LesikDee/Computer_Network/blob/master/Periscope/documentation/scheme1.png)

  
*Mirrors* and *server* - are modeled by independent processes, where
- The *server* reads information about surrounding objects (the position of the *target* and the location of the *mirrors* in space) and passes, if necessary, to processes simulated the operation of *mirrors*
- *Mirrors* can change their position in space, as well as exchange information with each other and the *server*.  

The vector that sets the *laser* beam does not change during operation, but the *target* can change its location within certain limits, and it is necessary to ensure that the system works in order that the *mirrors* rotate so that the beam hits the *target*.  
  
In space, a *mirrors* is a triangle, one of the vertices of which is fixed in space. And around which the triangle can rotate in two directions: around the pitch and roll Euler angles.

  
## Detailed statement of the problem:
The *target* is a small sphere, and for a unit of time, it cannot shift so much that the beam ceases to intersect with it, provided that the beam is initially directed to the center of the sphere.
  
*Mirrors* can always rotate so that the beam can cross the sphere in the center.

Triangles are isosceles.

It is needed  to solve the problem in two ways:
- To come up with and implement such an algorithm of actions for interaction/change of position in the space of *mirrors* so that the beam always intersects with the *target*.
- Using machine learning methods, obtain a model that controls the *mirrors* so that the beam always intersects with the *target*.
