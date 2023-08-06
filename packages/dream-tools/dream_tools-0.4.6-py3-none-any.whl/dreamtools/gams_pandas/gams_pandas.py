"""
"""
import os

import numpy as np
import pandas as pd
import gams
import logging
import builtins
import time
from copy import deepcopy
from .utility import index_from_symbol, symbol_is_scalar, series_from_variable, \
  series_from_parameter, is_iterable, map_lowest_level, set_symbol_records

logger = logging.getLogger(__name__)


class GamsPandasDatabase:
  """
  GamsPandasDatabase converts sets, parameters, and variables between a GAMS database and Pandas series.
  When as symbol is first retrieved it is converted to a Pandas series and stored in self.series
  Changes to retrieved series are written to the GAMS database on export.
  """

  def __init__(self, database=None, workspace=None, auto_sort_index=True):
    if database is None:
      if workspace is None:
        workspace = gams.GamsWorkspace()
      database = workspace.add_database()
    self.database = database
    self.auto_sort_index = auto_sort_index
    self.series = {}

  def __getattr__(self, item):
    return self[item]

  def copy(self):
    obj = type(self).__new__(self.__class__)
    obj.__dict__.update(self.__dict__)
    obj.database = self.database.workspace.add_database(source_database=self.database)
    obj.series = deepcopy(self.series)
    return obj

  def merge(self, other, symbol_names=None, inplace=False):
    """
    Merge two GamsPandasDatabases.
    symbol_names: list of symbol names to get from other. If None, all symbols in other are merged.
    """
    if inplace:
      db = self
    else:
      db = self.copy()

    if symbol_names is None:
      symbol_names = other.symbols

    for name in other.sets:
      if name in symbol_names:
        series = other[name].texts
        db.create_set(series.name, series.index, other[name].explanatory_text, series)

    for name in other.variables:
      if name in symbol_names:
        db.add_variable_from_series(other[name], other[name].explanatory_text)

    for name in other.parameters:
      if name in symbol_names:
        db.add_parameter_from_series(other[name], other[name].explanatory_text)

    return db

  @property
  def symbols(self):
    """Dictionary of all symbols in the underlying GAMS database"""
    return {symbol.name: symbol for symbol in self.database}

  @property
  def sets(self):
    """Dictionary of all sets in the underlying GAMS database"""
    return {symbol.name: symbol for symbol in self.database if isinstance(symbol, gams.GamsSet)}

  @property
  def variables(self):
    """Dictionary of all variables in the underlying GAMS database"""
    return {symbol.name: symbol for symbol in self.database if isinstance(symbol, gams.GamsVariable)}

  @property
  def parameters(self):
    """Dictionary of all parameters in the underlying GAMS database"""
    return {symbol.name: symbol for symbol in self.database if isinstance(symbol, gams.GamsParameter)}

  @property
  def equations(self):
    """Dictionary of all equations in the underlying GAMS database"""
    return {symbol.name: symbol for symbol in self.database if isinstance(symbol, gams.GamsEquation)}

  def add_to_builtins(self, *args):
    """Retrieve any number symbol names from the database and add their Pandas representations to the global namespace."""
    for identifier in args:
      setattr(builtins, identifier, self[identifier])

  def get(self, *args):
    """Retrieve any nymber of symbol names and return a list of their Pandas representations."""
    return [self[i] for i in args]

  def add_parameter_from_dataframe(self, identifier, df, explanatory_text="", add_missing_domains=False,
                                   value_column_index=-1):
    """Add parameter symbol to database based on a Pandas DataFrame."""
    domains = list(df.columns[:value_column_index:])
    for d in domains:
      if d not in self:
        if add_missing_domains:
          self.create_set(name=d, index=df[d].unique(), explanatory_text="")
        else:
          raise KeyError(
            f"'{d}' is not a set in the database. Enable add_missing_domains or add the set to the database manually.")
    self.database.add_parameter_dc(identifier, domains, explanatory_text)
    if domains:
      series = df.set_index(domains).iloc[:, 0]
    else:
      series = df[df.columns[0]]
    self.series[identifier] = series

  def add_parameter_from_series(self, series, explanatory_text="", add_missing_domains=False):
    """Add parameter symbol to database based on a Pandas series."""
    if len(series) == 1 and series.index.name in [None, "*"]:
      df = pd.DataFrame(series)
    else:
      df = series.reset_index()
    self.add_parameter_from_dataframe(series.name, df, explanatory_text, add_missing_domains)

  def add_variable_from_dataframe(self, identifier, df, explanatory_text="", add_missing_domains=False,
                                  value_column_index=-1):
    """Add variable symbol to database based on a Pandas DataFrame."""
    domains = list(df.columns[:value_column_index:])
    for d in domains:
      if d not in self:
        if add_missing_domains:
          self.create_set(name=d, index=df[d].unique(), explanatory_text="")
        else:
          raise KeyError(
            f"'{d}' is not a set in the database. Enable add_missing_domains or add the set to the database manually.")
    self.database.add_variable_dc(identifier, gams.VarType.Free, domains, explanatory_text)
    if domains:
      series = df.set_index(domains).iloc[:, 0]
    else:
      series = df[df.columns[0]]
    self.series[identifier] = series

  def add_variable_from_series(self, series, explanatory_text="", add_missing_domains=False):
    """Add variable symbol to database based on a Pandas series."""
    if len(series) == 1 and series.index.name in [None, "*"]:
      df = pd.DataFrame(series)
    else:
      df = series.reset_index()
    self.add_variable_from_dataframe(series.name, df, explanatory_text, add_missing_domains)

  def get_index(self, x):
    if x is None or isinstance(x, pd.Index):
      return x
    elif isinstance(x, str):
      return self[x]
    elif len(x) and isinstance(x[0], (pd.Index, tuple, list)):
      multi_index = pd.MultiIndex.from_product(x)
      multi_index.names = [getattr(i, "name", None) for i in x]
      return multi_index
    else:
      return pd.Index(x)

  def create_set(self, name, index, explanatory_text="", texts=None, domains=None):
    """
    Add a new GAMS Set to the database and return an Pandas representation of the Set.
    :param str name: Name of the set
    :param iterable index: Iterable of record keys to be added to the set
    :param str explanatory_text: Explanatory text added to the GAMS set
    :param iterable texts: Iterable of record labels - should match the size of the index parameter.
    :param iterable domains: Names of domains that the set should be defined over
    :return: Pandas Index
    """
    if len(index) and isinstance(index[0], pd.Index):
      multi_index = pd.MultiIndex.from_product(index)
      multi_index.names = [getattr(i, "name", None) for i in index]
      index = multi_index
    elif isinstance(index, pd.Index):
      index = index.copy()
    else:
      index = pd.Index(index)

    index.explanatory_text = explanatory_text

    if texts is None:
      texts = map_lowest_level(str, index)
    index.texts = pd.Series(texts, index=index)
    index.texts.name = index.name

    if domains is None:
      domains = ["*" if i in (None, name) else i for i in self.get_domains_from_index(index, name)]
    index.domains = domains
    index.names = domains
    index.name = name

    self.database.add_set_dc(index.name, domains, explanatory_text)
    self.series[index.name] = index
    return self[name]

  def __create_variable_or_parameter(self, symbol_type, name, index, explanatory_text, data, dtype, copy, add_missing_domains):
    if index is not None:
      series = pd.Series(data, self.get_index(index), dtype, name, copy)
      series.explanatory_text = explanatory_text
      getattr(self, f"add_{symbol_type}_from_series")(series, explanatory_text, add_missing_domains)
    elif isinstance(data, pd.DataFrame):
      getattr(self, f"add_{symbol_type}_from_dataframe")(name, data, explanatory_text, add_missing_domains)
    elif isinstance(data, pd.Series):
      getattr(self, f"add_{symbol_type}_from_series")(data, explanatory_text, add_missing_domains)
    else:
      if is_iterable(data) and len(data) and is_iterable(data[0]):
        self.__add_variable_or_parameter_to_database(symbol_type, name, len(data[0]), explanatory_text)
      elif is_iterable(data):
        getattr(self, f"add_{symbol_type}_from_dataframe")(name, pd.DataFrame(data), explanatory_text, add_missing_domains)
      else:
        self.__add_variable_or_parameter_to_database(symbol_type, name, 0, explanatory_text)
        self[name] = data
    return self[name]

  def __add_variable_or_parameter_to_database(self, symbol_type, name, dim, explanatory_text):
    assert symbol_type in ["parameter", "variable"]
    if symbol_type == "parameter":
      self.database.add_parameter(name, dim, explanatory_text)
    elif symbol_type == "variable":
      self.database.add_variable(name, dim, gams.VarType.Free, explanatory_text)

  def create_variable(self, name, index=None, explanatory_text="", data=None, dtype=None, copy=False, add_missing_domains=False):
    return self.__create_variable_or_parameter("variable", name, index, explanatory_text, data, dtype, copy, add_missing_domains)

  def create_parameter(self, name, index=None, explanatory_text="", data=None, dtype=None, copy=False, add_missing_domains=False):
    return self.__create_variable_or_parameter("parameter", name, index, explanatory_text, data, dtype, copy, add_missing_domains)

  @staticmethod
  def get_domains_from_index(index, name):
    if hasattr(index, "domains"):
      domains = index.domains
    elif hasattr(index, "name"):
      domains = index.names
    else:
      domains = [index.name]
    return ["*" if i in (None, name) else i for i in domains]

  @staticmethod
  @np.vectorize
  def detuple(t):
    """Returns the iterable unchanged, except if it is a singleton, then the element is returned"""
    if isinstance(t, str):
      return t
    try:
      if len(t) == 1:
        return t[0]
    except TypeError:
      pass
    return t

  def __getitem__(self, item):
    if item not in self.series:
      symbol = self.symbols[item]

      if isinstance(symbol, gams.GamsSet):
        self.series[item] = index_from_symbol(symbol)

      elif isinstance(symbol, gams.GamsVariable):
        if symbol_is_scalar(symbol):
          self.series[item] = symbol.find_record().level if len(symbol) else None
        else:
          self.series[item] = series_from_variable(symbol)
          if self.auto_sort_index:
            self.series[item] = self.series[item].sort_index()

      elif isinstance(symbol, gams.GamsParameter):
        if symbol_is_scalar(symbol):
          self.series[item] = symbol.find_record().value if len(symbol) else None
        else:
          self.series[item] = series_from_parameter(symbol)
          if self.auto_sort_index:
            self.series[item] = self.series[item].sort_index()

      elif isinstance(symbol, gams.GamsEquation):
        return symbol

    return self.series[item]

  def __setitem__(self, name, value):
    if name in self.symbols:
      if not is_iterable(value) and is_iterable(self[name]):  # If assigning a scalar to all records in a series
        value = pd.Series(value, index=self[name].index)
      set_symbol_records(self.symbols[name], value)
      self.series[name] = value
    else:
      if not value.name:
        value.name = name
      self.series[name] = value

  def items(self):
    return self.symbols.items()

  def keys(self):
    return self.symbols.keys()

  def values(self):
    return self.symbols.values()

  def save_series_to_database(self, series_names=None):
    """Save Pandas series to GAMS database"""
    if series_names is None:
      series_names = self.series.keys()
    for symbol_name in series_names:
      set_symbol_records(self.symbols[symbol_name], self.series[symbol_name])

  def export(self, path):
    """Save changes to database and export database to GDX file."""
    self.save_series_to_database()
    for i in range(1, 10):
      try:
        self.database.export(os.path.abspath(path))
        break
      except gams.workspace.GamsException:
        time.sleep(i)
    else:
      self.database.export(os.path.abspath(path))

  def __iter__(self):
    return iter(self.symbols)

  def __len__(self):
    return len(self.symbols)

  def get_text(self, name):
    """Get explanatory text of GAMS symbol."""
    return self.symbols[name].get_text()


