import paramiko

def create_ssh_session(hostname,keyfile,keyfile_4k):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # print(password)
    auth = None
    try:
        try:
            if keyfile_4k:
                key = paramiko.RSAKey.from_private_key_file(keyfile_4k)
                client.connect(hostname, port=22 ,username='root', pkey=key,
                               disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
                if client.get_transport():
                    auth ='4k'
                return client,auth

        except paramiko.ssh_exception.AuthenticationException:
            print(f"4k key failed  for {hostname}")


        try:
            if keyfile:
                key = paramiko.RSAKey.from_private_key_file(keyfile)
                # print(private_key)
                client.connect(hostname, username='root', port=22, pkey=key,
                               disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
                if client.get_transport():
                    auth ='2k'
                return client,auth
        except:

            print(f"2k key failed  for {hostname}")

        try:

            client.connect(hostname, username='root', port=22, password='sonic_root')
            if client.get_transport():
                auth ='password'
            return client,auth
        except:

            print(f"password failed for {hostname} ")



    except paramiko.ssh_exception.SSHException as ssh_ex:
        print("Error connecting to the SSH server:", str(ssh_ex))
        return None



