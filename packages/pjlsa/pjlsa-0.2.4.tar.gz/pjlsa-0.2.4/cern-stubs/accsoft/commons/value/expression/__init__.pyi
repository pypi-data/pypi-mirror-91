from typing import ClassVar as _py_ClassVar
from typing import overload
import cern.accsoft.commons.value
import cern.accsoft.commons.value.operation
import cern.accsoft.commons.value.operation.factory
import cern.accsoft.commons.value.spi.operation
import java.lang
import java.util


class Expression:
    def evaluate(self, valueMap: 'ValueMap') -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...

class ExpressionParser:
    ADDITION_OPERATOR: _py_ClassVar[str] = ...
    SUBTRACTION_OPERATOR: _py_ClassVar[str] = ...
    MULTIPLICATION_OPERATOR: _py_ClassVar[str] = ...
    DIVISION_OPERATOR: _py_ClassVar[str] = ...
    EXPONENTIATION_OPERATOR: _py_ClassVar[str] = ...
    UNARY_NEGATION_OPERATOR: _py_ClassVar[str] = ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, operationFactory: cern.accsoft.commons.value.operation.factory.OperationFactory): ...
    @overload
    def parse(self) -> Expression: ...
    @classmethod
    @overload
    def parse(cls, string: str) -> Expression: ...

class ExpressionSyntaxException(java.lang.Exception):
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...
    @overload
    def __init__(self, throwable: java.lang.Throwable): ...

class ValueMap:
    @overload
    def get(self, string: str) -> cern.accsoft.commons.value.ImmutableValue: ...
    @overload
    def get(self, string: str, int: int) -> cern.accsoft.commons.value.ImmutableValue: ...

class BinaryOperationExpression(Expression):
    def __init__(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, expression: Expression, expression2: Expression): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class BooleanConstantExpression(Expression):
    @overload
    def __init__(self, boolean: bool): ...
    @overload
    def __init__(self, string: str): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class ConstantExpression(Expression):
    def __init__(self, double: float): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class FunctionBasedOperationExpression(Expression):
    def __init__(self, multiOperation: cern.accsoft.commons.value.operation.MultiOperation, list: java.util.List[Expression]): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class UnaryOperationExpression(Expression):
    @overload
    def __init__(self, mathFunction: cern.accsoft.commons.value.MathFunction, expression: Expression): ...
    @overload
    def __init__(self, unaryOperation: cern.accsoft.commons.value.operation.UnaryOperation, expression: Expression): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class ValueMapAdapter(ValueMap):
    def __init__(self): ...
    @overload
    def get(self, string: str) -> cern.accsoft.commons.value.ImmutableValue: ...
    @overload
    def get(self, string: str, int: int) -> cern.accsoft.commons.value.ImmutableValue: ...

class VariableExpression(Expression):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class VectorExpression(Expression):
    def __init__(self, list: java.util.List[Expression]): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...

class BinaryOperationFunctionExpression(BinaryOperationExpression):
    def __init__(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, expression: Expression, expression2: Expression): ...
    def toString(self) -> str: ...

class IndexedVariableExpression(VariableExpression):
    def __init__(self, expression: Expression, indexing: cern.accsoft.commons.value.spi.operation.Indexing): ...
    def evaluate(self, valueMap: ValueMap) -> cern.accsoft.commons.value.Value: ...
    def getVariableNames(self) -> java.util.List[str]: ...
    def toString(self) -> str: ...
