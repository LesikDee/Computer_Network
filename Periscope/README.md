# Periscope system  
The periscope system that by independent processes cooperation keeps the target under the gun  

![***Result:***](https://github.com/LesikDee/Computer_Network/blob/master/Periscope/documentation/periscope.gif)

## Description
This program imitates the work of the periscope system. The system consist of a *laser installation*, a periscope (2 triangles *mirrors*), a *target*, and a *server* (*camera*).  If the target changes its position - it is needed to mirrors to rotate as that reflected ray strikes to the target. 
For more details see [statement of the problem.](https://github.com/LesikDee/Computer_Network/blob/master/Periscope/documentation/ProblemStatement.md)
   
There are two input configuration models: *2d* and *3d*. They both are working in 3d space, but in *2d* at start position *laser installation*, *target* and ray are in one plane.  

As it was required - the problem is solved by two approaches: direct and with neural nets. 

## Usage 
To start the program run scripts from root(Periscope) folder. There are two scripts: *app* and *demo*. 
The *app* has two optional arguments:
- '2d' or '3d' - input configuration file, '2d' by default
- 'direct' or 'net' - the solve method, 'direct' by default  

For example:	`python -m src.app 3d net`  

The *demo* script has no arguments, it always runs *2d* configuration with direct algorithm and besides all in one process.  
`python -m src.demo`
	
To move the target use keys: *UP*, *DOWN*, *LEFT*, *RIGHT*, *NUM1*, *NUM2*.
