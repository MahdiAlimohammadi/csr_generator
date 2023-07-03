# CSR Generator

This project generates a Certificate Signing Request (CSR) interactively or from a configuration file using OpenSSL.

## Requirements

- Python 3.x
- OpenSSL

## Installation

1. Clone the repository or download the code files.
2. Install the required dependencies:
   ```
    brew install openssl
   ```

## Usage

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command to start the CSR generation script:
   ```
   python csr_generation.py
   ```
4. Follow the prompts to choose the mode (Interactive or Configuration File) and provide the required information.

### Interactive Mode

In interactive mode, you will be prompted to enter the CSR details. Follow the instructions and provide the requested information, such as the Common Name, Organization, Organizational Unit, City, State/Province, Country, and Email Address.

### Configuration File Mode

In configuration file mode, you will need to create a configuration file in the specified format (*.conf). You can create a file using a text editor and save it with a `.conf` extension. Here's an example of a configuration file:

```ini
[req]
default_bits = 2048
distinguished_name = dn
prompt = no
req_extensions = req_ext

[dn]
countryName                = "US"
stateOrProvinceName        = "California"
localityName               = "San Francisco"
organizationName           = "Example Inc."
organizationalUnitName     = "IT Department"
commonName                 = "www.example.com"
emailAddress               = "admin@example.com"

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.0 = *.example.com
DNS.1 = *.dev.example.com
```

Replace the values in the file with the appropriate information for your CSR.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize the README file further to fit your project's specific requirements and conventions.
