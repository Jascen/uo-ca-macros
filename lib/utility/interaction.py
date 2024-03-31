
class InteractionUtils:
    @classmethod
    def Prompt(cls, title, content, footer):
        result = ConfirmPrompt(
            "<center>{}</center>".format(title)
            + content
            + "<br><br>"
            + footer
            )
        
        Pause(350) # Small pause to let the user realize the window has changed

        return result