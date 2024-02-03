from utility.alias import AliasUtils
from services.logcutter import LogCutter
from entities.skillitem import LumberjackSkillItem


class UserOptions:
    ForcePromptLogContainer = True
    LogsToChop = [
        LumberjackSkillItem.Wood, # Plain logs
        LumberjackSkillItem.Ash,
        LumberjackSkillItem.Cherry,
        LumberjackSkillItem.Ebony,
        LumberjackSkillItem.GoldenOak,
        LumberjackSkillItem.Hickory,
        LumberjackSkillItem.Mohagony,
        LumberjackSkillItem.Driftwood,
        LumberjackSkillItem.Oak,
        LumberjackSkillItem.Pine,
        LumberjackSkillItem.Rosewood,
        LumberjackSkillItem.Walnut,

        # Are you really sure you want to do this?
        ### LumberjackSkillItem.Elven,
    ]


def Main():
    if UserOptions.ForcePromptLogContainer: AliasUtils.PromptContainer("log container")
    cutter = LogCutter()

    for skill_item in UserOptions.LogsToChop:
        cutter.Cut(skill_item, 1, False)


# Execute Main()
Main()