"""module to create single instance of glbl"""
##############################################################################
#
# xpdacq            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Timothy Liu, Simon Billinge
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
from .xpdacq_conf import GlblYamlDict, glbl_dict

glbl = GlblYamlDict("glbl", **glbl_dict)
