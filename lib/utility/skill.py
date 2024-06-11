from ClassicAssist.Data.Macros.Commands.JournalCommands import ClearJournal, InJournal
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindObject
from ClassicAssist.Data.Macros.Commands.TargetCommands import CancelTarget, WaitForTarget, Target
from ClassicAssist.Data.Macros.Commands.SkillCommands import UseSkill, Skill, SkillCap
from ClassicAssist.Data.Macros.Commands.AliasCommands import FindAlias, PromptMacroAlias


class SkillUtils:
    @classmethod
    def ArmsLore(cls, serial_or_alias, retry = True):
        if retry: ClearJournal()

        cls.Target("Arms Lor", serial_or_alias, retry, 1000, lambda: not InJournal("It looks unused.") or FindObject(serial_or_alias))


    @staticmethod
    def EnsureTarget(skill_name, serial_or_alias, loop, delay, continue_predicate = None):
        if not FindAlias(serial_or_alias):
            while True:
                if PromptMacroAlias(serial_or_alias): break

        SkillUtils.Target(skill_name, serial_or_alias, loop, delay, continue_predicate)


    @staticmethod
    def Target(skill_name, serial_or_alias, loop, delay, continue_predicate):
        while not loop or Skill(skill_name) < SkillCap(skill_name):
            CancelTarget()
            UseSkill(skill_name)
            if not WaitForTarget(1000): continue

            Target(serial_or_alias)
            Pause(delay)
            if continue_predicate and not continue_predicate(): return
            if not loop: return