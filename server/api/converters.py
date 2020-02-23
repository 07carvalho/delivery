
class FloatConverter:

    """This class is used to parse the URL params of latitude and longitude"""

    regex = '[-+]?\d*\.\d+|\d+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return '{}'.format(value)

