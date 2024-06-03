from services.filter.core import MetaFilterBase, MultiFilterBase
from services.filter.implementations import AnyFilter, NameFilter, PropertyFilter, SerialFilter, TypeFilter
class FilterUtils:
    @classmethod
    def ResolveFilters(cls, filters, and_operator = None):
        for i, filter in enumerate(filters):
            if isinstance(filter, MultiFilterBase): cls.ResolveFilters(filter.filters, and_operator)
            elif isinstance(filter, MetaFilterBase):
                temp = [filter.filter]
                cls.ResolveFilters(temp, and_operator)
                filter.filter = temp[0]
            else: filters[i] = cls.ConvertShorthand(filter, and_operator)

    @classmethod
    def ConvertShorthand(cls, value, and_operator):
        if not isinstance(value, str) and not isinstance(value, int): return value # Assume it's a filter
        if and_operator == None or isinstance(value, int): return cls.__CreateImplicitFilter(value)

        return cls.__ConvertOperators(value, and_operator)    

    @classmethod
    def __ConvertOperators(cls, value, and_operator):
        start_index = -1
        and_list = []
        for i, c in enumerate(value):
            if c != and_operator: continue
        
            # Double operator, restart
            if i == start_index + 1:
                start_index = i
                continue
            
            # Extract value
            current_value = value[start_index + 1: i].strip()
            if current_value: and_list.append(current_value)

            start_index = i

        # Flush final index
        if start_index:
            last_value = value[start_index+1::].strip()
            if last_value: and_list.append(last_value)

        if not and_list: return None

        return AllFilter(map(cls.__CreateImplicitFilter, and_list))
    
    @classmethod
    def __CreateImplicitFilter(cls, value):
        if isinstance(value, int): return AnyFilter([SerialFilter(value), TypeFilter(value)])
        if isinstance(value, str): return AnyFilter([NameFilter(value), PropertyFilter(value)])
        return None