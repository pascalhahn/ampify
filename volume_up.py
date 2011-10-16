#!/usr/bin/python

import denon

if __name__ == '__main__':
  amp = denon.Denon3312('192.168.94.220')
  amp.MasterVolume.up()
