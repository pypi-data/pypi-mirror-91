import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections import namedtuple
import pathlib
import numpy as np
import pandas as pd
import sympy
from sympy import sympify, Symbol, lambdify
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import warnings


global_equation_file = 'hall_of_fame.csv'
global_n_features = None
global_variable_names = []
global_extra_sympy_mappings = {}

sympy_mappings = {
    'div':  lambda x, y : x/y,
    'mult': lambda x, y : x*y,
    'sqrtm':lambda x    : sympy.sqrt(abs(x)),
    'square':lambda x   : x**2,
    'cube': lambda x    : x**3,
    'plus': lambda x, y : x + y,
    'sub':  lambda x, y : x - y,
    'neg':  lambda x    : -x,
    'pow':  lambda x, y : sympy.sign(x)*abs(x)**y,
    'cos':  lambda x    : sympy.cos(x),
    'sin':  lambda x    : sympy.sin(x),
    'tan':  lambda x    : sympy.tan(x),
    'cosh': lambda x    : sympy.cosh(x),
    'sinh': lambda x    : sympy.sinh(x),
    'tanh': lambda x    : sympy.tanh(x),
    'exp':  lambda x    : sympy.exp(x),
    'acos': lambda x    : sympy.acos(x),
    'asin': lambda x    : sympy.asin(x),
    'atan': lambda x    : sympy.atan(x),
    'acosh':lambda x    : sympy.acosh(x),
    'asinh':lambda x    : sympy.asinh(x),
    'atanh':lambda x    : sympy.atanh(x),
    'abs':  lambda x    : abs(x),
    'mod':  lambda x, y : sympy.Mod(x, y),
    'erf':  lambda x    : sympy.erf(x),
    'erfc': lambda x    : sympy.erfc(x),
    'logm': lambda x    : sympy.log(abs(x)),
    'logm10':lambda x    : sympy.log10(abs(x)),
    'logm2': lambda x    : sympy.log2(abs(x)),
    'log1p': lambda x    : sympy.log(x + 1),
    'floor': lambda x    : sympy.floor(x),
    'ceil': lambda x    : sympy.ceil(x),
    'sign': lambda x    : sympy.sign(x),
    'round': lambda x    : sympy.round(x),
}

