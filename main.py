from user import User

import asyncio

async def main():

    bob  = User()
    alice= User()
    user_provisory = User()

    
    ### CREATE PROVISORY IDENTITY
    info_provisory_account = await user_provisory.create_provisory("bob@email.fr")

    ### Alice CRYPTS DATA
    await alice.connect("user36","passwd")
    ### crypt "test" and allow "bob@email.fr to decrypt it
    data = await alice.crypt("test","bob@email.fr")

    ### bob CONNECTS AND ATTACHS PROVISORY IDENTITY    
    identity = await bob.create("bob","passwd")
    await bob.disconnect()
    await bob.connect("bob","passwd")
    await bob.attach_provisional_identity(info_provisory_account)

    ### DECRYPT DATA
    cleardata = await bob.decrypt(data)
    print("clear datat:",cleardata)

if __name__ == "__main__":
    asyncio.run(main())
