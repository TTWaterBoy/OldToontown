# File: T (Python 2.4)

from otp.chat.ChatInputWhiteListFrame import ChatInputWhiteListFrame
from toontown.chat.TTWhiteList import TTWhiteList
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
import sys
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class TTChatInputWhiteList(ChatInputWhiteListFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTChatInputWhiteList')
    TFToggleKey = base.config.GetString('true-friend-toggle-key', 'alt')
    TFToggleKeyUp = TFToggleKey + '-up'
    
    def __init__(self, parent = None, **kw):
        entryOptions = {
            'parent': self,
            'relief': DGG.SUNKEN,
            'scale': 0.050000000000000003,
            'frameColor': (0.90000000000000002, 0.90000000000000002, 0.84999999999999998, 0.0),
            'pos': (-0.20000000000000001, 0, 0.11),
            'entryFont': OTPGlobals.getInterfaceFont(),
            'width': 8.5999999999999996,
            'numLines': 3,
            'cursorKeys': 0,
            'backgroundFocus': 0,
            'suppressKeys': 0,
            'suppressMouse': 1,
            'command': self.sendChat,
            'failedCommand': self.sendFailed,
            'focus': 0,
            'text': '',
            'sortOrder': DGG.FOREGROUND_SORT_INDEX }
        ChatInputWhiteListFrame.__init__(self, entryOptions, parent, **None)
        self.whiteList = TTWhiteList()
        base.whiteList = self.whiteList
        base.ttwl = self
        self.autoOff = 1
        self.sendBy = 'Data'
        self.prefilter = 0
        self.promoteWhiteList = 1
        self.typeGrabbed = 0
        self.deactivate()
        gui = loader.loadModel('phase_3.5/models/gui/chat_input_gui')
        self.chatFrame = DirectFrame(parent = self, image = gui.find('**/Chat_Bx_FNL'), relief = None, pos = (0.0, 0, 0.0), state = DGG.NORMAL)
        self.chatButton = DirectButton(parent = self.chatFrame, image = (gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos = (0.182, 0, -0.087999999999999995), relief = None, text = ('', OTPLocalizer.ChatInputNormalSayIt, OTPLocalizer.ChatInputNormalSayIt), text_scale = 0.059999999999999998, text_fg = Vec4(1, 1, 1, 1), text_shadow = Vec4(0, 0, 0, 1), text_pos = (0, -0.089999999999999997), textMayChange = 0, command = self.chatButtonPressed)
        self.cancelButton = DirectButton(parent = self.chatFrame, image = (gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr')), pos = (-0.151, 0, -0.087999999999999995), relief = None, text = ('', OTPLocalizer.ChatInputNormalCancel, OTPLocalizer.ChatInputNormalCancel), text_scale = 0.059999999999999998, text_fg = Vec4(1, 1, 1, 1), text_shadow = Vec4(0, 0, 0, 1), text_pos = (0, -0.089999999999999997), textMayChange = 0, command = self.cancelButtonPressed)
        self.whisperLabel = DirectLabel(parent = self.chatFrame, pos = (0.02, 0, 0.23000000000000001), relief = DGG.FLAT, frameColor = (1, 1, 0.5, 1), frameSize = (-0.23000000000000001, 0.23000000000000001, -0.070000000000000007, 0.050000000000000003), text = OTPLocalizer.ChatInputNormalWhisper, text_scale = 0.040000000000000001, text_fg = Vec4(0, 0, 0, 1), text_wordwrap = 9.5, textMayChange = 1)
        self.chatEntry.bind(DGG.OVERFLOW, self.chatOverflow)
        self.chatEntry.bind(DGG.TYPE, self.typeCallback)
        self.trueFriendChat = 0
        if base.config.GetBool('whisper-to-nearby-true-friends', 1):
            self.accept(self.TFToggleKey, self.shiftPressed)
        

    
    def shiftPressed(self):
        self.ignore(self.TFToggleKey)
        self.trueFriendChat = 1
        self.accept(self.TFToggleKeyUp, self.shiftReleased)

    
    def shiftReleased(self):
        self.ignore(self.TFToggleKeyUp)
        self.trueFriendChat = 0
        self.accept(self.TFToggleKey, self.shiftPressed)

    
    def handleTypeGrab(self):
        self.ignore('typeEntryGrab')
        self.accept('typeEntryRelease', self.handleTypeRelease)
        self.typeGrabbed = 1

    
    def handleTypeRelease(self):
        self.ignore('typeEntryRelease')
        self.accept('typeEntryGrab', self.handleTypeGrab)
        self.typeGrabbed = 0

    
    def typeCallback(self, extraArgs):
        if self.typeGrabbed:
            return None
        
        self.applyFilter(extraArgs)
        if localAvatar.chatMgr.chatInputWhiteList.isActive():
            return None
        else:
            messenger.send('wakeup')
            messenger.send('enterNormalChat')

    
    def destroy(self):
        self.chatEntry.destroy()
        self.chatFrame.destroy()
        self.ignoreAll()
        ChatInputWhiteListFrame.destroy(self)

    
    def delete(self):
        base.whiteList = None
        ChatInputWhiteListFrame.delete(self)

    
    def sendChat(self, text, overflow = False):
        if self.typeGrabbed:
            return None
        else:
            ChatInputWhiteListFrame.sendChat(self, self.chatEntry.get())

    
    def sendChatByData(self, text):
        if self.trueFriendChat:
            for (friendId, flags) in base.localAvatar.friendsList:
                if flags & ToontownGlobals.FriendChat:
                    self.sendWhisperByFriend(friendId, text)
                    continue
            
        elif not self.receiverId:
            base.talkAssistant.sendOpenTalk(text)
        elif self.receiverId and not (self.toPlayer):
            base.talkAssistant.sendWhisperTalk(text, self.receiverId)
        elif self.receiverId and self.toPlayer:
            base.talkAssistant.sendAccountTalk(text, self.receiverId)
        

    
    def sendWhisperByFriend(self, avatarId, text):
        online = 0
        if base.cr.doId2do.has_key(avatarId):
            online = 1
        
        avatarUnderstandable = 0
        av = None
        if avatarId:
            av = base.cr.identifyAvatar(avatarId)
        
        if av != None:
            avatarUnderstandable = av.isUnderstandable()
        
        if avatarUnderstandable and online:
            base.talkAssistant.sendWhisperTalk(text, avatarId)
        

    
    def chatButtonPressed(self):
        print 'chatButtonPressed'
        if self.okayToSubmit:
            self.sendChat(self.chatEntry.get())
        else:
            self.sendFailed(self.chatEntry.get())

    
    def cancelButtonPressed(self):
        self.requestMode('Off')
        localAvatar.chatMgr.fsm.request('mainMenu')

    
    def enterAllChat(self):
        ChatInputWhiteListFrame.enterAllChat(self)
        self.whisperLabel.hide()

    
    def exitAllChat(self):
        ChatInputWhiteListFrame.exitAllChat(self)

    
    def enterPlayerWhisper(self):
        ChatInputWhiteListFrame.enterPlayerWhisper(self)
        self.labelWhisper()

    
    def exitPlayerWhisper(self):
        ChatInputWhiteListFrame.exitPlayerWhisper(self)
        self.whisperLabel.hide()

    
    def enterAvatarWhisper(self):
        ChatInputWhiteListFrame.enterAvatarWhisper(self)
        self.labelWhisper()

    
    def exitAvatarWhisper(self):
        ChatInputWhiteListFrame.exitAvatarWhisper(self)
        self.whisperLabel.hide()

    
    def labelWhisper(self):
        if self.receiverId:
            self.whisperName = base.talkAssistant.findName(self.receiverId, self.toPlayer)
            self.whisperLabel['text'] = OTPLocalizer.ChatInputWhisperLabel % self.whisperName
            self.whisperLabel.show()
        else:
            self.whisperLabel.hide()

    
    def applyFilter(self, keyArgs, strict = False):
        text = self.chatEntry.get(plain = True)
        if len(text) > 0 and text[0] in [
            '~',
            '>']:
            self.okayToSubmit = True
        else:
            words = text.split(' ')
            newwords = []
            self.okayToSubmit = True
            flag = 0
            for (friendId, flags) in base.localAvatar.friendsList:
                if flags & ToontownGlobals.FriendChat:
                    flag = 1
                    continue
            
            for word in words:
                if word == '' and self.whiteList.isWord(word) or not (base.cr.whiteListChatEnabled):
                    newwords.append(word)
                    continue
                if self.checkBeforeSend:
                    self.okayToSubmit = False
                else:
                    self.okayToSubmit = True
                if flag:
                    newwords.append('\x01WLDisplay\x01' + word + '\x02')
                    continue
                newwords.append('\x01WLEnter\x01' + word + '\x02')
            
            if not strict:
                lastword = words[-1]
                if lastword == '' and self.whiteList.isPrefix(lastword) or not (base.cr.whiteListChatEnabled):
                    newwords[-1] = lastword
                elif flag:
                    newwords[-1] = '\x01WLDisplay\x01' + lastword + '\x02'
                else:
                    newwords[-1] = '\x01WLEnter\x01' + lastword + '\x02'
            
            newtext = ' '.join(newwords)
            self.chatEntry.set(newtext)
        self.chatEntry.guiItem.setAcceptEnabled(self.okayToSubmit)


