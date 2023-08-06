class BaseOperator:
    selector = None

    def __init__(self, *args, **kwargs):
        self._query = args
        self._extra = kwargs

        if not all([self.is_query(op) for op in self._query]):
            raise TypeError('args should be instanceof BaseOperator')

        self._operate()

    def is_same_query(self):
        return all([isinstance(query, self.__class__) for query in self._query])

    def _operate(self):
        raise NotImplementedError('_operate() should be update')

    def to_represent(self):
        if not self._query and not self._extra.keys():
            return {}
        return self._expressions

    def __repr__(self):
        expr = f' {self.selector} '.join([repr(op) for op in self._query])
        if expr:
            expr += f' {self.selector} {self.extra_repr}'
        else:
            expr = self.extra_repr
        return f'({expr})'

    def __and__(self, query):
        return AND(query, self)

    def __or__(self, query):
        return OR(query, self)

    @property
    def extra_repr(self):
        raise NotImplementedError('extra_repr() not implemented')

    @classmethod
    def is_query(self, query):
        return isinstance(query, BaseOperator)


class EMPTY(BaseOperator):
    def __init__(self, *args, **kwargs):
        pass

    def to_represent(self):
        return {}


class Logical(BaseOperator):
    def _query_expressions(self):
        result = [op.to_represent() for op in self._query]
        return result


class AND(Logical):
    selector = '$and'

    def _operate(self):
        expressions = [*self._query_expressions()]
        if self._extra.keys():
            expressions.append(self._extra)
        self._expressions = {
            self.selector: expressions
        }

    @property
    def extra_repr(self):
        return ' $and '.join([f'{key}={value}' for key, value in self._extra.items()])


class OR(Logical):
    selector = '$or'

    def _operate(self):
        or_extra = [{k: v} for k, v in self._extra.items()]
        if not self._query:
            self._expressions = {self.selector: or_extra}
        else:
            self._expressions = {
                self.selector: [
                    *self._query_expressions(),
                    *or_extra
                ]
            }


class NOR(Logical):
    selector = '$nor'


class NOT(BaseOperator):
    selector = '$not'

    def _operate(self):
        expressions = {}
        for k, value in self._extra.items():
            if self.is_query(value):
                expr = value.to_represent()
            else:
                expr = value
            expressions[k] = {
                self.selector: {
                    '$eq': expr
                }
            }
