class commands():
    async def getRewardVip(name):
        rewardCommand = f"lp user {name} parent addtemp vip 7d"
        return rewardCommand