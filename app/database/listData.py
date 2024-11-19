import json

class jsonData:
    async def createData(self, name):
        data = [{
            'name': name
        }]
        with open('app/database/event.json', 'w') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    async def addUser(self, name):
        newData = {
            'name': name
        }
        data = json.load(open("app/database/event.json"))
        data.append(newData)
        with open("app/database/event.json", "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    async def checkUser(self, name):
        data = json.load(open("app/database/event.json"))
        for user in data:
            if (user['name'] == name):
                return True