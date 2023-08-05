# MakeSignIn

A Simple, Sign in library for python to create a login place for your python project. To use it, use the the following python command.
```python
import makesignin
```
## Sign in

To sign in, import the library and enter the following python code
```python
makesignin.sign_in(user's_username, user's_password)
```
Change user's_username to the username the user should have and user's_password to the password the user should have. Then a sign in screen will be shown in your python project.
If the sign in function returns 0, that means sign in was insuccessful. If it returns 1, then signin was successful.

## Get Users login username
To get users login username, run the following command.
```python
makesignin.get_username()
```
