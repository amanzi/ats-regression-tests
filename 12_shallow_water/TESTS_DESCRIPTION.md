```
pipe_flow_different_flow_regimes:
```
Here we test the ability of the pipe flow model to transition back and forth between different flow regimes.
The pipe is initially dry (there is no water inside the domain). There is a time varying boundary condition on the discharge
on the left wall and an outflow boundary condition on the right wall (i.e. no boundary condition is imposed on the right wall).
The inlet discharge on the left boundary starts from a positive value and decreases linearly to zero, so that the flow inside
the pipe becomes pressurized. Note that at some point there is the coexistence of pressurized and ventilated flow within the
computational domain. Once the inlet discharge has reached the value of zero, it keeps decreasing linearly to a negative value,
hence water starts flowing out of the left boundary. In this way, the pressurized flow existing in the pipe is slowly reverted 
back to ventilated. The test shows that the pipe model has the ability to transition back and forth from ventilated to
pressurized flow. 
NOTE: the bathymetry is zero in this test. Please see pipe_flow_different_flow_regimes_bathymetry for a similar test but with
non-zero bathymetry.

```
pipe_flow_different_flow_regimes_bathymetry:
```

This test is similar to pipe_flow_different_flow_regimes except that there is a non-zero bathymetry for the pipe.

```
coupled_surface_pipe_model:
```
This test involves an overland shallow water flow coupled with a pipe flow. The outlet boundary condition for the shallow water
flow is such that water leaves the domain from the right boundary (with a linear outlet discharge of water) so that water initially
flows down from the surface to the pipe but at the same time the shallow water depth decreases allowing at some point an overflow 
from the pipe. In fact, for an overflow to happen, the pipe has to be in pressurized flow mode, and the pressure head in the pipe 
has to be larger than the sum of the drain length plus the shallow water depth, hence it is convenient that the shallow water depth 
be relatively small to initiate the overflow.  The boundary condition for the pipe is an inlet boundary condition on the discharge 
that grows linearly. In this way, the pipe flow becomes pressurized and overflow to the surface can occur. 
This test shows how the exchange of water can go back and forth from the surface to the pipe. NOTE: the bathymetry is zero in this test.

```
coupled_surface_pipe_model_bathymetry:
```
This test is similar to coupled_surface_pipe_model except that there is a non-zero bathymetry for both the pipe and the surface flow.
Water initially flows down the drain from the surface to the pipe. As the inflow of water from the inlet increases for the pipe, the
flow is eventually reverted and water starts overflowing from the pipe to the surface. Note that the pipe is half pressurized for the 
duration of the run. The manhole is located in the pressurized part and therefore overflow can happen. 

