#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

# Import modules
from ctypes import WinDLL

# Load dlls
advapi32 = WinDLL("advapi32", use_last_error=True)
CredFree = advapi32.CredFree
CredEnumerate = advapi32.CredEnumerateA

# Constants
CRED_TYPE_GENERIC = 0x1
CRED_TYPE_DOMAIN_VISIBLE_PASSWORD = 0x4
