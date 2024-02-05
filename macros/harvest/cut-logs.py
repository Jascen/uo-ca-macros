"""
Name: Log Cutter
Description: Cuts the configured log types in the amount specified
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

from utility.alias import AliasUtils
from services.logcutter import LogCutter
from entities.skillitem import LumberjackSkillItem


class UserOptions:
    ForcePromptLogContainer = True
    LogsToChop = [
        # [Amount to cut at a time, Type of wood]
        [1, LumberjackSkillItem.Wood], # Plain logs
        [1, LumberjackSkillItem.Ash],
        [1, LumberjackSkillItem.Cherry],
        [1, LumberjackSkillItem.Ebony],
        [1, LumberjackSkillItem.GoldenOak],
        [1, LumberjackSkillItem.Hickory],
        [1, LumberjackSkillItem.Mohagony],
        [1, LumberjackSkillItem.Driftwood],
        [1, LumberjackSkillItem.Oak],
        [1, LumberjackSkillItem.Pine],
        [1, LumberjackSkillItem.Rosewood],
        [1, LumberjackSkillItem.Walnut],

        # Are you really sure you want to change this?
        [1, LumberjackSkillItem.Elven],
    ]


def Main():
    if UserOptions.ForcePromptLogContainer: AliasUtils.PromptContainer("log container")
    cutter = LogCutter()

    for original in UserOptions.LogsToChop:
        # Set amounts to user-defined values
        amount = original[0]
        skill_item = original[1]
        cutter.Cut(skill_item, amount, False)


# Execute Main()
Main()