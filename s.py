import subprocess, datetime, json, shlex

apiKey=""
cmd = ""

def init():
    global apiKey
    global APIKeyExistence
    try:
        with open("envVar.json", "r") as envVarFile:
            data = json.load(envVarFile)
            apiKey = data.get("apiKey")
    except:
        apiKey = input("Please provide a valid xAi API-KEY: \n")
        with open("envVar.json", "w") as envVarFile:
            data ={
                    "apiKey":apiKey
            }
            json.dump(data, envVarFile)
            print(f"Created envVar File with your API Key at {datetime.datetime.now()}")

def commandCrafter(prompt:str):
    with open("command.json", "r") as commandCrafterFile:
        data = json.load(commandCrafterFile)

        uri = data.get("uri")
        sRole = data.get("sRole")
        content = data.get("content")
        uRole = data.get("uRole")
        model = data.get("model")

        cmd = f'curl {uri} -H "Content-Type: application/json" -H "Authorization: Bearer {apiKey}" -d \'{{ "messages": [{{ "role": "{sRole}", "content": "{content}" }}, {{ "role": "{uRole}", "content": "{prompt}" }}], "model": "{model}", "stream": false, "temperature": 0 }}\''

        return cmd

def checkApiKeyValidation():
    global APIKeyValidation
    cmd = commandCrafter(prompt="say hello")
    cmd_list = shlex.split(cmd)
    result = subprocess.run(cmd_list, capture_output=True, text=True)

    try:
        
        result_json = json.loads(result.stdout)

        with open("result.json", "w") as outputFile:
            json.dump(result_json, outputFile, indent=4)

    except json.JSONDecodeError:
        print("Error: The command output is not valid JSON.")


init()
checkApiKeyValidation()
