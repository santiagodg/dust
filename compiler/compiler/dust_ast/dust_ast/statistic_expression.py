from .plot_expression import PlotExpression
from .scatter_expression import ScatterExpression
from .histogram_expression import HistogramExpression
from .mean_expression import MeanExpression
from .median_expression import MedianExpression
from .mean_square_error_expression import MeanSquareErrorExpression
from .min_expression import MinExpression
from .max_expression import MaxExpression
from .standard_deviation_expression import StandardDeviationExpression
from .variance_expression import VarianceExpression
from .skewness_expression import SkewnessExpression
from .kurtosis_expression import KurtosisExpression
from .r_squared_expression import RSquaredExpression
from .sum_expression import SumExpression

class StatisticExpression:
    def __init__(
        self, 
        expression: PlotExpression 
            | ScatterExpression
            | HistogramExpression
            | MeanExpression
            | MedianExpression
            | MeanSquareErrorExpression
            | MinExpression
            | MaxExpression
            | StandardDeviationExpression
            | VarianceExpression
            | SkewnessExpression
            | KurtosisExpression
            | RSquaredExpression
            | SumExpression):

        self.__expression = expression

    def to_string(self, indent: int = 2, padding: int = 0) -> str:
        result: str = ''
        space_padding: str = ' ' * padding
        space_indent: str = ' ' * indent
        result += f'StatisticExpression:\n'
        expression_str: str = self.__expression.to_string(indent, padding + indent)
        result += f'{space_padding}{space_indent}expression: {expression_str}'
        return result

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = f'{type(self).__name__}('
        attr_str = []
        for key, value in vars(self).items():
            prefix = key.replace(f"_{type(self).__name__}", '')
            attr_str += [f'{prefix}={str(value)}']
        result += ','.join(attr_str)
        result += ')'
        return result
