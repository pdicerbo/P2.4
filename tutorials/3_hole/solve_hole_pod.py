# Copyright (C) 2015-2016 SISSA mathLab
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#
## @file solve_hole.py
#  @brief Example 3: geometrical parametrization
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from dolfin import *
from RBniCS import *

#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 3: GEOMETRICAL PARAMETRIZATION CLASS     ~~~~~~~~~~~~~~~~~~~~~~~~~# 
class Hole(ShapeParametrization(EllipticCoercivePODBase)):
    
    ###########################     CONSTRUCTORS     ########################### 
    ## @defgroup Constructors Methods related to the construction of the reduced order model object
    #  @{
    
    ## Default initialization of members
    def __init__(self, V, mesh, subd, bound):
        # Declare the shape parametrization map
        shape_parametrization_expression = [
            ("2.0-2.0*mu[0] + mu[0]*x[0] +(2.0-2.0*mu[0])*x[1]", "2.0 - 2.0*mu[1] + 0.5*(4.0 - 2.0 * mu[1] - mu[3])*x[1] + 0.5 * mu[3] * x[0]"), # subdomain 1
            ("2.0*mu[0]-2.0 +x[0] +(mu[0]-1.0)*x[1]", "2.0 * (1.0 - mu[1] + mu[3]) + (2.0 - mu[1] + mu[3]) * x[1]"), # subdomain 2
            ("2.0 - 2.0*mu[0] + (2.0-mu[0])*x[0]", "2.0 -2.0*mu[1] + (2.0-2.0*mu[1])*x[0] + mu[1]*x[1]"), # subdomain 3
            ("2.0 - 2.0*mu[0] + (2.0-mu[0])*x[0]", "2.0*mu[1] -2.0 + (mu[1]-1.0)*x[0] + x[1]"), # subdomain 4
            ("2.0*mu[0] -2.0 + (2.0-mu[0])*x[0]", "2.0 * (1.0 - mu[1] + mu[3]) + 0.5 * (-4.0 + 4.0 * mu[1] - 3. * mu[3]) * x[0] + 0.5 * (2. * mu[1] - mu[3]) * x[1]"), # subdomain 5
            ("2.0*mu[0] -2.0 + (2.0-mu[0])*x[0]", "2.0*mu[1] -2.0 + (1.0 - mu[1])*x[0] + x[1]"), # subdomain 6
            ("2.0 -2.0*mu[0] + mu[0]*x[0] + (2.0*mu[0]-2.0)*x[1]", "2.0*mu[1] -2.0 + (2.0 - mu[1])*x[1]"), # subdomain 7
            ("2.0*mu[0] -2.0 + x[0] + (1.0-mu[0])*x[1]", "2.0*mu[1] -2.0 + (2.0 - mu[1])*x[1]"), # subdomain 8
        ]
        # Call the standard initialization
        super(Hole, self).__init__(mesh, subd, V, None, shape_parametrization_expression)      
        # ... and also store FEniCS data structures for assembly
        self.dx = Measure("dx")(subdomain_data=subd)
        self.ds = Measure("ds")(subdomain_data=bound)
        
    #  @}
    ########################### end - CONSTRUCTORS - end ########################### 
    
    ###########################     PROBLEM SPECIFIC     ########################### 
    ## @defgroup ProblemSpecific Problem specific methods
    #  @{
    
    ## Set theta multiplicative terms of the affine expansion of a.
    def compute_theta_a(self):
        m1 = self.mu[0]
        m2 = self.mu[1]
        m3 = self.mu[2]
        m4 = self.mu[3]
        # subdomains 1
        theta_a0 = (16*m1*m1 - 32*m1 + 4*m2*m2 + 4*m2*m4 - 16*m2 + m4*m4 - 8*m4 + 32)/(2*(4*m1 - 2*m4 - 2*m1*m2 + m1*m4)) #K11
        theta_a1 = (4*m1*m1 + m4*m4)/(2*(4*m1 - 2*m4 - 2*m1*m2 + m1*m4)) #K22
        theta_a2 = (2*m2*m4 - 4*m4 - 8*m1 + 8*m1**2 + m4**2)/(2*(4*m1 - 2*m4 - 2*m1*m2 + m1*m4)) #K12 and K21
        # subdomains 2
        theta_a3 = m4 - m2 + (m1 - 1)**2/(m4 - m2 + 2) + 2
        theta_a4 = 1/(m4 - m2 + 2)
        theta_a5 = -(m1 - 1)/(m4 - m2 + 2)
        # subdomains 3
        theta_a6 = -m2/(m1 - 2)
        theta_a7 = - (m1 - 2)/m2 - (2*(2*m2 - 2)*(m2 - 1))/(m2*(m1 - 2))
        theta_a8 = -(2*(m2 - 1))/(m1 - 2)
        # subdomains 4 and 6
        theta_a9 = -1/(m1 - 2)
        theta_a10 = 2 - (m2 - 1)*(m2 - 1)/(m1 - 2) - m1
        theta_a11 = (m2 - 1)/(m1 - 2)
        # boundaries 5, 6, 7 and 8
        theta_a12 = m3

        # subdomains 5
        theta_a13 = -(m2-m4/2)/(m1 - 2)
        theta_a14 = - (2*(m1 - 2))/(2*m2 - m4) - (((3*m4)/2 - 2*m2 + 2)*(3*m4 - 4*m2 + 4))/((m1 - 2)*(2*m2 - m4))
        theta_a15 = -(3*m4 - 4*m2 + 4)/(2*(m1 - 2))
        # boundaries 7
        theta_a16 = - (m2 - 2)/m1 - (2*(2*m1 - 2)*(m1 - 1))/(m1*(m2 - 2)) #K11
        theta_a17 = -m1/(m2 - 2) #K22
        theta_a18 = -(2*(m1 - 1))/(m2 - 2) #K12 and K21
        # subdomains 8
        theta_a19 = 2 - (m1 - 1)*(m1 - 1)/(m2 - 2) - m2
        theta_a20 = -1/(m2 - 2)
        theta_a21 = (m1 - 1)/(m2 - 2)

        
        return (theta_a0, theta_a1, theta_a2, theta_a3, theta_a4, theta_a5, theta_a6, theta_a7, theta_a8, theta_a9, theta_a10, theta_a11, theta_a12, theta_a13,
                theta_a14, theta_a15, theta_a16, theta_a17, theta_a18, theta_a19, theta_a20, theta_a21)
    
    ## Set theta multiplicative terms of the affine expansion of f.
    def compute_theta_f(self):
        m1 = self.mu[0]
        m2 = self.mu[1]
        m4 = self.mu[2]
        theta_f0 = 2*m1 - m4 - m1*m2 + (m1*m4)/2 # boundary 1
        theta_f1 = -((m1 - 2)*(2*m2 - m4))/2 # boundary 2
        theta_f2 = - m1*(m2 - 2.0) # boundary 3
        theta_f3 = - m2*(m1 - 2.0) # boundary 4
        
        return (theta_f0, theta_f1, theta_f2, theta_f3)
    
    ## Set matrices resulting from the truth discretization of a.
    def assemble_truth_a(self):
        u = self.u
        v = self.v
        dx = self.dx
        ds = self.ds
        # subdomains 1
        a0 = inner(u.dx(0), v.dx(0))*dx(1)
        a1 = inner(u.dx(1), v.dx(1))*dx(1)
        a2 = inner(u.dx(0), v.dx(1))*dx(1) +  inner(u.dx(1), v.dx(0))*dx(1)
        # subdomains 2
        a3 = inner(u.dx(0), v.dx(0))*dx(2)
        a4 = inner(u.dx(1), v.dx(1))*dx(2)
        a5 = inner(u.dx(0), v.dx(1))*dx(2) +  inner(u.dx(1), v.dx(0))*dx(2)
        # subdomains 3
        a6 = inner(u.dx(0), v.dx(0))*dx(3)
        a7 = inner(u.dx(1), v.dx(1))*dx(3)
        a8 = inner(u.dx(0), v.dx(1))*dx(3) +  inner(u.dx(1), v.dx(0))*dx(3)
        # subdomains 4 and 6
        a9 = inner(u.dx(0), v.dx(0))*dx(4) +  inner(u.dx(0), v.dx(0))*dx(6)
        a10 = inner(u.dx(1), v.dx(1))*dx(4) +  inner(u.dx(1), v.dx(1))*dx(6)
        a11 = inner(u.dx(0), v.dx(1))*dx(4) +  inner(u.dx(1), v.dx(0))*dx(4) - (inner(u.dx(0), v.dx(1))*dx(6) +  inner(u.dx(1), v.dx(0))*dx(6))
        # boundaries 5, 6, 7 and 8
        a12 = inner(u,v)*ds(5) + inner(u,v)*ds(6) + inner(u,v)*ds(7) + inner(u,v)*ds(8)

        # subdomains 5
        a13 = inner(u.dx(0), v.dx(0))*dx(5)
        a14 = inner(u.dx(1), v.dx(1))*dx(5)
        a15 = - (inner(u.dx(0), v.dx(1))*dx(5) +  inner(u.dx(1), v.dx(0))*dx(5))
        # subdomains 7
        a16 = inner(u.dx(0), v.dx(0))*dx(7)
        a17 = inner(u.dx(1), v.dx(1))*dx(7)
        a18 = - (inner(u.dx(0), v.dx(1))*dx(7) +  inner(u.dx(1), v.dx(0))*dx(7))
        # subdomains 8
        a19 = inner(u.dx(0), v.dx(0))*dx(8)
        a20 = inner(u.dx(1), v.dx(1))*dx(8)
        a21 = - (inner(u.dx(0), v.dx(1))*dx(8) +  inner(u.dx(1), v.dx(0))*dx(8))

        
        # Assemble and return
        A0 = assemble(a0)
        A1 = assemble(a1)
        A2 = assemble(a2)
        A3 = assemble(a3)
        A4 = assemble(a4)
        A5 = assemble(a5)
        A6 = assemble(a6)
        A7 = assemble(a7)
        A8 = assemble(a8)
        A9 = assemble(a9)
        A10 = assemble(a10)
        A11 = assemble(a11)
        A12 = assemble(a12)
        A13 = assemble(a13)
        A14 = assemble(a14)
        A15 = assemble(a15)
        A16 = assemble(a16)
        A17 = assemble(a17)
        A18 = assemble(a18)
        A19 = assemble(a19)
        A20 = assemble(a20)
        A21 = assemble(a21)
        return (A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16, A17, A18, A19, A20, A21)
    
    ## Set vectors resulting from the truth discretization of f.
    def assemble_truth_f(self):
        v = self.v
        dx = self.dx
        ds = self.ds
        f0 = v*ds(1) # boundary 1
        f1 = v*ds(2) # boundary 2
        f2 = v*ds(3) # boundary 3
        f3 = v*ds(4) # boundary 4
        
        # Assemble and return
        F0 = assemble(f0)
        F1 = assemble(f1)
        F2 = assemble(f2)
        F3 = assemble(f3)
        return (F0, F1, F2, F3)
        
    #  @}
    ########################### end - PROBLEM SPECIFIC - end ########################### 
    
