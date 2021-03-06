"""Collection of tests for :mod:`orion.plotting.backend_plotly`."""
import plotly
import pytest

from orion.core.worker.experiment import ExperimentView
from orion.plotting.base import regret
from orion.testing import create_experiment

config = dict(
    name='experiment-name',
    space={'x': 'uniform(0, 200)'},
    metadata={'user': 'test-user',
              'orion_version': 'XYZ',
              'VCS': {"type": "git",
                      "is_dirty": False,
                      "HEAD_sha": "test",
                      "active_branch": None,
                      "diff_sha": "diff"}},
    version=1,
    pool_size=1,
    max_trials=10,
    working_dir='',
    algorithms={'random': {'seed': 1}},
    producer={'strategy': 'NoParallelStrategy'},
)

trial_config = {
    'experiment': 0,
    'status': 'completed',
    'worker': None,
    'start_time': None,
    'end_time': None,
    'heartbeat': None,
    'results': [],
    'params': []
}


def assert_regret_plot(plot):
    """Checks the layout of a regret plot"""
    assert plot.layout.title.text == "Regret for experiment 'experiment-name'"
    assert plot.layout.xaxis.title.text == "Trials ordered by suggested time"
    assert plot.layout.yaxis.title.text == "Objective 'loss'"

    trace1 = plot.data[0]
    assert trace1.type == "scatter"
    assert trace1.name == "trials"
    assert trace1.mode == "markers"
    assert len(trace1.y) == 1
    assert not trace1.x

    trace2 = plot.data[1]
    assert trace2.type == "scatter"
    assert trace2.name == "best-to-date"
    assert trace2.mode == "lines"
    assert len(trace2.y) == 1
    assert not trace2.x


class TestRegret:
    """Tests the ``regret()`` method provided by the plotly backend"""

    def test_requires_argument(self):
        """Tests that the experiment data are required."""
        with pytest.raises(ValueError):
            regret(None)

    def test_returns_plotly_object(self):
        """Tests that the plotly backend returns a plotly object"""
        with create_experiment(config, trial_config, ['completed']) as (_, _, experiment):
            plot = regret(experiment)

        assert type(plot) is plotly.graph_objects.Figure

    def test_graph_layout(self):
        """Tests the layout of the plot"""
        with create_experiment(config, trial_config, ['completed']) as (_, _, experiment):
            plot = regret(experiment)

        assert_regret_plot(plot)

    def test_experiment_worker_as_parameter(self):
        """Tests that ``Experiment`` is a valide parameter"""
        with create_experiment(config, trial_config, ['completed']) as (_, experiment, _):
            plot = regret(experiment)

        assert_regret_plot(plot)

    def test_experiment_view_as_parameter(self):
        """Tests that ``ExperimentView`` is a valid parameter"""
        with create_experiment(config, trial_config, ['completed']) as (_, experiment, _):
            plot = regret(ExperimentView(experiment))

        assert_regret_plot(plot)

    def test_ignore_uncompleted_statuses(self):
        """Tests that uncompleted statuses are ignored"""
        with create_experiment(config, trial_config) as (_, _, experiment):
            plot = regret(experiment)

        assert_regret_plot(plot)

    def test_unsupported_order_key(self):
        """Tests that unsupported order keys are rejected"""
        with create_experiment(config, trial_config) as (_, _, experiment):
            with pytest.raises(ValueError):
                regret(experiment, order_by='unsupported')
