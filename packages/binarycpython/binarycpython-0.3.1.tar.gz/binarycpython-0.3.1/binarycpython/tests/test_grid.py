"""
Test cases for the grid

Tasks:
    TODO: write tests for load_from_sourcefile
"""

import os
import sys
import json
import unittest
import tempfile
import datetime
import numpy as np

from binarycpython.utils.grid import Population
from binarycpython.utils.functions import (
    temp_dir,
    extract_ensemble_json_from_string,
    merge_dicts,
    remove_file,
)
from binarycpython.utils.custom_logging_functions import binary_c_log_code

binary_c_temp_dir = temp_dir()


def parse_function_test_grid_evolve_2_threads_with_custom_logging(self, output):
    """
    Simple parse function that directly appends all the output to a file
    """

    # Get some information from the
    data_dir = self.custom_options["data_dir"]

    # make outputfilename
    output_filename = os.path.join(
        data_dir,
        "test_grid_evolve_2_threads_with_custom_logging_outputfile_population_{}_thread_{}.dat".format(
            self.grid_options["_population_id"], self.process_ID
        ),
    )

    # Check directory, make if necessary
    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(output_filename):
        with open(output_filename, "w") as first_f:
            first_f.write(output + "\n")
    else:
        with open(output_filename, "a") as first_f:
            first_f.write(output + "\n")


# class test_(unittest.TestCase):
#     """
#     Unittests for function
#     """

#     def test_1(self):
#         pass

# def test_(self):
#     """
#     Unittests for the function
#     """


