# Squat model v1: prescribed motion, sagittal inverse dynamics

This model replaces the generic lever on the barbell squat page. It is an educational multi-segment model, not a clinically validated subject-specific musculoskeletal model or a free-running forward-dynamics simulation. No MuJoCo/OpenSim runtime or experimental validation is claimed.

## Geometry and motion

Coordinates are metres, x forward, y up. Both feet stay on the ground and both legs share loads equally. Ankle is at (0, 0.08 m); assumed contact interval is x = [-0.09, 0.20] m. Shin, thigh and upper-body lengths are user-controlled. The upper body (head, arms and torso) is one rigid segment; a point load at its upper endpoint represents the bar. The foot size is fixed. No frontal/transverse motion, sliding, tendon compliance, individual muscle recruitment or separate spine model is represented.

One repetition follows u(t) = (1 - cos(2πt/T))/2. Shin inclination is u times its maximum and knee flexion is u times the selected depth. Trunk inclination is solved to keep whole-system centre of mass over its upright reference (x = foot mass × 0.055 / total mass). Required trunk angles outside ±70° are clamped and explicitly marked infeasible. These prescribed trajectories are assumptions, not a prediction of the user's technique. Inputs describe the abstract segments, not automatically inferred anatomical measurements.

Assumed body mass fractions (both legs combined): feet 3%, shanks 10%, thighs 20%, upper body 67%. These are rounded teaching assumptions, not a personalised anthropometric dataset. Shank/thigh centres of mass are midpoints, upper-body COM is 55% from hip to shoulder. Segment inertia is mL²/12; the bar is a point mass with zero intrinsic rotational inertia. Whole-system COM is mass-weighted, including feet and bar.

## Inverse dynamics

Central differences at dt=0.0005 s provide COM accelerations and angular accelerations. For each joint J, sum over all bodies proximal to J:

M_J = 1/2 Σ[(x_i-x_J)m_i(g+a_yi) - (y_i-y_J)m_i a_xi + I_i α_i].

The half is bilateral load sharing. Moments are signed internal net joint moments, positive counter-clockwise on the proximal free body. Hip includes upper body and bar; knee adds both thighs; ankle adds both shanks. The calculation includes segment weights, bar weight and inertia. Quasi-static mode sets accelerations to zero at the same poses. Moment magnitudes do not describe muscle activation or joint contact forces.

Ground reaction is F=(Σm a_x, Σm(g+a_y)). Required centre of pressure is Σ[x m(g+a_y)-y m a_x+I α]/F_y. We display the implied resultant for the two feet. Contact feasibility requires F_y>0 and COP within the assumed foot interval; it does not include a friction test. Infeasible states remain visible, with flagged outputs rather than silent contact corrections.

## Verification and limits

Automated checks cover mass conservation, segment lengths, prescribed depth, upright static zero knee/hip moments, a separately calculated static free-body moment, load scaling, dynamic/static convergence for slow motion, vertical reaction, COP, period wrapping, parameter rejection, and finite outputs over a parameter sweep. These are mathematical checks, not validation against measured humans. Before using outputs for training prescriptions, model geometry, anthropometry, kinematics and forces need experimental comparison.

Background methodology:

- OpenSim: How Inverse Dynamics Works — https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090079/How+Inverse+Dynamics+Works
- OpenSim: Working with Static Optimization — https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53085189/Working+with+Static+Optimization (additional assumptions needed to estimate individual muscle forces).

Next extension: empirical trajectories and anthropometry, separate trunk/head/arms, machine/contact constraints and benchmark comparison with OpenSim or MuJoCo.
