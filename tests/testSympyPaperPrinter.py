import sympy as sy
import math as math
from sympy.core import evaluate
import os
import sys
sys.path.insert(1, os.path.dirname(sys.path[0])) # need to import 1 directories up (so spp is a subfolder)
import sympyPaperPrinter as spp
import unittest
from datetime import datetime

class CustomStdout():
    def __init__(self, start_time=None):
        self.stdout = sys.stdout
        self.start_time = start_time or datetime.now()
        self.log = []

    def write(self, text):
        elapsed = datetime.now() - self.start_time

        text = text.rstrip()
        if len(text) == 0:
            return

        elapsed_str = '[%d.%03d seconds]' % (elapsed.seconds, elapsed.microseconds / 1000.)
        self.stdout.write('%s %s\n' % (elapsed_str, text))
        self.log.append(text)

class testSympyPaperPrinterClass(unittest.TestCase) :
    def testSilentMarkdown(self) :
        orgOut = sys.stdout
        try :
            customOut = CustomStdout()
            sys.stdout = customOut
            someMdString = "Print $a=5$"
            spp.printMarkdown(someMdString)
            assert someMdString in customOut.log
            spp.silent = True
            customOut.log = []
            spp.printMarkdown(someMdString)
            assert not someMdString in customOut.log
        finally :
            sys.stdout = orgOut
    
    def testFilteringOfSympyFunctionArguments(self) :
        x = sy.Symbol('x')
        y = sy.Symbol('y')
        t = sy.Symbol('t')
        z = sy.Function('z')(t)
        testExpression = sy.Function("g")(x,y,t)*sy.cos(x)*sy.Derivative(z, t)
        cleanedExpression = spp.cleanOutUnwantedArguments(testExpression, [x,t])

        print(cleanedExpression)
        expectedExpression = sy.Function("g")(y)*sy.cos(x)*sy.Derivative(z, t)
        assert str(cleanedExpression) == "g(y)*cos(x)*Derivative(z(t), t)"
        assert cleanedExpression == expectedExpression

    def testConvertingTimeDerivativesToDots(self):
        t = sy.Symbol('t')
        x = sy.Symbol('x')
        y = sy.Symbol('y')
        z = sy.Function('z')(t,x)
        dzdt =z.diff(t)
        ddzdtt = z.diff(t).diff(t)
        testExpression = z*dzdt*ddzdtt*y
        cleanedExpression = spp.convertTimeDerivativeToDotSymbol(testExpression)
        zS = sy.Symbol('z')
        expectedSymbol = zS*sy.Symbol(r'\dot{z}')*sy.Symbol(r'\ddot{z}')*y
        assert expectedSymbol == cleanedExpression
      

