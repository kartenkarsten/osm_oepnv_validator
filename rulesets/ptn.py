#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import stat
import datetime

from imposm.parser import OSMParser
from mako.lookup import TemplateLookup

import rlc
import rmc
import rvoc
import rn

class PublicTransportNetwork(rn.RouteNetwork, rvoc.RelationValidationOverviewCreator, rlc.RouteListCreator, rmc.RouteMapCreator):

	# used by rvoc, rlc and rmc
	# pattern for roles of nodes of routes
	# http://wiki.openstreetmap.org/wiki/Relation:route#Members
	route_node_roles_pattern = "^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$"

	# all valid keys for a relation (both, route or route_master)
	valid_keys = ["name", "network", "operator", "ref", "route_master", "route", "type", "from", "to", "via", "by_night", "wheelchair", "bus", "direction", "note", "fixme", "FIXME", "color", "colour", "service_times", "description", "wikipedia"]

	# keys that can't appear on a route_master
	invalid_keys_route_master = ["route", "from", "to", "via"]

	# keys that can't appear on a route
	invalid_keys_route = ["route_master"]

	# valid values for route attribute
	# http://wiki.openstreetmap.org/wiki/Relation:route#Core_values
	valid_route_values = ["bus", "trolleybus", "share_taxi", "train", "monorail", "subway", "tram", "ferry", "light_rail"]

	# valid values for route_master attribute
	valid_route_master_values = valid_route_values

	# pattern for roles of nodes of routes
	# http://wiki.openstreetmap.org/wiki/Relation:route#Members
	route_node_roles_pattern = "^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$"

	# pattern for roles of ways of routes that need to be connected to each other
	# http://wiki.openstreetmap.org/wiki/Relation:route#Members
	# TODO: remove platform, but allow as role
	route_way_roles_pattern = "^(|route|forward|backward|platform:[0-9]+|platform)$"

