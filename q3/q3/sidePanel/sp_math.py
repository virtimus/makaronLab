

from q3.ui.engine import qtw,qtc,qtg

#constexpr double scale(const double& valueIn, const double& baseMin, const double& baseMax, const double& limitMin, const double& limitMax)
#{
#    return ((limitMax - limitMin) * (valueIn - baseMin) / (baseMax - baseMin)) + limitMin;
#}


def scale(valueIn,baseMin, baseMax, limitMin, limitMax):
    return ((limitMax - limitMin) * (valueIn - baseMin) / (baseMax - baseMin)) + limitMin


#QPointF q_sp::lerp(const qreal t, const QPointF &a, const QPointF &b) {
#    return (1.0-t)*a + t*b;
#}

def lerpPoint(t,a,b:qtc.QPointF):
    return (1.0-t)*a + t*b


#QRectF q_sp::lerp(const qreal t, const QRectF &a, const QRectF &b) {
#    const QPointF topLeft   = lerp(t, a.topLeft(),     b.topLeft());
#    const QPointF bottRight = lerp(t, a.bottomRight(), b.bottomRight());
#    return QRectF(topLeft, bottRight);
#}
def lerp(t,a:qtc.QRectF,b:qtc.QRectF):
    topLeft   = lerpPoint(t, a.topLeft(),     b.topLeft())
    bottRight = lerpPoint(t, a.bottomRight(), b.bottomRight())
    return qtc.QRectF(topLeft, bottRight)

import time as t

class mTime():
    def __init__(self, ftime):
        self._ftime = ftime
        self._itime = int(ftime)

    #time_since_epoch().count()
    def count(self):
        return self._itime

    def time_since_epoch(self):
        return self

#std::chrono::system_clock::now();
def time():
    #return mTime(t.time())
    return t.time()

def timeSinceEpoch(tin):
    return tin #int(tin)?