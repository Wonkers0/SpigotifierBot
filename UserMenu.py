import hikari
import miru

class UserButton(miru.Button):
  def __init__(self, userNameAndID):
    super().__init__(style=hikari.ButtonStyle.SECONDARY, label=userNameAndID)

  async def callback(self, ctx: miru.Context):
    await ctx.respond("Test")
    self.view.stop()

