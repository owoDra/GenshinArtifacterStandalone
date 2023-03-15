from Utilities import EnkaUtils
from UserInterface.UI_Base import BaseUI

import PySimpleGUI as PSG

class UI_SetUID(BaseUI):
    def __init__(self, Func):
        super().__init__(Func)
    
    def Construct(self):
        Layout = [  [PSG.Text('読み込むユーザーのUIDを入力してください。')],
                    [PSG.InputText(key='InputUID')],
                    [PSG.Button('読み込み'), PSG.Button('キャンセル')] ]
        
        return PSG.Window('ユーザー読み込み', Layout)
    
    def Update(self, Event, Values):
        if Event == PSG.WIN_CLOSED or Event == 'キャンセル': 
            self.Close()
            
        elif Event == '読み込み':
            self.TryFetchUser(Values['InputUID'])
            
    def TryFetchUser(self, Uid):
        Data = EnkaUtils.FetchUserData(Uid)
        if Data == None:
            PSG.popup_error('読み込み失敗: UIDが間違っている可能性があります')
        else:
            self.Close(SendHandler = True, Arg = Data)