# Standard Library
import unittest

# Third party
import matplotlib.pyplot as plt
import numpy as np
from modelbase.ode import Model, mca
from modelbase.ode import ratefunctions as rf


class MCATests(unittest.TestCase):
    def testSubstrateElasticityIrreversibleMassAction(self):
        """Should yield 1 regardless of the concentration"""
        parameters = {"kf": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_reaction(
            rate_name="v1",
            function=rf.mass_action_1,
            stoichiometry={"x": -1, "y": 1},
            modifiers=None,
            parameters=["kf"],
            reversible=False,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1], t=0, normalized=True),
            1,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[10], t=0, normalized=True),
            1,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[100], t=0, normalized=True),
            1,
        )

    def testSubstrateElasticityIrreversibleMichaelisMenten(self):
        """Should tend to 1 for small and to 0 for large concentrations"""
        parameters = {"vmax": 1, "km": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_reaction(
            rate_name="v1",
            function=rf.michaelis_menten,
            stoichiometry={"x": -1, "y": 1},
            modifiers=None,
            parameters=["vmax", "km"],
            reversible=False,
        )

        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1e-12], t=0, normalized=True),
            1,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1], t=0, normalized=True),
            0.5,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1e12], t=0, normalized=True),
            0,
        )

    def testParameterElasticityIrreversibleMichaelisMenten(self):
        """Should be 1 for vmax"""
        parameters = {"vmax": 1, "km": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_reaction(
            rate_name="v1",
            function=rf.michaelis_menten,
            stoichiometry={"x": -1, "y": 1},
            modifiers=None,
            parameters=["vmax", "km"],
            reversible=False,
        )

        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1e-12], t=0, normalized=True),
            1,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1], t=0, normalized=True),
            0.5,
        )
        np.testing.assert_almost_equal(
            mca.get_compound_elasticity(model=model, compound="x", y=[1e12], t=0, normalized=True),
            0,
        )


