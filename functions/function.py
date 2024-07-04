import os
import paramiko
import io
import pandas as pd
import tempfile

def process_excel_and_create_text_file(input_xlsx_file, script_directory):
    try:
        # Create a temporary directory to store the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, input_xlsx_file.name)
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in input_xlsx_file.chunks():
                    temp_file.write(chunk)

            df = pd.read_excel(temp_file_path, engine='openpyxl')

            # Convert the date and time columns to datetime format with the specified format
            df['dateofcall'] = pd.to_datetime(df['dateofcall'], format='mixed')
            df['starttime'] = pd.to_datetime(df['starttime'], format='%H:%M:%S')
            output_text_file = os.path.join(script_directory, 'output_text_file.txt')
            df['FormattedData'] = df.apply(lambda row: f"{row['DateofCall'].strftime('%Y-%m-%d')}/{row['Starttime'].strftime('%H/%M')}", axis=1)

            with open(output_text_file, 'w') as text_file:
                for data in df['FormattedData']:
                    text_file.write(f"{data}\n")

            print(f"Data extracted and written to {output_text_file}")
            return output_text_file  # Return the path to the created text file
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None  # Return None in case of an error


def handle_uploaded_file(f):
    local_directory = 'static/upload/'
    os.makedirs(local_directory, exist_ok=True)
    local_file_path = os.path.join(local_directory, f.name)

    with open(local_file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return local_file_path

def restore(output_text_file):
    username = 'ec2-user'
    vm_ip_address = '10.40.1.101'
    remote_file_path = '/home/ec2-user/file.txt'
    script_directory = os.path.dirname(os.path.abspath(__file__))

    id_rsa_path = os.path.join(script_directory, 'id_rsa')

    with open(id_rsa_path, 'r') as file:
        private_key_string = file.read()

    private_key = paramiko.RSAKey(file_obj=io.StringIO(private_key_string))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=vm_ip_address, username=username, pkey=private_key)
        scp_client = ssh_client.open_sftp()
        scp_client.put(output_text_file, remote_file_path)
        scp_client.close()

        command = 'sudo su - -c "cd /home/ec2-user/ && ./trial.sh"'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            print(f"Command failed with exit status {exit_status}")

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
        ssh_client.close()
