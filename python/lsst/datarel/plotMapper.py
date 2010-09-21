import os
import lsst.daf.persistence as dafPersist

class PlotMapper(dafPersist.Mapper):
    def __init__(self, filepattern=None):
        self.pattern = filepattern

    def map_plotdata(self, dataId):
        print 'PlotMapper.map_plotdata: dataId is', dataId
        print '(self is', self, ')'
        print 'filename pattern is', self.pattern
        path = self.pattern % dataId
        print 'Writing to path', path
        dirnm = os.path.dirname(path)
        if not os.path.exists(dirnm):
            os.makedirs(dirnm)
        return dafPersist.ButlerLocation(
            None, None, 'PickleStorage', path, dataId)



def testPlotMapper():
    plotbase = 'plotbase'
    pbf = dafPersist.ButlerFactory(mapper=PlotMapper(
        root=plotbase))
    plotButler = pbf.create()

    D = {'test':'ing'}
    print 'D is', D
    fn='D'
    plotButler.put(D, 'plotdata', filename=fn)

    X = plotButler.get('plotdata', filename=fn)
    print 'X is', X

if __name__ == '__main__':
    testPlotMapper()
    
