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
    python manage.py makemigrations User File
    python manage.py migrate
    python manage.py runserver
    ```


## To Test API
- <b>Post Method</b>: `/register`: User Registration
    ```
    {
    "username": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "password": ""
    }
    ```

- <b>Post Method</b>: `/verify-otp`: OTP Verification
    ```
    {
    "email": "",
    "otp": ""
    }
    ```
- <b>Post Method</b>: `/resend-otp`: Resend OTP if it expires
    ```
    {
    "email": ""
    }
    ```

- <b>Post Method</b>: `/login`: Login User
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
- <b>Post Method</b>: `/forgot-pass`: Send OTP for resetting password
    ```
    {
    "email": ""
    }
    ```
- <b>Post Method</b>: `/reset-pass`: Reset Password
    ```
    {
    "email": "",
    "otp": "",
    "new_password": ""
    }
    ```
<b>NOTE: </b> Now other endpoint needs JWT token to authenticate.

>To Pass JWT Header: `Authorization:  Bearer <access_token>`

- <b>Post Method</b>: `/logout`: For Logging Out
    ```
    {
    "refresh": "<refresh_token>"
    }
    ```

- <b>Post Method</b>: `/upload-file`: To Upload CSV File
    ```
    {
    "csv_file": "<csv_file>"
    }
    ```
    >Respone on Success:
    ```
    {
    "message": "File Uploaded Successfully",
    "File ID": "0d5ec8b6-8fe4-4da4-9c08-bd1dbe876e4a",
    "counts": {
        "0": 369,
        "1": 337
        }
    }
    ```

- <b>Get Method</b>: `/getAllFiles`: To List All the File User has Uploaded
    ```
    [
        {
            "id": "d64d5038-071c-4252-ae06-a90605ca6ac7",
            "csv_file": "/csv_files/demo_1x1o1ft.csv",
            "result_file": "/result_files/result_d64d5038-071c-4252-ae06-a90605ca6ac7.csv"
        },
        {
            "id": "b949d05f-ff5f-4f90-9e89-f75075f078eb",
            "csv_file": "/csv_files/demo_JjEQxpk.csv",
            "result_file": "/result_files/result_b949d05f-ff5f-4f90-9e89-f75075f078eb.csv"
        },
        {
            "id": "0d5ec8b6-8fe4-4da4-9c08-bd1dbe876e4a",
            "csv_file": "/csv_files/demo_BLuUOMV.csv",
            "result_file": "/result_files/result_0d5ec8b6-8fe4-4da4-9c08-bd1dbe876e4a.csv"
        }
    ]
    ```

- <b>Get Method</b>: `/download/<File.id>`: To Download Result File
    ```
    Eg: /download/0d5ec8b6-8fe4-4da4-9c08-bd1dbe876e4a
    ```

- <b>Get Method</b>: `/delete/<File.id>`: To delete File 
    ```
    Eg: /delete/0d5ec8b6-8fe4-4da4-9c08-bd1dbe876e4a
    ```

- <b>Post Method</b>: `/change-pass`: To change Password inside dashboard 
    ```
    {
        "new_password": "password"
    }
    ```

- <b>Get Method</b>: `/me`: To Get User Details 
    >Respone on Success:
    ```
    {
    "id": "dbc70a09-3e4e-4ba8-b6cc-e6ec0f417021",
    "first_name": "",
    "last_name": "",
    "email": ""
    }
    ```