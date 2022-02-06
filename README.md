# PYFINCH - Self Replicating and Evolving Programs. WIP!
Pyfinch is an attempt to create self-replicating an evolving computer programs.

This is a beginner's learning project.

Computer programs (Pyfinches) will be constructed out of custom instruction sets and compete for time and space. Mutation, self-replication, and recombination result in evolutionary traits being expressed.

Pyfinch is heavily inspired by [Tierra](https://github.com/acisternino/tierra) and [Avida](https://github.com/devosoft/avida).

## Current Progress
### terminal.py
This file contains the terminal interface used to run Pyfinch. However, components of Pyfinch would ideally be easy to incorporate into other project with the preprocessor file and finch file doing the bulk of the work.

### visual.py
This is a simple terminal aesthetic boost, as well as an easy template for messages and quick actions.

### preprocessor.py
This contains the parsing components of Pyfinch. Currently, it only supports one config file, that supports a single instruction set, and one type of organism. this will change soon. The methods in this file check the "lexome" of the organism for validity.

### pyfinches.py
This contains the classes for each pyfinch, and the virtual CPUs and various things to keep track of.

### lexome.py
This is the information for every single operation possible. This will need to be updated with various instruction sets, but instruction sets can be a subset of these.

### aviary.py
This is the "petri dish" where the pyfinches will live, breed, and die. 