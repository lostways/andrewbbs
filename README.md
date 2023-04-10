# Andrew BBS
An expirement in "deep web" content mangement

All contnet must be accesed using a appropite access code. Once screens are unlocked they are sotred in the session. If a user wants to save thier finding they can register as a member.

Uses:

* [Django Framework](https://www.djangoproject.com/)
* [Bootstrap 386 Theme](https://github.com/kristopolous/BOOTSTRA.386)
 
## Development
Docker is the prefered way to run a local development environment. Everything is automated using Make.

Copy the local .env.example to .env and fill in the correct vars for your setup
```
cp ./.envs/local/.env.example ./envs/local/.env
```

To build the image, make and run migrations, and run the dev server, use:
```
make run
```

The first time you run the app you'll want to create a superuser
```
make manage createsuperuser
```

If you want to run the tests:
```
make test
```

To run a django mangement command use `make manage`. For example:
```
make manage shell
```

## OTP Login
The app is able to use the Twilio api to do OTP login. See [Twilio Verification API](https://www.twilio.com/docs/verify/api) for more details. 

For development there is a local OTP provider that doesn't depend on Twilio. To use it set `OTP_PROVIER` to `local`. The correct auth code is sent to the logs. Use it to login.

## Database
A Postgress DB should be running on `localhost:5432`. 
PgAdmin web app should be runing on `localhost:5050`. 

After you log in to PgAdmin you can access the DB by adding a new server with Mantaience DB set to your POSTGRES_DB, host set to `andrewbbs-postgres`, and our username and password set to the same ones you set in your .env

## TODO
- DevOps
  - add make targets for production
  - add continuous deployment via workflows
  - move certs to volumes
  - Reduce size of django image?
- App
  - Add view and edit member details
  - Add view member list
  - Add message sysop feature 
  - Alerts for new joins