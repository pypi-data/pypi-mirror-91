import getpass
import win10toast
def sign_in(username_for_user, password_of_user):
  username = input("Enter your username: ")
  if username != username_for_user:
    print ("Wrong username")
    return "Wrong Username, Try again"
    return 0
  else:
    password = getpass.getpass("Enter the password for this username: ")
    if password != password_of_user:
      print("Wrong Password")
      return "Wrong Password, Try again" 
      return 0
    else:
      if username_for_user == username and password_of_user == password:
        return 1
        print("Successful Sign In")
        notify = win10toast.ToastNotifier()
        notify.show_toast("Sign In", "Successful sign in", duration=7)
    
def get_username():
  username1 = getpass.getuser()
  return username1

