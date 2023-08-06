import asyncio

from asyncdrive import AsyncDrive

drive = AsyncDrive(
    'test/test_creds.json',
    ['https://www.googleapis.com/auth/drive'],
    ratelimit=10,
    cache=False
)

async def main():
    # print(await drive.list())
    async with drive.open('nocache-test.txt', 'r') as file:
        print(file.read())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
