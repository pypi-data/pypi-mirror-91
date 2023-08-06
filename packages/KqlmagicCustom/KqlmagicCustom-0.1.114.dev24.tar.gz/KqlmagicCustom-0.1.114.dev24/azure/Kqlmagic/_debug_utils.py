#!/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# because it is also executed from setup.py, make sure
# that it imports only modules, that for sure will exist at setup.py execution
# TRY TO KEEP IMPORTS TO MINIMUM
# --------------------------------------------------------------------------

from typing import Any
import os


debug_mode = os.getenv("KQLMAGIC_DEBUG", "").lower() == "true"

if debug_mode:
    def debug_print(obj:Any)->None:
        print(f">>> debug >>> {obj}")
else:
    def debug_print(obj:Any)->None:
        return
