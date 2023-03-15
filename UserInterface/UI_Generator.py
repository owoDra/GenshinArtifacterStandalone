from Utilities import EnkaUtils, ArtifacterUtils
from UserInterface.UI_Base import BaseUI
from UserInterface.UI_SetUID import UI_SetUID
from ThirdParty.ArtifacterImageGen import Generater

import PySimpleGUI as PSG

class UI_Generator(BaseUI):
    def __init__(self, Func, Data):   
        self.Uid = Data.profile.uid
        self.Nickname = Data.player.nickname
        self.Characters = Data.characters
        self.CharacterNames = []
        for Character in Data.characters:
            self.CharacterNames.append(Character.name)
        self.EvalType = ["攻撃%", "防御%", "元チャ効率", "HP%", "熟知"]
            
        super().__init__(Func)
        
    def Construct(self):
        Layout = [ [PSG.Text(f"プレイヤー名: {self.Nickname}")],
                   [PSG.Text("評価するキャラクター"), PSG.Combo(self.CharacterNames, self.CharacterNames[0], size = (25, 25), key='Character')],
                   [PSG.Text("評価の仕方　　　　　"), PSG.Combo(self.EvalType, self.EvalType[0], size = (25, 25), key='Evaluate')],
                   [PSG.Button('評価'), PSG.Button('ユーザー変更'), PSG.Button('終了')] ]
        
        return PSG.Window('キャラクター評価', Layout)
    
    def Update(self, Event, Values):
        if Event == PSG.WIN_CLOSED or Event == '終了': 
            self.Close()
            
        elif Event == 'ユーザー変更':
            self.Close(SendHandler = True)
            
        elif Event == '評価':
            self.TryEvaluate(Values['Character'], Values['Evaluate'])
            
    def TryEvaluate(self, CharacterName, EvalType):
        for Character in self.Characters:
            if Character.name == CharacterName:
                if ArtifacterUtils.EvaluateAndExpotData(self.Uid, Character, EvalType):
                    Generater.generation(Generater.read_json("Output/data.json"))
                else:
                    PSG.popup_error("評価失敗: 選択が間違っています")
                break