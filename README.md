# Object impact and water immersion simulation

**Disclaimer** : This python script is a work in progress, there are a number of physical innacuracies. This script can be used for educational purposes.

This Python script simulates the **vertical fall and water entry** of an object (either a **cylinder** or a **cone**) into water.  
It models the **forces, dynamics, and resulting motion** during the impact and submersion phases using a Runge-Kutta integration.

## Overview

The simulation computes:
- The object’s **height (z)**, **velocity (v)**, and **acceleration (a)** over time.  
- The **duration of impact**, **maximum depth reached**, and **depth at peak acceleration**.  
- The effects of:
  - **Weight**
  - **Buoyancy (Archimedes’ force)**
  - **Quadratic drag** (air and water)

Results are visualized with three plots:
1. Height vs Time  
2. Velocity vs Time  
3. Acceleration vs Time  

## Features

- Adjustable **geometry** (`cylinder` or `cone`)
- Realistic **progressive immersion model** (optional instant immersion mode)
- Customizable **initial height**, **velocity**, and **object parameters**
- Smooth numerical integration with `solve_ivp` (Runge–Kutta 4/5)
- Automatic detection of:
  - Water contact time  
  - Peak acceleration moment  
  - Maximum penetration depth  

## How to Use

1. **Select the object configuration**  
   Uncomment one of the parameter blocks:
   ```python
   # objet = "Ech 10"
   # objet = "Ech 4"
   # objet = "Ech 2"
   # objet = "Ech 1"
   objet = "BFS réel"
   ```

2. **Define the object shape**  
   ```python
   SHAPE = "cylinder"  # or "cone"
   ```

3. **Adjust initial conditions**
   ```python
   z0 = -5        # initial altitude (negative = above water)
   v0 = 0         # initial velocity
   CHOC_BRUTAL = False  # True = instant immersion
   ```

4. **Run the script**  
   Execute the file in your Python environment.  
   The console will display simulation results and open the corresponding plots.

## Output

At the end of the run, the script prints key results:
```
Object: BFS réel (cone)
Impact duration: 0.134 s
Maximum depth: 1.273 m
Depth at peak acceleration: 0.947 m
```

Three graphs are also displayed:
- **Height vs Time:** shows entry and submersion  
- **Velocity vs Time:** shows impact speed and terminal velocity  
- **Acceleration vs Time:** highlights the peak deceleration at impact  

## Troubleshooting

- **No visible impact event?**  
  → Increase the simulation time window:
  ```python
  t_span = (0, 8)  # Increase upper limit if needed
  ```
- **Unrealistic motion?**  
  → Check mass, drag coefficient `C_d`, or geometry parameters.

- **Exensive computing time?**
  → Try reducing the number of simulation points:
  ```python
  t_eval = np.linspace(*t_span, 1000000) # Decrease if computation is long
  ```

## Dependencies

Make sure you have the following Python packages installed:
```bash
pip install numpy matplotlib scipy
```

---

## Physics Model Summary

The motion is computed from:
\[
m \frac{dv}{dt} = mg - \rho_{water} g V_{immersed}(z) - k(z) v|v|
\]
\[
\frac{dz}{dt} = v
\]

Where:
- \( V_{immersed}(z) \): submerged volume (depends on shape)
- \( k(z) \): interpolated drag coefficient between air and water  
- \( \rho_{water}, \rho_{air} \): fluid densities  
- \( C_d \): drag coefficient  
- \( A \): cross-sectional area  

## File Structure

```
impact_simulation.py      # Main simulation script
README.md                 # Documentation (this file)
```

## Notes

This script is ideal for educational or research purposes involving **hydrodynamic impact modeling**, **submersion dynamics**, or **vehicle splashdown simulations**.

Feel free to adapt the parameters and physical models to match experimental data or scaled prototypes.

## TODO
1. Implement a more realistic air to water transition
2. Implement more complex shapes for better simulation results
3. Use advanced resolution techniques for more accurate fluid simulation
4. Make a 2D or 3D animation for improved visual representation
5. Buoyancy can be improved, depending on the shape and parameters of the object, it sometimes sinks and sometimes do not.
6. Add a physical limit to model free fall maximum Velocity, otherwise velocity goes over theoretical maximum.