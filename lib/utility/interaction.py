
class InteractionUtils:
    @classmethod
    def Prompt(cls, title, content, footer):
        return ConfirmPrompt(
            "<center>{}</center>".format(title)
            + content
            + "<br><br>" 
            + footer
            )