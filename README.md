# Andrew BBS

An expirement in "deep web" content mangement

All contnet must be accesed using a appropite access code. Once screens are unlocked they are sotred in the session. If a user wants to save thier finding they can register as a member.

Uses:

* [Django Framework](https://www.djangoproject.com/)
* [Bootstrap 386 Theme](https://github.com/kristopolous/BOOTSTRA.386)
 
## Development

Docker is the prefered way to run a local development environment. Everything is automated using Make.

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