class test_Population(unittest.TestCase):
    """
    Unittests for function
    """

    def test_setup(self):
        """
        Unittests for function _setup
        """
        test_pop = Population()

        self.assertTrue("orbital_period" in test_pop.defaults)
        self.assertTrue("metallicity" in test_pop.defaults)
        self.assertNotIn("help_all", test_pop.cleaned_up_defaults)
        self.assertEqual(test_pop.bse_options, {})
        self.assertEqual(test_pop.custom_options, {})
        self.assertEqual(test_pop.argline_dict, {})
        self.assertEqual(test_pop.persistent_data_memory_dict, {})
        self.assertTrue(test_pop.grid_options["parse_function"] == None)
        self.assertTrue(isinstance(test_pop.grid_options["_main_pid"], int))

    def test_set(self):
        """
        Unittests for function set
        """

        test_pop = Population()
        test_pop.set(amt_cores=2)
        test_pop.set(M_1=10)
        test_pop.set(data_dir="/tmp/binary_c_python")
        test_pop.set(ensemble_filter_SUPERNOVAE=1)

        self.assertIn("data_dir", test_pop.custom_options)
        self.assertEqual(test_pop.custom_options["data_dir"], "/tmp/binary_c_python")

        #
        self.assertTrue(test_pop.bse_options["M_1"] == 10)
        self.assertTrue(test_pop.bse_options["ensemble_filter_SUPERNOVAE"] == 1)

        #
        self.assertTrue(test_pop.grid_options["amt_cores"] == 2)

    def test_cmdline(self):
        """
        Unittests for function parse_cmdline
        """

        # copy old sys.argv values
        prev_sysargv = sys.argv.copy()

        # make a dummy cmdline arg input
        sys.argv = [
            "script",
            "--cmdline",
            "metallicity=0.0002 amt_cores=2 data_dir=/tmp/binary_c_python",
        ]

        # Set up population
        test_pop = Population()
        test_pop.set(data_dir="/tmp")

        # parse arguments
        test_pop.parse_cmdline()

        # metallicity
        self.assertTrue(isinstance(test_pop.bse_options["metallicity"], str))
        self.assertTrue(test_pop.bse_options["metallicity"] == "0.0002")

        # Amt cores
        self.assertTrue(isinstance(test_pop.grid_options["amt_cores"], int))
        self.assertTrue(test_pop.grid_options["amt_cores"] == 2)

        # datadir
        self.assertTrue(isinstance(test_pop.custom_options["data_dir"], str))
        self.assertTrue(test_pop.custom_options["data_dir"] == "/tmp/binary_c_python")

        # put back the other args if they exist
        sys.argv = prev_sysargv.copy()

    def test__return_argline(self):
        """
        Unittests for the function _return_argline
        """

        # Set up population
        test_pop = Population()
        test_pop.set(metallicity=0.02)
        test_pop.set(M_1=10)

        argline = test_pop._return_argline()
        self.assertTrue(argline == "binary_c M_1 10 metallicity 0.02")

        # custom dict
        argline2 = test_pop._return_argline(
            {"example_parameter1": 10, "example_parameter2": "hello"}
        )
        self.assertTrue(
            argline2 == "binary_c example_parameter1 10 example_parameter2 hello"
        )

    def test_add_grid_variable(self):
        """
        Unittests for the function add_grid_variable

        TODO: Should I test more here?
        """

        test_pop = Population()

        resolution = {"M_1": 10, "q": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        test_pop.add_grid_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            resolution="{}".format(resolution["q"]),
            spacingfunc="const(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        self.assertIn("q", test_pop.grid_options["_grid_variables"])
        self.assertIn("lnm1", test_pop.grid_options["_grid_variables"])
        self.assertEqual(len(test_pop.grid_options["_grid_variables"]), 2)

    def test_return_population_settings(self):
        """
        Unittests for the function return_population_settings
        """

        test_pop = Population()
        test_pop.set(metallicity=0.02)
        test_pop.set(M_1=10)
        test_pop.set(amt_cores=2)
        test_pop.set(data_dir="/tmp")

        population_settings = test_pop.return_population_settings()

        self.assertIn("bse_options", population_settings)
        self.assertTrue(population_settings["bse_options"]["metallicity"] == 0.02)
        self.assertTrue(population_settings["bse_options"]["M_1"] == 10)

        self.assertIn("grid_options", population_settings)
        self.assertTrue(population_settings["grid_options"]["amt_cores"] == 2)

        self.assertIn("custom_options", population_settings)
        self.assertTrue(population_settings["custom_options"]["data_dir"] == "/tmp")

    def test__return_binary_c_version_info(self):
        """
        Unittests for the function _return_binary_c_version_info
        """

        test_pop = Population()
        binary_c_version_info = test_pop._return_binary_c_version_info(parsed=True)

        self.assertTrue(isinstance(binary_c_version_info, dict))
        self.assertIn("isotopes", binary_c_version_info)
        self.assertIn("argpairs", binary_c_version_info)
        self.assertIn("ensembles", binary_c_version_info)
        self.assertIn("macros", binary_c_version_info)
        self.assertIn("dt_limits", binary_c_version_info)
        self.assertIn("nucleosynthesis_sources", binary_c_version_info)
        self.assertIn("miscellaneous", binary_c_version_info)

        self.assertIsNotNone(binary_c_version_info["argpairs"])
        self.assertIsNotNone(binary_c_version_info["ensembles"])
        self.assertIsNotNone(binary_c_version_info["macros"])
        self.assertIsNotNone(binary_c_version_info["dt_limits"])
        self.assertIsNotNone(binary_c_version_info["miscellaneous"])

        if binary_c_version_info["macros"]["NUCSYN"] == "on":
            self.assertIsNotNone(binary_c_version_info["isotopes"])
            self.assertIsNotNone(binary_c_version_info["nucleosynthesis_sources"])

    def test__return_binary_c_defaults(self):
        """
        Unittests for the function _return_binary_c_defaults
        """

        test_pop = Population()
        binary_c_defaults = test_pop._return_binary_c_defaults()
        self.assertIn("probability", binary_c_defaults)
        self.assertIn("phasevol", binary_c_defaults)
        self.assertIn("metallicity", binary_c_defaults)

    def test_return_all_info(self):
        """
        Unittests for the function return_all_info
        Not going to do too much tests here, just check if they are not empty
        """

        test_pop = Population()
        all_info = test_pop.return_all_info()

        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})

    def test_export_all_info(self):
        """
        Unittests for the function export_all_info
        """

        test_pop = Population()

        test_pop.set(metallicity=0.02)
        test_pop.set(M_1=10)
        test_pop.set(amt_cores=2)
        test_pop.set(data_dir=binary_c_temp_dir)

        # datadir
        settings_filename = test_pop.export_all_info(use_datadir=True)
        self.assertTrue(os.path.isfile(settings_filename))
        with open(settings_filename, "r") as f:
            all_info = json.loads(f.read())

        #
        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        #
        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})

        # custom name
        # datadir
        settings_filename = test_pop.export_all_info(
            use_datadir=False,
            outfile=os.path.join(binary_c_temp_dir, "example_settings.json"),
        )
        self.assertTrue(os.path.isfile(settings_filename))
        with open(settings_filename, "r") as f:
            all_info = json.loads(f.read())

        #
        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        #
        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})

        # wrong filename
        self.assertRaises(
            ValueError,
            test_pop.export_all_info,
            use_datadir=False,
            outfile=os.path.join(binary_c_temp_dir, "example_settings.txt"),
        )

    def test__cleanup_defaults(self):
        """
        Unittests for the function _cleanup_defaults
        """

        test_pop = Population()
        cleaned_up_defaults = test_pop._cleanup_defaults()
        self.assertNotIn("help_all", cleaned_up_defaults)

    def test__increment_probtot(self):
        """
        Unittests for the function _increment_probtot
        """

        test_pop = Population()
        test_pop._increment_probtot(0.5)
        self.assertEqual(test_pop.grid_options["_probtot"], 0.5)

    def test__increment_count(self):
        """
        Unittests for the function _increment_probtot
        """

        test_pop = Population()
        test_pop._increment_count()
        self.assertEqual(test_pop.grid_options["_count"], 1)

    def test__dict_from_line_source_file(self):
        """
        Unittests for the function _dict_from_line_source_file
        """

        source_file = os.path.join(binary_c_temp_dir, "example_source_file.txt")

        # write
        with open(source_file, "w") as f:
            f.write("binary_c M_1 10 metallicity 0.02\n")

        test_pop = Population()

        # readout
        with open(source_file, "r") as f:
            for line in f.readlines():
                argdict = test_pop._dict_from_line_source_file(line)

                self.assertTrue(argdict["M_1"] == 10)
                self.assertTrue(argdict["metallicity"] == 0.02)

    def test_evolve_single(self):
        """
        Unittests for the function evolve_single
        """

        CUSTOM_LOGGING_STRING_MASSES = """
        Printf("TEST_CUSTOM_LOGGING_1 %30.12e %g %g %g %g\\n",
            //
            stardata->model.time, // 1
            
            // masses
            stardata->common.zero_age.mass[0], //
            stardata->common.zero_age.mass[1], //

            stardata->star[0].mass,
            stardata->star[1].mass
            );
        """

        test_pop = Population()
        test_pop.set(
            M_1=10,
            M_2=5,
            orbital_period=100000,
            metallicty=0.02,
            max_evolution_time=15000,
        )

        test_pop.set(C_logging_code=CUSTOM_LOGGING_STRING_MASSES)

        output = test_pop.evolve_single()

        #
        self.assertTrue(len(output.splitlines()) > 1)
        self.assertIn("TEST_CUSTOM_LOGGING_1", output)

        #
        custom_logging_dict = {"TEST_CUSTOM_LOGGING_2": ["star[0].mass", "model.time"]}
        test_pop_2 = Population()
        test_pop_2.set(
            M_1=10,
            M_2=5,
            orbital_period=100000,
            metallicty=0.02,
            max_evolution_time=15000,
        )

        test_pop_2.set(C_auto_logging=custom_logging_dict)

        output_2 = test_pop_2.evolve_single()

        #
        self.assertTrue(len(output_2.splitlines()) > 1)
        self.assertIn("TEST_CUSTOM_LOGGING_2", output_2)


