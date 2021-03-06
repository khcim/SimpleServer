#!/usr/bin/python
# -*- coding=utf-8 -*-


__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import select


class Poll(object):

	READ = 0x01
	WRITE = 0x02
	ERROR = 0x04

	def poll(self, timeout):
		raise NotImplementedError

	def register(self, fd, events):
		raise NotImplementedError

	def unregister(self, fd):
		raise NotImplementedError

	def modify(self, fd, events):
		self.unregister(fd)
		self.register(fd, events)

	def close(self):
		raise NotImplementedError


class SelectPoll(Poll):

	def __init__(self):
		self._read_fds = set()
		self._write_fds = set()
		self._error_fds = set()

	def poll(self, timeout):
		readable, writeable, errors = select.select(self._read_fds,
		                                            self._write_fds,
		                                            self._error_fds,
		                                            timeout)
		events = {}
		for fd in readable:
			events[fd] = events.get(fd, 0) | SelectPoll.READ
		for fd in writeable:
			events[fd] = events.get(fd, 0) | SelectPoll.WRITE
		for fd in errors:
			events[fd] = events.get(fd, 0) | SelectPoll.ERROR

		return events.items()

	def register(self, fd, events):
		if fd in self._read_fds or fd in self._write_fds \
				or fd in self._error_fds:
			raise IOError("fd already registered")
		if events & SelectPoll.READ:
			self._read_fds.add(fd)
		if events & SelectPoll.WRITE:
			self._write_fds.add(fd)
		if events & SelectPoll.ERROR:
			self._error_fds.add(fd)
			self._read_fds.add(fd)

	def unregister(self, fd):
		self._read_fds.discard(fd)
		self._write_fds.discard(fd)
		self._error_fds.discard(fd)

	def close(self):
		pass