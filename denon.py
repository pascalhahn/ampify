#!/usr/bin/python

# Denon amp implementation

__author__ = 'Pascal Hahn <ph@lxd.bz>'

import ampify
import socket


class Denon3312(ampify.Amplifier):
  COMMANDS = {
      'Power': {
        'on': 'PWON',
        'off': 'PWSTANDBY'
        },
      'MasterVolume': {
        'up': 'MVUP',
        'down': 'MVDOWN',
        'set': 'MV%i',
        },
      'Mute': {
        'on': 'MUON',
        'off': 'MUOFF'
        },
      'Input': {
        'phono': 'SIPHONO',
        'cd': 'SICD',
        'tuner': 'SITUNER',
        'dvd': 'SIDVD',
        'bluray': 'SIBD',
        'tv': 'SITV',
        'cable': 'SISAT/CBL',
        'dvr': 'SIDVR',
        'game': 'SIGAME',
        'game2': 'SIGAME2',
        'v.aux': 'SIV.AUX',
        'dock': 'SIDOCK',
        'net_usb': 'SINET/USB',
        'lastfm': 'SILASTFM',
        'flickr': 'SIFLICKR',
        'favorites': 'SIFAVORITES',
        'iradio': 'SIIRADIO',
        'server': 'SISERVER',
        },
      'InputAndPlay': {
        'ipod': 'SIIPOD',
        'usb': 'SIUSB',
        'ipod_direct': 'SIIPD',
        'iradio': 'SIIRP',
        'favorites': 'SIFVR'
        },
      'MainZone': {
        'on': 'ZMON',
        'off': 'ZMOFF'
        },
      'SleepTimer': {
        'off': 'SLPOFF',
        'on': 'SL%i'
        },
      }

  def __init__(self, amp_ip):
    super(Denon3312, self).__init__(
        self.__class__.COMMANDS, 
        DenonIpConnector(amp_ip))


class DenonIpConnector(ampify.BaseConnector):
  def __init__(self, amp_ip, timeout=2, amp_port=23):
    self.amp_ip = amp_ip
    self.amp_port = amp_port
    self.timeout = timeout
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.amp_ip, self.amp_port))

  def execute(self, command):
    self.sock.send(command + '\r')

if __name__ == '__main__':
  myamp = Denon3312('192.168.94.220')
  import pdb
  pdb.set_trace()
