#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/Identifier) on 2019-11-06.
#  2019, SMART Health IT.


from . import element

class Identifier(element.Element):
    """ An identifier intended for computation.
    
    An identifier - identifies some entity uniquely and unambiguously.
    Typically this is used for business identifiers.
    """
    
    resource_type = "Identifier"
    
    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.use = None
        """ usual | official | temp | secondary | old (If known).
        Type `str`. """
        
        self.type = None
        """ Description of identifier.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.system = None
        """ The namespace for the identifier value.
        Type `str`. """
        
        self.value = None
        """ The value that is unique.
        Type `str`. """
        
        self.period = None
        """ Time period when id is/was valid for use.
        Type `Period` (represented as `dict` in JSON). """
        
        self.assigner = None
        """ Organization that issued id (may be just text).
        Type `FHIRReference` (represented as `dict` in JSON). """
        
        super(Identifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Identifier, self).elementProperties()
        js.extend([
            ("use", "use", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("system", "system", str, False, None, False),
            ("value", "value", str, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("assigner", "assigner", fhirreference.FHIRReference, False, None, False),
        ])
        return js


from . import codeableconcept
from . import fhirreference
from . import period