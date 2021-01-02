from django.db import models
from datetime import datetime, time, date


# Create your models here.



class UserManager(models.Manager):
    def register(self, name, username, password, confirm_password):
        # Check for validation and then create the fields in table User
        validation_result = self.validate(name, username, password, confirm_password)
        if validation_result['status'] == True:
            created_user = self.create(name=name, username=username,
                                       password=password)
            validation_result = {'status': validation_result['status'], 'created_user': created_user}
            return validation_result
        return validation_result

    def validate(self, name, username, password, confirm_password):
        errors = []
        result = {}
        #  Validate First Name
        if name == '':
            msg = "Name cannot be left blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(name) < 2:
            msg = "Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in name) == True:
            msg = "Name cannot have numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Validate username
        if username == '':
            msg = "User name cannot be left blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(self.filter(username=username)) > 0:
            msg = "User already exist in our database"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Password Validation
        if password == '':
            msg = "Password cannot be left blank"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif len(password) < 8:
            msg = "Password must be greater than 8 characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result

            # Confirm Password
        elif confirm_password != password:
            msg = "Passwords do not match"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result

        else:
            result = {'status': True, 'errors': "Validation successful"}
            return result


def login_validate(self, username, password):
    errors = []
    try:
        found_user = self.get(username=username)
        # if bcrypt.checkpw(password.encode('utf8'), found_user.password.decode('utf8')):
        if password == password:
            result = {'status': True, 'found_user': found_user}
            return result
        else:
            msg = "Username and Password do not match"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
    except:
        msg = "Username is not in our database"
        errors.append(msg)
        result = {'status': False, 'errors': errors[0]}
        return result

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        d = datetime.now()
        print("*******************")
        print(d)
        print("*******************")
        now=d.strftime("%Y-%m-%d")
        print("*******************")
        print(now)
        print("*******************")
        result = {
            'status' : False,
            'errors' : []
        }
        if len(postData['destination']) < 2:
            result['errors'].append("Must enter a destination of at least two characters")
        if len(postData['description']) < 10:
            result['errors'].append("Must enter a description of at least ten characters")
        if len(postData['date_from']) < 10:
            result['errors'].append("Must enter Travel Date From")
        if len(postData['date_to']) < 10:
            result['errors'].append("Must enter Travel Date To")
        if postData['date_to'] < postData['date_from']:
            result['errors'].append("Can't return earlier than you leave")
        if postData['date_from'] < now:
            result['errors'].append("Please don't enter a date in the past")
        if len(result['errors']) < 1:
            result['status'] = True
            newtrip = Trip.objects.create(
                destination=postData['destination'], start_date=postData['date_from'],
                end_date=postData['date_to'],
                plan=postData['description'],
                created_by=User.objects.get(id=postData['userid']))
            newtrip.trip_members.add(User.objects.get(id=postData['userid']))
            newtrip.save()
        return result

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=12)
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip_members = models.ManyToManyField(User, related_name="joined_trips")
    created_by = models.ForeignKey(User, related_name="created_trips", on_delete=models.CASCADE)
    objects = TripManager()
