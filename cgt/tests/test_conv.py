import numpy as np
import cgt
from cgt import nn
from cgt.tests import across_configs
from nose.plugins.skip import SkipTest

@across_configs()
def test_conv():
    try:
        import scipy.signal
    except ImportError:
        raise SkipTest("skipping because we don't have ndimage")

    np.random.seed(0)
    x = np.random.randn(2,2,5,17)
    filt = np.random.randn(3,2,4,7)

    filtrows = filt.shape[2]
    filtcols = filt.shape[3]

    batchsize = x.shape[0]
    outchans = filt.shape[0]

    out = np.zeros((batchsize,outchans,x.shape[2]+filtrows-1,x.shape[3]+filtcols-1))
    for b in range(x.shape[0]):
        for inchan in range(x.shape[1]):
            for outchan in range(outchans):
                out[b,outchan] += scipy.signal.convolve2d(x[b,inchan],filt[outchan,inchan][::-1,::-1],mode='full')

    f = cgt.function([], nn.conv2d(cgt.constant(x), cgt.constant(filt), kernelshape=(filtrows,filtcols), pad=(filtrows-1, filtcols-1)))
    out1 = f()
    # out1 = cgt.numeric_eval1(nn.conv2d(cgt.constant(x), cgt.constant(f), kersize=(filtrows,filtcols)), {})
    np.testing.assert_allclose(out, out1, atol={"single":1e-3,"double":1e-6}[cgt.get_precision()])

if __name__ == "__main__":
    import nose
    nose.runmodule()