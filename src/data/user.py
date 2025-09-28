"""user data module."""

from model.user import User
from .init import conn, curs, get_db, IntegrityError
from data.errors import Missing, Duplicate


curs.execute(
    """
    create table if not exists
        user(
        name text primary key,
        hash text
        ) 
    """
)

curs.execute(
    """
    create table if not exists 
        xuser(
        name text primary key,
        hash text
        )
    """
)


def row_to_model(row: tuple):
    """convert row to model."""
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> User:
    """get one user by name."""
    return user.model_dump()


def get_one(name: str) -> User:
    """get one user by name."""
    qry = """select * from user where name=:name"""
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row is None:
        raise Missing("user", name)
    return row_to_model(row)


def get_all() -> list[User]:
    """get all users."""
    qry = """select * from user"""
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(user: User, table: str = "user") -> User:
    """add user to user or xuser table."""

    qry = f"""insert into {table} (name, hash) values (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
        conn.commit()
        return get_one(user.name)
    except IntegrityError:
        raise Duplicate(msg=f"user with name {user.name} already exists")


def modify(name: str, user: User) -> User:
    """modify user."""
    qry = """update user set hash=:hash, name=:name where name=:name0"""
    params = {"name": user.name, "hash": user.hash, "name0": name}
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount == 1:
        return get_one(user.name)
    raise Missing("user", name)


def delete(name: str) -> None:
    """delete user."""
    qry = """delete from user where name=:name"""
    params = {"name": name}
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing("user", name)
    create(name, table="xuser")
