import cycgt
import cgt
import numpy as np
import unittest


class CyCgtTestCase(unittest.TestCase):
    def test_cycgt(self):
        x = cgt.vector('x')
        y = cgt.vector('y')
        z = y/x
        cs = cycgt.CallSequence([x,y],[z], list(cgt.topsorted([z])))

        xshp = (4,)
        yshp = (4,)
        zshp = (4,)

        xval = np.random.randn(*xshp).astype('float32')
        yval = np.random.randn(*yshp).astype('float32')
        zval = np.random.randn(*zshp).astype('float32')

        cs.set_shapes([xshp,yshp,zshp])
        cs.set_inputs([xval,yval])
        cs.execute()
        print(xval, yval)
        print(xval * yval)
        np.testing.assert_allclose(yval/xval , cs.get_outputs_numpy()[0])


if __name__ == "__main__":
    unittest.main()
