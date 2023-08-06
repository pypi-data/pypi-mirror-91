import os
import sys
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
from dreamtools import GamsPandasDatabase, Gdx


@np.vectorize
def approximately_equal(x, y, ndigits=0):
  return round(x, ndigits) == round(y, ndigits)


def test_gdx_read():
  gdx = Gdx("test.gdx")
  assert approximately_equal(gdx["qY"]["byg", 2010], 191)
  assert approximately_equal(gdx["qI_s"]["IB", "fre", 2010], 4.43)  # "IB" should be changed to "iB" in the GDX file.
  assert approximately_equal(gdx["eCx"], 1)
  assert gdx["s"].name == "s_"

def test_create_set_from_index():
  db = GamsPandasDatabase()
  t = pd.Index(range(2010, 2026), name="t")
  db.create_set("t", t)
  assert db["t"].name == "t"
  assert all(db["t"] == t)
  assert db.symbols["t"].domains_as_strings == ["*"]
  assert db.t.domains == ["*"]

  db.create_set("tsub", t[5:], domains=["t"])
  assert db["tsub"].name == "tsub"
  assert all(db["tsub"] == t[5:])
  assert db.symbols["tsub"].domains_as_strings == ["t"]
  assert db.tsub.domains == ["t"]

  s = pd.Index(["services", "goods"], name="s")
  st = pd.MultiIndex.from_product([s, t], names=["s", "t"])
  db.create_set("st", st)
  assert db["st"].name == "st"
  assert all(db["st"] == st[:])
  assert db.symbols["st"].domains_as_strings == ["s", "t"]
  assert db.st.domains == ["s", "t"]

def test_add_parameter_from_dataframe():
  db = GamsPandasDatabase()
  df = pd.DataFrame()
  df["t"] = range(2010, 2026)
  df["value"] = 1.3
  db.add_parameter_from_dataframe("par", df, add_missing_domains=True)
  assert all(db["par"] == 1.3)
  assert len(db["par"]) == 16

def test_multiply_added():
  db = GamsPandasDatabase()
  df = pd.DataFrame([
    [2010, "ser", 3],
    [2010, "goo", 2],
    [2020, "ser", 6],
    [2020, "goo", 4],
  ], columns=["t", "s", "value"])
  db.add_parameter_from_dataframe("q", df, add_missing_domains=True)

  df = pd.DataFrame([
    [2010, 1],
    [2020, 1.2],
  ], columns=["t", "value"])
  db.add_parameter_from_dataframe("p", df, add_missing_domains=True)

  v = db["p"] * db["q"]
  v.name = "v"
  db.add_parameter_from_series(v)

  assert db["v"][2020, "goo"] == 4.8

def test_add_parameter_from_series():
  db = GamsPandasDatabase()

  t = pd.Index(range(2010, 2026), name="t")
  par = pd.Series(1.4, index=t, name="par")
  db.add_parameter_from_series(par, add_missing_domains=True)
  assert all(db["par"] == 1.4)
  assert len(db["par"]) == 16

  ss = pd.Index(["foo"], name="ss")
  singleton = pd.Series(1.4, index=ss, name="singleton")
  db.add_parameter_from_series(singleton, add_missing_domains=True)
  assert db["singleton"]["foo"] == 1.4
  assert len(db["singleton"]) == 1

  scalar = pd.Series(1.4, name="scalar")
  db.add_parameter_from_series(scalar)
  assert all(db["scalar"] == 1.4)
  assert len(db["scalar"]) == 1

def test_create_variable():
  db = GamsPandasDatabase()
  db.create_variable("scalar", data=3.2)
  assert db.scalar == 3.2
  db.create_variable("vector", data=[1, 2], index=pd.Index(["a", "b"], name="ab"), add_missing_domains=True)
  assert all(db.vector == [1, 2])

  db.create_variable("dataframe",
                     data=pd.DataFrame([
                       [2010, "ser", 3],
                       [2010, "goo", 2],
                       [2020, "ser", 6],
                       [2020, "goo", 4],
                     ], columns=["t", "s", "value"]),
                     add_missing_domains=True
                     )
  db.export("test_export.gdx")
  assert Gdx("test_export.gdx")["scalar"] == 3.2
  assert all(Gdx("test_export.gdx")["vector"] == [1, 2])
  assert all(db.s == ["ser", "goo"])
  assert all(db.t == [2010, 2020])

def test_create_parameter():
  db = GamsPandasDatabase()
  db.create_parameter("scalar", data=3.2)
  assert db.scalar == 3.2
  db.create_parameter("vector", data=[1, 2], index=pd.Index(["a", "b"], name="ab"), add_missing_domains=True)
  assert all(db.vector == [1, 2])

  db.create_parameter("dataframe",
                     data=pd.DataFrame([
                       [2010, "ser", 3],
                       [2010, "goo", 2],
                       [2020, "ser", 6],
                       [2020, "goo", 4],
                     ], columns=["t", "s", "value"]),
                     add_missing_domains=True
                     )
  db.export("test_export.gdx")
  assert Gdx("test_export.gdx")["scalar"] == 3.2
  assert all(Gdx("test_export.gdx")["vector"] == [1, 2])
  assert all(db.s == ["ser", "goo"])
  assert all(db.t == [2010, 2020])

