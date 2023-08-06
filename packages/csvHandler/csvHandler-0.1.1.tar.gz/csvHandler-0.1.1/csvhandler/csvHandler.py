import pandas as pd
from databaseConnection import SqliteConnection

TABLE_NAME = 'combined'
NEW_VALUE_COLUMN_SUFFIX = '_new'
RECORD_TYPE_STR = 'recordType'
ID_COLUMN_STR = 'Id'
CHANGED_STR = 'changed'
ADDED_STR = 'added'
DELETED_STR = 'deleted'


def combine(file_path, added_path='', deleted_path='', changed_original_path='', changed_new_path=''):
    if ((changed_original_path and not changed_new_path) or (not changed_original_path and changed_new_path)):
        raise ValueError(
            'changed_original_path and change_new_path both must have values')

    concatenation_arr = []
    if added_path:
        added = pd.read_csv(added_path)
        added[RECORD_TYPE_STR] = ADDED_STR
        concatenation_arr.append(added)

    if deleted_path:
        deleted = pd.read_csv(deleted_path)
        deleted[RECORD_TYPE_STR] = DELETED_STR
        concatenation_arr.append(deleted)

    if changed_original_path and changed_new_path:
        changed_original = pd.read_csv(changed_original_path)
        changed = pd.read_csv(changed_new_path)
        changed_merge = changed_original.merge(
            changed, on=ID_COLUMN_STR, suffixes=('', NEW_VALUE_COLUMN_SUFFIX))
        changed_merge[RECORD_TYPE_STR] = CHANGED_STR
        concatenation_arr.append(changed_merge)

    result = pd.concat(concatenation_arr, sort=False)
    result = result.sort_values([ID_COLUMN_STR])
    with SqliteConnection(file_path) as connection:
        connection.text_factory = str
        result.to_sql(name=TABLE_NAME, con=connection, index=False)
        cursor = connection.cursor()
        cursor.execute('create index id_idx on ' +
                       TABLE_NAME + '(' + ID_COLUMN_STR + ');')
        cursor.execute('create index record_type_idx on ' +
                       TABLE_NAME + '(' + RECORD_TYPE_STR + ');')
        connection.commit()


