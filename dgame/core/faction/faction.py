


class Faction:
    name = None
    shortname = None
    adjective = None
    colour = None
    pid = None

    def __init__(self,pid=pid):
        self.pid = pid


class KingdomofScotland:
    name = 'Kingdom of Scotland'
    shortname = 'scotland'
    adjective = 'scottish'
    colour = [0,0,190]


class KingdomofIreland:
    name = 'Kingdom of Ireland'
    shortname = 'ireland'
    adjective = 'irish'
    colour = [0,190,0]

REGISTER = [KingdomofIreland, KingdomofScotland]