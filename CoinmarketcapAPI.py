#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright (c) 2016-2018, Karbo developers (Lastick)
#
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from urlparse import urlparse
import urllib
import httplib
import json
from time import sleep
import sys

class CoinmarketcapAPI:

  socket_status = False
  api_status = False
  pairs = ['UAH', 'RUR', 'USD', 'EUR', 'BTC', 'XMR']
  api_url = 'https://api.coinmarketcap.com/v1/ticker/karbo/'
  user_agent = "KarboStatsMinibot/1.0"

  def __init__(self):
    pass

  def client(self, target = ''):
    buff = ''
    sub_url = ''
    self.socket_status = False
    try:
      o = urlparse(self.api_url)
      if (target != ''):
        sub_url = '?convert=' + target
      conn = httplib.HTTPSConnection(o.hostname, 443, timeout=15);
      headers = {"User-Agent": self.user_agent}
      sleep(0.07)
      conn.request("GET", o.path + sub_url, '', headers)
      res = conn.getresponse()
      if (res.status == 200):
        buff = res.read()
        self.socket_status = True
        conn.close()
    except Exception as e:
      self.socket_status = False
      print('-> Markets error: ' + str(e))
    return buff;

  def getTickers(self):
    res = []
    get_status_t = False
    for pair in self.pairs:
      price = 0.0
      get_status_t = False
      pair_data = self.client(pair)
      if (self.socket_status):
        try:
          json_obj = json.loads(pair_data)
          if (len(json_obj) == 1):
            ticker = json_obj[0]
            if ('id' in ticker):
              if (ticker['id'] == 'karbo'):
                price_str = 'price_' + pair.lower()
                if (price_str in ticker):
                  price = float(ticker[price_str])
                  get_status_t = True
        except:
          get_status_t = False
      res.append({'pair': pair, 'price': price})
    if (get_status_t):
      self.api_status = True
    else:
      self.api_status = False
    #print(res)
    return res

  def getInfo(self):
    res = {}
    get_status_t = False
    volume = 0.0
    market_cap = 0.0
    change = 0.0
    res = self.client()
    if (self.socket_status):
      try:
        json_obj = json.loads(res)
        if (len(json_obj) == 1):
          info = json_obj[0]
          if ('id' in info):
            if (info['id'] == 'karbo'):
              if ('24h_volume_usd' in info):
                volume = float(info['24h_volume_usd'])
              if ('market_cap_usd' in info):
                market_cap = float(info['market_cap_usd'])
              if ('percent_change_24h' in info):
                change = float(info['percent_change_24h'])
              get_status_t = True
      except:
        get_status_t = False
    if (get_status_t):
      self.api_status = True
    else:
      self.api_status = False
    res = {'volume': volume, 'market_cap': market_cap, 'change': change}
    #print(res)
    return res

  def getStatus(self):
    return self.api_status