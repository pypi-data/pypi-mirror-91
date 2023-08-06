#include <Python.h>
#include "binary_c_python.h"
#include <time.h>
#include <sys/timeb.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

/*
 * binary_c/PYTHON API interface functions
 *
 * This module will be available as _binary_c_bindings, as a part of the binarycpython package.
 * 
 * The first section contains the functions that will be available 
 * to python as part of the submodule _binary_c_bindings
 * 
 * The second section is composed of the functions that interface with the binary_c API 
 *
 * Written by David Hendriks (davidhendriks93@gmail.com), Robert Izzard (r.izzard@surrey.ac.uk). 
 * Based on initial work of Jeff Andrews
 * Remember: variables must be passed by references
 * (i.e. as pointers).
 *
 * See tests/python_API_test.py for an example of how to use these functions.
 *
 * Backup reading material for making C-extensions:
 * http://www-h.eng.cam.ac.uk/help/tpl/languages/mixinglanguages.html
 * https://realpython.com/build-python-c-extension-module/
 * https://docs.python.org/3/extending/extending.html
 * https://docs.python.org/3/c-api/arg.html#c.PyArg_ParseTuple
 * https://realpython.com/python-bindings-overview/
 * http://scipy-lectures.org/advanced/interfacing_with_c/interfacing_with_c.html
 * 
 * Open tasks for the Extension:
 * TODO: Put in clear debug statements
 * TODO: properly return stderr
 * TODO: describe all functions with docstrings
 * TODO: properly pass through all the pointers using Capsules:  
    https://docs.python.org/3.6/c-api/capsule.html#c.PyCapsule_New
    https://gist.github.com/Sleepingwell/5259476
    https://bfroehle.com/2011/07/18/python-capsules/
    https://docs.python.domainunion.de/3.6/howto/cporting.html
    https://lappweb.in2p3.fr/~paubert/ASTERICS_HPC/5-6-3-651.html
    https://www.geeksforgeeks.org/c-api-from-extension-module-in-python-set-1/
    http://pageperso.lif.univ-mrs.fr/~francois.denis/IAAM1/python-3.6.5rc1-docs-html/howto/cporting.html
    http://python3porting.com/cextensions.html
    
 */


/************************************************************
 ************************************************************
 ** Section 1: Python module functions and creation of module
 ************************************************************
 ************************************************************/

/************************************************************
 *
 * function prototypes : these are the functions
 * called by PYTHON code, without the trailing underscore.
 *
 ************************************************************/

/* Preparing all the functions of the module */
// Docstrings
static char module_docstring[] MAYBE_UNUSED =
    "This module is a python3 wrapper around binary_c";

// Evolution function docstrings
static char run_system_docstring[] = 
    "Function to run a system. This is a general function that will be able to handle different kinds of situations: single system run with different settings, population run with different settings, etc. To avoid having too many functions doing slightly different things. \n\nArguments:\n\targstring: argument string for binary_c\n\t(opt) custom_logging_func_memaddr: memory address value for custom logging function. Default = -1 (None)\n\t(opt) store_memaddr: memory adress of the store. Default = -1 (None)\n\t(opt) write_logfile: Boolean (in int form) for whether to enable the writing of the log function. Default = 0\n\t(opt) population: Boolean (in int form) for whether this system is part of a population run. Default = 0.";

// Utility function docstrings
static char return_arglines_docstring[] =
    "Return the default args for a binary_c system";
static char return_help_info_docstring[] = 
    "Return the help info for a given parameter";
static char return_help_all_info_docstring[] = 
    "Return an overview of all the parameters, their description, categorized in sections";
static char return_version_info_docstring[] = 
    "Return the version information of the used binary_c build";

// other functionality
static char return_store_memaddr_docstring[] = 
    "Return the store memory adress that will be passed to run_population";
static char return_persistent_data_memaddr_docstring[] = 
    "Return the store memory adress that will be passed to run_population";

static char free_persistent_data_memaddr_and_return_json_output_docstring[] = 
    "Frees the persistent_data memory and returns the json output";
