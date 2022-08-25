

"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta,datetime
import logging
import voluptuous
import json
from requests.structures import CaseInsensitiveDict
import requests
import pytz
from homeassistant import const
from homeassistant.helpers import entity
from homeassistant import util
from homeassistant.helpers import config_validation

_LOGGER = logging.getLogger(__name__)


DEFAULT_NAME = 'Espn_premier_league'
UPDATE_FREQUENCY = timedelta(seconds=1)


def setup_platform(
    hass,
    config,
    add_entities,
    discovery_info
):
    """Set up the Espn sensors."""
  
    add_entities([LivePremierLeagueSensor()],True)


class LivePremierLeagueSensor(entity.Entity):
    """Representation of a Espn sensor."""

    def __init__(self):
        """Initialize a new Espn sensor."""
        self._attr_name = " Live Premier League"
        self.event = None
       


    @property
    def icon(self):
        """Return icon."""
        return "mdi:bank"


    @util.Throttle(UPDATE_FREQUENCY)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        event=[]
    
        url = "https://star.content.edge.bamgrid.com/svc/content/CuratedSet/version/5.1/region/BR/audience/k-false,l-true/maturity/1850/language/en/setId/633fde36-78f6-4183-a304-99647a13eb51/pageSize/15/page/1"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer eyJ6aXAiOiJERUYiLCJraWQiOiJRVmxCQXpUeFUzMVRtNWVfZTIzams0dFpwRWJpRERteWp6MDNsSS1hRVVBIiwiY3R5IjoiSldUIiwiZW5jIjoiQzIwUCIsImFsZyI6ImRpciJ9..Ynhc5FHxOEgzvdEp.60DAguKWzuqMt5x3sqeDOwq7NfCEx0EsjnXymj26X3Mq-pUCEgC3Kp_hQySehZrQkz_hDzK_GsjsqMJJwmQgNGr0L9mFP5-SqA-1mW59jm1RXj0lnbxmf8o6MRm9CpU-envofgHtiqN8rpu_4F4Vj0sMF3Efzszxk0VIee70xN_d97GyUR5p1UT4yNedJj5BJmtaCJilJnYDBEVe4lUl6IqalnktIOFqyme2eWx1UPRIB2Jm1vzNgrj_bGI6RD74qp3pdaCoHNsPNftmFIMPOIfHVOGMk-F79Xwg4INQCmc3_URn6b_QfMUwwXy2kb7NOIBi7NC_gw2CMLEQMt5al18SpeYe6VurBUO8tl6PzwBdGf3qB0WbHi-mq5r3gHED9v4DBQJtx269MhnMMyCVIVrafeLaRZUASi2vgpU41y9rU1x-xWwRqrZ0tb1yqagKMZe0Z_nzKV_iVJc9aOjMQ6n4nrHyg_HNoXu-o3GuUzmna0KltTMOKxYVice_56CZOyMypaZ3cbOILYPQWD4nk6r6p9ziIbIlOa4IXVxZlRLqsuUXFbIBGq5-Oe_ll_xn0u1ULL-OXBe8M3pD_w7TSdcc0ZHDymAVabFnSJaQ0nrWx_RvRZQ94hpGUdKG1gSP-Lwg5fQb3pzZMuVQyyGZCAXKysI53lG1aOVWw6jLFRWFWYt3TSK00t2DGJg3Q-ZxI4X7RGcYvFRJOZm5jN8ELH4BPTTsd0q6bE9RMsFjsujA4at4NRYEd5ayk6Zn0bOKogpPubtj5_tMBvY1oyT7mmgC4CoHuE7wwhJH1lheMe6ewPzA0-WPDvsH1e4sjPuXconOr0ggk76Qp_Uk1ttzCxom0VTA6WA0tcu7ULiIZIKfeXSbAy76Jv_CTxCi9o_Rh0C021iZEWByQBybvOnVeqaxgITyS9wGejAE7uK-NQpuzMpHSeRELMKBQhO_XCAx1zbUxZch81xsPShDTYWaLRR6WcBdDPiPiJakzyMdhmuZ49ODUlrkf_TmKpxM8752QpFDF6mNa-dkJkWueMV2jJgIwwR3vSR_2Rjxt4KytpPNje4UkG88pT8sMovAorBFRRf7veCvr2q0eLBiOicIDGt1KvRNBVAQzLzJn9cx6pEqSHNTlkSJqKD9F_1YzBBShfowX2MEE1ggl-WaT4H2cUTfAzLv0eqHvLvNgIkqDDm9Ls9pTVUDIufAR6zhbn8L0JNpnk159dedZtfYLfNU_ZG82aAJJQfN_DTsh8RUHIwXk2BBwIA5YIy9lPZuwJAf-sylnWRjwdUzW8LD4y77xH1EGaFuR2l_a4jKjwibHMQ0lq3IhEoMn7YFEc4AisYcpztTay2B4sTt1YOmdxTEQmDQ3dvYvuKDqdvSZCObuJ-suIpJgpLJZYrFWoqniZUFsMsG3s2rEZ-B54RbKzPdH870CsQP7wzgO5oZD_NUDmV0y3hzlUH-V7pKH3YNMa5jKnDqESIxcgdjvk-5y7SAae8_MnJLkDJhtUWDthFHgBeq_bftmcv6CU0gGiQiXkcobVKGN6XApRk2j7QQQ00y3QYrB1ei5RGZJjKHrD2rKQrAaG8AaQND9g-RNYW5SpVTlmwc8Ncutc6bMT3qIM3NUrEQdFdH6r6EqE8VWJlJ_TX2r1lfd-YkvXRMgGZzp31t7z7WAFXMkkXVdZ2ePKb2uLV52AVmp7yJNy3nVRAi8X2hKZRgptkPm3czT7YN14QrGfGw434U2XkMPL6NjQtGJY03IvwVYNXYmeNov45sk9clxAb6ZewP3BkPn7_ZSDjd3UdcnVA8XSKRR3-M8JnU37gB4DcekLifJo4G7IXj4ibhAO-AAyW7RRU4yNBaQil3iLv-c4w4bZ1BroeBHV6oy6gfu7t6FxBAp0ax52JDV2fsoQkhVFUx5ZzA1D7GJ08iYE0DCWfjSybJqCKRyNa6wVFVq768iFz2FkS4I_gZJbxUiguLQPubNoUHhno_3aw_Dy8xX36oEM5hcfAHhn9XfEjWcicqFY5MBXAiPvEep-XtMBT3TIL6su7msDguM-esEl5YSZyKq-z3gxpwpJVsxWO1tDcz_F4KuCAfz_oqXZV9nm79me-vmbcsI1PAyiLSpTMvMXDJwkyeIFotNpzNZHHYOkHYqyqlELcBBVBy5GSGW2XIIygGzSQNd_5WO1KAIoCmQbqDvW_ePng61lS6MYFMIhRZEgvjBNnDj3fBwAvZcH41ipQljqrxOvoh2kHo0v-J4m05Wl1p2x2gGEZpUK5HjZIC32JfA5rcLrp_84KrujbXojgleOszXxC3PP1iRIQwpeewS5yk0r0iEgsnrF7B7ug_f96lzFIsfoH0CinCCCxi_d1haZ59_c6Nb5gQOnWoLzr4qWoxRLm9x90_UHlRjmux5UAE3QT28RkxAqhwcq2yNQkC1nSG9wDgIZ8vbsaiKIZetPjWg2wmck0vpDjvMoTAUXkdCttKSqrqcDnDFfB30PqKhpouesb5t44t4YQenafdAtNkGz62XIfuGnRH0iv3h1-eADyMDhoM78bgMe6bwV1hcCTeuIEk_nXhn22paM50Ssp4t6z11pszBiG_EynNsrQzzyWcwY8pr2JD3LE9fJWX7dR1Qyx66J8-THxfibOokgqEZHWUtGwhP69q-h9iMZq17PMhmbXLqC1_uTgxBn06dA6jieDDdeeiM7Nl9Na5_pSsWpn5ajgVYzWrH6ZKjoMsvw.Ih8Xbama0Odjgs3F8x8ORw"


        resp = requests.get(url, headers=headers)
        data  = resp.content
        data = json.loads(data)
        data = data['data']['CuratedSet']
    

        for items in data['items'][0:10]:
            today = datetime.today().strftime('%Y-%m-%d')
            matches_today = items['startDate'].replace('Z', '+00:00')
            matches_today = datetime.fromisoformat(matches_today).strftime('%Y-%m-%d')
            
            if matches_today == "2022-08-27" :  

                name = items['text']['title']['full']['program']['default']['content']
                encodedFamilyId =items['family']['encodedFamilyId']
                poster = items['image']['tile']['1.78']['program']['default']['url']
                date_z =items['startDate'].replace('Z', '+00:00') 
                date = datetime.fromisoformat(date_z)
                new_date = date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M')
                startDate = new_date

                data = {"event":{"name": name,"encodedFamilyId":'https://www.starplus.com/live-event/'+encodedFamilyId,"poster": poster,"startDate":startDate}}
                self.event.append(data)
                self.event.sort(key = lambda x:(x['event']["startDate"],x['event']["name"]))

        self.matches = self.espn.get_matches(league)
        
            


    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        self._attributes = {
            "Live_events": self.live,

        }
        return  self._attributes

  
