from zope import interface
from zope.schema.fieldproperty import FieldProperty
import datetime
from bs4 import BeautifulSoup
from . import ISGSession
from .shot import SGShotFromBSTrSpec

@interface.implementer(ISGSession)
class SGSessionFromBSDivSpec(object):
    id = FieldProperty(ISGSession['id'])
    date = FieldProperty(ISGSession['date'])
    club = FieldProperty(ISGSession['club'])
    duration = FieldProperty(ISGSession['duration'])
    total_shots = FieldProperty(ISGSession['total_shots'])
    
    def __repr__(self):
        return u"{}".format(self.__dict__)
    
    def __init__(self, context):
        headerView = context.find('div', class_='headerView')
        stat = context.find('div', class_='stat')
        swing = context.find('div', class_='swing')
        
        self.id = self._text(context['id'])
        self.date = self._get_date_from_headerView(headerView)
        self.club = self._text(headerView.find('span', class_='club').string)
        self.duration = self._get_timedelta_from_headerView(headerView)
        self.total_shots = int(headerView.find('span', class_='session-total-shot').text.split()[-1])
        
        swing_details = swing.find('div', class_='swings-details-table')
        tbody = swing_details.find('tbody')
        self.shots = [SGShotFromBSTrSpec(tr) for tr in tbody.find_all('tr')]
        
    def _text(self, bs_string):
        """Return a html special chars converted string"""
        return u"{}".format(list(BeautifulSoup(bs_string, 'html.parser').stripped_strings)[0])
    
    def _get_date_from_headerView(self, headerView):
        date_string = u"{}".format(headerView.find('div', class_='club').string)
        m,d,y = date_string.split(sep=" ")
        if len(d) < 2:
            d = '0'+d
        dt = datetime.datetime.strptime(u"{} {} {}".format(m,d,y), '%b %d %Y')
        return datetime.date(year=dt.year, month=dt.month, day=dt.day)
    
    def _get_timedelta_from_headerView(self, headerView):
        duration = headerView.find('span', class_='session-duration')
        splits = duration.text.split(" ")
        for i, v in enumerate(splits):
            if v[-1] == 'h':
                hours = int(v[:-1])
            if v == 'min':
                minutes = int(splits[i-1])
        return datetime.timedelta(hours=hours, minutes=minutes)
                