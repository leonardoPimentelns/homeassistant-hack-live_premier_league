

"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta,datetime
from distutils.command.config import config
import logging
from multiprocessing import Event
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


DEFAULT_NAME = 'MatchDay'
UPDATE_FREQUENCY = timedelta(minutes=10)

TOKEN ="your token"
PLATFORM_SCHEMA = config_validation.PLATFORM_SCHEMA.extend(
    {
        voluptuous.Required(TOKEN): config_validation.string
       

    }
)


def setup_platform(
    hass,
    config,
    add_entities,
    discovery_info
):
    """Set up the Espn sensors."""
  
    add_entities([MatchDaySensor(config)],True)


class MatchDaySensor(entity.Entity):
    """Representation of a Espn sensor."""

    def __init__(self,config):
        """Initialize a new Espn sensor."""
        self._attr_name = "MatchDay"
        self.live_event = None
        self.config = config
       


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
    
        url = "https://star.content.edge.bamgrid.com/svc/content/CuratedSet/version/5.1/region/BR/audience/k-false,l-true/maturity/1850/language/en/setId/9b5397d8-d4fc-4d63-bacf-58295ef465ff/pageSize/15/page/1"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = self.config[TOKEN] 

        
        resp = requests.get(url, headers=headers)
        data  = resp.content
        data = json.loads(data)
        data = data['data']['CuratedSet']
    

        for items in data['items'][0:10]:
            today = datetime.today().strftime('%Y-%m-%d')
            matches_today = items['startDate'].replace('Z', '+00:00')
            matches_today = datetime.fromisoformat(matches_today).strftime('%Y-%m-%d')
            
            if matches_today == "2022-08-27" :  

                league =items['league']['text']['name']['full']['league']['default']['content']
                name = items['text']['title']['full']['program']['default']['content']
                encodedFamilyId =items['family']['encodedFamilyId']
                poster = items['image']['tile']['1.78']['program']['default']['url']
                date_z =items['startDate'].replace('Z', '+00:00') 
                date = datetime.fromisoformat(date_z)
                start_date = date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%m/%d')
                start_time = date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M')
            

                data = {"event":{"league": league,"name": name,"encodedFamilyId":'https://www.starplus.com/live-event/'+encodedFamilyId,"poster": poster,"start_date":start_date,"start_time":start_time}}
                event.append(data)
                event.sort(key = lambda x:(x['event']["start_date"],x['event']["name"]))
                self.live_event = event

        self.matches = ""
        
            


    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        self._attributes = {
            "Live_events": self.live_event,

        }
        return  self._attributes

  
