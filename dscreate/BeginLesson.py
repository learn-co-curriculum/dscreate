import os
import json

text = ['import os\n',
 'import glob\n',
 'import types\n',
 '\n',
 'import pickle as pkl\n',
 '\n',
 'import numpy as np\n',
 'import pandas as pd\n',
 'from IPython.display import Markdown, display\n',
 '\n',
 '\n',
 'class Test():\n',
 '    """\n',
 '        Provides a way for students to check their objects against \n',
 '        objects created in solution cells\n',
 '        How to use this class\n',
 '        ---------------------\n',
 '        In a solution cell: \n',
 '        once you have an object you would like students to replicate,\n',
 '        call Test().save(object, object_nickname) to pkl the object\n',
 '        in a class-defined directory\n',
 '            This will: \n',
 "                - check to see if there's a directory at the level of the book called test_obj, \n",
 "                and create it if there's not.  (The directory name can be altered \n",
 '                with the attribute Test().dir)\n',
 '                - check to see if there\'s a file at the path f"test_obj/{object_nickname+\'.pkl\'}"\n',
 '                If there is, it is deleted.  (This allows for writing Test().save once and \n',
 '                re-saving the object every time the cell is run)\n',
 '                - pkl the object and save it at the path f"test_obj/{object_nickname+\'.pkl\'}"\n',
 '        In a student-facing cell: \n',
 '        call Test().run_test(student_object, object_nickname) and have students run the cell\n',
 "        to check whether their object matches the pkl'd object\n",
 '            This will: \n',
 '                - import the pkl\'d object at the path f"test_obj/{object_nickname+\'.pkl\'}"\n',
 '                - run an assert against the student-created object "student_object" and the pkl\'d object\n',
 '                - print "Hey, you did it.  Good job" if an AssertError is not thrown, "try again" if one is\n',
 '                - the variable name of the first parameter is not bound by anything and need not be\n',
 "                the original name of the object that was pkl'd.  It's up to the instructor whether\n",
 '                to\n',
 '                    - tell students to create an object with a specific name, and pre-populate\n',
 '                    Test.run_test() with that name as the first parameter\n',
 '                    - not specify a name for students to assign student_object, but rely on\n',
 '                    the student to place their object as the first parameter for Test.run_test()\n',
 '        Type-specific assert methods\n',
 '        ----------------------------\n',
 '        Some types need additional methods to be asserted.  \n',
 '        Examples include numpy arrays, pandas series and dataframes.  \n',
 '        These type-specific methods are run if an object of that type is the first\n',
 '        parameter for Test().run_test\n',
 '        A dictionary containing these type-specific assert methods is stored in Test().obj_tests_dict \n',
 '        with the type as the key.\n',
 '        There is a Test().obj_tests_dict_kwargs attribute which contains parameters to pass to \n',
 '        type-specific assertion methods.  \n',
 '        The dataframe assertion method has a "check_like" parameter which ignores the sort order\n',
 '        and will assert True if identical frames sorted differently are compared.  This class \n',
 '        sets "check_like" to True by default.\n',
 '        Is this robust for students with Windows filepaths?\n',
 '        ---------------------------------------------------\n',
 '        Not yet, working on it.\n',
 '    """\n',
 '    \n',
 "    def __init__(self, directory='test_obj'):\n",
 '                \n',
 '        self.directory=directory\n',
 '        \n',
 '        self.obj_tests_dict = {\n',
 '            np.ndarray: np.testing.assert_array_equal,\n',
 '            pd.core.series.Series: pd.testing.assert_series_equal,\n',
 '            pd.core.frame.DataFrame: pd.testing.assert_frame_equal,\n',
 '            types.MethodType: lambda x, y: x.__code__.co_code == y.__code__.co_code\n',
 '        }\n',
 '\n',
 '        self.obj_tests_dict_kwargs = {\n',
 '            np.ndarray: {},\n',
 '            pd.core.series.Series: {},\n',
 "            pd.core.frame.DataFrame: {'check_like': True},\n",
 '            types.MethodType: {}\n',
 '        }\n',
 '\n',
 '        return\n',
 '\n',
 '    def test_dir(self):\n',
 "        '''\n",
 '        check if test_obj dir is there; if not, create it\n',
 "        '''\n",
 '\n',
 '        if not os.path.isdir(self.directory):\n',
 '            os.mkdir(self.directory)\n',
 '\n',
 '        return\n',
 '\n',
 '    def get_file_name(self, glob_listing):\n',
 "        '''\n",
 '        gets str of one file name in test_obj dir w/o .pkl extension\n',
 '        Parameters:\n',
 '            glob_listing: single returned object from glob\n',
 '        Output:\n',
 '            str of file name w/o .pkl extension\n',
 "        '''\n",
 '\n',
 '        #get filename\n',
 '        directory, file_name = os.path.split(glob_listing)\n',
 '        \n',
 '        # remove .pkl\n',
 '        listing, file_extension = os.path.splitext(file_name)\n',
 '        return listing\n',
 '\n',
 '    def save_ind(self, object, object_name):\n',
 "        '''\n",
 '        saves object to test_obj dir w/ object_name.pkl\n',
 '        Parameters:\n',
 '            object: object to pkl\n',
 '            object_name: pkl file name\n',
 "        '''\n",
 '        \n',
 "        with open(os.path.join(self.directory, f'{object_name}.pkl'), 'wb') as f:\n",
 '            pkl.dump(object, f)\n',
 '\n',
 '        return\n',
 '\n',
 '    def save(self, object, object_name):\n',
 "        '''\n",
 '        parse test_obj dir to see if object_name.pkl prev saved\n',
 '        if so, delete it\n',
 "        save object under f'test_obj/{object_name}.pkl'\n",
 '        Parameters:\n',
 '            object: object to save as pkl file\n',
 '            object_name: name to save pkl object as under f\'test_obj/{object_name+".pkl"}\'\n',
 "        '''\n",
 '        self.test_dir()\n',
 '\n',
 '        files = glob.glob(\n',
 '            os.path.join(\n',
 "                self.directory, f'{object_name}.pkl'\n",
 '            )\n',
 '        )\n',
 '\n',
 '        existing_files = [self.get_file_name(file) for file in files]\n',
 '\n',
 "        if object_name+'.pkl' in existing_files:\n",
 '            os.remove(\n',
 '                os.path.join(\n',
 "                    self.directory, f'{object_name}.pkl'\n",
 '                )\n',
 '            )\n',
 '\n',
 '        self.save_ind(object, object_name)\n',
 '\n',
 '        return\n',
 '\n',
 '    def load_ind(self, object_name):\n',
 "        '''\n",
 '        loads and unpkls object from f"self.dir/{object_name+\'.pkl\'}"\n',
 "        returns: unpkl'd object\n",
 "        '''\n",
 '\n',
 "        with open(os.path.join(self.directory, f'{object_name}.pkl'), 'rb') as f:\n",
 '            obj = pkl.load(f)\n',
 '\n',
 '        return obj\n',
 '\n',
 '    def output(self, result=True):\n',
 '\n',
 '        if result:\n',
 "            display(Markdown('✅ **Hey, you did it.  Good job.**'))\n",
 '        else:\n',
 "            display(Markdown('❌ **Try Again**'))\n",
 '\n',
 '    def run_test(self, obj, name):\n',
 "        '''\n",
 '        runs assert against obj and f"self.dir/{name+\'.pkl\'}"\n',
 '        checks type of obj and, if type has assert method in self.obj_tests_dict, runs\n',
 '        that assert method instead.  Any kwargs for that asssert method in \n',
 '        obj_tests_dict_kwargs are also passed.\n',
 "        '''\n",
 '\n',
 '        kind = type(obj)\n',
 '\n',
 '        test_obj = self.load_ind(name)\n',
 '\n',
 '        try:\n',
 '            if kind in self.obj_tests_dict.keys():\n',
 '                self.obj_tests_dict[kind](\n',
 '                    obj, test_obj, **self.obj_tests_dict_kwargs[kind])\n',
 '\n',
 '            else:\n',
 '                assert obj == test_obj\n',
 '\n',
 '            self.output()\n',
 '\n',
 '        except AssertionError:\n',
 '\n',
 '            self.output(result=False)']

