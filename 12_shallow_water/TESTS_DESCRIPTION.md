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
Water initially flows down the drain from the surface to the pipe. As the inflow of water from the inlet increases for the pipe, 
overflow starts happening. Note that the overflow onset depends on the water level on the surface over the manhole, which is oscillating.
Hence, there cannot be a steady overflow from the pipe to the surface.

```
coupled_fernandez_pato_garcia_navarro:
```
This test case reproduces the Single Sewer/Surface Flow Exchange test case from  "Development of a New Simulation Tool Coupling a 2D Finite Volume 
Overland Flow Model and a Drainage Network Model" by Fernandez-Pato and Garcia-Navarro. 

```
coupled_surface_pipe_model_water_balance:
```
This test considers the coupling of a surface flow and a pipe flow. Water is exchanged one-way from the surface flow into the pipe.
The purpose of this test was to verify that the coupling term between the models was constructed appropriately in order to guarantee
water conservation. The boundary conditions for this test are prescribed inlet and outlet discharge for both the surface flow and the 
pipe flow. The output of this test, called coupled_water_balance.csv, should be fed as input (after proper formatting) to plot_coupled_water_balance.py which lies in the water balance repo: https://github.com/gcapodag/amanzi_water_balance.

```
coupled_surface_pipe_model_water_balance_junction:
```
Similar test to coupled_surface_pipe_model_water_balance, with the difference that now there is a junction in the pipe. Moreover, the
pipe diameters of the pipes joining in the junction are 1 m (left pipe) and 0.5 m (right pipe). The output of this test, called coupled_water_balance.csv, should be fed as input (after profer formatting) to plot_coupled_water_balance_with_junction.py which lies in the water balance repo: https://github.com/gcapodag/amanzi_water_balance.

```
shallow_water_1D:
```
This is a dam break test for a 1D shallow water model. The ponded depth is initialized to 0.5 only on the left half of the domain.
Boundary conditions are of Dirichlet type on ponded depth and velocity.

```
pipe_flow_1D:
```
This test is the equivalent of shallow_water_1D but using a pipe model. Note that the boundary condition here is imposed on the 
the velocity and wetted area, not on the water depth. The initialization is the same as in shallow_water_1D.

```
pipe_flow_drain_source:
```
Just a simple test to verify that the input source through the manhole was going inside the pipe. There is an analytic constant
inflow of water through the manhole. The pipe is initially dry, and it just keeps on getting more filled while remaining in 
a ventilated flow regime.

```
pipe_flow_hydraulic_routing:
```
This is currently the only test case for the pipe flow for which we have experimental results. It tests the ventilated regime and
implementes Test 4 from "Improved Modeling of Flows in Sewer Pipes with a Novel, Well-Balanced MUSCL Scheme" by Liu and Chen.
The numerical model results agree with the red curves in Figure 11 from the aforementioned paper.

```
pipe_flow_hydraulic_routing_y_axis:
```
Same test as pipe_flow_hydraulic_routing but with the mesh oriented along the y-axis instead of the x-axis.

```
pipe_flow_lake_at_rest:
```
This is Test 2 from "Improved Modeling of Flows in Sewer Pipes with a Novel, Well-Balanced MUSCL Scheme" by Liu and Chen.
Here it is possible to test the pipe model in partially pressurized regime, ventilated but fully flooded cells, and 
ventilated with dry cells, and partially flooded cells. With appropriate changes to the xml file, it is possible to run this
case also for the shallow water model.

```
pipe_flow_lake_at_rest_with_junction:
```
Same as pipe_flow_lake_at_rest but with a junction cell placed on the 12-th cell of the pipe (we are using 24 cells).
On the junction, a shallow water model is solved instead of a pipe model.

```
pipe_flow_lake_at_rest_with_junction_y_axis:
```
Same as pipe_flow_lake_at_rest_with_junction but with the mesh oriented along the y-axis. Note that the pipe model is a 1D
model by definition although the shallow water model is a 2D model. Hence this difference is taken into account during the
computation of the fluxes in the code.

```
coupled_flow_network_mild_incline:
```
This test couples an overland flow described by the shallow water equations with a pipe network. There are 6 manholes and 16 junctions in the pipe network. A rain source on the surface is also included.

```
surface_flow_network_mild_incline:
```
Test that was used to create coupled_flow_network_mild_incline. It only considers the surface flow and no pipe network flow.

```
pipe_network_with_junction_1m:
```
Pipe network flow with two pipes that join into a junction.
