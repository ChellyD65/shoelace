#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 2015
@author: Chelly
"""

class Utilities:

    def get_tsel_both(self, d, threshold=None):
        tpm_r  = np.log2(d['tpm_real_s']+1)
        tpm_v  = np.log2(d['tpm_virt_s']+1)
        tsel_r = tpm_r[:,d['i_grThresh_both']] 
        tsel_v = tpm_v[:,d['i_grThresh_both']]
        return tsel_r, tsel_v