static char free_store_memaddr_docstring[] = 
    "Frees the store memaddr";
static char test_func_docstring[] = 
    "Function that contains random snippets. Do not expect this to remain available, or reliable. i.e. dont use it. ";

/* Initialize pyobjects */

// Evolution function headers
static PyObject* binary_c_run_system(PyObject *self, PyObject *args, PyObject *kwargs);

// Utility function headers
static PyObject* binary_c_return_arglines(PyObject *self, PyObject *args);
static PyObject* binary_c_return_help_info(PyObject *self, PyObject *args);
static PyObject* binary_c_return_help_all_info(PyObject *self, PyObject *args);
static PyObject* binary_c_return_version_info(PyObject *self, PyObject *args);

// Other function headers
static PyObject* binary_c_return_store_memaddr(PyObject *self, PyObject *args);
static PyObject* binary_c_return_persistent_data_memaddr(PyObject *self, PyObject *args);

// Free functions
static PyObject* binary_c_free_persistent_data_memaddr_and_return_json_output(PyObject *self, PyObject *args);
static PyObject* binary_c_free_store_memaddr(PyObject *self, PyObject *args);
static PyObject* binary_c_test_func(PyObject *self, PyObject *args);



/* Set the module functions */
static PyMethodDef module_methods[] = {
    // Wierdly, this casting to a PyCFunction, which usually takes only 2 args, now works when giving keywords. See https://stackoverflow.com/q/10264080
    {"run_system", (PyCFunction)binary_c_run_system, METH_VARARGS|METH_KEYWORDS, run_system_docstring}, 

    //
    {"return_arglines", binary_c_return_arglines, METH_VARARGS, return_arglines_docstring},
    {"return_help", binary_c_return_help_info, METH_VARARGS, return_help_info_docstring},
    {"return_help_all", binary_c_return_help_all_info, METH_VARARGS, return_help_all_info_docstring},
    {"return_version_info", binary_c_return_version_info, METH_VARARGS, return_version_info_docstring},

    //
    {"return_store_memaddr", binary_c_return_store_memaddr, METH_VARARGS, return_store_memaddr_docstring},
    {"return_persistent_data_memaddr", binary_c_return_persistent_data_memaddr, METH_NOARGS, return_persistent_data_memaddr_docstring},

    //
    {"free_persistent_data_memaddr_and_return_json_output", binary_c_free_persistent_data_memaddr_and_return_json_output, METH_VARARGS, free_persistent_data_memaddr_and_return_json_output_docstring},
    {"free_store_memaddr", binary_c_free_store_memaddr, METH_VARARGS, free_store_memaddr_docstring},
    {"test_func", binary_c_test_func, METH_NOARGS, test_func_docstring},

    //
    {NULL, NULL, 0, NULL}
};

/* ============================================================================== */
/* Making the module                                                              */
/* ============================================================================== */

/* Initialise the module. Removed the part which supports python 2 here on 17-03-2020 */
/* Python 3+ */
static struct PyModuleDef Py__binary_c_bindings =
{
    PyModuleDef_HEAD_INIT,
    "_binary_c_bindings", /* name of module */
    "Module to interface the Binary_c API with python.",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit__binary_c_bindings(void)
{
    return PyModule_Create(&Py__binary_c_bindings);
}

/* ============================================================================== */
/* Some function that we started out with. Unused now.                            */
/* ============================================================================== */

/*
    Below are the real functions:
    binary_c_run_population
    binary_c_run_system

    binary_c_return_arglines
    binary_c_return_help_info
    binary_c_return_help_all_info
    binary_c_return_version_info
*/

/* ============================================================================== */
/* Wrappers to functions that evolve binary systems.                              */
/* ============================================================================== */

static PyObject* binary_c_run_system(PyObject *self, PyObject *args, PyObject *kwargs)
{

    static char* keywords[] = {"argstring", "custom_logging_func_memaddr", "store_memaddr", "persistent_data_memaddr", "write_logfile", "population", NULL};

    /* set vars and default values for some*/
    char *argstring;
    long int custom_logging_func_memaddr = -1;
    long int store_memaddr = -1;
    long int persistent_data_memaddr = -1;
    int write_logfile = 0;
    int population = 0;

    // By using the keywords argument it scans over the given set of kwargs, but if they are not given then the default value is used
    /* Parse the input tuple */
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "s|lllii", keywords, &argstring, &custom_logging_func_memaddr, &store_memaddr, &persistent_data_memaddr, &write_logfile, &population))
    {
        return NULL;
    }

    // printf("Input persistent_Data_memaddr: %lu\n", persistent_data_memaddr);

    /* Call c-function */
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = run_system(argstring,                    // the argstring
                                      custom_logging_func_memaddr,  // memory adress for the function for custom logging
                                      store_memaddr,                // memory adress for the store object
                                      persistent_data_memaddr,      // memory adress for the persistent data
                                      write_logfile,                // boolean for whether to write the logfile
                                      population,                   // boolean for whether this is part of a population.
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    /* Display error */
    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_run_system): %s\n",
                error_buffer);
    }

    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

