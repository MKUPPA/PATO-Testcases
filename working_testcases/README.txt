Solution strategy
=================================================

1. Species flux disabled (stagline_pato_PARK5_noflux)
-----------------------------------------------------------------------

- Comment out flux of all species in system/porousMat/preciceDict
- conductionTransfer = True, radiationTransfer = True
- Gradually increase CFL for HEGEL convergence 

2. Species flux enabled (stagline_pato_PARK5_wflux) 
-----------------------------------------------------------------------

- Uncomment out flux of all species in system/porousMat/preciceDict
- Use the flux disabled solution to restart w flux 
- Gradually increase CFL for HEGEL convergence


3. PARK5 with heat flux disabled (stagline_pato_PARK5_noQ)
-----------------------------------------------------------------------

- Comment out q in system/porousMat/preciceDict
- conductionTransfer = True, radiationTransfer = True, blowingChar = True, diffusionTransport = True, sourceTransport = True 
- Use flux enabled but surface chemistry disabled solution to restart with PARK5 surface chem
- Gradually increase CFL for HEGEL convergence
- Required larger hegel iterations for watchpoint convergence and coupling stability 
- Required delayed freezing start and smaller pato-precice time steps

4. PARK5 with hear flux enables (stagline_pato_PARK5_Q)
-----------------------------------------------------------------------

- All data exchange is now active 
- Use heat flux disabled solution to restart with PARK5 surface chemistry
- Decreased A_Bo to 0.43, increased E_Bo to 1360, decreased A_Bo2 to 0.005 and increased E_Bo2 to 1550
This reduces the rate of CO production and stabilizes the coupling
