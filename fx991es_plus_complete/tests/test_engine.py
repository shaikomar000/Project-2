import unittest
from calculator_engine import CalculatorEngine, CalculatorError

class EngineTests(unittest.TestCase):
    def setUp(self): self.c=CalculatorEngine()
    def test_arithmetic(self): self.assertEqual(self.c.calculate('2+3*4'),14)
    def test_degrees(self): self.assertAlmostEqual(self.c.calculate('sin(30)'),.5,places=10)
    def test_radians(self):
        self.c.angle_mode='RAD'; self.assertAlmostEqual(self.c.calculate('sin(pi/2)'),1,places=10)
    def test_factorial(self): self.assertEqual(self.c.calculate('factorial(5)'),120)
    def test_zero_division(self):
        with self.assertRaises(CalculatorError): self.c.calculate('1/0')
    def test_fraction(self): self.assertEqual(self.c.fraction(.75),'3/4')
    def test_stats(self): self.assertEqual(self.c.stats('1,2,3,4')['Mean'],2.5)
    def test_matrix(self): self.assertEqual(self.c.matrix('[[1,2],[3,4]]','determinant'),'-2')
    def test_equation(self): self.assertIn('x1 = 2',self.c.solve('x**2-5*x+6=0'))
    def test_calculus(self): self.assertIn('Derivative: 2*x',self.c.calculus('x**2',point='3'))

if __name__=='__main__': unittest.main()
