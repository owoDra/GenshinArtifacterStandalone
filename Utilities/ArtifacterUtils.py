from enkanetwork import CharacterInfo, EquipmentsType, DigitType, EquipmentsStats
import json

def ResolveOptionName(Stat: EquipmentsStats):
    Name = Stat.name
    if Stat.type == DigitType.PERCENT:
        if Name == "攻撃力":
            Name = "攻撃パーセンテージ"
        
        elif Name == "防御力":
            Name = "防御パーセンテージ"
            
        elif Name == "HP":
            Name = "HPパーセンテージ"
            
    return Name
    

def CalculateScore(Artifact, Eval: str):
    TotalSocre = 0.0
    
    EvalOpt = []
    if Eval == "攻撃%":
        EvalOpt = ["攻撃力"]
    elif Eval == "防御%":
        EvalOpt = ["防御力"]
    elif Eval == "元チャ効率":
        EvalOpt = ["元素チャージ効率", "攻撃力"]
    elif Eval == "HP%":
        EvalOpt = ["HP"]
    elif Eval == "熟知":
        EvalOpt = ["熟知", "攻撃力"]
        
    for Substate in Artifact.detail.substats:
        if Substate.name in EvalOpt:
            if Substate.type == DigitType.PERCENT or Substate.name == "熟知":
                TotalSocre = TotalSocre + Substate.value
            
        elif Substate.name == "会心率":
                TotalSocre = TotalSocre + Substate.value * 2
                
        elif Substate.name == "会心ダメージ":
                TotalSocre = TotalSocre + Substate.value
                
    return round(TotalSocre, 1)
        

def EvaluateAndExpotData(Uid: int, Character: CharacterInfo, Eval: str):
    ArtifactTypes: dict = {
        "EQUIP_BRACER": "flower",
        "EQUIP_NECKLACE": "wing",
        "EQUIP_SHOES": "clock",
        "EQUIP_RING": "cup",
        "EQUIP_DRESS": "crown"
    }
    ElementTypes: dict = {
        "Ice": "氷",
        "Water": "水",
        "Wind": "風",
        "Fire": "炎",
        "Rock": "岩",
        "Electric": "雷"
    }
    
    Item_Uid = {"uid": Uid}
    Item_Input = {"input": ""}
    Item_Character = {
        "Character": {
            "Name": Character.name,
            "Const": Character.rarity,
            "Level": Character.level,
            "Love": Character.friendship_level,
            "Status": {
                "HP": round(Character.stats.FIGHT_PROP_MAX_HP.value),
                "攻撃力": round(Character.stats.FIGHT_PROP_CUR_ATTACK.value),
                "防御力": round(Character.stats.FIGHT_PROP_CUR_DEFENSE.value),
                "元素熟知": round(Character.stats.FIGHT_PROP_ELEMENT_MASTERY.value),
                "会心率": round(Character.stats.FIGHT_PROP_CRITICAL.value * 100, 1),
                "会心ダメージ": round(Character.stats.FIGHT_PROP_CRITICAL_HURT.value * 100, 1),
                "元素チャージ効率": round(Character.stats.FIGHT_PROP_CHARGE_EFFICIENCY.value * 100, 1),
            },
            "Talent": {
                "通常": Character.skills[0].level,
                "スキル": Character.skills[1].level,
                "爆発": Character.skills[2].level
            },
            "Base":{
                "HP": round(Character.stats.BASE_HP.value),
                "攻撃力": round(Character.stats.FIGHT_PROP_BASE_ATTACK.value),
                "防御力": round(Character.stats.FIGHT_PROP_BASE_DEFENSE.value)
            }
        }
    }
    Item_Weapon = {
        "Weapon": {
            "name": Character.equipments[-1].detail.name,
            "Level": Character.equipments[-1].level,
            "totu": Character.equipments[-1].refinement,
            "rarelity": Character.equipments[-1].detail.rarity,
            "BaseATK": Character.equipments[-1].detail.mainstats.value,
            "Sub": {
                "name": Character.equipments[-1].detail.substats[0].name,
                "value": round(
                    Character.equipments[-1].detail.substats[0].value, (1 if Character.equipments[-1].detail.substats[0].type == DigitType.PERCENT else 0))
            }
        }
    }
    Item_Scores = {"State": Eval}
    
    Item_Artifact = {}
    TotalScore = 0.0
    for Artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, Character.equipments):
        if Artifact.detail.artifact_type in ArtifactTypes:
            Title = ArtifactTypes[Artifact.detail.artifact_type]
            Socre = CalculateScore(Artifact, Eval)
            TotalScore = TotalScore + Socre
            
            Item_Score = {Title: Socre}
            
            Item_SubStates = []
            for Substate in Artifact.detail.substats:
                Item_SubState = {
                    "option": ResolveOptionName(Substate),
                    "value": round(Substate.value, (1 if Substate.type == DigitType.PERCENT else 0))
                }
                Item_SubStates.append(Item_SubState)
            
            Item_ArtifactOpt = {
                Title: {
                    "type": Artifact.detail.artifact_name_set,
                    "Level": Artifact.level,
                    "rarelity": Artifact.detail.rarity,
                    "main": {
                        "option": ResolveOptionName(Artifact.detail.mainstats),
                        "value": Artifact.detail.mainstats.value
                    },
                    "sub": Item_SubStates
                }
            }
            Item_Artifact |= Item_ArtifactOpt
            Item_Scores |= {Title: Socre}
    Item_Scores |= {"total": round(TotalScore, 1)}
    
    Item_Score = {"Score": Item_Scores}
    Item_Artifacts = {"Artifacts": Item_Artifact}
    
    Item_Element = {"元素": ElementTypes[Character.element]}    
    
    Dict_Data: dict = {}
    Dict_Data |= Item_Uid
    Dict_Data |= Item_Input
    Dict_Data |= Item_Character
    Dict_Data |= Item_Weapon
    Dict_Data |= Item_Score
    Dict_Data |= Item_Artifacts
    Dict_Data |= Item_Element
    
    with open(f"./Output/data.json", "w", encoding="utf-8") as w:
            json.dump(Dict_Data, w, indent=4, ensure_ascii=False)
    
    print(f"{Item_Character}")
    
    return True
  