#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 3: MAIN PROGRAM     ~~~~~~~~~~~~~~~~~~~~~~~~~# 

# 1. Read the mesh for this problem
mesh = Mesh("data/hole.xml")
subd = MeshFunction("size_t", mesh, "data/hole_physical_region.xml")
bound = MeshFunction("size_t", mesh, "data/hole_facet_region.xml")

# 2. Create Finite Element space (Lagrange P1)
V = FunctionSpace(mesh, "Lagrange", 1)

# 3. Allocate an object of the Hole class
hole = Hole(V, mesh, subd, bound)

# 4. Choose PETSc solvers as linear algebra backend
parameters.linear_algebra_backend = 'PETSc'

# 5. Set mu range, xi_train and Nmax
mu_range = [(0.5, 1.5), (0.5, 1.5), (0.01, 1.0), (-0.1, 0.1)]
hole.setmu_range(mu_range)
# hole.setxi_train(500)
hole.setxi_train(50)
hole.setNmax(20)

# 6. Perform the offline phase
# first_mu = (0.5, 0.5, 0.01, 0.)
first_mu = (1., 1., 0.01, 0.05)
hole.setmu(first_mu)
hole.offline()

# 7. Perform an online solve
# online_mu = (0.5,0.5,0.01, 0.)
online_mu = (0.5,0.5,0.01, -0.1)
hole.setmu(online_mu)
hole.online_solve()

# 8. Perform an error analysis
# hole.setxi_test(500)
hole.setxi_test(50)
hole.error_analysis()

