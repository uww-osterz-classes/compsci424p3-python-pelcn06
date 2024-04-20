"""
COMPSCI 424 Program 3
Name: Noah Pelc
"""

#General Instructions
"""
Instructions:
General instructions

Write a multithreaded implementation of the Banker's algorithm. In this implementation, you will create a model of a multiprocessing computer system where several processes are requesting and releasing random amounts of resources at random times.

------------------------------------------------------
 
Command-line arguments

Your starter code in GitHub Classroom will include code to accept two command-line arguments, as described in this section. You should not need to write code for this part.

Your program should accept two command-line arguments.

    One of two words: manual if your program will run in manual mode, or auto if your program will run in automatic mode.
    The path to a "setup file", a text file that describes the initial setup for the system that you will simulate. Your program will use this file to initialize its data structures.

If you write your program in Java, if your main class is named Program3, and if your input file is named test2.txt and is in the directory where you are issuing the Java command, then your command to run the Java program might look like

java Program3 manual test2.txt

If you write your program in C or C++, and if your input file is named test2.txt and is in the same directory as your compiled program file, then you might run your program with a command like

./a.out manual test2.txt

---------------------------------------------------------- 

Setup file

The structure of your setup file should be similar to the following example. The specific numbers can be different, but the structure should be the same.

3 resources
5 processes
Available
6 7 12
Max
4 5 6
3 1 2
1 2 2
0 3 1
5 4 7
Allocation
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0

Your program should use this input file to set the numbers of resources and processes (customers), then initialize the Available, Max, and Allocation arrays. (See the Banker's Algorithm data structures page for more information about these arrays.)

This makes it easier for you to run your code with different test cases. Visit the Test Cases for Program 3 page to get input files and commands for two pre-made test cases. When I grade your program, I will try running it with these two test cases, plus some additional test cases that I will write.

----------------------------------------------------------
 
Check initial conditions

Before continuing to the next part, your program should perform checks to ensure that all of the following conditions are true at the start for every process Pi 
and every resource type Rj

1. 1. Allocation[Pi][Rj] <= Maximum[Pi][Rj]

2. (SUMi( Allocation[Pi][Rj]) + Available[Rj] = Total[Rj]
	(in English: You can't allocate more resources of a given type than actually exist.)
	1. Theres really nothing to check here.  However, it might help you to create a Total array, where for each resource type Rj, Total[Rj] stores the total number of (available + allocated) instances of that resource type.

3. The system is in a ssafe state.
	1. The system is in a safe state if and only if the system's claim graph is completely reducible, as shown in zyBook section 5.3.
	2. In your program, you should use the table-based approach in zyBook Participation Activity 5.3.5 to decide whether the system is in a safe state. You may want to move this code into its own method so you can call it repeatedly.

If any of these conditions are false, the program should display an appropriate error message and then exit.

If all of these conditions are true, then the program should continue to the next step.

 
Choose a mode: manual or automatic

Your program should be able to run in two different modes: manual mode if manual is given on the command line, or automatic mode if auto is given on the command line.

 
Manual mode

In manual mode, your program should allow the user to enter any of the following three types of commands.

request I of J for K
release I of J for K
end

A request or release command word should be followed on the same line by

   1. number of elements being requested (requests between 0 and Max[K][J], releases between 0 and Allocation[K][J]), then
   2. the word of followed by the resource type ID being requested (between 0 and m-1), then
   3. the word for followed by the process ID making the request (between 0 and n-1).

For example, request 3 of 1 for 0 requests 3 units of resource R_1 for process p_0.

An end command word exits the program.

 
Automatic mode

In automatic mode, your program will apply the Banker's algorithm to a simulation of a multiprocess system. Your program must create one thread for each of the n processes ("customers") in the system that you are simulating.

Each thread must randomly generate 3 request commands and 3 release commands for itself. Please do not hard-code these numbers.

Within each thread, requests should alternate with releases: each request should be followed by one release.

When each thread completes its 3 requests and 3 releases, that thread should terminate. The program ends after all threads terminate.

Note that processes should not release all of their resources immediately after a request for more resources is granted. Both requests and releases should be randomly generated.

The threads should be able to run in parallel if your system allows it. All threads will share the same set of arrays, so you will need to control access to the arrays using mutex locks, semaphores, or similar structures in order to ensure data integrity (unless you are writing in Rust).

 
Handling requests

Each request must be checked using the Banker's algorithm before it is granted.

A request must be granted if and only if the Banker's algorithm shows that the system will still be in a safe state after the request is granted.

If the request will put the system into an unsafe state, then do the following steps.

   1. Deny the request.
   2. Reverse any changes that were made to the arrays during the Banker's algorithm (unless the program worked on copies of the arrays).
   3. Allow the requesting thread to continue. You do not need to make the requesting thread wait for enough resources to become available.

 
Handling releases

If the number of units to be released is valid (non-negative and not more than the process holds), then release the resources.

Otherwise, display an error message and do not change the arrays.

 
Required output

Your program must display the following output, to help you debug your program and to help me grade it. This output should be displayed in both manual mode and automatic mode.

       1. For each request, (a) the process/thread number, (b) the type and number of requested resource units, and (c) whether the request was granted or denied.
            Example: "Process 2 requests 3 units of resource 1: denied"
       2. For each release, (a) the process/thread number and (b) the type and number of released resource units.
            Example: "Process 1 releases 4 units of resource 2"

You may also want to display the initial state of the system (i.e., contents of "maximum" and "available" arrays at start) to help you debug your program. However, this is not required.

"""

