import collections
from typing import Tuple
from pyspark.sql.dataframe import DataFrame
from databricksbundle.notebook.logger.LoggerWrapper import LoggerWrapper

class DuplicateColumnsChecker:

    def __init__(
        self,
        loggerWrapper: LoggerWrapper,
    ):
        self.__loggerWrapper = loggerWrapper

    def check(self, df: DataFrame, fun: callable, sources: Tuple[callable]):
        fieldNames = [field.name.lower() for field in df.schema.fields]
        duplicateFields = dict()

        for fieldName, count in collections.Counter(fieldNames).items():
            if count > 1:
                duplicateFields[fieldName] = []

        if duplicateFields == dict():
            return

        g = fun.__globals__

        fields2Tables = dict()

        for source in sources:
            sourceDf = g[source.__name__ + '_df']
            for field in sourceDf.schema.fields:
                fieldName = field.name.lower()

                if fieldName not in fields2Tables:
                    fields2Tables[fieldName] = []

                fields2Tables[fieldName].append(source.__name__)

        for duplicateField in duplicateFields:
            self.__loggerWrapper.getLogger().error(f'Duplicate field {duplicateField}', extra={'source dataframes': fields2Tables[duplicateField]})

        fieldsString = ', '.join(duplicateFields)
        raise Exception(f'Duplicate output column(s): {fieldsString}. Disable by setting @transformation(checkDuplicateColumns=False)')
