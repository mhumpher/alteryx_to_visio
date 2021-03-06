# Alteryx to Visio

The purpose of this code is to convert the XML of an Alteryx workflow into a Visio diagram to automate documentation. 

Goals:
* Generate a Visio that replicates the tools and dependencies of the Alteryx workflow as a Visio diagram
* Generate a Visio that displays the links between source data through formula calculations and dependencies between calculations
  * Include a way to filter fields of interest using RegEx or selecting output fields to trace back to source
* Update a Visio while mantaining markup with updated version of Alteryx workflow

Difficulties:
* Formula Dependencies
  * Determining the links between formula definitions back to source data - XML provides a way of determine connections between tools, but we need connections between field names possibly separated by many tools
  * Determining renames between formula definitions
  
* Updating Visio
  * Matching tools to Visio shape objects - need to read Alteryx XML and Visio and determine one-to-one connections
  
* Working Ideas
  * Create Class for Tools with dictionaries of connections in and out
  * Create Class for Workflow with dictionary of tools
  * Create Class for Formulae with dictionary of dependencies
    * This needs to be a dependency to formula in another tool to trace back through tools
  
* Phases
  * Phase I: Establish Tools with properties
  * Phase II: Establish connections between tools
  * Phase III: Establish dependencies between tools of formula
    * Need to track formula, summarizing, filtering, renaming
    * Need to start from terminal tools and trace back to initial tools
 