def pysr(X=None, y=None, weights=None,
            procs=4,
            populations=None,
            niterations=100,
            ncyclesperiteration=300,
            binary_operators=["plus", "mult"],
            unary_operators=["cos", "exp", "sin"],
            alpha=0.1,
            annealing=True,
            fractionReplaced=0.10,
            fractionReplacedHof=0.10,
            npop=1000,
            parsimony=1e-4,
            migration=True,
            hofMigration=True,
            shouldOptimizeConstants=True,
            topn=10,
            weightAddNode=1,
            weightInsertNode=3,
            weightDeleteNode=3,
            weightDoNothing=1,
            weightMutateConstant=10,
            weightMutateOperator=1,
            weightRandomize=1,
            weightSimplify=0.01,
            perturbationFactor=1.0,
            nrestarts=3,
            timeout=None,
            extra_sympy_mappings={},
            equation_file=None,
            test='simple1',
            verbosity=1e9,
            maxsize=20,
            fast_cycle=False,
            maxdepth=None,
            variable_names=[],
            batching=False,
            batchSize=50,
            select_k_features=None,
            warmupMaxsize=0,
            constraints={},
            useFrequency=False,
            tempdir=None,
            delete_tempfiles=True,
            limitPowComplexity=False, #deprecated
            threads=None, #deprecated
            julia_optimization=3,
        ):
    """Run symbolic regression to fit f(X[i, :]) ~ y[i] for all i.
    Note: most default parameters have been tuned over several example
    equations, but you should adjust `threads`, `niterations`,
    `binary_operators`, `unary_operators` to your requirements.

    :param X: np.ndarray or pandas.DataFrame, 2D array. Rows are examples,
        columns are features. If pandas DataFrame, the columns are used
        for variable names (so make sure they don't contain spaces).
    :param y: np.ndarray, 1D array. Rows are examples.
    :param weights: np.ndarray, 1D array. Each row is how to weight the
        mean-square-error loss on weights.
    :param procs: int, Number of processes (=number of populations running).
    :param populations: int, Number of populations running; by default=procs.
    :param niterations: int, Number of iterations of the algorithm to run. The best
        equations are printed, and migrate between populations, at the
        end of each.
    :param ncyclesperiteration: int, Number of total mutations to run, per 10
        samples of the population, per iteration.
    :param binary_operators: list, List of strings giving the binary operators
        in Julia's Base, or in `operator.jl`.
    :param unary_operators: list, Same but for operators taking a single `Float32`.
    :param alpha: float, Initial temperature.
    :param annealing: bool, Whether to use annealing. You should (and it is default).
    :param fractionReplaced: float, How much of population to replace with migrating
        equations from other populations.
    :param fractionReplacedHof: float, How much of population to replace with migrating
        equations from hall of fame.
    :param npop: int, Number of individuals in each population
    :param parsimony: float, Multiplicative factor for how much to punish complexity.
    :param migration: bool, Whether to migrate.
    :param hofMigration: bool, Whether to have the hall of fame migrate.
    :param shouldOptimizeConstants: bool, Whether to numerically optimize
        constants (Nelder-Mead/Newton) at the end of each iteration.
    :param topn: int, How many top individuals migrate from each population.
    :param nrestarts: int, Number of times to restart the constant optimizer
    :param perturbationFactor: float, Constants are perturbed by a max
        factor of (perturbationFactor*T + 1). Either multiplied by this
        or divided by this.
    :param weightAddNode: float, Relative likelihood for mutation to add a node
    :param weightInsertNode: float, Relative likelihood for mutation to insert a node
    :param weightDeleteNode: float, Relative likelihood for mutation to delete a node
    :param weightDoNothing: float, Relative likelihood for mutation to leave the individual
    :param weightMutateConstant: float, Relative likelihood for mutation to change
        the constant slightly in a random direction.
    :param weightMutateOperator: float, Relative likelihood for mutation to swap
        an operator.
    :param weightRandomize: float, Relative likelihood for mutation to completely
        delete and then randomly generate the equation
    :param weightSimplify: float, Relative likelihood for mutation to simplify
        constant parts by evaluation
    :param timeout: float, Time in seconds to timeout search
    :param equation_file: str, Where to save the files (.csv separated by |)
    :param test: str, What test to run, if X,y not passed.
    :param maxsize: int, Max size of an equation.
    :param maxdepth: int, Max depth of an equation. You can use both maxsize and maxdepth.
        maxdepth is by default set to = maxsize, which means that it is redundant.
    :param fast_cycle: bool, (experimental) - batch over population subsamples. This
        is a slightly different algorithm than regularized evolution, but does cycles
        15% faster. May be algorithmically less efficient.
    :param variable_names: list, a list of names for the variables, other
        than "x0", "x1", etc.
    :param batching: bool, whether to compare population members on small batches
        during evolution. Still uses full dataset for comparing against
        hall of fame.
    :param batchSize: int, the amount of data to use if doing batching.
    :param select_k_features: (None, int), whether to run feature selection in
        Python using random forests, before passing to the symbolic regression
        code. None means no feature selection; an int means select that many
        features.
    :param warmupMaxsize: int, whether to slowly increase max size from
        a small number up to the maxsize (if greater than 0).
        If greater than 0, says how many cycles before the maxsize
        is increased.
    :param constraints: dict of int (unary) or 2-tuples (binary),
        this enforces maxsize constraints on the individual
        arguments of operators. E.g., `'pow': (-1, 1)`
        says that power laws can have any complexity left argument, but only
        1 complexity exponent. Use this to force more interpretable solutions.
    :param useFrequency: bool, whether to measure the frequency of complexities,
        and use that instead of parsimony to explore equation space. Will
        naturally find equations of all complexities.
    :param julia_optimization: int, Optimization level (0, 1, 2, 3)
    :param tempdir: str or None, directory for the temporary files
    :param delete_tempfiles: bool, whether to delete the temporary files after finishing
    :returns: pd.DataFrame, Results dataframe, giving complexity, MSE, and equations
        (as strings).

    """
    if threads is not None:
        raise ValueError("The threads kwarg is deprecated. Use procs.")
    if limitPowComplexity:
        raise ValueError("The limitPowComplexity kwarg is deprecated. Use constraints.")
    if maxdepth is None:
        maxdepth = maxsize
    if equation_file is None:
        date_time = datetime.now().strftime("%Y-%m-%d_%H%M%S.%f")[:-3]
        equation_file = 'hall_of_fame_' + date_time + '.csv'

    if isinstance(X, pd.DataFrame):
        variable_names = list(X.columns)
        X = np.array(X)

    use_custom_variable_names = (len(variable_names) != 0)

    if len(X.shape) == 1:
        X = X[:, None]

    # Check for potential errors before they happen
    assert len(unary_operators) + len(binary_operators) > 0
    assert len(X.shape) == 2
    assert len(y.shape) == 1
    assert X.shape[0] == y.shape[0]
    if weights is not None:
        assert len(weights.shape) == 1
        assert X.shape[0] == weights.shape[0]
    if use_custom_variable_names:
        assert len(variable_names) == X.shape[1]


    if len(X) > 10000 and not batching:
        warnings.warn("Note: you are running with more than 10,000 datapoints. You should consider turning on batching (https://pysr.readthedocs.io/en/latest/docs/options/#batching). You should also reconsider if you need that many datapoints. Unless you have a large amount of noise (in which case you should smooth your dataset first), generally < 10,000 datapoints is enough to find a functional form with symbolic regression. More datapoints will lower the search speed.")

    if select_k_features is not None:
        selection = run_feature_selection(X, y, select_k_features)
        print(f"Using features {selection}")
        X = X[:, selection]

        if use_custom_variable_names:
            variable_names = [variable_names[selection[i]] for i in range(len(selection))]

    if populations is None:
        populations = procs

    if isinstance(binary_operators, str): binary_operators = [binary_operators]
    if isinstance(unary_operators, str): unary_operators = [unary_operators]

    if X is None:
        if test == 'simple1':
            eval_str = "np.sign(X[:, 2])*np.abs(X[:, 2])**2.5 + 5*np.cos(X[:, 3]) - 5"
        elif test == 'simple2':
            eval_str = "np.sign(X[:, 2])*np.abs(X[:, 2])**3.5 + 1/(np.abs(X[:, 0])+1)"
        elif test == 'simple3':
            eval_str = "np.exp(X[:, 0]/2) + 12.0 + np.log(np.abs(X[:, 0])*10 + 1)"
        elif test == 'simple4':
            eval_str = "1.0 + 3*X[:, 0]**2 - 0.5*X[:, 0]**3 + 0.1*X[:, 0]**4"
        elif test == 'simple5':
            eval_str = "(np.exp(X[:, 3]) + 3)/(np.abs(X[:, 1]) + np.cos(X[:, 0]) + 1.1)"

        X = np.random.randn(100, 5)*3
        y = eval(eval_str)
        print("Running on", eval_str)

    # System-independent paths
    pkg_directory = Path(__file__).parents[1] / 'julia'
    pkg_filename = pkg_directory / "sr.jl"
    operator_filename = pkg_directory / "operators.jl"

    tmpdir = Path(tempfile.mkdtemp(dir=tempdir))
    hyperparam_filename = tmpdir / f'hyperparams.jl'
    dataset_filename = tmpdir / f'dataset.jl'
    runfile_filename = tmpdir / f'runfile.jl'
    X_filename = tmpdir / "X.csv"
    y_filename = tmpdir / "y.csv"
    weights_filename = tmpdir / "weights.csv"

    def_hyperparams = ""

    # Add pre-defined functions to Julia
    for op_list in [binary_operators, unary_operators]:
        for i in range(len(op_list)):
            op = op_list[i]
            is_user_defined_operator = '(' in op

            if is_user_defined_operator:
                def_hyperparams += op + "\n"
                # Cut off from the first non-alphanumeric char:
                first_non_char = [
                        j for j in range(len(op))
                        if not (op[j].isalpha() or op[j].isdigit())][0]
                function_name = op[:first_non_char]
                op_list[i] = function_name

    #arbitrary complexity by default
    for op in unary_operators:
        if op not in constraints:
            constraints[op] = -1
    for op in binary_operators:
        if op not in constraints:
            constraints[op] = (-1, -1)
        if op in ['plus', 'sub']:
            if constraints[op][0] != constraints[op][1]:
                raise NotImplementedError("You need equal constraints on both sides for - and *, due to simplification strategies.")
        elif op == 'mult':
            # Make sure the complex expression is in the left side.
            if constraints[op][0] == -1:
                continue
            elif constraints[op][1] == -1 or constraints[op][0] < constraints[op][1]:
                constraints[op][0], constraints[op][1] = constraints[op][1], constraints[op][0]

    constraints_str = "const una_constraints = ["
    first = True
    for op in unary_operators:
        val = constraints[op]
        if not first:
            constraints_str += ", "
        constraints_str += f"{val:d}"
        first = False

    constraints_str += """]
const bin_constraints = ["""

    first = True
    for op in binary_operators:
        tup = constraints[op]
        if not first:
            constraints_str += ", "
        constraints_str += f"({tup[0]:d}, {tup[1]:d})"
        first = False
    constraints_str += "]"

    def_hyperparams += f"""include("{_escape_filename(operator_filename)}")
{constraints_str}
const binops = {'[' + ', '.join(binary_operators) + ']'}
const unaops = {'[' + ', '.join(unary_operators) + ']'}
const ns=10;
const parsimony = {parsimony:f}f0
const alpha = {alpha:f}f0
const maxsize = {maxsize:d}
const maxdepth = {maxdepth:d}
const fast_cycle = {'true' if fast_cycle else 'false'}
const migration = {'true' if migration else 'false'}
const hofMigration = {'true' if hofMigration else 'false'}
const fractionReplacedHof = {fractionReplacedHof}f0
const shouldOptimizeConstants = {'true' if shouldOptimizeConstants else 'false'}
const hofFile = "{equation_file}"
const nprocs = {procs:d}
const npopulations = {populations:d}
const nrestarts = {nrestarts:d}
const perturbationFactor = {perturbationFactor:f}f0
const annealing = {"true" if annealing else "false"}
const weighted = {"true" if weights is not None else "false"}
const batching = {"true" if batching else "false"}
const batchSize = {min([batchSize, len(X)]) if batching else len(X):d}
const useVarMap = {"true" if use_custom_variable_names else "false"}
const mutationWeights = [
    {weightMutateConstant:f},
    {weightMutateOperator:f},
    {weightAddNode:f},
    {weightInsertNode:f},
    {weightDeleteNode:f},
    {weightSimplify:f},
    {weightRandomize:f},
    {weightDoNothing:f}
]
const warmupMaxsize = {warmupMaxsize:d}
const limitPowComplexity = {"true" if limitPowComplexity else "false"}
const useFrequency = {"true" if useFrequency else "false"}
"""

    op_runner = ""
    if len(binary_operators) > 0:
        op_runner += """
@inline function BINOP!(x::Array{Float32, 1}, y::Array{Float32, 1}, i::Int, clen::Int)
    if i === 1
        @inbounds @simd for j=1:clen
            x[j] = """f"{binary_operators[0]}""""(x[j], y[j])
        end"""
        for i in range(1, len(binary_operators)):
            op_runner += f"""
    elseif i === {i+1}
        @inbounds @simd for j=1:clen
            x[j] = {binary_operators[i]}(x[j], y[j])
        end"""
        op_runner += """
    end
end"""

    if len(unary_operators) > 0:
        op_runner += """
@inline function UNAOP!(x::Array{Float32, 1}, i::Int, clen::Int)
    if i === 1
        @inbounds @simd for j=1:clen
            x[j] = """f"{unary_operators[0]}(x[j])""""
        end"""
        for i in range(1, len(unary_operators)):
            op_runner += f"""
    elseif i === {i+1}
        @inbounds @simd for j=1:clen
            x[j] = {unary_operators[i]}(x[j])
        end"""
        op_runner += """
    end
end"""

    def_hyperparams += op_runner

    def_datasets = """using DelimitedFiles"""

    np.savetxt(X_filename, X, delimiter=',')
    np.savetxt(y_filename, y, delimiter=',')
    if weights is not None:
        np.savetxt(weights_filename, weights, delimiter=',')

    def_datasets += f"""
const X = readdlm("{_escape_filename(X_filename)}", ',', Float32, '\\n')
const y = readdlm("{_escape_filename(y_filename)}", ',', Float32, '\\n')"""

    if weights is not None:
        def_datasets += f"""
const weights = readdlm("{_escape_filename(weights_filename)}", ',', Float32, '\\n')"""

    if use_custom_variable_names:
        def_hyperparams += f"""
const varMap = {'["' + '", "'.join(variable_names) + '"]'}"""

    with open(hyperparam_filename, 'w') as f:
        print(def_hyperparams, file=f)

    with open(dataset_filename, 'w') as f:
        print(def_datasets, file=f)

    with open(runfile_filename, 'w') as f:
        print(f'@everywhere include("{_escape_filename(hyperparam_filename)}")', file=f)
        print(f'@everywhere include("{_escape_filename(dataset_filename)}")', file=f)
        print(f'@everywhere include("{_escape_filename(pkg_filename)}")', file=f)
        print(f'fullRun({niterations:d}, npop={npop:d}, ncyclesperiteration={ncyclesperiteration:d}, fractionReplaced={fractionReplaced:f}f0, verbosity=round(Int32, {verbosity:f}), topn={topn:d})', file=f)
        print(f'rmprocs(nprocs)', file=f)


    command = [
        f'julia', f'-O{julia_optimization:d}',
        f'-p', f'{procs}',
        str(runfile_filename),
        ]
    if timeout is not None:
        command = [f'timeout', f'{timeout}'] + command

    global global_n_features
    global global_equation_file
    global global_variable_names
    global global_extra_sympy_mappings

    global_n_features = X.shape[1]
    global_equation_file = equation_file
    global_variable_names = variable_names
    global_extra_sympy_mappings = extra_sympy_mappings

    print("Running on", ' '.join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1)
    try:
        while True:
            line = process.stdout.readline()
            if not line: break
            print(line.decode('utf-8').replace('\n', ''))

        process.stdout.close()
        process.wait()
    except KeyboardInterrupt:
        print("Killing process... will return when done.")
        process.kill()

    if delete_tempfiles:
        shutil.rmtree(tmpdir)

    return get_hof()


