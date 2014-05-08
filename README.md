= litehack =

Simple Django-based Web App for displaying battery and wifi status (written for LiteElements job application)

This implements an asynchronous design in that the hardware status is maintained in a DataBase table separately from the server process. This is accomplished with the hwupdate.py management command (which is just a loop that probes the hardware and updates the DataBase). The hwupdate loops with a period of 0.5seconds currently, but is configurable.

The web application then merely displays the information from the DataBase, and uses AJAX to keep the relevant sections of the HTML page up to date (currently 2 minute refresh for battery).

To use this, one must have the following installed:
 1. django
 1. acpi

This project makes use of the python-acpi parser project, but this is included as a submodule and so need not be manually installed.

== Quick start ==
 1. `python manage.py hwupdate start &`
 1. `python manage.py runserver 0.0.0.0:8000`
 1. point browser at http://localhost:8000/batteries
