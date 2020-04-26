# Open Shortest Path First protocol 

OSPF implementation with GUI demonstration

## Description
This program demonstrates the work of the OSPF protocol. For visualization this program uses *pygame* library. 
Routers are imitated by separate processes (by *multiprocessing* python library)  
In the beginning there are two processes: 
-	main (server) process with thread for input 
-	display process

Then for each router adds the process. 
  
  
In this program there are 2 built-in constants:
-	Max count of existing routers (15 by default)
-	Max router *signal range* (0.25 by default)  
They could be changed in [ospf_net.py](https://github.com/LesikDee/Computer_Network/blob/master/OSPF/src/ospf_net.py) file.
  
  
#### Functionality:
-	Add router to the window with (x, y) router coordinates; (x, y) must be in range [0;1]
-	Ping from one (existing) router to another to see the path; each router has it ones id's (it represents on the window)
-	Run one of three pat scenarios: *circle*, *polygon* or *mill*; it adds a couple of routers by one command

Command *help* for full report  
Command *exit* for correct program terminate  
 

#### Representation:
On display, router is colored to one of three colors, each color mean the specific state, in which the router is at this moment 
-	**red:** default state 
-	**blue:** transit state: the message transits throw this router 
-	**green:** end node state: message delivered (to this node) 

## Usage 
To start the program run next script from root(OSPF) folder:
	`python -m src.main`
	
#### Examples
##### Example 1:
```console
add 0.3 0.6
add 0.3 0.4
add 0.5 0.4
add 0.5 0.6
add 0.6 0.4
add 0.8 0.5
ping 0 5
```


![***Result:***](https://github.com/LesikDee/Computer_Network/blob/master/OSPF/screenshots/Example1.png)

##### Example 2:
```console
scenario circle
ping 0 4
```


![***Result:***](https://github.com/LesikDee/Computer_Network/blob/master/OSPF/screenshots/Example2.png)