def begin():
    notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "===SOLUTION===\n",
    "\n",
    ">This notebook is meant for curriculum development. \n",
    "\n",
    "## Instructions:\n",
    "\n",
    "### Overview\n",
    "\n",
    "When you have completed writing your lesson, run `ds -create` from the root of this lesson folder. This will create an `index.ipynb` notebook containing the student facing content in the root directory of this lesson. An `index.ipynb` file will be added to the `.solution_files` directory containing all solution materials. \n",
    "\n",
    "## How to use this file\n",
    "\n",
    "**Solution Tags:**\n",
    "\n",
    "Markdown cells: \n",
    "- `===SOLUTION===`\n",
    "\n",
    "Code cells: \n",
    "- `#__SOLUTION__`\n",
    "\n",
    "\n",
    "#### Create Solution Cells:\n",
    "- To designate a cell as a solution, place the solution tag on its own line within the cell. This cell is an example of a \"solution markdown cell\".\n",
    "\n",
    "- Below is an example of a solution code cell."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {},
   "outputs": [],
   "source": [
    "#__SOLUTION__\n",
    "\n",
    "\"\"\"\n",
    "This is a solution cell and \n",
    "will not be copied \n",
    "to the lesson index.ipynb file\n",
    "\"\"\""
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 2
}


    notebook_file = open('curriculum.ipynb', 'w')
    json.dump(notebook, notebook_file)
    notebook_file.close()

    if not os.path.isdir('data'):
        os.mkdir('data')

    if not os.path.isdir('.test_scripts'):
        os.mkdir('.test_scripts')


    test_path = os.path.join('.test_scripts', 'test_script.py')
    test_file = open(test_path, 'w')
    test_file.writelines(text)
    test_file.close()


