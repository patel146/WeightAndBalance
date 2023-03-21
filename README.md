# WeightAndBalance
A Python script written to perform aircraft weight estimations and inertia calculations

# Context
The 2023 Class of Aeronautical Engineering at the Royal Military College of Canada has been working together to design an attack aircraft capable of anti-tank, 
close air support and interdiction missions. My role in this project is to estimate the weight of the aircraft (including its subsystems), calculate the centre of
gravity and moments of inertia.

# Methodology
Equations are sourced from Airplane Design Part V: Component Weight Estimation by Dr. Jan Roskam. The purpose of this script is to create an efficient workflow 
that applies all the equations from the book. This is the first version of a script which I hope to turn into an application soon.

# Problems
- Code is poorly commented
- Automated testing not implemented
- Conceptual error regarding weight estimation procedure causes innacurate results (The code I wrote works, but it is the wrong approach)
- Requires time consuming manual effort to dig through files and change values (should be an app)

# Plus Points
- Implemented a logging system to automatically generate reports each time script is run
- Can generate graphs to visualize results

# Moving Forward
- Rewrite this script as an application
  - Pure Python:
    - High code commonality, easy to reuse code
    - However, harder to share with team if they need to use it
  - Pure Web (Angular):
    - Can deploy to web for easy team access
    - However, will take time to convert Python to TypeScript
  - Hybrid (Flask):
    - Use a Python based web framework to get the benefits of both!
    
    
