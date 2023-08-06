"""
    Copyright 2020 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""

import re
from typing import List
from cdmn.idpname import idp_name

"""
The glossary object contains the entire cDMN glossary table.
It interprets each line, and creates a Type or Predicate object.

A Type is a "variable" in cDMN. There's three types of Type:

    * Normal Type
    * DateType
    * DateInt

DateType is a representation of dates.
DateType has a different vocabulary and structure.

DateInt is a representation of operation on dates.
DateInt is actually a representation of two things: a DateInt variable, and an
xBetween variable (where x is either Day, Week or Month).
"""


class Glossary:
    """
    The Glossary object contains all types, functions and predicates.
    During initialisation, it reads and interprets all the types, functions,
    constants, relations and booleans it can find and it reports any errors.
    Once the Glossary is created and initialized without errors, it's
    possible to print out the predicates in their IDP version.
    """
    def __init__(self, glossary_dict: dict):
        """
        Initialise the glossary.
        Create 4 default types, create an empty list of predicates, and
        interpret all 5 different glossaries.

        :arg dict: glossary_dict, the dictionary containing for each glossary
            type their tables.
        """
        self.types = [Type('String', None),
                      Type('Int', None),
                      Type('Float', None),
                      Type('DateString', None),
                      Type('Real', None)]
        self.predicates: List[Predicate] = []
        self.__read_types(glossary_dict["Type"], 0, 1, 2)
        self.__read_predicates(glossary_dict["Function"], "Function")
        self.__read_predicates(glossary_dict["Constant"], "Constant",
                               zero_arity=True)
        self.__read_predicates(glossary_dict["Relation"], "Relation")
        self.__read_predicates(glossary_dict["Boolean"], "Boolean",
                               zero_arity=True)

    def __str__(self):
        """
        Magic method to convert the Glossary to string.
        Prints out all the types, predicates and functions it contains.
        """
        retstr = "Glossary containing:\n"
        for typ in self.types:
            retstr += "\t{}\n".format(str(typ))
        for pred in self.predicates:
            retstr += "\t{}\n".format(str(pred))
        return retstr

    def contains(self, typestr):
        """
        Checks whether or not a type was already added to the glossary.

        :returns bool: True if the type has been added already.
        """
        for typ in self.types:
            if typestr == typ.name:
                return True
        return False

    def find_type(self, t):
        """
        Looks for types in the glossary.

        :returns List<Type>: the types found.
        """
        types = []
        for typ in self.types:
            if typ.match(t):
                types.append(typ)
        return next(filter(lambda x: x.match(t), self.types))

    def __read_types(self, array, ix_name=0, ix_type=1, ix_posvals=2):
        """
        Read and interpret all the types listed in the Type glossary.
        When it finds the keyword, it tries to interpret the other columns on
        that row.

        :arg np.array: the numpy array containing the Type glossary.
        :arg int: ix_name, the index for the name column.
        :arg int: ix_type, the index for the type column.
        :arg int: ix_posvals, the type for the posvals column.
        :returns None:
        """
        error_message = ""
        rows, cols = array.shape
        # Skip the first 2 rows, as these are headers.
        for row in array[2:]:
            # Loop over all the rows.
            name = row[ix_name]
            name = name.strip()

            # Get, and try to decypher the type.
            # If we're not able to find the type, raise error.
            typ = row[ix_type]
            try:
                typ = self.find_type(typ)
            except StopIteration:
                error_message = ("DataType \"{}\" should be either a"
                                 " (String, Int, Float, DateString) or a"
                                 " user-defined type"
                                 .format(typ))
                raise ValueError(error_message)

            # Check for possible values.
            posvals = row[ix_posvals]
            try:
                # Match for the int range type, for instance [1, 10].
                int_reg = r'(\[|\()(-?\d+)\s*(?:\.\.|,)\s*(-?\d+)\s*(\]|\))'
                match = re.match(int_reg, posvals)

            except Exception:  # TODO: find errortype to except and fix except.
                match = None

            # Interpret range of int, if a match was found.
            if match:
                match = list(match.groups())
                if match[0] == '(':
                    match[1] += 1
                if match[-1] == ')':
                    match[2] -= 1
                posvals = '..'.join(match[1:-1])
            elif posvals is not None:
                posvals = ', '.join([idp_name(x) for x in
                                    re.split(r'\s*,\s*', posvals)])

            # Check for exception types DateString and DaysBetween and create
            # them if found. Otherwise, create normal Type.
            if typ.name == "DateString":
                self.types.append(DateType(name, typ, posvals))
            elif "Between" in name:
                # DaysBetween needs to be supplied by a list of all the
                # possible dates.
                dates = self._find_dates()
                self.types.append(DateInt(name, typ, posvals, dates))
            else:
                # Create the type and append it to the list.
                self.types.append(Type(name, typ, posvals))

    def __read_predicates(self, array, glosname, ix_name=0,
                          ix_type=1, zero_arity=False):
        """
        Method to read and interpret predicates.
        Loops over an array containing only predicates or functions,
        and filters them into subcategories.

        The possible entries are: Relation, Function, partial Function,
            boolean, and relation..

        :arg array: a glossary table
        :arg glosname: the name of the glossary, i.e. Function, Relation,
            Constant or Boolean
        :arg ix_name: the column index of the name column. By default this is
            always the first column.
        :arg ix_type: the column index of the type column. By default this is
            always the second column.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).

        :returns None:
        """
        # It's possible that there's no glossary defined.
        if array is None:
            return

        for row in array[2:]:
            full_name = row[ix_name].strip()
            partial = False
            typ = None
            predicate = None

            # Check if it's a (partial) function/constant or a
            # relation/boolean.
            if re.match('(partial )?Function|Constant', glosname):
                predicate = False
                typ = row[ix_type]
                if typ:
                    typ = typ.strip()

                # Check if it's a partial function
                partial = bool(re.match('(?i)partial', full_name))
                full_name = full_name.replace('partial ', '')
                try:
                    typ = self.find_type(typ)
                except TypeError:
                    raise ValueError('DataType of Function "{}" is empty'
                                     .format(full_name))
                except StopIteration:
                    raise ValueError('DataType "{}" of "{}" is not an existing'
                                     ' Type'.format(typ, full_name))

            # The predicate is a relation.
            else:
                predicate = True

            # Create the predicate.
            p = Predicate.from_string(full_name, predicate, typ, self,
                                      partial, zero_arity)

            # Append the new predicate to the list.
            self.predicates.append(p)

    def lookup(self, string: str):
        """
        TODO
        REWORK ENTIRE METHOD.
        """
        return list(filter(lambda x: x,
                           map(lambda x: x.lookup(string), self.predicates)))

    def _find_dates(self):
        """
        Looks for types containing DateString and returns the list of all the
        dates it holds.
        """
        for datatype in self.types:
            try:
                if datatype.super_type.name == "DateString":
                    return datatype.struct_args
            except AttributeError:
                continue
        raise ValueError("A DateString needs to be declared before a DateInt")

    def read_datatables(self, datatables, parser):
        """
        Reads and interprets the datatables.
        Also checks if the values in the datatables appear in the possible
        values column of the glossary.

        Firstly it checks which columns are input, and which are output.
        A column is an inputcolumn if it contains the table title in the first
        cell, and an output if it contains `None` in the first cell.

        Iterates over every outputcolumn, deciphers which predicate the
        outputcolumn represents, and sets its "struct_args" to a combination
        of the input arguments and the output column's arguments.
        The predicate uses this struct_args to format its struct string.

        :arg List<np.array>: datatables, containing all the datatables.
        :arg parser:
        :returns None:
        """
        # return
        if len(datatables) == 0:
            return
        for table in datatables:
            inputs = []
            outputs = []
            tablename = table[0][0]
            # First, we find the input and outputcolumns.
            for column in table.T[1:]:
                # If a column contains the table title, it's an inputcolumn.
                if column[0] is not None:
                    # We also want to find out the input variables.
                    inputs.append(column[1:])
                else:
                    outputs.append(column[1:])
            # Second, we check if the inputcolumns contain the right values.
            # This also adds those values to the "constructed from" if needed.
            for i, inputarr in enumerate(inputs):
                header = inputarr[0]
                # The header can be just the Type name, or "Type called ..".
                typename = header.split(" ")[0]

                # Look for the type name in the glossary.
                for typ in self.types:
                    if typename == typ.name:
                        typ.check_values(inputarr[1:], tablename)

            # Third, we check if the outputcolumns contain the right values.
            # This also adds those values to the "constructed from" if needed.
            for i, outputarr in enumerate(outputs):
                header = outputarr[0]
                # The header can be a function like "Department of Person".
                # Or it can be a relation. If it's a relation, we skip.
                typename = header.split(" ")[0]
                pred = parser.interpreter.interpret_value(header).pred
                if pred.is_relation():
                    continue
                typename = pred.super_type.name

                # Look for the type name in the glossary, and check its values.
                for typ in self.types:
                    if typename == typ.name:
                        typ.check_values(outputarr[1:], tablename)

            # Then we iterate over the outputcolumns.
            for i, output in enumerate(outputs):
                header = output[0]
                # Format the args.
                args = {}
                # Iterate over each row of the outputcolumn.
                # Skip the first cell because it's always None.
                for j, value in enumerate(output[1:]):
                    # Find the inputvalues for the same row, in order to create
                    # the `args` dictionary. This contains the output values
                    # for every predicate in a data table.
                    inputvals = []
                    for inputcol in inputs:
                        inputval = str(inputcol[j+1])
                        inputvals.append(inputval)
                    inputval = "|".join(inputvals)

                    args[inputval] = value

                header = parser.interpreter.interpret_value(header).pred.name

                # Look for the predicate name.
                success = False
                for pred in self.predicates:
                    if pred.full_name == header or pred.name == header:
                        pred.struct_args = args
                        success = True
                        break
                if not success:
                    raise ValueError("Predicate \"{}\" in datatable but not in"
                                     " glossary".format(header))

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Function which turns every object in a glossary into their vocabulary
        definitions.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns voc: string
        """
        voc = ''.join(map(lambda x: x.to_idp_voc(target_lang),
                          self.types+self.predicates))
        # Add error specific concepts.
        return voc

    def to_json_dicts(self):
        """
        Creates a dict entry for every predicate and function, which is later
        turned into json.

        :returns dict:
        """
        json_dicts = []
        for pred in self.predicates:
            json_dicts.append(pred.to_json_dict())
        return json_dicts

    def add_aux_var(self, aux):
        """
        Some variables need to use auxiliary variables, for instance those
        found in the outputcolumns of C# tables.
        This method allows the creation of those variables.
        No aux var are created when makin an IDP file for the autoconfig
        interfaces.

         :arg List<str> a list containing strings of the variables.
         """
        for var in aux:
            # Split of the predicate name.
            p_name = var.split('(')[0]
            p_name = p_name.replace('_', ' ')
            for p in self.predicates:
                if p_name == p.name:
                    new_name = "_{}".format(p.name)
                    new_p = Predicate(new_name, p.args, p.super_type,
                                      partial=p.partial)
                    self.predicates.append(new_p)


