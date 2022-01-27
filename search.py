import sys
from subprocess import Popen, PIPE
from pathlib import Path
import requests
import webbrowser


def get_file_name():
    """
    Function is used to get file name passed as command line argument.

    Returns:
        file-name: string
    """
    try:
        return sys.argv[1]
    except:
        print("File name not passed")
        exit()


def validate_file(file_name):
    """Function accepts a file name and checks if the file passed is a valid Python file and the file exists.

    Args:
        file_name (string): name of the file, whose validity is to be checked.

    Returns:
        bool: returns true if file exists and is valid or else it terminates the program.
    """
    file = Path(file_name)
    if file.is_file():
        return True
    else:
        print("Pass valid Python file name")
        exit()


def execute_file(file):
    """
    This function executes the Python file passed to it.

    Args:
        file ([string]): [name of the file to execute]

    Return:

    """
    command = f"python3 {file}"
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    if stderr.decode("utf-8") == "":
        print("No errors encountered!")
        stdout = stdout.decode("utf-8")
        print(f"Output : {stdout}")
        exit()
    else:
        return stderr.decode("utf-8")


def api_request(error):
    """This function makes api call to the perimeter passed.

    Args:
        error (string): key-word for which the API call is to be made.

    Returns:
        JSON object: returns the API response received as Python dictionary.
    """
    response = requests.get(
        f"https://api.stackexchange.com/2.2/search?order=desc&tagged=python&sort=activity&intitle={error}&site=stackoverflow"
    )
    return response.json()


def open_urls(json_dict):
    """This function extracts URLs from the dictionary received and opens URL in browser instance.

    Args:
        json_dict (dictionary): API response containing the URLs
    """
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == len(i) or count == 3:
            break

    for url in url_list:
        webbrowser.open(url)


def main():
    """driver code
    """
    file = get_file_name()
    validate_file(file)
    execute_file(file)
    error = execute_file(file)
    print(f"Error : {error}")
    error_code = error.strip().split("\n")[-1]
    error_codes = error_code.split(":")
    code_1 = error_codes[0]
    code_2 = error_codes[1]
    response_1 = api_request(code_1)
    response_2 = api_request(code_2)
    response_3 = api_request(error_code)
    open_urls(response_1)
    open_urls(response_2)
    open_urls(response_3)


# call to script
if __name__ == "__main__":
    main()
