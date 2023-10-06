import os
import paramiko
import io
def handle_uploaded_file(f):
    # Define the local directory where you want to save the uploaded files
    local_directory = 'static/upload/'

    # Ensure the local directory exists, create it if necessary
    os.makedirs(local_directory, exist_ok=True)

    # Generate a unique file path for the uploaded file in the local directory
    local_file_path = os.path.join(local_directory, f.name)

    with open(local_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Return the local file path for later use
    return local_file_path




def restore(f):
    username = 'ec2-user'
    vm_ip_address = '10.40.1.101'
    remote_file_path = '/home/ec2-user/file.txt'
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the id_rsa file relative to the script's location
    id_rsa_path = os.path.join(script_directory, 'id_rsa')

    with open(id_rsa_path, 'r') as file:
        private_key_string = file.read()

    # Load the private key from the string
    private_key = paramiko.RSAKey(file_obj=io.StringIO(private_key_string))

    # Create an SSH client object
    ssh_client = paramiko.SSHClient()

    # Automatically add the server's host key (this is insecure in production)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the VM
        ssh_client.connect(hostname=vm_ip_address, username=username, pkey=private_key)

        # Call handle_uploaded_file to save the uploaded file and get the local file path
        local_file_path = handle_uploaded_file(f)

        # Create an SCP client
        scp_client = ssh_client.open_sftp()

        # Upload the local file to the remote VM
        scp_client.put(local_file_path, remote_file_path)

        # Close the SCP client
        scp_client.close()

        os.remove(local_file_path)

        # Execute the modified restore.sh script
        
        command = command = 'sudo su - -c "cd /home/ec2-user/ && ./trial.sh"'
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Wait for the command to finish
        exit_status = stdout.channel.recv_exit_status()

        # Check if the exit status is non-zero (indicating an error)
        if exit_status != 0:
            print(f"Command failed with exit status {exit_status}")

        # Capture and print the output of the command
        output = stdout.read().decode('utf-8')
        print("Output:")
        print(output)

    except paramiko.AuthenticationException as auth_err:
        print("Authentication failed:", auth_err)
    except paramiko.SSHException as ssh_err:
        print("SSH connection failed:", ssh_err)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the SSH connection
        ssh_client.close()






























# import paramiko
# import io
# import os
# def handle_uploaded_file(f):  
#     with open('static/upload/'+f.name, 'wb+') as destination:  
#         for chunk in f.chunks():  
#             destination.write(chunk)


# def restore(f):


    
#     username = 'coditas'
#     vm_ip_address = '34.67.84.213'
#     # local_file_path = 'C:\\Users\\Coditas\\Desktop\\python_shell\\hello.txt'  
#     remote_file_path = '/home/coditas/file.txt'

#     with open(('C:\\Users\\Coditas\\Desktop\\python_automation\\functions\\id_rsa'), 'r') as file:
#         private_key_string  = file.read()

#     # Load the private key from the string
#     private_key = paramiko.RSAKey(file_obj=io.StringIO(private_key_string))

#     # Create an SSH client object
#     ssh_client = paramiko.SSHClient()

#     # Automatically add the server's host key (this is insecure in production)
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     try:
#         # Connect to the VM
#         ssh_client.connect(hostname=vm_ip_address, username=username, pkey=private_key)

#         # Create an SCP client
#         scp_client = ssh_client.open_sftp()

#         # Upload the local file to the remote VM
#         scp_client.put(f, remote_file_path)

#         # Close the SCP client
#         scp_client.close()

#         # Execute the modified restore.sh script
#         command='sudo su'
#         ssh_client.exec_command(command)
#         command = 'chmod +x ~/restore.sh && ~/restore.sh'
#         stdin, stdout, stderr = ssh_client.exec_command(command)

#         # Wait for the command to finish
#         exit_status = stdout.channel.recv_exit_status()

#         # Check if the exit status is non-zero (indicating an error)
#         if exit_status != 0:
#             print(f"Command failed with exit status {exit_status}")

#         # Capture and print the output of the command
#         output = stdout.read().decode('utf-8')
#         print("Output:")
#         print(output)
          

#     except paramiko.AuthenticationException as auth_err:
#         print("Authentication failed:", auth_err)
#     except paramiko.SSHException as ssh_err:
#         print("SSH connection failed:", ssh_err)
#     except Exception as e:
#         print("An error occurred:", e)
#     finally:
#         # Close the SSH connection
#         ssh_client.close()