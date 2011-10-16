#!/usr/bin/python

# API to control amplifiers

__author__ = 'Pascal Hahn <ph@lxd.bz>'

import re

class Error(Exception):
  """module level error"""


class InvalidDataError(Error):
  """Input data is invalid."""


class UsageError(Error):
  """Usage error."""


class Amplifier(object):
  def __init__(self, commands_dict, connector, add_commands=True):
    self.connector = connector
    if add_commands:
      self.add_commands_from_dict(commands_dict)

  def add_commands_from_dict(self, commands_dict, group=None):
    for name, cmd in commands_dict.iteritems():
      # If we have to add a group
      if isinstance(cmd, dict):
        if group:
          # This could be done, just too lazy to work on this for now.
          raise InvalidDataError('No nested groups are allowed.')
        self.add_commands_from_dict(cmd, group=name)
        continue

      command = Command(name, cmd, self.connector)
      if group:
        if not self.has_group(group):
          self.add_group_by_name(group)
        groupobj = getattr(self, group)
        groupobj.add_command(command)
        continue
      self.add_command(command)

  def add_command(self, command):
    setattr(self, command.name, command)

  def has_group(self, group_name):
    groupobj = getattr(self, group_name, None)
    if groupobj:
      if not isinstance(groupobj, CommandGroup):
        raise InvalidDataError(
          '%s is already existing and not a CommandGroup but a %s' % (
            group_name, type(groupobj)))
      return True
    return False

  def add_group_by_name(self, group_name):
    setattr(self, group_name, CommandGroup(group_name))


class Command(object):
  SUPPORTED_SUBSTITUTES = ['%s', '%i']
  def __init__(self, name, command, connector):
    self.name = name
    self.command = command
    self.connector = connector

  def get_subst_count(self, command):
    return len(re.findall('|'.join(self.__class__.SUPPORTED_SUBSTITUTES),
      command))

  def execute(self):
    self.connector.execute(self.command)

  def __call__(self, *args):
    if len(args) != self.get_subst_count(self.command):
      raise UsageError(
          '%s requires %i parameters, %i given' % (
            self.command, self.get_subst_count(self.command),
            len(args)))
    self.connector.execute(self.command % args)


class CommandGroup(object):
  def __init__(self, name):
    self.name = name

  def add_command(self, command):
    setattr(self, command.name, command)

  def add_commands(self, commands):
    for command in commands:
      self.add_command(command)


class BaseConnector(object):
  def execute(self, command):
    raise NotImplementedError(
      'You at least have to implement execute for a connector')