class CsvHandler():
    def __init__(self, file_path):
        self.file_path = file_path
        with SqliteConnection(self.file_path) as connection:
            columns = pd.read_sql('select * from ' + TABLE_NAME +
                                  ' limit 0', con=connection).columns.tolist()  # Get columns
            rows_number = self.__calculate_rows('', con=connection)

            self.metadata = {'rows': {'all': rows_number},
                             'filePath': self.file_path,
                             'columns': columns}

    def get_metadata(self):
        return self.metadata

    def get_page(self, page_number, page_size, orderby='', is_asc=True, filter_exp='', projection=[], exclude_columns=[]):
        if page_number <= 0:
            raise ValueError('page_number cannot be less or equal to zero')

        if page_size < 0:
            raise ValueError('page_size cannot be less than zero')

        with SqliteConnection(self.file_path) as connection:
            where_clause = self.__odata_filter_to_where(
                filter_exp) if filter_exp else ''
            self.metadata['rows']['filtered'] = None

            if where_clause:
                rows_number = self.__calculate_rows(
                    where_clause, con=connection)
                self.metadata['rows']['filtered'] = rows_number

            data_frame = self.__get_data(orderby, is_asc, where_clause, projection,
                                         exclude_columns, con=connection, page_number=page_number, page_size=page_size)
            return self.__page_format(data_frame)

    def export(self, export_path, orderby='', is_asc=True, filter_exp='', projection=[], exclude_columns=[]):
        with SqliteConnection(self.file_path) as connection:
            where_clause = self.__odata_filter_to_where(
                filter_exp) if filter_exp else ''

            data_frame = self.__get_data(orderby, is_asc, where_clause, projection,
                                         exclude_columns, con=connection)

            data_frame.to_csv(export_path, na_rep='NA', index=False)

    def __get_data(self, orderby, is_asc, where_clause, projection, exclude_columns, con, **kwargs):
        query = self.__select(projection, exclude_columns)
        query += where_clause

        query += self.__order_by(orderby if orderby else ID_COLUMN_STR, is_asc)

        page_size = kwargs.get('page_size', None)
        page_number = kwargs.get('page_number', None)

        if(page_number != None and page_size != None):
            query += self.__limit(page_number, page_size)

        return pd.read_sql(query, con=con)

    def __calculate_rows(self, where_clause, con):
        data_frame = pd.read_sql('select ' + RECORD_TYPE_STR + ',count(*) from ' +
                                 TABLE_NAME + where_clause + ' group by ' + RECORD_TYPE_STR, con=con)
        rows = {'total': 0, CHANGED_STR: 0, ADDED_STR: 0, DELETED_STR: 0}
        total = 0
        for record in data_frame.to_dict('records'):
            rows[record[RECORD_TYPE_STR]] = record['count(*)']
            total += int(record['count(*)'])
        rows['total'] = total
        return rows

    def __select(self, projection, exclude_columns):
        columns = projection if len(projection) > 0 else list(
            self.metadata['columns'])
        # Exclude columns
        for column_name in exclude_columns:
            if column_name != ID_COLUMN_STR and column_name != RECORD_TYPE_STR and column_name in columns:
                columns.remove(column_name)

        # Add Id column if does not exist
        if not (ID_COLUMN_STR in columns):
            columns.append(ID_COLUMN_STR)

        # Add recordType column if does not exist
        if not (RECORD_TYPE_STR in columns):
            columns.append(RECORD_TYPE_STR)

        # Make sure all columns of new values are included
        columns_to_add = []
        for column_name in columns:
            if (column_name.find(NEW_VALUE_COLUMN_SUFFIX, len(column_name)-len(NEW_VALUE_COLUMN_SUFFIX), len(column_name)) > -1 or
                    column_name == RECORD_TYPE_STR or
                    column_name == ID_COLUMN_STR):
                continue

            if not (column_name + NEW_VALUE_COLUMN_SUFFIX) in columns:
                columns_to_add.append(column_name + NEW_VALUE_COLUMN_SUFFIX)

        for column_name in columns_to_add:
            columns.append(column_name)

        columns_str = '*' if len(projection) == 0 and len(
            exclude_columns) == 0 else ','.join(columns)
        return 'SELECT ' + columns_str + ' from ' + TABLE_NAME

    def __limit(self, page_number, page_size):
        return ' LIMIT ' + str((page_number-1)*page_size) + ', ' + str(page_size)

    def __order_by(self, orderby, is_asc):
        return ' ORDER BY ' + orderby+(' ASC' if is_asc else ' DESC')

    def __page_format(self, data_frame):
        records = data_frame.to_dict('records')
        page = []
        for record_dict in records:
            record = {}
            record['id'] = record_dict[ID_COLUMN_STR]
            record[RECORD_TYPE_STR] = record_dict[RECORD_TYPE_STR]
            data = []
            for column_name, value in record_dict.iteritems():
                if (column_name.find(NEW_VALUE_COLUMN_SUFFIX, len(column_name)-len(NEW_VALUE_COLUMN_SUFFIX), len(column_name)) > -1 or
                    column_name == RECORD_TYPE_STR or
                        column_name == ID_COLUMN_STR):
                    continue

                item = {}
                item['columnName'] = column_name
                item['columnType'] = type(value).__name__
                item['value'] = None if pd.isna(value) else value
                if record[RECORD_TYPE_STR] == CHANGED_STR and value != record_dict[column_name + NEW_VALUE_COLUMN_SUFFIX]:
                    item['newValue'] = record_dict[column_name +
                                                   NEW_VALUE_COLUMN_SUFFIX]

                data.append(item)

            record['data'] = data
            page.append(record)
        return page

    def __odata_filter_to_where(self, query):
        comparison_operators_map = {' eq ': ' = ', ' ne ': ' != ',
                                    ' gt ': ' > ', ' lt ': ' < ', ' ge ': ' >= ', ' le ': ' <= '}
        logical_operators_map = {' not ': ' NOT ',
                                 ' and ': ' AND ', ' or ': ' OR '}
        # It's not a full solution, but it's a good enough solution.
        special_operators_map = {('contains(', 'contains ('): ' instr('}

        for (key, value) in comparison_operators_map.iteritems():
            query = query.replace(key, value)

        for (op_str_tuple, value) in special_operators_map.iteritems():
            for op_str in op_str_tuple:
                query = query.replace(op_str, value)

        for (key, value) in logical_operators_map.iteritems():
            query = query.replace(key, value)

        return ' WHERE ' + query
