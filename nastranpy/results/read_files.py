from io import StringIO
import pandas as pd
from nastranpy.results.tables_specs import tables_specs


class ResultsTable(object):

    def __init__(self, dataframe=None, name=None, element_type=None, header=None, title=None, subtitle=None, label=None, subcase=None, element_id=None):
        self.df = dataframe
        self.name = name
        self.element_type = element_type
        self.header = header
        self.title = title
        self.subtitle = subtitle
        self.label = label
        self.subcase = subcase
        self.element_id = element_id


def tables_in_pch(file, tables_specs=None):

    with open(file) as f:
        is_header = False
        header_row = 0
        table = None

        for line in f:

            if line[0] == '$':

                if not is_header:

                    if line[:6] != '$TITLE':
                        continue

                    is_header = True
                    header_row = 0

                    if table:
                        data.seek(0)

                        if is_format:
                            table.df = pd.read_fwf(data, names=names, widths=widths,
                                                   usecols=usecols, dtype=dtype,
                                                   index_col=index_col)[sorted_cols]
                        else:
                            table.df = pd.read_fwf(data, header=0)

                        yield table

                    table = ResultsTable(header='', title=line[10:72].strip())
                    data = StringIO()
                    table_type = None
                    item_id = ''
                    line_separator = ''

                header_row += 1
                table.header += line

                if line[:9] == '$SUBTITLE':
                    table.subtitle = line[10:72].strip()
                elif line[:6] == '$LABEL':
                    table.label = line[10:72].strip()
                elif header_row == 4:
                    table.name = line[1:72].strip()
                elif line[:11] == '$SUBCASE ID':
                    subcase = line[13:13 + 18]
                    table.subcase = int(subcase.strip())
                elif line[:13] == '$ELEMENT TYPE':
                    table.element_type = line[27:50].strip()
                    table_type = '{} - {}'.format(table.name, table.element_type)

                if tables_specs and table_type and table_type in tables_specs:
                    is_format = True
                    names = [name if name else f'foo{i}' for i, name in
                             enumerate(name for row in tables_specs[table_type]['pch_format'] for name, _ in row)]
                    widths = [18 for row in tables_specs[table_type]['pch_format'] for _, _ in row]
                    usecols = tables_specs[table_type]['columns']
                    sorted_cols = [name for name in usecols if name not in tables_specs[table_type]['index']]
                    dtype = tables_specs[table_type]['dtypes']
                    index_col = [i for index in tables_specs[table_type]['index'] for row in
                                 tables_specs[table_type]['pch_format'] for i, (name, _) in enumerate(row) if name == index]
                else:
                    is_format = False


            else:
                is_header = False

                if line[0] == ' ':

                    if item_id == line[:18]:
                        data.write(line[18:72])
                    else:
                        data.write(line_separator + subcase + line[:72])

                    item_id = line[:18]
                    line_separator = '\n'
                elif line[:6] == '-CONT-':
                    data.write(line[18:72])

        if table:
            data.seek(0)

            if is_format:
                table.df = pd.read_fwf(data, names=names, widths=widths,
                                       usecols=usecols, dtype=dtype,
                                       index_col=index_col)[sorted_cols]
            else:
                table.df = pd.read_fwf(data, header=0)

            yield table