#Python Instructions
"""
Python Specific Instructions

Python

Any Python 3 version will work. If you develop on washington.uww.edu or another Linux system, make sure your program works with python3.

Learn more about Python multithreading from these sites.

The official Python threading library documentation (https://docs.python.org/3/library/threading.html)
An Intro to Threading in Python
(https://realpython.com/intro-to-python-threading), at Real Python (https://realpython.com/) (one of my favorite Python tutorial sites)

To earn full points, your program's automatic mode must be implemented using the multithreading facilities provided by the Python 3 threading module (https://docs.python.org/3/library/threading.html)

You can use other modules in addition to threading, but you must use the threading module. This is for consistency with Java and C++ developers.

Here's a link to information about accepting command-line arguments in Python (https://docs.python.org/3/tutorial/stdlib.html#command-line-arguments)

"""

"""
Banker's Algorithm data structures

The claim graph that is used in the Banker's Algorithm can be represented by the following set of arrays. In these definitions, m is the number of different resource types and n is the number of processes.

R[m] or Available[m]
    A 1-dimensional array of integers that stores the number of available (unallocated) units of each resource. Each entry R[j] or Available[j] records the number of units of resource R_j .
P[n][m] or Max[n][m]
    A 2-dimensional array of integers that stores the maximum possible claim by each process for each type of resource. Each entry P[i][j] or Max[i][j] records the maximum number of units of resource R_j that process p_i will ever request.
Allocation[n][m]
    A 2-dimensional array of integers that shows how many units of each resource are currently allocated to each process. Each entry Allocation[i][j] records the number of units of resource R_j that are currently allocated to process p_i.
Request[n][m]
    A 2-dimensional array of integers that represents the request edges in the claim graph. Each entry Request[i][j] records the number of units of resource R_j that process p_i is currently requesting.

Participation Exercise 5.3.5 in the zyBook illustrates how this works. In that exercise,

    the "Maximum claims" part of the table corresponds to P[n][m] or Max[n][m]
    the "Current allocations" part of the table corresponds to Allocation[n][m]
    the "Current requests" part of the table corresponds to Request[n][m]
    the "Available units" table, off to the side, corresponds to R[m] or Available[m]

 

The description of the Banker's algorithm in our old textbook (Operating Systems Concepts) also refers to three other arrays, which are created during the execution of the Banker's algorithm. Using these arrays in your Banker's algorithm code may make your work simpler.

Need[n][m]
    A 2-dimensional array of integers that represents the potential request edges in the claim graph. Need[i][j] = Max[i][j] - Allocation[i][j] for each process p_i and each resource type R_j. This corresponds to the "Potential requests" part of the table in Participation Exercise 5.3.5 in the zyBook.

Work[m]
    A 1-dimensional array of integers that can be used to help with the graph reduction. In the "dinosaur book", Work is initialized as a copy of Available, so initially Work[j] = Available[j] for each resource R_j. As each unblocked process is removed (step 2 in the "safety algorithm" on pages 331-332), its allocated resources are added to Work. (In the zyBook, these changes are made directly to R[j] or Available[j]. It's good to use a separate copy of R or Available to "try out" the graph reduction before committing to it.)

Finish[n]
    A 1-dimensional array of Boolean values that can be used to help with the graph reduction. For each process p_i, Finish[i] is true if process p_i has already been removed from the claim graph (zyBook explanation) or selected and processed by the safety algorithm ("dinosaur book" explanation"). Otherwise, Finish[i] is false.

Total[m]
    A 1-dimensional array of integers that shows the total number of instances of each resource type in the system.
    Note: It is possible to correctly write this program without using a Total array.
    At the start of the program, create this array so that Total[Rj] = SUMi(Allocation[Pi][Rj]) + Available[Rj].  Since your startup file gives you all values for the Available and Allocation arrays, this should be simple to do.
    After the setup file has been processed, the values in the Total array should never change.
"""


import os
import sys
import threading # standard Python threading library

# (Comments are just suggestions. Feel free to modify or delete them.)