class Type:
    """
    TODO
    """
    def __init__(self, name: str, super_type, posvals="-"):
        """
        :arg str: the name of the type.
        :arg Type: the super type of the type.
        :arg str: posvals, the possible values of the type.
        """
        self.name = name
        if name != "Int" and name != "Float" and name != "Real" \
                and name != "String":
            self.display_name = self.name + "_t"
        else:
            self.display_name = self.name
        self.super_type = super_type
        self.possible_values = posvals

        self.struct_args = []
        self.knows_values = True
        self.source_datatable = ""

        # Check the input.
        if posvals is None:
            raise ValueError("Values column for type {} is empty."
                             " Did you forget a '-'?"
                             .format(self.name))

        # Toggle knows_values if the values are known.
        if posvals == "_" or posvals == "-" or posvals == "−":
            self.knows_values = False
            self.possible_values = ""

        if re.search("(?i)see_Data_Table|see_DataTable", posvals):
            self.knows_values = False
            self.possible_values = ""
            m = re.search(r"(?i)(?<=see_Data_Table_)(.*?)(?=\Z)"
                          r"|(?<=see_DataTable_)(.*?)(?=\Z)",
                          posvals)
            self.source_datatable = m[0]

    def __str__(self):
        """
        Magic method to turn the type into a string.

        :returns str: the typename.
        """
        return "Type: {}".format(self.name)

    def to_theory(self):
        """
        TODO
        """
        return self.display_name

    def match(self, value):
        if self.basetype == self:  # When comparing with string, int, float,...
            return re.match('^{}$'.format(self.name), value, re.IGNORECASE)
        else:
            return re.match('^{}$'.format(self.name), value)

    @property
    def basetype(self):
        """
        The basetype represents one of the ancestor types, such as int or str.

        :returns type: the basetype.
        """
        try:
            return self.super_type.basetype
        except AttributeError:
            return self

    def check_values(self, values, tablename):
        """
        Method to check if the values listed in a datatable match with the
        values listed in the possible values column(if a datatable was used).

        If the possible values column is left empty, then it assumes all the
        values are correct and it fills the possible values automatically.
        This is needed so that the type can input these values into constructed
        from.

        If the possible values column contains values, then every value used in
        a datatable needs to match a value in the possible values.

        :returns boolean: True if all the values match.
        :throws ValueError: if a value appears in the datatable but not in
            posvals.
        """

        # We only check the data if the tablename (see datatable ...) is
        # explicitly given or a wildcard (-) was used in the glossary.
        if self.source_datatable not in tablename:
            return

        if self.basetype.name == "String":
            # If no possible values were listed, read the datatable values and
            # add them to the possible values.
            if not self.knows_values:
                if self.possible_values is None:
                    self.possible_values = ""

                # Check for each value if it exists already, add it if not.
                for value in values:
                    subvalues = str(value).split(',')
                    for subvalue in subvalues:
                        subvalue = subvalue.strip()
                        subvalue = idp_name(subvalue)
                        regex = r"(?<!\w){}(?!\w)".format(idp_name(subvalue))
                        if not re.search(regex, self.possible_values):
                            if not self.possible_values == "":
                                self.possible_values += ","
                            self.possible_values += " {}".format(subvalue)
                return

            # If possible values were listed in the glossary, we check for
            # typos in the data table.
            for value in values:
                subvalues = str(value).split(',')
                for subvalue in subvalues:
                    subvalue = subvalue.strip()
                    subvalue = idp_name(subvalue)
                    regex = r"(?<!\w){}(?!\w)".format(subvalue)
                    if not re.search(regex, self.possible_values):
                        raise ValueError("Error: value {} in datatable but not"
                                         " in possible values."
                                         .format(subvalue))

        elif self.basetype.name == "Int":
            # For integers we only check if they're in the right range.
            # We don't add them if the possible values is empty, because there
            # is no clear way of defining a range.
            if not self.knows_values:
                raise ValueError("The values column for integer type {} was"
                                 " left empty".format(self.name))

            # A range should be declared in the possible values. We need to
            # check if our value is within that range.
            leftbound, rightbound = None, None
            possible_values = None
            if ".." in self.possible_values:
                # E.g. "[0..30]"
                leftbound, rightbound = self.possible_values.split("..")
            elif '[' in self.possible_values and \
                    self.possible_values.count(",") == 1:
                # E.g. "[0, 30]"
                leftbound, rightbound = self.possible_values.split(",")
            else:
                # E.g. "0, 1, 2, 3, 4"
                possible_values = [int(x) for x in
                                   self.possible_values.split(",")]

            for value in values:
                subvalues = str(value).split(',')
                for subvalue in subvalues:
                    subvalue = int(subvalue.strip())
                    # If we know boundaries, the value should be within them.
                    if rightbound and (int(rightbound) < subvalue or
                                       subvalue < int(leftbound)):
                        raise ValueError("Error: value \"{}\" for type {} in"
                                         " datatable but not in"
                                         " range of possible values"
                                         .format(subvalue, self.name))
                    # If we know a list of values, the value should be in it.
                    if possible_values and subvalue not in possible_values:
                        raise ValueError("Error: value \"{}\" for type {} in"
                                         " datatable but not in"
                                         " list of possible values"
                                         .format(subvalue, self.name))

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Converts all the information of the Type into a string for the IDP
        vocabulary.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the vocabulary form of the type.
        """
        # Check for 'string', 'int', and other default types which don't need
        # to explicitly be declared.
        if self.name == self.basetype.name:
            return ''

        typename = idp_name(self.display_name)
        # If it's a string, use constructed from.
        if self.basetype.name == 'String':
            constr_from = 'constructed from'
        # Else, we use "=" and semicolons instead of commas.
        else:
            constr_from = '='
            self.possible_values = self.possible_values.replace(',', ';')
        if self.possible_values is None:
            return 'type {}\n'.format(typename)

        if self.basetype.name == 'String' or target_lang != 'idp':
            isa = ''
        else:
            isa = 'isa {}'.format(self.basetype.name.lower())

        if self.basetype.name == 'Int' and target_lang == 'idp':
            vals = self.possible_values.replace(',', ';')
        else:
            vals = self.possible_values

        voc = ('\ttype {} {} {{ {} }} {}\n'.format(
               typename,
               constr_from,
               vals,
               isa
               ))

        return voc

    def to_idp_struct(self, target_lang: str = 'idp'):
        """
        Converts all the information of the Type into a string for the IDP
        structure.
        Normal types don't need a structure, as their possible values are
        listed as "constructed from" in the voc.
        This is here for future's sake.

        :returns str: the string for the structure.
        """
        return ""


class DateType(Type):
    """
    TODO
    """
    def __init__(self, name: str, super_type, posvals=None):
        """
        Datestring needs a seperate formatting, because we need to expand the
        dates between start and end date.

        Form the structure arguments first. Date doesn't use "constructed
        from", but instead uses the structure for it's values.
        These are special, because we need to expand them.
        """
        super().__init__(name, super_type, posvals)

        possible_values = self.possible_values.replace("[", "")
        possible_values = possible_values.replace("]", "")
        possible_values = possible_values.replace("“", "")
        possible_values = possible_values.replace("”", "")
        possible_values = possible_values.replace("\"", "")

        if ".." in possible_values:
            dates = possible_values.split("..")
            dates = self.expand_dates(dates[0], dates[1])
            self.struct_args = dates
        elif "," in possible_values:
            dates = possible_values.split(",")
            self.struct_args = dates
        else:
            raise ValueError("Illegal date!")

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Converts the DateType to a string for the IDP vocabulary.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the string for the vocabulary.
        """
        # Form the voc.
        voc = ('\ttype {} isa string\n'.format(self.name))
        return voc

    def to_idp_struct(self):
        """
        Converts the DateType to a string for the IDP structure.
        This structure contains every possible data.

        :returns str: the string for the vocabulary.
        """

        # Format the struct.
        struct = "\t {} = {{".format(self.name)
        for date in self.struct_args:
            struct += "{}; ".format(date)
        struct += "}\n"
        return struct

    def expand_dates(self, startdate, enddate):
        """
        Generates all the possible dates between a start and end date.
        Uses datetime to check whether days exists (e.g. feb 29).

        :arg str: startdate, the first date.
        :arg str: enddate, the last date.
        :returns List<str>: a list of all the dates, in string form.
        :raises ValueError: if an incorrect date is used, or the startdate is
                            later than the enddate.
        """
        import datetime
        syear, smonth, sday = startdate.split("/")
        eyear, emonth, eday = enddate.split("/")

        try:
            d1 = datetime.datetime(int(syear), int(smonth), int(sday))
            d2 = datetime.datetime(int(eyear), int(emonth), int(eday))
        except ValueError:
            raise ValueError("Incorrect dates used!")
        if d1.date() > d2.date():
            raise ValueError("Startdate later than enddate!")
        dates = ["\"{}/{}/{}\"".format(syear, smonth, sday)]
        while d1.date() != d2.date():
            d1 += datetime.timedelta(days=1)
            date = d1.date()
            dates.append("\"{}/{:02d}/{:02d}\""
                         .format(int(date.year),
                                 int(date.month),
                                 int(date.day)))

        dates.append("\"{}/{}/{}\"".format(eyear, emonth, eday))
        return dates


