import mxdevtool as mx
import mxdevtool.termstructures as ts

class SampleMarketData(mx.MarketData):
    def __init__(self, data=None):
        mx.MarketData.__init__(self, data)

    # def get_quote(self, arg):
    #     # extract in [] ?
    #     # ex : irskrw[3m] -> irskrw , 3m
    #     return 0.02


class SampleMarketDataProvider(mx.MarketDataProvider):
    def __init__(self):
        self.sample_data = None
        self.initialize()

    def initialize(self):
        m = mx.MarketData()

        refDate = mx.Date(2021,1,5)

        m.quote['kospi2'] = 400
        m.quote['spx'] = 3700
        m.quote['cd91'] = 0.025
        m.quote['alpha1'] = 0.1
        
        zerocurve1 = { 
            'clsnm' : ts.ZeroYieldCurve.__name__,
            'refDate' : str(refDate),
            'periods': ['3m', '20Y'],
            'zeroRates': [0.03, 0.03],
            'interpolationType': 'Linear',
            'extrapolationType': 'FlatForward',
            'calendar': str(mx.SouthKorea()),
            'dayCounter': str(mx.Actual365Fixed()),
            'businessDayConvention': mx.businessDayConventionToString(mx.ModifiedFollowing),
            'compounding': mx.compoundingToString(mx.Compounded)
        }

        m.yieldCurve['zerocurve1'] = zerocurve1

        zerocurve2 = ts.ZeroYieldCurve(refDate, ['3m', '20Y'], [0.03, 0.03])
        m.yieldCurve['zerocurve2'] = zerocurve2.toDict()

        const_volTs1 = { 
            'clsnm' : ts.BlackConstantVol.__name__,
            'refDate' : str(refDate),
            'vol': 0.25,
            'calendar': str(mx.SouthKorea()),
            'dayCounter': str(mx.Actual365Fixed()),
        }

        m.volTs['const_volTs1'] = const_volTs1

        const_volTs2 = ts.BlackConstantVol(refDate, 0.25)
        m.volTs['const_volTs2'] = const_volTs2.toDict()

        self.sample_data = m

    def get_data(self, **kwargs):
        return self.sample_data