from donttrust import DontTrust, Schema

changePasswdValidation = DontTrust(old_pass=Schema().string().required().min(4).max(4).alphanum(),
                                   new_pass=Schema().string().required().min(4).max(4).alphanum()
                                   )

claimBoxValidation = DontTrust(password=Schema().string().required().min(4).max(4).alphanum())

registerBoxValidation = DontTrust(id=Schema().string().required(),
                                  password=Schema().string().required().min(4).max(4).alphanum()
                                  )

loginBoxValidation = DontTrust(id=Schema().string().required(),
                                  password=Schema().string().required().min(4).max(4).alphanum()
                                  )