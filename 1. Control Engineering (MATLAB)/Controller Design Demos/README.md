# Controller Design

This folder shows examples of the different types of controllers I have built design and analysis tools. The analysis includes modeling of a linear actuator or filter. The examples shown use a linear second order actuator in the design analysis. I have made demos for the following types of controllers.
  - LQR - the design optimizes to minimize difference between the min singular values of the Return Difference and Stability Robustness transfer functions.
  - RSLQR - the same as above, but containing an integrator in the controller
  - SCP RSLQR - designs an RSLQR controller like above, assuming knowledge of an actuator in the system, then attempts to keep the dominant eigenvalues for the closed-loop system.
  - RSLQG - designs an RSLQR controller like above with an LQG observer.
  - OBLTR - designs an RSLQR controller like above with an LQG observer with Observer-Based Loop Transfer Recovery.
  - PID - designs a PID controller by picking the best value from an array of given P, I and D values, and provides analysis on the results. This design optimizes based on minimizing the sum of the squares of rise and settle time.

Each controller design has a "[Controller]\_test_functions.m", a "[Controller]\_design.mat", and "[Controller]\_design.doc" files. The first contains the script, the second contains a structure with the all the relevant information from the design process, and the last is a print of the scripts outputs and figures. (PID doesn't have a .doc file since it was written in Octave after my MATLAB license expired.) The 'functions' folder contains helper functions I wrote to help with my analysis and includes the main part of the controller designs in the "design\_[Controller].m" files.  
**the square_system_inputs_pp.m and crosst.m functions were written by Ross Gadient, Kevin Wise and Eugene Lavretsky; they were provided code from a class, and are used in some of my code.*

For each type of controller, I build an state-space controller in common controller form, and use that to form the open-loop and closed-loop transfer functions, and performs both time and frequency domain analysis, iteratively testing controllers with different gains to minimize a criteria and select the best design.

I also developed an interactive demo for PID and RSLQR controllers, allowing you to select the P, I and D values, and view the resulting change to the step response, nyqust plot, and key metrics ("interactive\_[controller]\_design.m"):  
![](interactive_pid_gif.gif)  
![](interactive_rslqr_gif.gif)
