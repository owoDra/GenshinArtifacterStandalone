from enkanetwork import EnkaNetworkAPI
import asyncio

Client = EnkaNetworkAPI(lang="jp")

# ==============================================
# UId から UserData を取得する
#
# @Param  Uid       ゲーム内右下に表示されるID
# @Return UserData  ゲーム内名刺に表示される情報
# ==============================================
def FetchUserData(Uid):
    return asyncio.run(__Async_GetPlayerInfo(Uid))

async def __Async_GetPlayerInfo(Uid):
    async with Client:
        try:
            Data = await Client.fetch_user_by_uid(Uid)
            print("=== Player Info ===")
            print(f"Nickname: {Data.player.nickname}")
            print(f"Level: {Data.player.level}")
            print(f"Signature: {Data.player.signature}")
            print(f"Achievement: {Data.player.achievement}")
            print(f"Abyss floor: {Data.player.abyss_floor} - {Data.player.abyss_room}")
            print(f"Cache timeout: {Data.ttl}")
            return Data
            
        except Exception as Error:
            print(Error)
            
