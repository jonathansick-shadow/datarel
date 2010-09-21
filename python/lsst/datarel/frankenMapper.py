def makeFrankenMapper(torso, limb):
    '''
    Dynamically adds map_X methods from "limb" to the "torso".

    Calls to torso.map_X() will be delegated to "limb.map_X()".
    '''
    import types

    class Bolt(object):
        '''
        This is where the evil magic happens: we need a class in order
        to store a reference to the limb and its bound method.  This
        class has a __call__ method so is callable and can be turned
        into a class method of torso.
        '''
        def __init__(self, f):
            self.f = f
        def __call__(self, torso, *args, **kwargs):
            return self.f(*args, **kwargs)

    for t in limb.getDatasetTypes():
        fname = 'map_' + t
        # lf is a bound method (bound to limb)
        lf = getattr(limb, fname)
        # Now we make the torso's bound method...
        tf = types.MethodType(Bolt(lf), torso, torso.__class__)
        if hasattr(torso, fname):
            # You can override methods, but are you sure you want to?
            #print >> sys.stderr, 'in makeFrankenMapper: overriding method', fname, 'in', torso
            pass
        # And add it in.
        setattr(torso, fname, tf)
        #print 'Adding function', fname, 'to', torso
        #print 'tf:', tf

if __name__ == '__main__':
    from lsst.obs.cfht import CfhtMapper
    from lsst.datarel.plotMapper import PlotMapper
    import lsst.daf.persistence as dafPersist
    import os.path

    class TestMapper(dafPersist.Mapper):
        def __init__(self, root='.'):
            self.root = root
        def map_test(self, dataId):
            print 'map_test, dataId=', dataId
            return os.path.join(self.root, dataId['filename'])

    class TestMapper2(dafPersist.Mapper):
        def __init__(self, root='.'):
            self.root = root
        def map_test2(self, dataId):
            print 'map_test2, dataId=', dataId
            return os.path.join(self.root, dataId['filename'])


    cfht =  CfhtMapper()
    pm = PlotMapper()
    makeFrankenMapper(cfht, pm)
    cfht.map_plotdata(dict(filename='x'))
    tm = TestMapper()
    makeFrankenMapper(cfht, tm)
    X = cfht.map_test(dict(filename='x'))
    print 'map_test returned:', X
    X = cfht.map_plotdata(dict(filename='x'))
    print 'map_plotdata returned:', X
    X = cfht.map('plotdata', dict(data=3, filename='y'))
    print 'map_plotdata returned:', X
    X = cfht.map('test', dict(data=7, filename='z'))
    print 'map_test returned:', X
    print cfht.getDatasetTypes()

    # You can chain them too.
    tm1 = TestMapper()
    tm2 = TestMapper2()
    print 'Before: tm1 has', tm1.getDatasetTypes()
    print 'Before: tm2 has', tm2.getDatasetTypes()
    makeFrankenMapper(tm1, tm2)
    print 'After: tm1 has', tm1.getDatasetTypes()
    pm = PlotMapper()
    makeFrankenMapper(pm, tm1)
    print 'After: pm has', pm.getDatasetTypes()
    # Now pm has methods from tm1 and tm2.
    D = {'filename':'z', 'x':42}
    pm.map('test', D)
    pm.map('test2', D)
    pm.map('plotdata', D)

    
