# RaritanKiller

RaritanKiller is a Python-developed application for managing outlets in a Raritan Power Distribution Unit (PDU) using the Raritan RPC library. It allows you to connect to a specific PDU and perform operations such as enabling, disabling, and restarting outlets. The application also provides options to check for turned-off outlets across all PDUs and automatically turn them on. Additionally, future development plans include adding features to check power consumption statistics for individual outlets.

## Features

- **on**: Choose an outlet and turn it on. Syntax: `[on] <outlet_number>`

- **turn_all**: Turn on all outlets among all PDUs with an offline status. Syntax: `[turn_all]`

- **off**: Choose an outlet and turn it off. Syntax: `[off] <outlet_number>`

- **restart**: Choose an outlet and restart it. Syntax: `[restart] <outlet_number>`

- **show_off**: Show all outlets with an off status. Syntax: `[show_all] <raritan_ip>`

- **show**: Show the status of outlets in the current Raritan PDU. Syntax: `[show]`

- **switch**: Switch to another PDU. Syntax: `[switch] <raritan_nr>` or `[switch] <raritan_ip>`

- **close**: Close the program. Syntax: `[close]`

- **exit**: Return to the main menu. Syntax: `[exit]`

## Usage

To use the RaritanKiller application, follow these steps:

1. Install the necessary dependencies by running `pip install raritan`.

2. Clone this repository or download the source code files.

3. Import the Raritan RPC library and the RaritanKiller module into your Python project.

4. Establish a connection with the Raritan PDU using the appropriate credentials and connection details.

5. If your work environment has a different naming convention for outlets than the platform hostnames, you can use the **translate_hostname** function provided in the RaritanKiller module. This function allows you to map the outlet numbers to their corresponding hostnames in your environment. You can customize this translation logic based on your naming conventions, with usage of excel file.

6. Use the available commands to manage the outlets in the PDU. Refer to the features section for the command syntax.

7. Customize the application or integrate it into your own project as needed.

## Future Enhancements

The RaritanKiller application is under active development, and the following enhancements are planned for future releases:

- Support for checking and displaying power consumption statistics of individual outlets.

- Integration with external monitoring systems to provide real-time alerts and notifications.

- Addition of a web-based interface for easier management and control of outlets.

- Improved error handling and logging capabilities.

- Compatibility with other PDU models and manufacturers.



Thank you for using RaritanKiller! We hope this application simplifies the management of outlets in your Raritan PDUs and contributes to a more efficient power distribution system.
