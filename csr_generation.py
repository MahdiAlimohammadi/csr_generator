import os
import subprocess


def generate_csr_interactive():
    try:
        # Get input from user
        common_name = input("Enter the Common Name (e.g., www.example.com): ")
        organization = input("Enter the Organization: ")
        organizational_unit = input("Enter the Organizational Unit: ")
        city = input("Enter the City/Locality: ")
        state = input("Enter the State/Province: ")
        country = input("Enter the Country (e.g., US, CA, GB): ")
        email = input("Enter the Email Address: ")

        # Create the directory with the domain name
        domain_directory = common_name.replace(".", "_")
        os.makedirs(domain_directory, exist_ok=True)

        # Create the conf file
        conf_file = os.path.join(domain_directory, f"{common_name}_mycsr.conf")
        with open(conf_file, "w") as f:
            f.write(f"""[req]
default_bits = 2048
distinguished_name = dn
prompt             = no
req_extensions = req_ext

[dn]
countryName                = {country}
stateOrProvinceName        = {state}
localityName               = {city}
organizationName           = {organization}
organizationalUnitName     = {organizational_unit}
commonName                 = {common_name}
emailAddress               = {email}

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.0 = *.{common_name}
DNS.1 = *.dev.{common_name}
""")

        generate_csr_from_config(conf_file)

    except subprocess.CalledProcessError as e:
        print("An error occurred while executing OpenSSL commands:")
        print(e.stderr.decode().strip())
    except Exception as e:
        print("An error occurred while generating the CSR:")
        print(str(e))


def generate_csr_from_config(conf_file):
    try:
        domain_directory = os.path.dirname(conf_file)
        common_name = None

        # Read the commonName from the configuration file
        with open(conf_file, "r") as f:
            for line in f:
                if line.strip().startswith("commonName"):
                    common_name = line.strip().split("=")[1].strip().strip('"')
                    break

        if common_name:
            # Create the directory with the domain name
            domain_directory = common_name.replace(".", "_")
            os.makedirs(domain_directory, exist_ok=True)

            # Add common_name at the beginning of file names
            common_name_prefix = common_name.replace(".", "_")

            # Generate the private key
            private_key_file = os.path.join(domain_directory, f"{common_name_prefix}_private.key")
            openssl_key_cmd = f"openssl genpkey -algorithm RSA -out {private_key_file}"
            subprocess.run(openssl_key_cmd, shell=True, check=True)

            # Generate the CSR
            csr_file = os.path.join(domain_directory, f"{common_name_prefix}_csr.pem")
            openssl_csr_cmd = f"openssl req -new -config {conf_file} -key {private_key_file} -out {csr_file}"
            subprocess.run(openssl_csr_cmd, shell=True, check=True)

            print("\nCSR generated successfully!")
            print(f"CSR file: {os.path.abspath(csr_file)}")
            print(f"Private key file: {os.path.abspath(private_key_file)}")
        else:
            print("Error: Common Name (commonName) not found in the configuration file.")

    except subprocess.CalledProcessError as e:
        print("An error occurred while executing OpenSSL commands:")
        print(e.stderr.decode().strip())
    except Exception as e:
        print("An error occurred while generating the CSR:")
        print(str(e))


def main():
    print("CSR Generation")
    print("---------------")
    print("1. Interactive Mode")
    print("2. Configuration File Mode")

    choice = input("Choose an option (1 or 2): ")
    if choice == "1":
        generate_csr_interactive()
    elif choice == "2":
        try:
            conf_file = input("Enter the path to the configuration file: ")
            generate_csr_from_config(conf_file)
        except Exception as e:
            print("An error occurred while generating the CSR:")
            print(str(e))
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
