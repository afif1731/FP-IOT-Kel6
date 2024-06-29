from donttrust import DontTrust, Schema

registerValidation = DontTrust(name=Schema().string().required(),
                               email=Schema().email().required(),
                               password=Schema().string().required()
                               )

loginValidation = DontTrust(email=Schema().email().required(),
                            password=Schema().string().required()
                            )