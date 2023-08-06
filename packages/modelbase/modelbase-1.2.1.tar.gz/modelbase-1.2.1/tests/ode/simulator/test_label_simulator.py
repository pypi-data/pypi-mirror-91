# Standard Library
import unittest

# Third party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from modelbase.ode import LabelModel, Simulator


def GENERATE_RESULTS():
    label_model = LabelModel()
    label_model.add_label_compounds({"x": 2, "y": 2, "z": 4})
    label_model.add_labelmap_reaction(
        rate_name="v1",
        function=lambda x, y: x - y,
        stoichiometry={"x": -1, "y": 1},
        labelmap=[1, 0],
        reversible=True,
    )
    label_model.add_labelmap_reaction(
        rate_name="v2",
        function=lambda x, y, z: x * y - z,
        stoichiometry={"x": -1, "y": -1, "z": 1},
        labelmap=[0, 1, 2, 3],
        reversible=True,
    )

    base_y0 = {"x": 2, "y": 2, "z": 4}
    y0 = label_model.generate_y0(base_y0=base_y0, label_positions={"x": 0})
    simulator = Simulator(model=label_model)
    simulator.initialise(y0=y0)
    t, y = simulator.simulate(t_end=100, steps=10)
    return simulator


SIM = GENERATE_RESULTS()


class LabelSimualtorTests(unittest.TestCase):
    def test_generate_y0(self):
        label_model = LabelModel()
        label_model.add_label_compounds({"x": 2, "y": 2, "z": 4})
        base_y0 = {"x": 2, "y": 2, "z": 4}
        simulator = Simulator(label_model)
        self.assertEqual(
            label_model.generate_y0(base_y0, label_positions={"x": 0}),
            simulator.generate_y0(base_y0, label_positions={"x": 0}),
        )

    def test_get_total_concentration(self):
        simulator = SIM.copy()
        np.testing.assert_array_almost_equal(simulator.get_total_concentration(compound="x"), 2.0)
        np.testing.assert_array_almost_equal(simulator.get_total_concentration(compound="y"), 2.0)
        np.testing.assert_array_almost_equal(simulator.get_total_concentration(compound="z"), 4.0)

    def test_get_labeled_and_unlabeled(self):
        simulator = SIM.copy()
        np.testing.assert_array_almost_equal(
            simulator.get_unlabeled_concentration(compound="x") + simulator.get_total_label_concentration(compound="x"),
            2.0,
        )
        np.testing.assert_array_almost_equal(
            simulator.get_unlabeled_concentration(compound="y") + simulator.get_total_label_concentration(compound="y"),
            2.0,
        )
        np.testing.assert_array_almost_equal(
            simulator.get_unlabeled_concentration(compound="z") + simulator.get_total_label_concentration(compound="z"),
            4.0,
        )

    def test_get_all_isotopomer_concentrations_df(self):
        simulator = SIM.copy()
        df = simulator.get_all_isotopomer_concentrations_df(compound="x")
        np.testing.assert_array_equal(
            df.index,
            [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        )
        np.testing.assert_array_equal(df.columns, ["x__00", "x__01", "x__10", "x__11"])
        np.testing.assert_array_almost_equal(df.sum(axis=1).values, 2)

    def test_get_all_isotopomer_concentrations_dict(self):
        simulator = SIM.copy()
        d = simulator.get_all_isotopomer_concentrations_dict(compound="x")
        self.assertEqual(list(d.keys()), ["x__00", "x__01", "x__10", "x__11"])
        np.testing.assert_array_almost_equal(np.sum(list(d.values()), axis=0), 2)

    def test_get_all_isotopomer_concentrations_array(self):
        simulator = SIM.copy()
        arr = simulator.get_all_isotopomer_concentrations_array(compound="x")
        self.assertEqual(arr.shape, (11, 4))
        np.testing.assert_array_almost_equal(arr.sum(axis=1), 2)

    def test_get_concentrations_by_reg_exp_df(self):
        simulator = SIM.copy()
        pd.testing.assert_frame_equal(
            simulator.get_concentrations_by_reg_exp_df(reg_exp="x__\d+"),
            simulator.get_all_isotopomer_concentrations_df(compound="x"),
        )

    def test_get_concentrations_by_reg_exp_dict(self):
        simulator = SIM.copy()
        simulator.get_concentrations_by_reg_exp_dict(
            reg_exp="x__\d+"
        ).keys() == simulator.get_all_isotopomer_concentrations_dict(compound="x").keys()

    def test_get_concentrations_by_reg_exp_array(self):
        simulator = SIM.copy()
        np.testing.assert_array_equal(
            simulator.get_concentrations_by_reg_exp_array(reg_exp="x__\d+"),
            simulator.get_all_isotopomer_concentrations_array(compound="x"),
        )

    def test_get_concentration_at_positions(self):
        simulator = SIM.copy()
        np.testing.assert_array_almost_equal(
            (
                simulator.get_concentration_at_positions(compound="x", positions=0)
                + simulator.get_concentration_at_positions(compound="x", positions=1)
                + simulator.get_unlabeled_concentration(compound="x")
            ),
            2,
        )

    def test_get_concentrations_of_n_labeled_array(self):
        simulator = SIM.copy()
        simulator.get_concentrations_of_n_labeled_array(compound="x", n_labels=1)
        np.testing.assert_array_almost_equal(
            (
                simulator.get_concentrations_of_n_labeled_array(compound="x", n_labels=0).sum(axis=1)
                + simulator.get_concentrations_of_n_labeled_array(compound="x", n_labels=1).sum(axis=1)
                + simulator.get_concentrations_of_n_labeled_array(compound="x", n_labels=2).sum(axis=1)
            ),
            2,
        )

    def test_get_concentrations_of_n_labeled_dict(self):
        simulator = SIM.copy()
        simulator.get_concentrations_of_n_labeled_dict(compound="x", n_labels=1)
        list(simulator.get_concentrations_of_n_labeled_dict(compound="x", n_labels=0).keys()), ["x__00"]
        list(simulator.get_concentrations_of_n_labeled_dict(compound="x", n_labels=1).keys()), [
            "x__10",
            "x__01",
        ]
        list(simulator.get_concentrations_of_n_labeled_dict(compound="x", n_labels=2).keys()), ["x__11"]

    def test_get_concentrations_of_n_labeled_df(self):
        simulator = SIM.copy()
        self.assertEqual(
            list(simulator.get_concentrations_of_n_labeled_df(compound="x", n_labels=0).columns),
            ["x__00"],
        )
        self.assertEqual(
            list(simulator.get_concentrations_of_n_labeled_df(compound="x", n_labels=1).columns),
            ["x__10", "x__01"],
        )
        self.assertEqual(
            list(simulator.get_concentrations_of_n_labeled_df(compound="x", n_labels=2).columns),
            ["x__11"],
        )


class PlottingTests(unittest.TestCase):
    def test_plot(self):
        simulator = SIM.copy()
        fig, ax = simulator.plot()
        plt.close()

    def test_plot_label_distribution(self):
        simulator = SIM.copy()
        fig, ax = simulator.plot_label_distribution(compound="x")
        plt.close()

    def test_plot_label_distribution_grid(self):
        simulator = SIM.copy()
        fig, ax = simulator.plot_label_distribution_grid(compounds=["x", "y", "z"])
        plt.close()

    def test_plot_all_label_distributions(self):
        simulator = SIM.copy()
        fig, ax = simulator.plot_all_label_distributions()
        plt.close()
