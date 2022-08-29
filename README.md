# MicroSpace
MicroSpace is an open source framework for developing microservice satellites and ground systems

Developed by the InSECTS team at Johns Hopkins University, Andrew, Julia, Hunter, and Ryan

# Overview
The repository here contains three main components, a ground system, a satellite system, and common libraries used by both. Both the ground system and the satellite system are developed to be cloud native in a microservice approach. Within the architecture, every software application deployed and running is containerized and managed by K3S Rancher. Each containerized application is known as either a service or an app, where services are necessary to running the digital ecosystem, and apps are user developed containerized software applications. Both apps and services are built, deployed, and managed the same.


# Setup
Development can proceed in a cloud environment, local virtual machine, or on local hardware. This guide will help the user setup the development environment on a local virtual machine.

1. Download and install a virtual machine client such as virtualbox
2. Download a Linux distro to virtualize. Ubuntu 20 was tested and used during this project.
