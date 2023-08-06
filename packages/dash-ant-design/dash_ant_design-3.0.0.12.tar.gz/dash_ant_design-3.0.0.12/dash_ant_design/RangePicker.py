# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RangePicker(Component):
    """A RangePicker component.


Keyword arguments:
- id (string; optional): todo
- allowClear (boolean; optional): todo
- showTime (boolean; optional)
- value (dict; optional): todo
- output (list of strings; optional)
- defaultValue (string; optional)
- style (dict; optional): Dash-assigned callback that should be called whenever any of the
properties change
- className (string; optional)
- changed (list of strings; optional)
- placeholder (list of strings; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, allowClear=Component.UNDEFINED, showTime=Component.UNDEFINED, value=Component.UNDEFINED, output=Component.UNDEFINED, defaultValue=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, changed=Component.UNDEFINED, placeholder=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowClear', 'showTime', 'value', 'output', 'defaultValue', 'style', 'className', 'changed', 'placeholder']
        self._type = 'RangePicker'
        self._namespace = 'dash_ant_design'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowClear', 'showTime', 'value', 'output', 'defaultValue', 'style', 'className', 'changed', 'placeholder']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(RangePicker, self).__init__(**args)
