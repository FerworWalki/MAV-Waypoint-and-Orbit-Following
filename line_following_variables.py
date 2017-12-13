class LineFollowingVariables(object):
    """ r- origin of path
        r.d - north coordinate
        r.e - east coordinate
        r.d - down coordinate
    """
    class r(object):    
        n = 0.0
        e = 0.0
        d = 0.0
        
    """ q -  unit vector describing direction of travel
        q.d - north coordinate
        q.e - east coordinate
        q.d - down coordinate
    """
    class q(object):
        n = 0.0
        e = 0.0
        d = 0.0
