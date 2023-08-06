#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:10:19 2021

@author: wongj
"""

import pandas as pd
import numpy as np

#------------------------------------------------------------------------------
# Diagnostics
def load_kinetic(run_ID,directory):
    '''Load e_kin.run_ID diagnostic data'''
    filename="e_kin." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","ke_per_unit_vol","poloidal_ke","toroidal_ke","axisymmetric_poloidal_ke","axisymmetric_toroidal_ke"]    
    return (data)

def load_magnetic(run_ID,directory):    
    '''Load e_mag.run_ID diagnostic data'''
    filename="e_mag." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","me_per_unit_vol","poloidal_me","toroidal_me","axisymmetric_poloidal_me","axisymmetric_toroidal_me"]    
    return (data)

def load_nusselt(run_ID,directory):
    '''Load Nuss.run_ID diagnostic data'''
    filename="Nuss." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    # data=data.astype(dtype='float') # convert string to float
    data.columns=["time","nu1","nu2"]
    return (data)

def load_dipole(run_ID,directory):
    '''Load dipole.run_ID diagnostic data'''
    filename="dipole." + run_ID.lower()
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","dipole_colatitude","g10","g11","surface_rms_B","dipole_rms_B", "surface_rms_B_deg12"]
    return (data)

def load_power(run_ID,directory):
    '''Load power.run_ID diagnostic data'''
    filename="power." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","available_convective_power_per_unit_vol","viscous","magnetic"]    
    return (data)

def load_scales(run_ID,directory):
    '''Load scales.run_ID diagnostic data'''
    filename="scales." + run_ID.lower()
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","mean_l_velocity","mean_l_field","mean_l_temperature", \
                  "median_l_velocity","median_l_field","median_l_temperature", \
                  "dissipation_scale_velocity","dissipation_scale_field"]    
    return (data)

def load_spec_l(run_ID,directory):
    '''Load spec_l.run_ID diagnostic data'''
    filename="spec_l." + run_ID.lower()
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["sh_degree","spectrum_instant_velocity","spectrum_instant_field", \
                  "spectrum_time_avg_velocity", "spectrum_time_avg_field"]
    return (data)

def load_spec_m(run_ID,directory):
    '''Load spec_m.run_ID diagnostic data'''
    filename="spec_m." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["sh_order","spectrum_instant_velocity","spectrum_instant_field", \
                  "spectrum_time_avg_velocity", "spectrum_time_avg_field"]    
    return (data)

def load_mantle(run_ID,directory):
    '''Load mantle.run_ID diagnostic data'''
    filename="mantle." + run_ID.lower()
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","mantle_rotation_rate","rotation_rate_on_CMB_fluid_side", \
                  "magnetic_torque_on_mantle","gravitational_torque_on_mantle", \
                  "total_angular_momentum_ic+oc+m"]    
    return (data)

def load_innercore(run_ID,directory):
    '''Load innercore.run_ID diagnostic data'''
    filename="innercore." + run_ID.lower()    
    data=pd.read_csv(directory+filename,header=None,delim_whitespace=True)
    data=data.replace({'D':'E'},regex=True) # replace Fortran float D to E notation
    data=data.astype(dtype='float') # convert string to float
    data.columns=["time","me_ic","poloidal","toroidal","rotation_sic", \
                  "rotation_fic","viscous_torque_ic", "magnetic_torque_ic", \
                  "gravity_torque_ic","total_angular_momentum_ic+oc+m"]    
    return (data)

#------------------------------------------------------------------------------
def fread(fid, nelements, dtype):
     '''Matlab fread equivalent'''
     if dtype is np.str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str
     else:
         dt = dtype
     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array
 
def parodyload(filename):
    '''PARODY-JA4.3/Matlab/parodyload_v4.m equivalent'''
    fid = open(filename, 'rb')

    version = fread(fid, 1, np.int16)
    version = version[0][0]
    dummy = fread(fid, 1, np.int16)
    phypar = fread(fid, 10, np.float64)
    # Simulation parameters
    time = phypar[0][0]
    DeltaU = phypar[1][0]
    Coriolis = phypar[2][0]
    Lorentz = phypar[3][0]
    Buoyancy = phypar[4][0]
    ForcingU = phypar[5][0]
    DeltaT = phypar[6][0]
    ForcingT = phypar[7][0]
    DeltaB = phypar[8][0]
    ForcingB = phypar[9][0]
    
    Ek = 1/Coriolis
    Ra = Buoyancy*Ek
    Pm = 1/DeltaB
    Pr = 1/DeltaT
    
    # Grid parameters
    gridpar = fread(fid, 8, np.int16)
    nr = int(gridpar[0][0])
    ntheta = int(gridpar[2][0])
    nphi = int(gridpar[4][0])
    azsym = int(gridpar[6][0])
    
    radius = fread(fid, nr, np.float64)
    radius = radius.transpose()[0]
    theta = fread(fid, ntheta, np.float64)
    theta = theta.transpose()[0]
    phi = np.arange(1,nphi+1)*2*np.pi/(nphi*azsym)
    
    # Output fields
    Vr = np.zeros((nphi,ntheta,nr))
    Vt = np.zeros((nphi,ntheta,nr))
    Vp = np.zeros((nphi,ntheta,nr))
    Br = np.zeros((nphi,ntheta,nr))
    Bt = np.zeros((nphi,ntheta,nr))
    Bp = np.zeros((nphi,ntheta,nr))
    T = np.zeros((nphi,ntheta,nr))
    
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Vr = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Vt = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Vp = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Br = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Bt = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    Bp = np.reshape(a,(nphi,ntheta,nr),order='F')
    a = fread(fid, nr*ntheta*nphi, np.float32)
    T = np.reshape(a,(nphi,ntheta,nr),order='F')
    
    fid.close()
    
    return (version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU, 
            DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
            nr, ntheta, nphi, azsym, radius, theta, phi, Vr, Vt, Vp,
            Br, Bt, Bp, T)

def surfaceload(filename):
    '''PARODY-JA4.3/Matlab/surfaceload_v4.m equivalent'''
    fid = open(filename, 'rb')

    version = fread(fid, 1, np.int16)
    version = version[0][0]
    dummy = fread(fid, 1, np.int16)
    phypar = fread(fid, 11, np.float64)
    # Simulation parameters
    time = phypar[0][0]
    dt = phypar[1][0]
    DeltaU = phypar[2][0]
    Coriolis = phypar[3][0]
    Lorentz = phypar[4][0]
    Buoyancy = phypar[5][0]
    ForcingU = phypar[6][0]
    DeltaT = phypar[7][0]
    ForcingT = phypar[8][0]
    DeltaB = phypar[9][0]
    ForcingB = phypar[10][0]
    
    Ek = 1/Coriolis
    Ra = Buoyancy*Ek
    Pm = 1/DeltaB
    Pr = 1/DeltaT
    
    # Grid parameters
    gridpar = fread(fid, 8, np.int16)
    nr = int(gridpar[0][0])
    ntheta = int(gridpar[2][0])
    nphi = int(gridpar[4][0])
    azsym = int(gridpar[6][0])
    
    radius = fread(fid, nr, np.float64)
    radius = radius.transpose()[0]
    theta = fread(fid, ntheta, np.float64)
    theta = theta.transpose()[0]
    phi = np.arange(1,nphi+1)*2*np.pi/(nphi*azsym)
    
    Vt = np.zeros((nphi,ntheta,nr))
    Vp = np.zeros((nphi,ntheta,nr))
    Br = np.zeros((nphi,ntheta,nr))
    dtBr = np.zeros((nphi,ntheta,nr))
    
    a = fread(fid, ntheta*nphi, np.float32)
    Vt = np.reshape(a,(nphi,ntheta),order='F')
    a = fread(fid, ntheta*nphi, np.float32)
    Vp = np.reshape(a,(nphi,ntheta),order='F')
    a = fread(fid, ntheta*nphi, np.float32)
    Br = np.reshape(a,(nphi,ntheta),order='F')
    a = fread(fid, ntheta*nphi, np.float32)
    dtBr = np.reshape(a,(nphi,ntheta),order='F')    
    
    fid.close()
    
    return (version, time, DeltaU, Coriolis, Lorentz, Buoyancy, ForcingU, 
            DeltaT, ForcingT, DeltaB, ForcingB, Ek, Ra, Pm, Pr,
            nr, ntheta, nphi, azsym, radius, theta, phi, Vt, Vp, Br,
            dtBr)