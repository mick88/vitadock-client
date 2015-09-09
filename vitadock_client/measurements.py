import datetime

__author__ = 'Michal'


class BaseMeasurement:
    id = None
    measurementDate = None
    updatedDate = None
    version = None
    active = True

    @property
    def measurement_date(self):
        """
        Measurement date as datetime object
        :return: datetime
        """
        return datetime.datetime.utcfromtimestamp(self.measurementDate / 1000)

    def __init__(self, **values):
        for key, value in values.iteritems():
            setattr(self, key, value)


class CardiodocksMeasurement(BaseMeasurement):
    systole = None
    diastole = None
    pulse = None
    type = None
    arrhythmic = 0
    systoleTargetMin = 0
    systoleTargetMax = 0
    diastoleTargetMin = 0
    diastoleTargetMax = 0
    pulseTargetMin = 0
    pulseTargetMax = 0

    def __unicode__(self):
        return u'{}/{}'.format(self.systole, self.diastole)
