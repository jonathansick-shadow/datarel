import os.path
import lsst.daf.persistence as dafPersist

class PlotMapper(dafPersist.Mapper):
    def __init__(self, root='.'):
        self.root = root

    def map_plotdata(self, dataId):
        print 'dataId is', dataId
        fn = dataId.get('filename', 'plotdata.pickle')
        path = os.path.join(self.root, fn)
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
    
