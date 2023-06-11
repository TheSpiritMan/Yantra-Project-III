# Yantra Backend

## Packages requirements
- `pip install virtualenv`
- `virtualenv venv && source venv/bin/activate`

- `pip install -r requirements.txt`


## DB setup
- Install PostgreSql locally

# Environments Setup
- `env.example` can be found
- Copy `env.example` into `.env` and insert value



## Run Project
- Make Migrations
    ```
    python manage.py makemigrations User 
    python manage.py runserver
    ```


## To Test API
- [Post Method]: `/register`: User Registration
    ```
    {
    "username": "",
    "email": "",
    "password": ""
    }
    ```

- [Post Method]: `/verify-otp`: OTP Verification
    ```
    {
    "email": "",
    "otp": ""
    }
    ```
- [Post Method]: `/resend-otp`: Resend OTP if it expires
    ```
    {
    "email": ""
    }
    ```