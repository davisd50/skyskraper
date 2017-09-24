from zope import interface
from zope.schema.fieldproperty import FieldProperty
from . import ISGShot

@interface.implementer(ISGShot)
class SGShotFromBSTrSpec(object):
    sequence = FieldProperty(ISGShot['sequence'])
    ball_speed = FieldProperty(ISGShot['ball_speed'])
    club_speed = FieldProperty(ISGShot['club_speed'])
    launch_angle = FieldProperty(ISGShot['launch_angle'])
    backspin = FieldProperty(ISGShot['backspin'])
    sidespin = FieldProperty(ISGShot['sidespin'])
    carry_distance = FieldProperty(ISGShot['carry_distance'])
    total_distance = FieldProperty(ISGShot['total_distance'])
    deviation = FieldProperty(ISGShot['deviation'])
    
    def __repr__(self):
        return u"{}".format(self.__dict__)
    
    def __init__(self, context):
        for i, td_tag in enumerate(context.find_all('td', recursive=False)):
            if i == 0: self.sequence = int(td_tag.text)
            if i == 1: self.ball_speed = int(td_tag.text)
            if i == 2: self.club_speed = int(td_tag.text)
            if i == 3: self.launch_angle = float(td_tag.text)
            if i == 4: self.backspin = int(td_tag.text)
            if i == 5: self.sidespin = int(td_tag.text)
            if i == 6: self.carry_distance = int(td_tag.text)
            if i == 7: self.total_distance = int(td_tag.text)
            if i == 8: self.deviation = int(td_tag.text)
