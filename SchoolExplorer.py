#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from keys import googleKey

import gmaps
import numpy as np
import pandas as pd
import requests
import time
from us import states
from IPython.display import display
import ipywidgets as widgets


# In[2]:


## https://jupyter-gmaps.readthedocs.io/en/latest/app_tutorial.html
gmaps.configure(api_key=googleKey.gkey)
class SchoolExplorer(object
):
    """
    Jupyter widget for exploring the AustinSchools dataset

    Choose the type of School using checkboxes. 
    Options allow user to choose one or more.
    """

    def __init__(self, df):
        self._df = df
        self._symbol_layer = None
    
        self._public_symbols = self._create_symbols_for_schools(
          'public', 'rgba(0, 0, 150, 0.4)')
        self._private_symbols = self._create_symbols_for_schools(
          'private', 'rgba(0, 150, 0, 0.4)')
        self._charter_symbols = self._create_symbols_for_schools(
          'charter', 'rgba(150, 0, 0, 0.4)')
        
        title_widget = widgets.HTML(
            '<h3>Student Enrollment in Austin, by type</h3>'
            '<h4>Data from <a href="https://www.greatschools.org/">Great Schools API</a></h4>'
        )
        controls = self._render_controls(True, True, True)
        map_figure = self._render_map(True, True, True)
        self._container = widgets.VBox(
          [title_widget, controls, map_figure])

    def render(self):
        """ Render the widget """
        display(self._container)

    def _render_map(self, initial_include_private, initial_include_public, initial_include_charter):
        """ Render the initial map """
        fig = gmaps.figure(layout={'width': '1000px','height': '1000px','border': '1px solid black','padding': '1px'})
        symbols = self._generate_symbols(True, True, True)
        self._symbol_layer = gmaps.Markers(markers=symbols)
        fig.add_layer(self._symbol_layer)
        return fig

    def _render_controls(
        self,
        initial_include_private,
        initial_include_public,
        initial_include_charter
    ):
        """ Render the checkboxes """
        self._private_checkbox = widgets.Checkbox(
              value=initial_include_private,
              description='Private Schools'
        )
        self._public_checkbox = widgets.Checkbox(
              value=initial_include_public,
              description='Public Schools'
        )
        self._charter_checkbox = widgets.Checkbox(
              value=initial_include_charter,
              description='Charter Schools'
        )
        self._private_checkbox.observe(
          self._on_controls_change, names='value')
        self._public_checkbox.observe(
          self._on_controls_change, names='value')
        self._charter_checkbox.observe(
          self._on_controls_change, names='value')
        controls = widgets.VBox(
          [self._private_checkbox, self._public_checkbox,self._charter_checkbox])
        return controls

    def _on_controls_change(self, obj):
        """
        Called when the checkboxes change

        This method builds the list of symbols to include on the map,
        based on the current checkbox values. It then updates the
        symbol layer with the new symbol list.
        """
        include_private = self._private_checkbox.value
        include_public = self._public_checkbox.value
        include_charter = self._charter_checkbox.value
        symbols = self._generate_symbols(include_private, include_public, include_charter)
        # Update the layer with the new symbols:
        self._symbol_layer.markers = symbols

    def _generate_symbols(self, include_private, include_public, include_charter):
        """ Generate the list of symbols to includs """
        symbols = []
        if include_private:
            symbols.extend(self._private_symbols)
        if include_public:
            symbols.extend(self._public_symbols)
        if include_charter:
            symbols.extend(self._charter_symbols)
        return symbols

    def _create_symbols_for_schools(self, schoolType, color):
        schoolType_df = self._df[self._df['schoolType'] == schoolType]
        symbols = []
        for latitude, longitude, enroll, name in zip(schoolType_df["latitude"], 
                                               schoolType_df["longitude"],
                                               schoolType_df["Percent enrollment"],
                                               schoolType_df['schoolName']):
            symbol = gmaps.Symbol(
              location=(latitude, longitude),
              stroke_color=color,
              fill_color=color,
              scale=(int(enroll)+1)*4,
              info_box_content=name
            )
            symbols.append(symbol)
        
        return symbols
        
        

