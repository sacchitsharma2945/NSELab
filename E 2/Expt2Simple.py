# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 10:02:29 2025

@author: navee
"""

import hashlib 

M="Hello"
Digest=hashlib.sha256(M.encode()).hexdigest()
print (M)
print(Digest)
M="Hell"
Digest=hashlib.sha256(M.encode()).hexdigest()
print(Digest)