class MCALinearChainTests(unittest.TestCase):
    def create_model(self):
        parameters = {
            "k_in": 1,
            "k_fwd": 1,
            "k_out": 1,
        }

        model = Model(parameters=parameters)
        model.add_compounds(compounds=["X", "Y"])
        model.add_reaction(
            rate_name="v_in",
            function=rf.constant,
            stoichiometry={"X": 1},
            parameters=["k_in"],
        )
        model.add_reaction(
            rate_name="v1",
            function=rf.mass_action_1,
            stoichiometry={"X": -1, "Y": 1},
            parameters=["k_fwd"],
        )
        model.add_reaction(
            rate_name="v_out",
            function=rf.mass_action_1,
            stoichiometry={"Y": -1},
            parameters=["k_out"],
        )
        y0 = {"X": 1, "Y": 1}
        parameters = ["k_in", "k_fwd", "k_out"]
        compounds = ["X", "Y"]
        return model, y0, parameters, compounds

    def test_get_compound_elasticity(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticity(model=model, compound="X", y=y0, t=0, normalized=False),
            [0.0, 1.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticity(model=model, compound="X", y=y0, t=0, normalized=True),
            [0.0, 1.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticity(model=model, compound="Y", y=y0, t=0, normalized=False),
            [0.0, 0.0, 1.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticity(model=model, compound="Y", y=y0, t=0, normalized=True),
            [0.0, 0.0, 1.0],
        )

    def test_get_compound_elasticities_array(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticities_array(
                model=model,
                compounds=compounds,
                y=y0,
                t=0,
                normalized=False,
            ),
            [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_compound_elasticities_array_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_compound_elasticities_array(
                model=model,
                compounds=compounds,
                y=y0,
                t=0,
                normalized=True,
            ),
            [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_compound_elasticities_df(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_compound_elasticities_df(
            model=model,
            compounds=compounds,
            y=y0,
            t=0,
            normalized=False,
        )
        self.assertEqual(list(df.index), ["X", "Y"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(
            df.values,
            [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_compound_elasticities_df_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_compound_elasticities_df(
            model=model,
            compounds=compounds,
            y=y0,
            t=0,
            normalized=True,
        )
        self.assertEqual(list(df.index), ["X", "Y"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(
            df.values,
            [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_parameter_elasticity(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=False,
            ),
            [1.0, 0.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=True,
            ),
            [1.0, 0.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=False,
            ),
            [0.0, 1.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=True,
            ),
            [0.0, 1.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=False,
            ),
            [0.0, 0.0, 1.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticity(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=True,
            ),
            [0.0, 0.0, 1.0],
        )

    def test_get_parameter_elasticities_array(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticities_array(
                model=model,
                parameters=parameters,
                y=y0,
                t=0,
                normalized=False,
            ),
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_parameter_elasticities_array_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_parameter_elasticities_array(
                model=model,
                parameters=parameters,
                y=y0,
                t=0,
                normalized=True,
            ),
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_parameter_elasticities_df(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_parameter_elasticities_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(
            df.values,
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_parameter_elasticities_df_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_parameter_elasticities_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(
            df.values,
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        )

    def test_get_concentration_response_coefficient(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=False,
            ),
            [1, 1],
        )
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=True,
            ),
            [1, 1],
        )
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=False,
            ),
            [-1, 0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=True,
            ),
            [-1, 0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=False,
            ),
            [0, -1],
        )
        np.testing.assert_array_almost_equal(
            mca.get_concentration_response_coefficient(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=True,
            ),
            [0, -1],
        )

    def test_get_concentration_response_coefficients_array(self):
        model, y0, parameters, compounds = self.create_model()
        arr = mca.get_concentration_response_coefficients_array(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        np.testing.assert_array_almost_equal(
            arr,
            [
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
        )

    def test_get_concentration_response_coefficients_array_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        arr = mca.get_concentration_response_coefficients_array(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        np.testing.assert_array_almost_equal(
            arr,
            [
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
        )

    def test_get_concentration_response_coefficients_df(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_concentration_response_coefficients_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        np.testing.assert_array_almost_equal(
            df.values,
            [
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["X", "Y"])

    def test_get_concentration_response_coefficients_df_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_concentration_response_coefficients_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        np.testing.assert_array_almost_equal(
            df.values,
            [
                [1, 1],
                [-1, 0],
                [0, -1],
            ],
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["X", "Y"])

    def test_get_flux_response_coefficient(self):
        model, y0, parameters, compounds = self.create_model()
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=False,
            ),
            [1, 1, 1],
        )
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_in",
                y=y0,
                t=0,
                normalized=True,
            ),
            [1, 1, 1],
        )
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=False,
            ),
            [0.0, 0.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_fwd",
                y=y0,
                t=0,
                normalized=True,
            ),
            [0.0, 0.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=False,
            ),
            [0.0, 0.0, 0.0],
        )
        np.testing.assert_array_almost_equal(
            mca.get_flux_response_coefficient(
                model=model,
                parameter="k_out",
                y=y0,
                t=0,
                normalized=True,
            ),
            [0.0, 0.0, 0.0],
        )

    def test_get_flux_response_coefficients_array(self):
        model, y0, parameters, compounds = self.create_model()
        arr = mca.get_flux_response_coefficients_array(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        np.testing.assert_array_almost_equal(arr, [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    def test_get_flux_response_coefficients_array_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        arr = mca.get_flux_response_coefficients_array(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        np.testing.assert_array_almost_equal(arr, [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    def test_get_flux_response_coefficients_df(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_flux_response_coefficients_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(df.values, [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    def test_get_flux_response_coefficients_df_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        df = mca.get_flux_response_coefficients_df(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        self.assertEqual(list(df.index), ["k_in", "k_fwd", "k_out"])
        self.assertEqual(list(df.columns), ["v_in", "v1", "v_out"])
        np.testing.assert_array_almost_equal(df.values, [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    def test_plot_concentration_response_coefficients(self):
        model, y0, parameters, compounds = self.create_model()
        mca.plot_concentration_response_coefficients(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        plt.close()

    def test_plot_concentration_response_coefficients_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        mca.plot_concentration_response_coefficients(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        plt.close()

    def test_plot_flux_response_coefficients(self):
        model, y0, parameters, compounds = self.create_model()
        mca.plot_flux_response_coefficients(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=False,
        )
        plt.close()

    def test_plot_flux_response_coefficients_normalized(self):
        model, y0, parameters, compounds = self.create_model()
        mca.plot_flux_response_coefficients(
            model=model,
            parameters=parameters,
            y=y0,
            t=0,
            normalized=True,
        )
        plt.close()
