Python FHIR Parser
==================
[![Pyversions](https://img.shields.io/pypi/pyversions/fhirparser.svg)](https://pypi.python.org/pypi/fhirparser)

[![PyPi](https://img.shields.io/pypi/v/fhirparser.svg)](https://pypi.python.org/pypi/fhirparser)

A Python FHIR specification parser for model class generation.
If you've come here because you want _Swift_ or _Python_ classes for FHIR data models, look at our client libraries instead:

- [Swift-FHIR][] and [Swift-SMART][]
- Python [client-py][]
- [fhir_model_generator][]

This fork is currently capable of parsing [R4] and the latest [R5] builds.  
We are still working on issues with earlier versions -- stay posted.
The `master` branch is currently capable of parsing _STU3_ and _DSTU2_, but it doesn't generate any test code because
the needed examples are not included in _examples-json.zip_.
There may be tags for specific freezes, see [releases](https://github.com/hsolbrig/fhir-parser/releases).

This work is licensed under the [APACHE license][license].
FHIR® is the registered trademark of [HL7][] and is used with the permission of HL7.


Tech
----
The _generate.py_ script downloads the following files from the URL supplied on the command line, or, if none, the
 `specification_url` named in _settings.py_.
 - _version.info_ - used to get identifying information about the build, version and the like
 - _examples-json.zip_ - contains _profiles-resources.json_ as well as (theoretically), all of the FHIR resource examples. 
 ("Theoretially" because there are no examples in the STU3 zip file (?))
 

The _generate.py_ script downloads [FHIR specification][fhir] files, parses the profiles (using _fhirspec.py_) and 
represents them as `FHIRClass` instances with `FHIRClassProperty` properties (found in _fhirclass.py_).
Additionally, `FHIRUnitTest` (in _fhirunittest.py_) instances get created that can generate unit tests from provided FHIR examples.
These representations are then used by [Jinja][] templates to create classes in certain programming languages, mentioned below.

This script does its job for the most part, but it doesn't yet handle all FHIR peculiarities and there's no guarantee the output is correct or complete.
This repository **does not include the templates and base classes** needed for class generation, you must do this yourself in your project.
You will typically add this repo as a submodule to your framework project, create a directory that contains the necessary base classes and templates, create _settings_ and _mappings_ files and run the script.
Examples on what you would need to do for Python classes can be found in _Sample/settings.py_, _Sample/mappings.py_ and _Sample/templates*_.


Use
---
1. `pipenv install fhirparser`
2. `generate [options]` where options are:
```
usage: fhirparser [-h] [-f] [-c] [-lo] [-po] [-u FHIRURL] [-td TEMPLATEDIR]
                  [-o OUTPUTDIR] [-cd CACHEDIR] [--nosort]
                  settings

positional arguments:
  settings              Location of the settings file. Default is settings.py

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Force download of the spec
  -c, --cached          Force use of the cached spec (incompatible with "-f")
  -lo, --loadonly       Load the spec but do not parse or write resources
  -po, --parseonly      Load and parse but do not write resources
  -u FHIRURL, --fhirurl FHIRURL
                        FHIR Specification URL (overrides
                        settings.specifications_url)
  -td TEMPLATEDIR, --templatedir TEMPLATEDIR
                        Templates base directory (overrides settings.tpl_base)
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Directory for generated class models. (overrides
                        settings.tpl_resource_target)
  -cd CACHEDIR, --cachedir CACHEDIR
                        Cache directory (default: downloads)
  --nosort              If set, do not sort resource properties alphabetically
```
Use
---
1. Create the file `mappings.py` in your project, to be copied to fhir-parser root.
    First, import the default mappings using `from Default.mappings import *` (unless you will define all variables yourself anyway).
    Then adjust your `mappings.py` to your liking by overriding the mappings you wish to change.
    
3. Similarly, create the file `settings.py` in your project, using the [Default settings]
    First, import the default settings using `from Default.settings import *` and override any settings you want to change.
    Then, import the mappings you have just created with `from mappings import *`.
    The default settings import the default mappings, so you may need to overwrite more keys from _mappings_ than you'd first think.
    You most likely want to change the topmost settings found in the default file, which are determining where the templates can be found and generated classes will be copied to.

5. Create a script that copies your `mappings.py` and `settings.py` file to the root of `fhir-parser`, _cd_s into `fhir-parser` and then runs `generate.py`.
    The _generate_ script by default wants to use Python _3_, issue `python generate.py` if you don't have Python 3 yet.
    * Supply the `-f` flag to force a re-download of the spec.
    * Supply the `--cache-only` (`-c`) flag to deny the re-download of the spec and only use cached resources (incompatible with `-f`).

> NOTE that the script currently overwrites existing files without asking and without regret.


Languages
=========

This repo used to contain templates for Python and Swift classes, but these have been moved to the respective framework repositories.
A very basic Python sample implementation is included in the `Sample` directory, complementing the default _mapping_ and _settings_ files in `Default`.

To get a sense of how to use _fhir-parser_, take a look at these libraries:

- [**Swift-FHIR**][swift-fhir]
- [**fhirclient**][client-py]
- [fhir_model_generator][]


Tech Details
============

This parser still applies some tricks, stemming from the evolving nature of FHIR's profile definitions.
Some tricks may have become obsolete and should be cleaned up.

### How are property names determined?

Every “property” of a class, meaning every `element` in a profile snapshot, is represented as a `FHIRStructureDefinitionElement` instance.
If an element itself defines a class, e.g. `Patient.animal`, calling the instance's `as_properties()` method returns a list of `FHIRClassProperty` instances – usually only one – that indicates a class was found in the profile.
The class of this property is derived from `element.type`, which is expected to only contain one entry, in this matter:

- If _type_ is `BackboneElement`, a class name is constructed from the parent element (in this case _Patient_) and the property name (in this case _animal_), camel-cased (in this case _PatientAnimal_).
- If _type_ is `*`, a class for all classes found in settings` `star_expand_types` is created
- Otherwise, the type is taken as-is (e.g. _CodeableConcept_) and mapped according to mappings' `classmap`, which is expected to be a valid FHIR class.

> TODO: should `http://hl7.org/fhir/StructureDefinition/structuredefinition-explicit-type-name` be respected?


[license]: ./LICENSE.txt
[hl7]: http://hl7.org/
[fhir]: http://www.hl7.org/implement/standards/fhir/
[jinja]: http://jinja.pocoo.org/
[swift]: https://developer.apple.com/swift/
[swift-fhir]: https://github.com/smart-on-fhir/Swift-FHIR
[swift-smart]: https://github.com/smart-on-fhir/Swift-SMART
[client-py]: https://github.com/smart-on-fhir/client-py
[fhir_model_generator]: https://github.com/hsolbrig/fhir_model_generator
[R4]: http://hl7.org/fhir/R4
[R5]: http://build.fhir.org/R5
