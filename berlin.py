#!/usr/bin/env python
# -*- coding: utf-8 -*-

# berlin.py - validation rules for public transport in Berlin

import re

from ptn import PublicTransportNetwork

class PublicTransportNetworkBerlin(PublicTransportNetwork):

	def __init__(self):

		self.route_validators.append(self.validate_name)
		self.route_master_validators.append(self.validate_name)
		self.route_validators.append(self.check_color)
		self.route_master_validators.append(self.check_color)

		self.text_region = "Berlin"
		self.text_filter = "All relations with (type=route or type=route_master) and network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH)."
		self.text_datasource = "berlin.osm.pbf from geofabrik.de"

	def relation_filter(self, relation):
		# defines which relations to validate
		osmid, tags, members = relation
		# for fast DEBUGGING:
		# Bus 100:
		# return osmid in [17697, 1900690, 1900691]
		# U 55:
		# return osmid in [58430, 2227743, 2227744]
		# U 2:
		# return osmid in [58428]
		# Bus 255:
		# return osmid in [1639447, 1990677, 1990676]
		return "network" in tags \
			and tags["network"] == "VBB" \
			and "operator" in tags \
			and (tags["operator"] == "BVG" or tags["operator"] == "S-Bahn Berlin GmbH") \
			and "type" in tags \
			and tags["type"] in ["route", "route_master"]

	def ignore_relation(self, relation):
		# defines which relations are excluded from validation
		osmid, tags, members = relation
		# don't try to validate "...linien in Berlin"-relations
		return osmid in [18812, 174283, 53181, 174255]

	def validate_name(self, relation):
		osmid, tags, members = relation

		if "type" not in tags or tags["type"] not in ["route", "route_master"]:
			return []
		key = tags["type"]

		if key not in tags:
			return []

		if "name" not in tags:
			return []

		if tags[key] == "bus" and not re.match("^Buslinie ", tags["name"]):
				return [("wrong_name", u'name does not match convention ("Buslinie ...")')]
		if tags[key] == "ferry" and not re.match(u"^Fähre ", tags["name"]):
				return [("wrong_name", u'name does not match convention ("Fähre ...")')]
		if tags[key] == "tram" and not re.match(u"^Straßenbahnlinie ", tags["name"]):
				return [("wrong_name", u'name does not match convention ("Straßenbahnlinie ...")')]
		if tags[key] == "subway" and not re.match(u"^U-Bahnlinie ", tags["name"]):
				return [("wrong_name", u'name does not match convention ("U-Bahnlinie ...")')]
		if tags[key] == "light_rail" and not re.match(u"^S-Bahnlinie ", tags["name"]):
				return [("wrong_name", u'name does not match convention ("U-Bahnlinie ...")')]

		return []

	def check_color(self, relation):
		osmid, tags, members = relation

		if "type" not in tags or tags["type"] not in ["route", "route_master"]:
			return []
		key = tags["type"]

		if key not in tags:
			return []

		# TODO: it actually should be "colour" instead of "color"!
		# http://wiki.openstreetmap.org/wiki/Key:colour
		if tags[key] in ["subway", "tram", "light_rail"] and "color" not in tags:
			return [("no_color", 'missing color=#... for %s' % tags[key])]

		if "color" in tags and not re.match("^#[a-fA-F0-9]{6}$", tags["color"]):
			return [("wrong_color", 'color should be specified as hexadecimal value like #ff0000')]

		return []

	def is_normal_bus(self, r):
		return (("route" in r[1] and r[1]["route"] == "bus") or \
				("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
				("ref" in r[1] and re.match("^[0-9]+$", r[1]["ref"]))

	def is_metro_bus(self, r):
		return (("route" in r[1] and r[1]["route"] == "bus") or \
				("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
				("ref" in r[1] and re.match("^M[0-9]+$", r[1]["ref"]))

	def is_express_bus(self, r):
		return (("route" in r[1] and r[1]["route"] == "bus") or \
				("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
				("ref" in r[1] and (re.match("^X[0-9]+$", r[1]["ref"])) or (r[1]["ref"] == "TXL"))

	def is_normal_tram(self, r):
		return (("route" in r[1] and r[1]["route"] == "tram") or \
				("route_master" in r[1] and r[1]["route_master"] == "tram")) and \
				("ref" in r[1] and re.match("^[0-9]+$", r[1]["ref"]))

	def is_metro_tram(self, r):
		return (("route" in r[1] and r[1]["route"] == "tram") or \
				("route_master" in r[1] and r[1]["route_master"] == "tram")) and \
				("ref" in r[1] and re.match("^M[0-9]+$", r[1]["ref"]))

	def is_ubahn(self, r):
		return (("route" in r[1] and r[1]["route"] == "subway") or \
				("route_master" in r[1] and r[1]["route_master"] == "subway")) and \
				("ref" in r[1] and re.match("^U[0-9]+$", r[1]["ref"]))

	def is_sbahn(self, r):
		return (("route" in r[1] and r[1]["route"] == "light_rail") or \
				("route_master" in r[1] and r[1]["route_master"] == "light_rail")) and \
				("ref" in r[1] and re.match("^S[0-9]+$", r[1]["ref"]))

	def is_s_or_u_bahn(self, r):
		return self.is_sbahn(r) or self.is_ubahn(r)