def test_add_variable_from_series():
  db = GamsPandasDatabase()
  t = pd.Index(range(2010, 2026), name="t")
  var = pd.Series(1.4, index=t, name="var")
  db.add_variable_from_series(var, add_missing_domains=True)
  assert all(db["var"] == 1.4)
  assert len(db["var"]) == 16

def test_add_variable_from_dataframe():
  db = GamsPandasDatabase()
  df = pd.DataFrame([
    [2010, "ser", 3],
    [2010, "goo", 2],
    [2020, "ser", 6],
    [2020, "goo", 4],
  ], columns=["t", "s", "value"])
  db.add_variable_from_dataframe("q", df, add_missing_domains=True)
  assert all(db.t == [2010, 2020])
  assert all(db.s == ["ser", "goo"])

def test_multiply_with_different_sets():
  assert approximately_equal(
    sum(Gdx("test.gdx")["qBNP"] * Gdx("test.gdx")["qI"] * Gdx("test.gdx")["qI_s"]),
    50730260150
  )

def test_export_with_no_changes():
  Gdx("test.gdx").export("test_export.gdx", relative_path=True)
  assert round(os.stat("test.gdx").st_size, -5) == round(os.stat("test_export.gdx").st_size, -5)

def test_export_variable_with_changes():
  gdx = Gdx("test.gdx")
  gdx["qY"] = gdx["qY"] * 2
  gdx.export("test_export.gdx", relative_path=True)
  old, new = Gdx("test.gdx"), Gdx("test_export.gdx")
  assert all(old["qY"] * 2 == new["qY"])

def test_export_scalar_with_changes():
  gdx = Gdx("test.gdx")
  gdx["eCx"] = gdx["eCx"] * 2
  gdx.export("test_export.gdx", relative_path=True)

  old, new = Gdx("test.gdx"), Gdx("test_export.gdx")
  assert approximately_equal(old["eCx"] * 2, new["eCx"])

def test_export_set_with_changes():
  gdx = Gdx("test.gdx")
  gdx["s"].texts["tje"] = "New text"
  gdx.export("test_export.gdx", relative_path=True)
  assert Gdx("test_export.gdx")["s"].texts["tje"] == "New text"

def test_copy_set():
  gdx = Gdx("test.gdx")
  gdx["alias"] = gdx["s"]
  gdx["alias"].name = "alias"
  index = gdx["alias"]
  domains = ["*" if i in (None, index.name) else i for i in gdx.get_domains_from_index(index, index.name)]
  gdx.database.add_set_dc(index.name, domains, "")
  index = index.copy()
  index.domains = domains
  gdx.series[index.name] = index
  gdx.export("test_export.gdx", relative_path=True)
  assert all(Gdx("test_export.gdx")["alias"] == gdx["s"])

def test_export_added_variable():
  gdx = Gdx("test.gdx")
  gdx.create_variable("foo", [gdx.a, gdx.t], explanatory_text="Variable added from Python.")
  gdx["foo"] = 42
  gdx.export("test_export.gdx", relative_path=True)
  assert all(approximately_equal(Gdx("test_export.gdx")["foo"], 42))

def test_export_NAs():
  db = GamsPandasDatabase()
  t = db.create_set("t", range(5))
  p = db.create_parameter("p", t)
  assert len(db["p"]) == 5
  assert len(db.symbols["p"]) == 0
  db.export("test_export.gdx")

  db = Gdx("test_export.gdx")
  assert all(pd.isna(db["p"]))
  assert len(db["p"]) == 0
  assert len(db.symbols["p"]) == 0

def test_detuple():
  assert GamsPandasDatabase.detuple("aaa") == "aaa"
  assert GamsPandasDatabase.detuple(("aaa",)) == "aaa"
  assert list(GamsPandasDatabase.detuple(("aaa", "bbb"))) == ["aaa", "bbb"]
  assert GamsPandasDatabase.detuple(1) == 1
  assert list(GamsPandasDatabase.detuple([1, 2])) == [1, 2]

def test_create_methods():
  # Create empty GamsPandasDatabase and alias creation methods
  db = GamsPandasDatabase()
  Par, Var, Set = db.create_parameter, db.create_variable, db.create_set

  # Create sets from scratch
  t = Set("t", range(2000, 2021), "Årstal")
  s = Set("s", ["tjenester", "fremstilling"], "Brancher", ["Tjenester", "Fremstilling"])
  st = Set("st", [s, t], "Branche x år dummy")
  sub = Set("sub", ["tjenester"], "Subset af brancher", domains=["s"])

  one2one = Set("one2one", [(2010, 2015), (2011, 2016)], "1 til 1 mapping", domains=["t", "t"])

  one2many = Set("one2many",
                 [("tot", "tjenester"), ("tot", "fremstilling")],
                 "1 til mange mapping", domains=["*", "s"],
                 )
  assert one2many.name == "one2many"
  assert one2many.names == ["*", "s"]
  assert one2many.domains == ["*", "s"]

  # Create parameters and variables based on zero ore more sets
  gq = Par("gq", None, "Produktivitets-vækst", 0.01)
  fq = Par("fp", t, "Vækstkorrektionsfaktor", (1 + 0.01)**(t-2010))
  d = Par("d", st, "Dummy")
  y = Var("y", [s,t], "Produktion")

  assert gq == 0.01
  assert all(fq.loc[2010:2011] == [1, 1.01])
  assert pd.isna(d["tjenester",2010])
  assert pd.isna(y["tjenester",2010])