def run_feature_selection(X, y, select_k_features):
    """Use a gradient boosting tree regressor as a proxy for finding
        the k most important features in X, returning indices for those
        features as output."""

    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.feature_selection import SelectFromModel, SelectKBest

    clf = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0, loss='ls') #RandomForestRegressor()
    clf.fit(X, y)
    selector = SelectFromModel(clf, threshold=-np.inf,
            max_features=select_k_features, prefit=True)
    return selector.get_support(indices=True)

def get_hof(equation_file=None, n_features=None, variable_names=None, extra_sympy_mappings=None):
    """Get the equations from a hall of fame file. If no arguments
    entered, the ones used previously from a call to PySR will be used."""

    global global_n_features
    global global_equation_file
    global global_variable_names
    global global_extra_sympy_mappings

    if equation_file is None: equation_file = global_equation_file
    if n_features is None: n_features = global_n_features
    if variable_names is None: variable_names = global_variable_names
    if extra_sympy_mappings is None: extra_sympy_mappings = global_extra_sympy_mappings

    global_equation_file = equation_file
    global_n_features = n_features
    global_variable_names = variable_names
    global_extra_sympy_mappings = extra_sympy_mappings

    try:
        output = pd.read_csv(equation_file + '.bkup', sep="|")
    except FileNotFoundError:
        print("Couldn't find equation file!")
        return pd.DataFrame()

    scores = []
    lastMSE = None
    lastComplexity = 0
    sympy_format = []
    lambda_format = []
    use_custom_variable_names = (len(variable_names) != 0)
    local_sympy_mappings = {
            **extra_sympy_mappings,
            **sympy_mappings
    }

    if use_custom_variable_names:
        sympy_symbols = [sympy.Symbol(variable_names[i]) for i in range(n_features)]
    else:
        sympy_symbols = [sympy.Symbol('x%d'%i) for i in range(n_features)]

    for i in range(len(output)):
        eqn = sympify(output.loc[i, 'Equation'], locals=local_sympy_mappings)
        sympy_format.append(eqn)
        lambda_format.append(lambdify(sympy_symbols, eqn))
        curMSE = output.loc[i, 'MSE']
        curComplexity = output.loc[i, 'Complexity']

        if lastMSE is None:
            cur_score = 0.0
        else:
            cur_score = - np.log(curMSE/lastMSE)/(curComplexity - lastComplexity)

        scores.append(cur_score)
        lastMSE = curMSE
        lastComplexity = curComplexity

    output['score'] = np.array(scores)
    output['sympy_format'] = sympy_format
    output['lambda_format'] = lambda_format

    return output[['Complexity', 'MSE', 'score', 'Equation', 'sympy_format', 'lambda_format']]

def best_row(equations=None):
    """Return the best row of a hall of fame file using the score column.
    By default this uses the last equation file.
    """
    if equations is None: equations = get_hof()
    best_idx = np.argmax(equations['score'])
    return equations.iloc[best_idx]

def best_tex(equations=None):
    """Return the equation with the best score, in latex format
    By default this uses the last equation file.
    """
    if equations is None: equations = get_hof()
    best_sympy = best_row(equations)['sympy_format']
    return sympy.latex(best_sympy.simplify())

def best(equations=None):
    """Return the equation with the best score, in sympy format.
    By default this uses the last equation file.
    """
    if equations is None: equations = get_hof()
    best_sympy = best_row(equations)['sympy_format']
    return best_sympy.simplify()

def best_callable(equations=None):
    """Return the equation with the best score, in callable format.
    By default this uses the last equation file.
    """
    if equations is None: equations = get_hof()
    return best_row(equations)['lambda_format']

def _escape_filename(filename):
    """Turns a file into a string representation with correctly escaped backslashes"""
    repr = str(filename)
    repr = repr.replace('\\', '\\\\')
    return repr
