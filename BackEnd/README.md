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

- [Post Method]: `/login`: Login User
    ```
    {
    "username": "",
    "password": ""
    }
    ```
    >Respone on Success
    ```
    {
    "message": "Login successful",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTE4OTU2OCwiaWF0IjoxNjg2NTk3NTY4LCJqdGkiOiJkZjBhMGU3MzI4MzE0M2JiYjQyOWJmMTBhODgzNTg3YiIsInVzZXJfaWQiOiIxMDNkZjI3OS0yNzUzLTRhMjUtYTkxYS1mNTFiMDFlYmYzN2QifQ.Rz5IS0Yvx8d1iSJMFmU20oJDidAQI29USpxPUNOAPHI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NTk4NDY4LCJpYXQiOjE2ODY1OTc1NjgsImp0aSI6IjQwZGNjMWVkYzE3MzRiMjE5NWJiNzljZmRiYjg3ZWY0IiwidXNlcl9pZCI6IjEwM2RmMjc5LTI3NTMtNGEyNS1hOTFhLWY1MWIwMWViZjM3ZCJ9.CYynTtIlx6nnLFYQbOIhBsg-l2jpQazRcOjglN-Rwl0"
    }
    ```
- [Post Method]: `/forgot-pass`: Send OTP for resetting password
    ```
    {
    "email": ""
    }
    ```
- [Post Method]: `/reset-pass`: Reset Password
    ```
    {
    "email": "",
    "otp": "",
    "new_password": ""
    }
    ```

<b>NOTE: </b> Now other endpoint needs JWT token to authenticate.