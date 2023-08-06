#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:46:05 2020

@author: tamir
"""
import os
import memly

# Setup access to datafiles
THIS_DIR = "/mnt/3a29b482-dac1-4563-be89-d63ad92354e9/sphingomyelin_to_ceramide/46_systems/1_3/"
traj = os.path.join(THIS_DIR, "eq4_proc.xtc")
top = os.path.join(THIS_DIR, "eq4_nonwater_new.pdb")

x = memly.Membrane(traj, top, load=True)

frame_id = 1
memly.membrane.export_frame_with_normals(x.sim[frame_id],
                                         x.hg_centroids[frame_id],
                                         x.normals[frame_id],
                                         os.path.join(THIS_DIR, "normals/"+str(frame_id)+"_normals.pdb"))
#
# for frame_i, frame in enumerate(x.sim):
#     memly.membrane.export_labelled_snapshot(frame, x.leaflets[frame_i], os.path.join(THIS_DIR, "leaflet_id/"+str(frame_i)+".pdb"))