/* ============================================================================== */
/* Wrappers to functions that call other API functionality like help and arglines */
/* ============================================================================== */

static PyObject* binary_c_return_arglines(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_arglines(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_arglines): %s\n",
                error_buffer);
    }

    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_help_info(PyObject *self, PyObject *args)
{
    /* Parse the input tuple */
    char *argstring;
    
    if(!PyArg_ParseTuple(args, "s", &argstring))
    {
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_help_info(argstring,
                                          &buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_help_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_help_all_info(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_help_all_info(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_help_all_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_return_version_info(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    int out MAYBE_UNUSED = return_version_info(&buffer,
                                          &error_buffer,
                                          &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_version_info): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

/* ============================================================================== */
/* Wrappers to functions that call other functionality */
/* ============================================================================== */

static PyObject* binary_c_return_store_memaddr(PyObject *self, PyObject *args)
{
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    long int out MAYBE_UNUSED = return_store_memaddr(&buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    PyObject * store_memaddr = Py_BuildValue("l", out);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_store_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return store_memaddr;
}

static PyObject* binary_c_return_persistent_data_memaddr(PyObject *self, PyObject *args)
{
    /* Python binding that wraps the c function which calls the binary_c api endpoint. */
    char * buffer;
    char * error_buffer;
    size_t nbytes;
    long int out MAYBE_UNUSED = return_persistent_data_memaddr(&buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    PyObject * persistent_data_memaddr = Py_BuildValue("l", out);
    // printf("persistent_data_memaddr: %ld\n", out);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_return_persistent_data_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return persistent_data_memaddr;
}

/* Memory freeing functions */
static PyObject* binary_c_free_persistent_data_memaddr_and_return_json_output(PyObject *self, PyObject *args)
{
    /* Python binding that calls the c function that free's the persistent data memory and prints out the json */

    long int persistent_data_memaddr = -1;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "l", &persistent_data_memaddr))
    {
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;

    long int out MAYBE_UNUSED = free_persistent_data_memaddr_and_return_json_output(persistent_data_memaddr,
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_free_persistent_data_memaddr_and_return_json_output): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    return return_string;
}

static PyObject* binary_c_free_store_memaddr(PyObject *self, PyObject *args)
{
    /* Python binding that calls the c function that free's the store memory */
    long int store_memaddr = -1;

    /* Parse the input tuple */
    if(!PyArg_ParseTuple(args, "l", &store_memaddr))
    {
        fprintf(stderr,
                "Error (in function: binary_c_free_store_memaddr): Got a bad input\n");
        return NULL;
    }

    char * buffer;
    char * error_buffer;
    size_t nbytes;

    long int out MAYBE_UNUSED = free_store_memaddr(store_memaddr,
                                      &buffer,
                                      &error_buffer,
                                      &nbytes);

    /* copy the buffer to a python string */
    PyObject * return_string MAYBE_UNUSED = Py_BuildValue("s", buffer);
    PyObject * return_error_string MAYBE_UNUSED = Py_BuildValue("s", error_buffer);

    if(error_buffer != NULL && strlen(error_buffer)>0)
    {
        fprintf(stderr,
                "Error (in function: binary_c_free_store_memaddr): %s\n",
                error_buffer);
    }
    
    Safe_free(buffer);
    Safe_free(error_buffer);

    Py_RETURN_NONE;
}


static PyObject* binary_c_test_func(PyObject *self, PyObject *args)
{
    // function to see if we can access the stability string
    printf("%s", RLOF_stability_string(1));

    Py_RETURN_NONE;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////

/************************************************************
 ************************************************************
 ** Section 2: binary_c interfacing functions
 **
 ** These functions call the binary_c API 
 ************************************************************
 ************************************************************/

/* Binary_c python API 
 * Set of c-functions that interface with the binary_c api.
 * These functions are called by python, through the functions defined above. 
 * 
 * Contains several functions:
 * // evolution functions:
 * run_system

 * // utility functions:
 * return_arglines
 * return_help_info
 * return_help_all_info
 * return_version_info

 * // memory allocating functions:
 * return_store_memaddr
 * free_persistent_data_memaddr_and_return_json_output
 * 
 * // Memory freeing functions:
 * free_store_memaddr 
 * free_persistent_data_memaddr_and_return_json_output
 */

// #define _CAPTURE
#ifdef _CAPTURE
static void show_stdout(void);
static void capture_stdout(void);
#endif

/* global variables */
int out_pipe[2];
int stdoutwas;

/* =================================================================== */
/* Functions to evolve systems                                         */
/* =================================================================== */

/* 
Function that runs a system. Has multiple input parameters:
Big function. Takes several arguments. See binary_c_python.c docstring.
TODO: Describe each input
*/
int run_system(char * argstring,
               long int custom_logging_func_memaddr,
               long int store_memaddr,
               long int persistent_data_memaddr,
               int write_logfile,
               int population,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* memory for system */
    struct libbinary_c_stardata_t *stardata = NULL;

    // Store:
    /* Check the value of the store_memaddr */
    struct libbinary_c_store_t *store;
    if(store_memaddr != -1)
    {
        // load the store from the integer that has been passed
        store = (void*)store_memaddr;
    }
    else
    {
        // struct libbinary_c_store_t * store = NULL;
        store = NULL;
    }

    // persistent_data:
    struct libbinary_c_persistent_data_t *persistent_data;
    if(persistent_data_memaddr != -1)
    {
        // load the persistent data from the long int that has been passed
        persistent_data = (void*)persistent_data_memaddr;
        debug_printf("Took long int memaddr %ld and loaded it to %p\n", persistent_data_memaddr, (void*)&persistent_data);
    }
    else
    {
        persistent_data = NULL;
        debug_printf("persistent_data memory adress was -1, now setting it to NULL\n");
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &argstring,         // argv
                        -1                  // argc
    );

    // Add flag to enable
    /* disable logging */
    if(write_logfile != 1)
    {
        snprintf(stardata->preferences->log_filename,
                 STRING_LENGTH-1,
                 "%s",
                 "/dev/null");
        snprintf(stardata->preferences->api_log_filename_prefix,
                 STRING_LENGTH-1,
                 "%s",
                 "/dev/null");
    }

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Check the value of the custom_logging_memaddr */
    if(custom_logging_func_memaddr != -1)
    {
        stardata->preferences->custom_output_function = (void*)(struct stardata_t *)custom_logging_func_memaddr;
    }

    debug_printf("ensemble_defer: %d\n", stardata->preferences->ensemble_defer);

    /* do binary evolution */
    binary_c_evolve_for_dt(stardata,
                           stardata->model.max_evolution_time);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* Determine whether to free the store memory adress*/
    Boolean free_store = FALSE;
    if (store_memaddr == -1)
    {
	debug_printf("Decided to free the store memaddr\n");
        free_store = TRUE;
    }

    /* Determine whether to free the persistent data memory adress*/
    Boolean free_persistent_data = FALSE;
    if (persistent_data_memaddr == -1)
    {
        debug_printf("Decided to free the persistent_data memaddr\n");
        free_persistent_data = TRUE;
    }

    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        free_store,                 // free_store
        FALSE,                      // free_raw_buffer
        free_persistent_data        // free_persistent
    );

    return 0;
}

/* =================================================================== */
/* Functions to call other API functionality like help and arglines    */
/* =================================================================== */

int return_arglines(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* memory for N binary systems */
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;
    char *empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* disable logging */
    snprintf(stardata->preferences->log_filename,
             STRING_LENGTH-1,
             "%s",
             "/dev/null");
    snprintf(stardata->preferences->api_log_filename_prefix,
             STRING_LENGTH-1,
             "%s",
             "/dev/null");

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* List available arguments */
    binary_c_list_args(stardata);

    /* get buffer pointer */
    binary_c_buffer_info(stardata,buffer,nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata,error_buffer);
    
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );
    
    return 0;
}


int return_help_info(char * argstring,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &argstring,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_help(stardata, argstring);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}


int return_help_all_info(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_help_all(stardata);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}


int return_version_info(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_version(stardata);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
    
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}

/* =================================================================== */
/* Functions to set up memory                                          */
/* =================================================================== */

long int return_store_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t * stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer and the store) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        FALSE,                      // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    /* convert the pointer */ 
    uintptr_t store_memaddr_int = (uintptr_t)store; // C Version converting ptr to int
    debug_printf("store is at address: %p store_memaddr_int: %ld\n", (void*)&store, store_memaddr_int);

    /* Return the memaddr as an int */
    return store_memaddr_int;
}


long int return_persistent_data_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* Function to allocate the persistent_data_memaddr */
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    struct libbinary_c_persistent_data_t * persistent_data = NULL; 
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* convert the pointer */
    uintptr_t persistent_data_memaddr_int = (uintptr_t)stardata->persistent_data; // C Version converting ptr to int
    debug_printf("persistent_data is at address: %p persistent_data_memaddr_int: %ld\n", (void*)&stardata->persistent_data, persistent_data_memaddr_int);
    
    /* free stardata (except the buffer and the persistent data) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        FALSE                       // free_persistent
    );

    /* Return the memaddr as an int */
    return persistent_data_memaddr_int;
}

/* =================================================================== */
/* Functions to free memory                                            */
/* =================================================================== */

int free_persistent_data_memaddr_and_return_json_output(long int persistent_data_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_store_t *store = NULL;
    struct libbinary_c_stardata_t *stardata = NULL;
    char * empty_str = "";

    // persistent_data:
    struct libbinary_c_persistent_data_t *persistent_data;
    if(persistent_data_memaddr != -1)
    {
        // load the persistent data from the long int that has been passed
        persistent_data = (void*)persistent_data_memaddr;
        debug_printf("Took long int memaddr %ld and loaded it to %p\n", persistent_data_memaddr, (void*)&persistent_data);
    }
    else
    {
        printf("ERROR: this function needs a valid persistent_data_memaddr value. not -1\n");
        // persistent_data = NULL;
        // TODO: put break in the function here. 
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* Set the model hash (usually done internally but we're not evolving a system here */
    stardata->model.ensemble_hash = stardata->persistent_data->ensemble_hash;

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get output and free memory */
    binary_c_output_to_json(stardata);

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* free the reststardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        FALSE                       // free_persistent. It already 
    );

    return 0;
}

int free_store_memaddr(long int store_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_persistent_data_t *persistent_data = NULL;
    char * empty_str = "";

    // Store:
    /* Check the value of the store_memaddr */
    struct libbinary_c_store_t *store;
    if(store_memaddr != -1)
    {
        // load the store from the integer that has been passed
        store = (void*)store_memaddr;
        debug_printf("Took long int store_memaddr %ld and loaded it to %p\n", store_memaddr, (void*)&store);
    }
    else
    {
        store = NULL;
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    debug_printf("freed store memaddr\n");

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* free the reststardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}