class test_grid_evolve(unittest.TestCase):
    """
    Unittests for function Population.evolve()
    """

    def test_grid_evolve_1_thread(self):
        """
        Unittests to see if 1 thread does all the systems
        """

        test_pop_evolve_1_thread = Population()
        test_pop_evolve_1_thread.set(
            amt_cores=1, verbosity=1, M_2=1, orbital_period=100000
        )

        resolution = {"M_1": 10}

        test_pop_evolve_1_thread.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop_evolve_1_thread.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.1503788456014623), 1e-10
        )
        self.assertTrue(analytics["total_count"] == 10)

    def test_grid_evolve_2_threads(self):
        """
        Unittests to see if multiple threads handle the all the systems correctly
        """

        test_pop = Population()
        test_pop.set(amt_cores=2, verbosity=1, M_2=1, orbital_period=100000)

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.1503788456014623), 1e-10
        )  #
        self.assertTrue(analytics["total_count"] == 10)

    def test_grid_evolve_2_threads_with_custom_logging(self):
        """
        Unittests to see if multiple threads do the custom logging correctly
        """

        data_dir_value = os.path.join(binary_c_temp_dir, "grid_tests")
        amt_cores_value = 2
        custom_logging_string = 'Printf("MY_STELLAR_DATA_TEST_EXAMPLE %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'

        test_pop = Population()

        test_pop.set(
            amt_cores=amt_cores_value,
            verbosity=1,
            M_2=1,
            orbital_period=100000,
            data_dir=data_dir_value,
            C_logging_code=custom_logging_string,  # input it like this.
            parse_function=parse_function_test_grid_evolve_2_threads_with_custom_logging,
        )
        test_pop.set(ensemble=0)
        resolution = {"M_1": 2}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        output_names = [
            os.path.join(
                data_dir_value,
                "test_grid_evolve_2_threads_with_custom_logging_outputfile_population_{}_thread_{}.dat".format(
                    analytics["population_name"], thread_id
                ),
            )
            for thread_id in range(amt_cores_value)
        ]

        for output_name in output_names:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                output_string = f.read()

            self.assertIn("MY_STELLAR_DATA_TEST_EXAMPLE", output_string)

            remove_file(output_name)

    def test_grid_evolve_with_condition_error(self):
        """
        Unittests to see if the threads catch the errors correctly.
        """

        test_pop = Population()
        test_pop.set(amt_cores=2, verbosity=1, M_2=1, orbital_period=100000)

        # Set the amt of failed systems that each thread will log
        test_pop.set(failed_systems_threshold=4)

        CUSTOM_LOGGING_STRING_WITH_EXIT = """
        Exit_binary_c(BINARY_C_NORMAL_EXIT, "testing exits");
        Printf("TEST_CUSTOM_LOGGING_1 %30.12e %g %g %g %g\\n",
            //
            stardata->model.time, // 1
            
            // masses
            stardata->common.zero_age.mass[0], //
            stardata->common.zero_age.mass[1], //

            stardata->star[0].mass,
            stardata->star[1].mass
            );
        """

        test_pop.set(C_logging_code=CUSTOM_LOGGING_STRING_WITH_EXIT)

        resolution = {"M_1": 10}
        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.1503788456014623), 1e-10
        )  #
        self.assertLess(np.abs(analytics["failed_prob"] - 0.1503788456014623), 1e-10)  #
        self.assertEqual(analytics["failed_systems_error_codes"], [0])
        self.assertTrue(analytics["total_count"] == 10)
        self.assertTrue(analytics["failed_count"] == 10)
        self.assertTrue(analytics["errors_found"] == True)
        self.assertTrue(analytics["errors_exceeded"] == True)

        # test to see if 1 thread does all the systems

        test_pop = Population()
        test_pop.set(amt_cores=2, verbosity=1, M_2=1, orbital_period=100000)

        resolution = {"M_1": 10, "q": 2}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        test_pop.add_grid_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            resolution="{}".format(resolution["q"]),
            spacingfunc="const(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            # condition="M_1 in dir()",  # Impose a condition on this grid variable. Mostly for a check for yourself
            condition="'random_var' in dir()",  # This will raise an error because random_var is not defined.
        )

        self.assertRaises(ValueError, test_pop.evolve)

    def test_grid_evolve_no_grid_variables(self):
        """
        Unittests to see if errors are raised if there are no grid variables
        """

        test_pop = Population()
        test_pop.set(amt_cores=1, verbosity=1, M_2=1, orbital_period=100000)

        resolution = {"M_1": 10}
        self.assertRaises(ValueError, test_pop.evolve)

    def test_grid_evolve_2_threads_with_ensemble_direct_output(self):
        """
        Unittests to see if multiple threads output the ensemble information to files correctly
        """

        data_dir_value = binary_c_temp_dir
        amt_cores_value = 2

        test_pop = Population()
        test_pop.set(
            amt_cores=amt_cores_value,
            verbosity=1,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
        )
        test_pop.set(
            data_dir=binary_c_temp_dir,
            ensemble_output_name="ensemble_output.json",
            combine_ensemble_with_thread_joining=False,
        )

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        output_names = [
            os.path.join(
                data_dir_value,
                "ensemble_output_{}_{}.json".format(
                    analytics["population_name"], thread_id
                ),
            )
            for thread_id in range(amt_cores_value)
        ]

        for output_name in output_names:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                file_content = f.read()

                self.assertTrue(file_content.startswith("ENSEMBLE_JSON"))

                ensemble_json = extract_ensemble_json_from_string(file_content)

                self.assertTrue(isinstance(ensemble_json, dict))
                self.assertNotEqual(ensemble_json, {})

                self.assertIn("number_counts", ensemble_json)
                self.assertNotEqual(ensemble_json["number_counts"], {})

    def test_grid_evolve_2_threads_with_ensemble_combining(self):
        """
        Unittests to see if multiple threads correclty combine the ensemble data and store them in the grid
        """

        data_dir_value = binary_c_temp_dir
        amt_cores_value = 2

        test_pop = Population()
        test_pop.set(
            amt_cores=amt_cores_value,
            verbosity=1,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
        )
        test_pop.set(
            data_dir=binary_c_temp_dir,
            combine_ensemble_with_thread_joining=True,
            ensemble_output_name="ensemble_output.json",
        )

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()

        self.assertTrue(isinstance(test_pop.grid_options["ensemble_results"], dict))
        self.assertNotEqual(test_pop.grid_options["ensemble_results"], {})

        self.assertIn("number_counts", test_pop.grid_options["ensemble_results"])
        self.assertNotEqual(
            test_pop.grid_options["ensemble_results"]["number_counts"], {}
        )

    def test_grid_evolve_2_threads_with_ensemble_comparing_two_methods(self):
        """
        Unittests to compare the method of storing the combined ensemble data in the object and writing them to files and combining them later. they have to be the same
        """

        data_dir_value = binary_c_temp_dir
        amt_cores_value = 2

        # First
        test_pop_1 = Population()
        test_pop_1.set(
            amt_cores=amt_cores_value,
            verbosity=1,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
        )
        test_pop_1.set(
            data_dir=binary_c_temp_dir,
            combine_ensemble_with_thread_joining=True,
            ensemble_output_name="ensemble_output.json",
        )

        resolution = {"M_1": 10}

        test_pop_1.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics_1 = test_pop_1.evolve()
        ensemble_output_1 = test_pop_1.grid_options["ensemble_results"]

        # second
        test_pop_2 = Population()
        test_pop_2.set(
            amt_cores=amt_cores_value,
            verbosity=1,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
        )
        test_pop_2.set(
            data_dir=binary_c_temp_dir,
            ensemble_output_name="ensemble_output.json",
            combine_ensemble_with_thread_joining=False,
        )

        resolution = {"M_1": 10}

        test_pop_2.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            resolution="{}".format(resolution["M_1"]),
            spacingfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics_2 = test_pop_2.evolve()
        output_names_2 = [
            os.path.join(
                data_dir_value,
                "ensemble_output_{}_{}.json".format(
                    analytics_2["population_name"], thread_id
                ),
            )
            for thread_id in range(amt_cores_value)
        ]
        ensemble_output_2 = {}

        for output_name in output_names_2:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                file_content = f.read()

                self.assertTrue(file_content.startswith("ENSEMBLE_JSON"))

                ensemble_json = extract_ensemble_json_from_string(file_content)

                ensemble_output_2 = merge_dicts(ensemble_output_2, ensemble_json)

        for key in ensemble_output_1["number_counts"]["stellar_type"]["0"]:
            self.assertIn(key, ensemble_output_2["number_counts"]["stellar_type"]["0"])

            # compare values
            self.assertLess(
                np.abs(
                    ensemble_output_1["number_counts"]["stellar_type"]["0"][key]
                    - ensemble_output_2["number_counts"]["stellar_type"]["0"][key]
                ),
                1e-8,
            )


if __name__ == "__main__":
    unittest.main()