class DateInt(Type):
    """
    DateInt is a type which represents any type of Date operation.
    These types are: DaysBetween, WeeksBetween and YearsBetween.
    For each two dates, it will calculate their xBetween and format it as a
    relation called "xBetween".
    """
    def __init__(self, name: str, super_type, posvals=None, dates="",
                 datename="Date"):
        """
        TODO
        """
        super().__init__(name, super_type, posvals)
        self.datename = datename
        self.dates = dates
        self.int_name = "{}Int".format(self.name)

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Formats the DateInt as a string for the IDP vocabulary.
        It consists of two parts.

            * An int which represents the amount of x between.
            * A relation, which lists the amount of x between two dates.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the vocabulary string.
        """
        voc = "\ttype {} isa int\n".format(self.int_name)
        voc += "\t{0}({1}, {2}, {2})\n".format(self.name,
                                               self.int_name,
                                               self.datename)
        return voc

    def to_idp_struct(self):
        """
        Formats the DateInt as a string for the IDP structure.

        DateInt introduces an "xBetween" relation, which lists the amount of
        x between every two dates.
        Comparable to a distance vector between dates.

        :returns str: the vocabulary theory.
        """
        lbound, rbound = self.possible_values.split("..")
        self.struct_args = [lbound, rbound]
        xbetween = self._create_distance_vector_dates(self.dates,
                                                      lbound, rbound)

        struct = "\t{} = {{ {}..{} }}\n".format(self.int_name,
                                                self.struct_args[0],
                                                self.struct_args[1])
        struct += "\t{} = {{".format(self.name)
        for i, pair in enumerate(xbetween):
            struct += "{},\"{}\",\"{}\";".format(pair[2], pair[0], pair[1])
            if i % 7 == 0:
                struct += "\n"
        struct += "}\n"
        return struct

    def to_theory(self):
        """
        Formats the DateInt as a string for the IDP theory.

        :returns str: the theory form of the xBetween.
        """
        return self.int_name

    def _create_distance_vector_dates(self, dates, lbound, rbound):
        """
        Method to calculate for each pair of dates the amount of x in
        between them.
        This x can be: days, or weeks.

        :arg List<str>: the list of all the dates.
        :arg int: lbound, the amount of x we want to look in the past.
        :arg int: rbound, the amount of x we want to look in the future.

        :returns List<List<str, str, int>>: the distance vector.
        """
        import datetime
        # Find out which x function is needed:
        if "Days" in self.name:
            xfunction = self._days_between
        elif "Weeks" in self.name:
            xfunction = self._weeks_between
        elif "Years" in self.name:
            xfunction = self._years_between
        else:
            raise ValueError("Date operator not yet implemented: {}"
                             .format(self.name))
        daysbetween = []
        lbound = int(lbound)
        rbound = int(rbound)
        for date1 in dates:
            # Create first datetime object.
            date1 = date1.replace("\"", "")
            syear, smonth, sday = date1.split("/")
            d1 = datetime.datetime(int(syear), int(smonth), int(sday))

            for date2 in dates:
                # Create second datetime object.
                date2 = date2.replace("\"", "")
                eyear, emonth, eday = date2.split("/")
                d2 = datetime.datetime(int(eyear), int(emonth), int(eday))
                x_amount = xfunction(d1, d2)
                # Don't save the difference if it's outside the bounds.
                if rbound < x_amount or x_amount < lbound:
                    continue
                delta = [date1, date2, abs(x_amount)]
                daysbetween.append(delta)
        return daysbetween

    def _days_between(self, datetime1, datetime2):
        """
        Finds the amount of days between two datetimes.

        :arg datetime:
        :arg datetime:
        :returns int: the days between the two datetimes.
        """
        return abs((datetime1-datetime2).days)

    def _weeks_between(self, datetime1, datetime2):
        """
        Finds the amount of weeks between two datetimes.

        :arg datetime:
        :arg datetime:
        :returns int: the weeks between the two datetimes.
        """
        import datetime
        # https://stackoverflow.com/questions/14191832/how-to-calculate-difference-between-two-dates-in-weeks-in-python
        monday1 = (datetime1 - datetime.timedelta(days=datetime1.weekday()))
        monday2 = (datetime2 - datetime.timedelta(days=datetime2.weekday()))

        return (monday2 - monday1).days // 7

    def _years_between(self, datetime1, datetime2):
        """
        Finds the amount of years between two datetimes.

        :arg datetime:
        :arg datetime:
        :returns int: the years between the two datetimes.
        """
        from dateutil.relativedelta import relativedelta
        return relativedelta(datetime1, datetime2).years


class Predicate:
    """
    Class which represents both predicates and functions.
    This double meaning is a relic of the past, and is to be fixed.
    In the future, a separate Function class should be created.
    """
    def __init__(self, name: str, args: List[Type], super_type: Type,
                 partial=False, full_name=None, zero_arity=False):
        """
        Initialises a predicate.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).
        """
        self.name = name
        self.args = args
        self.super_type = super_type
        self.partial = partial
        self.repr = self.interpret_name()
        self.full_name = full_name
        self.struct_args = {}
        self.zero_arity = zero_arity

        if not self.args and self.is_function and not zero_arity:
            print('WARNING: "{}" has been interpreted as single value'
                  ' instead of a function. Functions should be defined'
                  ' as FunctionName of Type and Type ...'
                  .format(self.name))
        elif not self.args and self.is_relation and not zero_arity:
            print('WARNING: "{}" has been interpreted as a boolean value'
                  ' instead of a relation. Relations should be defined'
                  ' as Type and Type ... is RelationName'
                  .format(self.name))

    def __str__(self):
        """
        TODO
        """
        retstr = "Predicate: {}".format(self.name)
        return retstr

    @staticmethod
    def from_string(full_name: str, predicate: bool, super_type: Type,
                    glossary: Glossary, partial=False,
                    zero_arity=False):
        """
        Static method to create a predicate from string.

        :arg str: full_name, the full name.
        :arg bool: predicate, true if predicate, false if function.
        :arg Type: super_type, the super type of the predicate.
        :arg Glossary: glossary, the glossary.
        :arg bool: partial, whether or not it's a partial function.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).
        :returns Predicate:
        """
        if not predicate:  # Check if it's a function.
            regex = (r'^(?P<name>.*)$')
            # regex = (r"^(?P<name>.*) of (?P<args>(?:{0})(?: and (?:{0}))*)$"
            #          .format('|'.join([x.name for x in glossary.types])))
        else:
            regex = (r'^(?P<name>.*)$')
        #    regex = ('^(?P<args>(?:{0})(?: and (?:{0}))*) is (?P<name>.*)$'
        #             .format('|'.join([x.name for x in glossary.types])))
        try:
            name = re.match(regex, full_name).group('name')
        except AttributeError:
            name = full_name
        try:
            # args = re.match(regex, full_name).group('args').split(' and ')
            raise IndexError
        except (AttributeError, IndexError):
            if zero_arity:
                return Predicate(full_name, [], super_type, partial,
                                 zero_arity=zero_arity)
            else:  # We need to find the relation's types.
                # We simply loop over all words and look for full matches.
                # TODO This should be done better. Types could be multiple
                # words.
                args = []
                name_elements = full_name.split(" ")

                for element in name_elements:
                    for t in glossary.types:
                        if re.fullmatch(element, t.name):
                            args.append(t)
                            break
                return Predicate(name, args,
                                 super_type, partial,
                                 full_name, zero_arity)

        return Predicate(name, [glossary.find_type(t) for t in args],
                         super_type, partial, full_name, zero_arity)

    def is_function(self):
        """
        Method to check whether the predicate is a function.
        Since only functions have super types, we use that as a check.
        Note that constants are a special case of functions.

        :returns boolean:
        """
        if self.super_type is None:
            return False
        else:
            return True

    def is_relation(self):
        """
        Method to check whether the predicate is a relation.
        A predicate is either a relation or a function, so we use that as a
        check. Note that booleans are a special case of relations.

        :returns boolean:
        """
        return not self.is_function()

    def interpret_name(self):
        """
        Method to interpret the name.
        This method forms a generic name representation, by replacing the
        arguments by dummies.
        In this way, it creates a skeleton structure for the name.

        Thus, it returns the name, without the arguments.
        For instance, `Country borders Country` becomes
        `(?P<arg0>.+) borders (?P<arg1>.+)`.
        This way, arg0 and arg1 can be found easily later on.
        """
        if not self.args:
            return self.name
        elif self.args:
            name_elements = self.name.split(" ")
            new_alias = ""
            arg_index = 0
            arglist = [arg.name for arg in self.args]
            for element in name_elements:
                if element in arglist:
                    new_alias += "(?P<arg{}>.+) ".format(arg_index)
                    arg_index += 1
                    continue
                else:
                    new_alias += "{} ".format(element)
            return new_alias[:-1]  # We drop the last space.
        else:
            raise ValueError("No idea what went wrong.")

    def lookup(self, string: str):
        """
        Method to compare a string to this predicate, to see if the predicate
        appears in the string in any form.
        TODO: make this more clear.
        """
        d = re.match(self.repr, string)
        if d:
            d = d.groupdict()
            return self, [v for k, v in sorted(d.items(),
                                               key=(lambda x: int(x[0][3:])))]

    def to_idp_voc(self, target_lang: str):
        """
        Convert the predicate/function to a string for the IDP vocabulary.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the predicate/function in vocabulary format.
        """
        voc = '\tpartial ' if self.partial else '\t'
        voc += '{}'.format(idp_name(self.name))
        if self.args:
            voc += '({})'.format(', '.join(map(lambda t:
                                               idp_name(t.display_name),
                                               self.args)))
        if self.is_function():
            voc += ': {}'.format(idp_name(self.super_type.display_name))
        return voc + "\n"

    def to_idp_struct(self, target_lang: str = 'idp'):
        """
        If a function or predicate receives a value in a datatable, we need to
        set it's values in the structure.
        When parsing the datatable in "read_datatables", we set the
        "struct_args" of the predicates/functions that get a value.
        struct_args could look like: {key1|key2:value}. However, it's possible
        to input multiple keys per cell to save space.

        For instance:
        "Jim|Skydiving, Soccer" needs to be formatted as
        "Jim, Skydiving; Jim, Soccer".
        The same goes for functions.

        To achieve this, we split the keys on their seperator, and then we
        split each key on a comma. This way, we have an array of keys in which
        each item is an array of subkeys. We need to form every possible
        combination of these keys, and to do this we use itertools.product.

        :arg target_lang: the target language format. Either `idp` or `idpz3`.
        :returns: str
        """
        lang_dict = {'idp':  {'funcsign': ' -> '},
                     'idpz3': {'funcsign': ', '}}

        import itertools
        if len(self.struct_args) == 0:
            return None
        struct = '\t{} = {{'.format(idp_name(self.name))
        # If the pred is a function, the format is "arg,.. -> arg".
        if self.is_function():
            default_val = None
            for key, arg in self.struct_args.items():
                default_val = arg  # TODO: actual default arg!
                keys = key.split('|')
                keys = [x.split(',') for x in keys]
                keys_product = itertools.product(*keys)
                for combination in list(keys_product):
                    idp_combination = [idp_name(x.strip())
                                       for x in combination]
                    struct += ("{}{}{}; "
                               .format(','.join(idp_combination),
                                       lang_dict[target_lang]['funcsign'],
                                       idp_name(arg)))
            struct += '}'
            if target_lang == 'idpz3':
                struct += " else {} \n".format(default_val)
            else:
                struct += "\n"

        else:
            for key, arg in self.struct_args.items():
                # Check if the relation is a boolean (booleans have no keys).
                if key == "":
                    if re.match("(?i)yes", arg):
                        struct = "\t{} = true\n".format(idp_name(self.name))
                        return struct
                    if re.match("(?i)no", arg):
                        struct = "\t{} = false\n".format(idp_name(self.name))
                        return struct
                # Only add a relation if the value of the argument is yes.
                if not re.match("(?i)yes", arg):
                    continue
                # The key can consist of multiple values.
                keys = key.split('|')
                keys = [x.split(',') for x in keys]
                keys_product = itertools.product(*keys)
                for combination in list(keys_product):
                    idp_combination = [idp_name(x.strip())
                                       for x in combination]
                    struct += ",".join(idp_combination) + ";"
            struct += '}\n'

        return struct

    def to_json_dict(self):
        json_dict = {}
        json_dict['idpname'] = idp_name(self.name)
        # json_dict['expandArgs'] = 1
        if self.is_function():
            json_dict['type'] = "function"
            if self.zero_arity:
                basetype = self.super_type.basetype.name
                if basetype == "Int" or basetype == "Float":
                    json_dict['showOptimize'] = "true"
        else:
            if self.zero_arity:
                json_dict['type'] = "proposition"
            else:
                json_dict['type'] = "predicate"
        return json_dict
