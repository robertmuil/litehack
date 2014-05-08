# litehack

Simple Django-based Web App for displaying battery and wifi status (written for LiteElements job application)

(NB: wifi status not yet implemented.)

This implements an asynchronous design in that the hardware status is maintained in a DataBase table separately from the server process. This is accomplished with the hwupdate.py management command (which is just a loop that probes the hardware and updates the DataBase). The hwupdate loops with a period of 0.5seconds currently, but is configurable.

The web application then merely displays the information from the DataBase, and uses AJAX to keep the relevant sections of the HTML page up to date (currently 2 minute refresh for battery).

The asynchronous aspect of the hardware querying is important to avoid the need for any HTML request from a client blocking on server IO. It also allows the IO to be conducted efficiently, doing system checks and file opens only when required rather than on each request, while also allowing the possibility for the HTML interface to be RESTful (RESTfulness is not guaranteed here, but is made more easy by the separation of concerns (splitting hardware access and HTML serving).

## Required packages
To use this, the following must be installed:
 1. `django`
 1. `acpi`

This project makes use of the python-acpi parser project, but this is included as a submodule and so need not be manually installed.

## Quick start
 1. clone this repository
 1. go into base litehack directory
 1. get the submodules (`git submodule update --init`)
 1. `python manage.py hwupdate start &`
 1. `python manage.py runserver 0.0.0.0:8000`
 1. point browser at http://localhost:8000/batteries
