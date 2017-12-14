import cgt, numpy as np,numpy.random as nr
from cgt.tests import across_configs


@across_configs
def test_einsum():
    x = cgt.tensor3()
    y = cgt.tensor3()

    sizes = {'i':2,'j':3,'k':5,'l':7}
    xaxes = 'ijk'
    yaxes = 'ikl'
    zaxes = 'ijl'
    for i in range(10):
        xperm = xaxes
        (yperm,zperm) = permaxes = [[chars[i] for i in np.random.permutation(3)] for chars in [yaxes,zaxes]]
        desc = "%s,%s->%s"%tuple("".join(chars) for chars in [xperm] + permaxes)
        z = cgt.einsum(desc, x, y)
        xval = nr.randn(*(sizes[c] for c in xperm))
        yval = nr.randn(*(sizes[c] for c in yperm))
        np.testing.assert_allclose(
            cgt.numeric_eval(z, {x : xval, y : yval}),
            np.einsum(desc, xval, yval),
            atol={"single":1e-3,"double":1e-6}[cgt.get_precision()])


if __name__ == "__main__":
    import nose
    nose.runmodule()
