from zope import interface
from zope import schema

class ISGShot(interface.Interface):
    sequence = schema.Int(
            title=u"Shot",
            description=u"sequence number of shot within the session",
            min=1)
    ball_speed = schema.Int(
            title=u"Ball Speed (mph)",
            description=u"Speed of ball",
            min=0)
    club_speed = schema.Int(
            title=u"Club Speed (mph)",
            description=u"Speed of club as it hits ball",
            min=0)
    launch_angle = schema.Float(
            title=u"Launch angle (deg)",
            description=u"Angle of ball launch vs ground",
            min=0.0)
    backspin = schema.Int(
            title=u"Back spin (rpm)",
            description=u"back spin on ball")
    sidespin = schema.Int(
            title=u"Sidespin (rpm)",
            description=u"Side spin on ball, negative numbers indicate right to left spin (draw hit for a right handed golfer)")
    carry_distance = schema.Int(
            title=u"Yards of carry",
            description=u"distance before ball hits ground",
            min=0)
    total_distance = schema.Int(
            title=u"Total yards",
            description=u"distance before ball hits ground",
            min=0)
    deviation = schema.Int(
            title=u"Deviation yards",
            description=u"Yards away from target line")

class ISGSession(interface.Interface):
    id = schema.TextLine(
            title=u"Session identity",
            description=u"Unique session identity",
            required=True,
            readonly=True)
    date = schema.Date(
            title=u"Date",
            description=u"Date of the session",
            required=True)
    club = schema.TextLine(
            title=u"Club",
            description=u"Club used in the session")
    duration = schema.Timedelta(
            title=u"Duration",
            description=u"Duration of the session")
    total_shots = schema.Int(
            title=u"Total shots",
            description=u"Number of shots taken during the session",
            min=1)
    shots = schema.List(
            title=u"Individual shots",
            description=u"List of ISGShot providers",
            value_type=schema.Object(schema=ISGShot),
            unique=True
            )
