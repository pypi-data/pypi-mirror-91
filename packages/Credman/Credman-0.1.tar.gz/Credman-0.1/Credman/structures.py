#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

# Import modules
from base64 import b64encode
from ctypes import POINTER, c_char, Structure
from ctypes.wintypes import FILETIME, LPSTR, DWORD, LPBYTE

# The CREDENTIAL_ATTRIBUTE structure contains an application-defined attribute of the credential. 
# An attribute is a keyword-value pair. 
# It is up to the application to define the meaning of the attribute.
class CREDENTIAL_ATTRIBUTE(Structure):
    _fields_ = [
        ("Keyword", LPSTR),
        ("Flags", DWORD),
        ("ValueSize", DWORD),
        ("Value", LPBYTE)
    ]

# The CREDENTIAL structure contains an individual credential.
class CREDENTIAL(Structure):
    _fields_ = [
        ("Flags", DWORD),
        ("Type", DWORD),
        ("TargetName", LPSTR),
        ("Comment", LPSTR),
        ("LastWritten", FILETIME),
        ("CredentialBlobSize", DWORD),
        ("CredentialBlob", POINTER(c_char)),
        ("Persist", DWORD),
        ("AttributeCount", DWORD),
        ("Attributes", POINTER(CREDENTIAL_ATTRIBUTE)),
        ("TargetAlias", LPSTR),
        ("UserName", LPSTR)
    ]

# Try decode credential blob
def BlobToString(blob:bytes) -> str:
    if not blob: return ''
    try:
        utf8 = blob.decode("utf-8")
        if "�" in utf8 or "" in utf8:
            return blob.decode("utf-16")
        return utf8
    except UnicodeDecodeError:
        return "Base64:" + b64encode(blob).decode()

# Credential object
class Credential(object):
    def __init__(self, TargetName:bytes, UserName:bytes, CredentialBlob: bytes):
        self.TargetName = TargetName
        self.UserName = UserName
        self.CredentialBlob = CredentialBlob
    
    def __str__(self) -> str:
        name = BlobToString(self.TargetName)
        user = BlobToString(self.UserName)
        cred = BlobToString(self.CredentialBlob)

        if not user:
            return "TargetName: {}\nCredentialBlob: {}\n\n".format(name, cred)
        return "TargetName: {}\nUserName: {}\nCredentialBlob: {}\n\n".format(name, user, cred)

