#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

# Import modules
from ctypes import POINTER, byref, c_ulong
# Import packages
from .structures import CREDENTIAL, Credential
from .functions import (
        CredEnumerate, CredFree,
        CRED_TYPE_DOMAIN_VISIBLE_PASSWORD, CRED_TYPE_GENERIC
    )

# Read credentials
def ReadPasswords() -> list:
    passwords = []
    count = c_ulong()
    creds = POINTER(POINTER(CREDENTIAL))()

    if CredEnumerate(None, 0, byref(count), byref(creds)) == 1:
        for i in range(count.value):
            c = creds[i].contents
            if c.Type == CRED_TYPE_GENERIC or c.Type == CRED_TYPE_DOMAIN_VISIBLE_PASSWORD:
                passwords.append(
                    Credential(c.TargetName, c.UserName,
                        c.CredentialBlob[:c.CredentialBlobSize.real].replace(b"\x00", b""))
                )

        CredFree(creds)
    return passwords

# Demo
#if __name__ == '__main__':
#    for cred in ReadPasswords():
#        print(str(cred))
