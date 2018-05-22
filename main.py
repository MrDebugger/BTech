from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from functools import partial
import requests,json,re

##################################
##    ____ ______          __  	##
##   / __ )_  __/__  _____/ /_ 	##
##  / __  |/ / / _ \/ ___/ __ \	##
## / /_/ // / /  __/ /__/ / / /	##
##/_____//_/  \___/\___/_/ /_/ 	##
##	 -Coded by Ijaz Ur Rahim-	##
##	 -AKA Muhammad Ibraheem-	##
##		The Alien || P.C.G.		##
##################################                           

##########################################
##				CONTACT					##
##	Website: https://ijazurrahim.com/	##
##	Facebook: @muibraheem96				##
##	Twitter: @muibraheem96				##
##	Instagram: @muibraheem96			##
##	Github: IJAZ9913					##
##	Medium: @muibraheem96				##
##	LinkedIn: @muibraheem96				##
##	Fiverr: @muibraheem96				##
##	StackOverFlow: @muibraheem96		##
##########################################

Builder.load_string('''
<Test>:
	orientation: 'vertical'
	padding: [0,10,0,0]
	ScrollView:
		Label:
			id: myLabel
			text: root.Clear()
			text_size: self.width,None
			size_hint_y: None
			height: self.texture_size[1]
			width: self.texture_size[0]
			markup: True
			font_name: 'Arial'
	GridLayout:
		cols: 4
		height: '50dp'
		size_hint_y: None
		BoxLayout:
			orientation: 'vertical'
			valign: 'bottom'
			Button:
				id: RunButton
				text: "Run"
				height: self.parent.height
				size_hint_y: None
				on_release: root.ChangeText()
		BoxLayout:
			orientation: 'vertical'
			valign: 'bottom'
			Button:
				text: "Copy"
				size_hint_y: None
				height: self.parent.height
				on_release: root.Copy()
		BoxLayout:
			orientation: 'vertical'
			valign: 'bottom'
			Button:
				text: "Paste"
				size_hint_y: None
				height: self.parent.height
				on_release: root.Paste()
		BoxLayout:
			orientation: 'vertical'
			valign: 'bottom'
			Button:
				id: ClearButton
				text: "Clear"
				size_hint_y: None
				height: self.parent.height
				on_release: root.Clear()
	TextInput:
		id: MyText
		hint_text: "http://site.com or 127.0.0.1"
		height: self.font_size + 45
		font_size: 45
		width: root.width
		multiline:0
		size_hint_y: None
		focus: True
		on_text_validate: root.ChangeText()

	''')
class Test(BoxLayout):
	
	def ChangeText(self):
		global sitesFound
		global abc
		try:
			self.ids.myLabel.text = "[color=00ff00]root[/color][color=0000ff]@[/color][color=ff0000]android[/color] $"
			target = self.ids.MyText.text.replace("http://","")
			target = target.replace("https://","")
			target = target.replace("/","")
			data={"remoteAddress":target,"key":""}
			headers = {"user-agent":"Mozilla/5.0 (Windows NT 5.1; rv:24.0) Gecko/20100101 Firefox/24.0"}
			r = requests.post("https://domains.yougetsignal.com/domains.php",data=data,headers=headers,timeout=2)
			Data = json.loads(r.text)
			self.ids.myLabel.text += " [color=00FF00]./BTech --target " + self.ids.MyText.text + "[/color]"
			adminPanels = ["admin","wp-admin","login.php","user","Admin","adminlogin","adminpanel","admin_login"]
			if Data['status'] == 'Success':
				self.ids.myLabel.text += "\n[color=00FFEC]Target[/color]: " + Data['remoteAddress']
				self.ids.myLabel.text += "\n[color=00FFEC]Ip Address[/color]: " + Data['remoteIpAddress']
				self.ids.myLabel.text += "\n[color=00FFEC]Total Domains Found[/color]: " + Data['domainCount']
				self.ids.myLabel.text += "\n[color=00FFEC][b]Please Wait While i am Checking the Admin Panels[/b][/color]\n"
				argum = []
				sitesFound = []
				def next_step(*_):
					ar = len(argum)
					argum.append("a")
					for admin in adminPanels:
						try:
							siteTest = Data['domainArray'][ar][0]+"/"+admin
							try:	
								site = requests.get("http://"+siteTest,timeout=2)
							except:
								site = requests.get("https://"+siteTest,timeout=2)
							if site.status_code != 404:
								rsp=site.content
								rx=re.findall('type="Password"',rsp,re.I)
								if len(rx) == 1:
									if "wp-admin" in rsp:
										form = "[b][color=0fff00]Wordpress[/color][/b]"
									elif "joomla" in rsp:
										form = "[b][color=ffff00]Joomla[/color][/b]"
									else:
										form = "[b][color=00ffff]Simple Web[/color][/b]"
									self.ids.myLabel.text = self.ids.myLabel.text.replace("[color=00FFEC][b]Please Wait While i am Checking the Admin Panels[/b][/color]\n","")
									self.ids.myLabel.text += "\n[color=FF8000]" + siteTest + "[/color] => " + form
									sitesFound.append(siteTest)
									break
									
								else:
									pass
						except:
							pass
					self.ids.RunButton.text = str(ar + 1)
					self.ids.ClearButton.text = "Cancel"
					if ar == (len(Data['domainArray'])-2):
						self.ids.myLabel.text += "\n\n[color=00ff00]Scanning Completed, You can Copy List now[/color]"
						self.ids.RunButton.text = "Run"
						self.ids.ClearButton.text = "Clear"
						abc.cancel()
					else:
						pass
				abc = Clock.schedule_interval(next_step,0.000000001)
			else:
				self.ids.myLabel.text += "\n[color=ff0000]Domain Not Found[/color]"
		except:
			self.ids.myLabel.text += "\n[color=ff0000]Something went Wrong[/color]"
	def Copy(self):
		a = "\n".join(sitesFound)
		Clipboard.copy(a)
	def Paste(self):
		self.ids.MyText.text = Clipboard.paste()
	def Clear(self):
		try:
			abc.cancel()
		except:
			pass
		self.ids.myLabel.text = "[color=00ff00]root[/color][color=0000ff]@[/color][color=ff0000]android[/color] $"
		self.ids.MyText.text = ""
		return self.ids.myLabel.text
runTouchApp(Test())
