import paramiko

def create_ssh_session(hostname, keyfile_2k=None, keyfile_4k=None, password=None, username='root'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    auth = None

    try:
        if keyfile_4k:
            try:
                print(keyfile_4k)
                key = paramiko.RSAKey.from_private_key_file(keyfile_4k)
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(hostname, port=22, username=username, pkey=key,
                               disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
                if client.get_transport() and client.get_transport().is_active():
                    auth = '4k'
                    return client, auth
                else:
                    client.close()
            except paramiko.ssh_exception.AuthenticationException:
                print(f"4k key failed for {hostname}")

        if keyfile_2k:
            try:
                key = paramiko.RSAKey.from_private_key_file(keyfile_2k)
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(hostname, port=22, username=username, pkey=key,
                               disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
                if client.get_transport() and client.get_transport().is_active():
                    auth = '2k'
                    return client, auth
                else:
                    client.close()
            except paramiko.ssh_exception.AuthenticationException:
                print(f"2k key failed for {hostname}")

        if password:
            try:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(hostname, port=22, username=username, password=password)
                if client.get_transport() and client.get_transport().is_active():
                    auth = 'password'
                    return client, auth
                else:
                    client.close()
            except paramiko.ssh_exception.AuthenticationException:
                print(f"Password failed for {hostname}")

    except paramiko.ssh_exception.SSHException as ssh_ex:
        print("Error connecting to the SSH server:", str(ssh_ex))

    return None, None
#
# # Example usage:
# hostname = 'your.remote.host'
# keyfile_4k = '/path/to/your/4k_key'
# keyfile_2k = '/path/to/your/2k_key'
# password = 'your_password'
#
# client, auth_method = create_ssh_session(hostname, keyfile_2k=keyfile_2k, keyfile_4k=keyfile_4k, password=password)
# if client:
#     print(f"Authenticated using {auth_method}")
# else:
#     print("Failed to authenticate using any method")
