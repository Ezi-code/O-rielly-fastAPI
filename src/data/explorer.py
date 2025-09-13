"""explorer database file."""

from model.explorer import Explorer
from .init import curs, conn, IntegrityError
from .errors import Duplicate, Missing


curs.execute(
    """create table if not exists explorer(
name text primary key,
description text, 
country text)"""
)


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], description=row[1], country=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found!")


def get_all() -> Explorer:
    qry = "select * from explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    qry = """insert into explorer values (:name, :description, :country)"""
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
        conn.commit()
        return get_one(explorer.name)

    except IntegrityError:
        raise Duplicate(msg=f"Explorer with same name already exist")


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    qry = """update explorer
             set country=:country,
             name=:name, 
             description=:description 
             where name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    conn.commit()
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(mdg=f"Explorer {name} not found")


def replace(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> Explorer:
    if not name:
        return False
    qry = "delete from explorer where name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
    return bool(res)