# When you start a thread with a call to "threading.Thread", you will
# need to pass in the name of the function whose code should run in
# that thread.

# If you want your variables and data structures for the banker's
# algorithm to have global scope, declare them here. This may make
# the rest of your program easier to write. 
#  
# Most software engineers say global variables are a Bad Idea (and 
# they're usually correct!), but systems programmers do it all the
# time, so I'm allowing it here.


# Let's write a main method at the top
def main():
    # Code to test command-line argument processing.
    # You can keep, modify, or remove this. It's not required.
    if len(sys.argv) < 3:
        sys.stderr.write("Not enough command-line arguments provided, exiting.")
        sys.exit(1)

    print("Selected mode:", sys.argv[1])
    print("Setup file location:", sys.argv[2])

    # 1. Open the setup file using the path in argv[2]
    num_resources = 0
    num_processes = 0
    R = [] #Available
    P = [[0 for x in range(num_resources)] for y in range(num_processes)] #Max
    Allocation = [[0 for x in range(num_resources)] for y in range(num_processes)]
    Request = [[0 for x in range(num_resources)] for y in range(num_processes)]
    Need = [[0 for x in range(num_resources)] for y in range(num_processes)]
    Work = []
    Finish = []
    Total = []
    with open(sys.argv[2], 'r') as setup_file:
        # 2. Get the number of resources and processes from the setup
        # file, and use this info to create the Banker's Algorithm
        # data structures
        num_resources = int(setup_file.readline().split()[0])
        print(num_resources, "resources")
        num_processes = int(setup_file.readline().split()[0])
        print(num_processes, "processes")

        # 3. Use the rest of the setup file to initialize the data structures
        
        #R[m] - A 1-dimensional array of integers that stores the number of available (unallocated) units of each resource. Each entry R[j] or Available[j] records the number of units of resource R_j.
        dump = setup_file.readline()
        holder = setup_file.readline().split()
        for i in range(0, num_resources, 1):
            R[i] = holder[i]
            
        #P[n][m] (P[[m]n]) - A 2-dimensional array of integers that stores the maximum possible claim by each process for each type of resource. Each entry P[i][j] or Max[i][j] records the maximum number of units of resource R_j that process p_i will ever request.
        dump = setup_file.readline()    
        for i in range(0, num_processes, 1):
            holder = setup_file.readline()
            for j in range(0, num_resources, 1):
                P[i][j] = holder[j]
        
        #Allocation[n][m] -  A 2-dimensional array of integers that shows how many units of each resource are currently allocated to each process. Each entry Allocation[i][j] records the number of units of resource R_j that are currently allocated to process p_i.
        dump = setup_file.readline()
        for i in range(0, num_processes, 1):
            holder = setup_file.readline()
            for j in range(0, num_resources, 1):
                Allocation[i][j] = holder[i][j]
              

    
    # 4. Check initial conditions to ensure that the system is
    # beginning in a safe state: see "Check initial conditions"
    # in the Program 3 instructions
    
    """
    Check initial conditions

    Before continuing to the next part, your program should perform checks to ensure that all of the following conditions are true at the start for every process Pi 
    and every resource type Rj

        



        3. The system is in a ssafe state.
	        1. The system is in a safe state if and only if the system's claim graph is completely reducible, as shown in zyBook section 5.3.
	        2. In your program, you should use the table-based approach in zyBook Participation Activity 5.3.5 to decide whether the system is in a safe state. You may want to move this code into its own method so you can call it repeatedly.

    If any of these conditions are false, the program should display an appropriate error message and then exit.

    If all of these conditions are true, then the program should continue to the next step.
    """
    # 1. Allocation[Pi][Rj] <= Maximum[Pi][Rj]
    for i in range(0, num_resources, 1):
        for j in range(0, num_processes, 1):
             if Allocation[i][j] > P[i][j]:
                sys.stderr.write("Not enough resources for this test!")
                sys.exit(1)
                
    """
       2. (SUMi( Allocation[Pi][Rj]) + Available[Rj] = Total[Rj]
	        (in English: You can't allocate more resources of a given type than actually exist.)
	        1. Theres really nothing to check here.  However, it might help you to create a Total array, where for each resource type Rj, Total[Rj] stores the total number of (available + allocated) instances of that resource type.
    """
    for i in range(0, num_resources, 1):
        for j in range(0, num_processes, 1):
            if Allocation[i][j] > P[i][j]:
                sys.stderr.write("You can't allocate more resources of a given type than actually exist.")
                sys.exit(1)
        
    
    

    # 5. Go into either manual or automatic mode, depending on
    # the value of args[0]; you could implement these two modes
    # as separate methods within this class, as separate classes
    # with their own main methods, or as additional code within
    # this main method.

# fill in other methods here as desired

main() # call the main function