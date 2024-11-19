class commands():
    async def getRewardVip(name):
        rewardCommand = f"lp user {name} parent addtemp vip 3d"
        return rewardCommand

    async def setNewPassword(password, user):
        cmd = f"authme password {user} {password}"
        return  cmd