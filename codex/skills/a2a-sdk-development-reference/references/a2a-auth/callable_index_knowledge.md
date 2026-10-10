# Complete source and callable index

AST inventory includes classes, functions, properties, methods, conditional definitions and nested helpers. Signature/source-docstring summaries are supplementary evidence: manually written behavioral guides explain actual execution. Non-Python files are inventoried and linked even though they have no runtime AST callables.

## `__init__.py`

Behavior: [init_knowledge.md](init_knowledge.md). Source: [__init__.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/__init__.py).

No declared runtime callables. Configuration/import/template/static role is explained in the linked guide.

## `user.py`

Behavior: [user_knowledge.md](user_knowledge.md). Source: [user.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py).

<!-- declaration:user.py:6:User -->
### `User`

```python
class User(ABC)
```

Source: [User](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:6). Source-docstring summary: A representation of an authenticated user.

<!-- declaration:user.py:11:User.is_authenticated -->
### `User.is_authenticated`

```python
def is_authenticated(self) -> bool
```

Source: [User.is_authenticated](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:11). Source-docstring summary: Returns whether the current user is authenticated.

<!-- declaration:user.py:16:User.user_name -->
### `User.user_name`

```python
def user_name(self) -> str
```

Source: [User.user_name](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:16). Source-docstring summary: Returns the user name of the current user.

<!-- declaration:user.py:20:UnauthenticatedUser -->
### `UnauthenticatedUser`

```python
class UnauthenticatedUser(User)
```

Source: [UnauthenticatedUser](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:20). Source-docstring summary: A representation that no user has been authenticated in the request.

<!-- declaration:user.py:24:UnauthenticatedUser.is_authenticated -->
### `UnauthenticatedUser.is_authenticated`

```python
def is_authenticated(self) -> bool
```

Source: [UnauthenticatedUser.is_authenticated](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:24). Source-docstring summary: Returns whether the current user is authenticated.

<!-- declaration:user.py:29:UnauthenticatedUser.user_name -->
### `UnauthenticatedUser.user_name`

```python
def user_name(self) -> str
```

Source: [UnauthenticatedUser.user_name](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py:29). Source-docstring summary: Returns the user name of the current user.

