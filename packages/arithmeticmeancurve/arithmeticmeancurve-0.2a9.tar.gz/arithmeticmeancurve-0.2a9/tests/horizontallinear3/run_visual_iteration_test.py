import examplecurves
from arithmeticmeancurve import FrozenStdExtrapolation, VisualIterationTester, \
    MeanCurvePlotter, ArithmeticMeanCurve

test_family_name = "VerticalLinear1"
sample_curves = examplecurves.Static.create(family_name=test_family_name)

extrapolates = FrozenStdExtrapolation(use_previous_iteration=False, target_threshold=0.0001)
VisualIterationTester.plot_extrapolation_test(
    curves=sample_curves,
    extrapolates=extrapolates,
)

extrapolates = FrozenStdExtrapolation(use_previous_iteration=False, target_threshold=0.0001)
a_mean_curve = ArithmeticMeanCurve(sample_curves, method=extrapolates)
MeanCurvePlotter.test_plot_mean_curve(
    a_mean_curve,
    upper_title="Family of curves {}".format(test_family_name),
    lower_title="Focus on end points. X, Y distances may be distorted."
)