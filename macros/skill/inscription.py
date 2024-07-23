from entities.craftmenuitem import *
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils

Spells = [
    [
        ReactiveArmor,
        Clumsy,
        CreateFood,
        Feeblemind,
        Heal,
        MagicArrow,
        NightSight,
        Weaken,
    ],
    [
        Agility,
        Cunning,
        Cure,
        Harm,
        MagicTrap,
        MagicUntrap,
        Protection,
        Strength,
    ],
    [
        Bless,
        Fireball,
        MagicLock,
        Poison,
        Telekinesis,
        Teleport,
        Unlock,
        WallOfStone,
    ],
    [
        ArchCure,
        ArchProtection,
        Curse,
        FireField,
        GreaterHeal,
        Lightning,
        ManaDrain,
        Recall,
    ],
    [
        BladeSpirits,
        DispelField,
        Incognito,
        MagicReflection,
        MindBlast,
        Paralyze,
        PoisonField,
        SummonCreature,
    ],
    [
        Dispel,
        EnergyBolt,
        Explosion,
        Invisibility,
        Mark,
        MassCurse,
        ParalyzeField,
        Reveal,
    ],
    [
        ChainLightning,
        EnergyField,
        Flamestrike,
        GateTravel,
        ManaVampire,
        MassDispel,
        MeteorSwarm,
        Polymorph,
    ],
    [
        Earthquake,
        EnergyVortex,
        Resurrection,
        SummonAirElemental,
        SummonDaemon,
        SummonEarthElemental,
        SummonFireElemental,
        SummonWaterElemental,
    ],
]


def Meditate(min_mana):
    if Mana("self") < min_mana:
        UseSkill("Meditatio")
        while Mana("self") < MaxMana():
            HeadMsg("Meditating...")
            Pause(1000)


def MakeCircle(service, circle, resources):
    skill_item = None
    while not Dead():
        for i, spell in enumerate(Spells[circle - 1]):
            if circle == 1: skill_item = SkillItem(spell, resources, 0,    14.2) # 25
            if circle == 2: skill_item = SkillItem(spell, resources, 14.2, 28.5) # 39.2
            if circle == 3: skill_item = SkillItem(spell, resources, 28.5, 42.8) # 53.5
            if circle == 4: skill_item = SkillItem(spell, resources, 42.8, 57.1) # 67.8
            if circle == 5: skill_item = SkillItem(spell, resources, 57.1, 71.4) # 82.1
            if circle == 6: skill_item = SkillItem(spell, resources, 71.4, 85.7) # 96.4
            if circle == 7: skill_item = SkillItem(spell, resources, 85.7, 100) # 110.7
            if circle == 8: skill_item = SkillItem(spell, resources, 100,  125) # 125

            skill_value = Skill("inscriptio")
            if skill_value < skill_item.min_level: return # Impossible to craft

            # Bail if no gains are possible and we're on the first Spell
            if skill_item.max_level < skill_value and i == 0: return
            
            Meditate(50)
            service.CraftItem(skill_item.item, skill_item.resources)


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Inscription, resource_container)

    resources = [
        service.GetResource("blank scroll", 10, 50), 
        service.GetResource("nightshade", 50, 100),
        service.GetResource("black pearl", 50, 100),
        service.GetResource("blood moss", 50, 100),
        service.GetResource("sulfurous ash", 50, 100),
        service.GetResource("mandrake root", 50, 100),
        service.GetResource("garlic", 50, 100),
        service.GetResource("ginseng", 50, 100),
        service.GetResource("spiders' silk", 50, 100),
    ]

    # Magery spells
    for i in range(8):
        MakeCircle(service, i + 1, resources)


# Execute Main()
Main()