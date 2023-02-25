import sys
from phBot import *
import QtBind
from threading import Timer
import json
import os
import struct
from datetime import datetime

pVersion = '0.1.2'
pName = 'AutoJobCaravan'

# Globals
delayMsg = 60000 # 60000 delay between messages
delayCounter = 0
inGame = False
pFull = False
pBoss = False

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblMobs = QtBind.createLabel(gui,'#     0 = Slot scripti  \n#     1 = kervan taşıma scripti        \n#     2 = job suit alma npcsi \n#     3 = Job Suit çıkartma',494,3)
tbxMobs = QtBind.createLineEdit(gui,"C:/Sro/bot/job/--.txt",31,11,208,22)
lstMobs = QtBind.createList(gui,31,56,208,206)
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"    Script Ekle    ",80,37)
btnAddSc = QtBind.createButton(gui,'btnAddSc_clicked',"   Orjinal Script Ekle    ",300,37)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"     Kaldır     ",80,261)
line_x = QtBind.createLineEdit(gui, "C:/Sro/bot/job/--.txt",245,11,210,22)

lstIgnore = []
selfKervan = []

lblTitan = QtBind.createLabel(gui,'CH Hunter Male (5)',251,64)
cbxIgnoreTitan = QtBind.createCheckBox(gui,'cbxIgnoreTitan_clicked','',358,64)
def cbxIgnoreTitan_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'5')

lblStrong = QtBind.createLabel(gui,'CH Hunter Female (6)',251,83)
cbxIgnoreStrong = QtBind.createCheckBox(gui,'cbxIgnoreStrong_clicked','',358,85)
def cbxIgnoreStrong_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'6')

lblElite = QtBind.createLabel(gui,'CH Thief Male (7)',251,102)
cbxIgnoreElite = QtBind.createCheckBox(gui,'cbxIgnoreElite_clicked','',358,104)
def cbxIgnoreElite_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'7')

lblUnique = QtBind.createLabel(gui,'CH Thief Female (8)',251,121)
cbxIgnoreUnique = QtBind.createCheckBox(gui,'cbxIgnoreUnique_clicked','',358,123)
def cbxIgnoreUnique_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'8')

lblEUHM = QtBind.createLabel(gui,'EU Hunter Male (4)',414,64)
cbxIgnoreEUHM = QtBind.createCheckBox(gui,'cbxIgnoreEUHM_clicked','',524,64)
def cbxIgnoreEUHM_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'4')
    
lblEUHF = QtBind.createLabel(gui,'EU Hunter Female (3)',414,83)
cbxIgnoreEUHF = QtBind.createCheckBox(gui,'cbxIgnoreEUHF_clicked','',524,85)
def cbxIgnoreEUHF_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'3')

lblEUTM = QtBind.createLabel(gui,'EU Thief Male (9)',414,102)
cbxIgnoreEUTM  = QtBind.createCheckBox(gui,'cbxIgnoreEUTM_clicked','',524,104)
def cbxIgnoreEUTM_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'9')

lblEUTF = QtBind.createLabel(gui,'EU Thief Female (2)',414,121)
cbxIgnoreEUTF = QtBind.createCheckBox(gui,'cbxIgnoreEUTF_clicked','',524,123)
def cbxIgnoreEUTF_clicked(checked):
	Checkbox_Checked(checked,lstIgnore,"lstIgnore",'2')
    

otokervan = QtBind.createLabel(gui,'Otomatik Kervan',251,165)
cbxkervan = QtBind.createCheckBox(gui,'cbxkervan_clicked','',344,167)
def cbxkervan_clicked(checked):
	Checkbox_Checked(checked,selfKervan,"selfKervan",'yes')
    
# Generalizing checkbox methods
def Checkbox_Checked(checked,lst,lstName,mobType):
	if checked:
		lst.append(mobType)
	else:
		lst.remove(mobType)
	saveConfig(lstName,lst)

def getConfig():
	return get_config_dir()+get_character_data()["server"]+"_"+get_character_data()["name"]+"_"+pName+".json"

def joined_game():
    configFile = get_config_dir()+get_character_data()["server"]+"_"+get_character_data()["name"]+"_"+pName+".json"
    if not os.path.exists(configFile):
        defaultConfig = get_config_dir()+"AutoJobCaravan.json"
        if os.path.exists(defaultConfig):
            ReplaceFile(defaultConfig,configFile,"Plugin: Default AutoJobCaravan JSON loaded")
    
    configFile = get_config_dir()+get_character_data()["server"]+"_"+get_character_data()["name"]+"_"+pName+".json"
    if os.path.exists(configFile):
        log("Plugin: Ayarlar yüklendi")
        data = {}
        with open(getConfig(),"r") as f:
            data = json.load(f)
        # Check to load config
        if "lstMobs" in data:
            for d in data["lstMobs"]:
                QtBind.append(gui,lstMobs,d)
        if "lstIgnore" in data:
            lstIgnore = data["lstIgnore"]
            for i in range(len(lstIgnore)):
                if lstIgnore[i] == '8':
                    QtBind.setChecked(gui,cbxIgnoreUnique,True)
                elif lstIgnore[i] == '7':
                    QtBind.setChecked(gui,cbxIgnoreElite,True)
                elif lstIgnore[i] == '6':
                    QtBind.setChecked(gui,cbxIgnoreStrong,True)
                elif lstIgnore[i] == '5':
                    QtBind.setChecked(gui,cbxIgnoreTitan,True)
                elif lstIgnore[i] == '4':
                    QtBind.setChecked(gui,cbxIgnoreEUHM,True)
                elif lstIgnore[i] == '3':
                    QtBind.setChecked(gui,cbxIgnoreEUHF,True)
                elif lstIgnore[i] == '9':
                    QtBind.setChecked(gui,cbxIgnoreEUTM,True)
                elif lstIgnore[i] == '2':
                    QtBind.setChecked(gui,cbxIgnoreEUTF,True)
        if "selfKervan" in data:
            selfKervan = data["selfKervan"]
            for i in range(len(selfKervan)):
                if selfKervan[i] == 'yes':
                    QtBind.setChecked(gui,cbxkervan,True)
    
    global inGame,pFull,pBoss
    inGame = True
    pFull = True
    pBoss = True

# Save specific value at config
def saveConfig(key,value):
	if key:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		data[key] = value
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

def btnAddSc_clicked():
	text = QtBind.text(gui,line_x)
	if text and not QtBind_ItemsContains(text,lstMobs):
		QtBind.append(gui,lstMobs,str(get_training_area()["path"]))
		QtBind.setText(gui,line_x,"C:/Sro/bot/job/--.txt")

# Add mob to the list
def btnAddMob_clicked():
	text = QtBind.text(gui,tbxMobs)
	if text and not QtBind_ItemsContains(text,lstMobs):
		QtBind.append(gui,lstMobs,text)
		QtBind.setText(gui,tbxMobs,"C:/Sro/bot/job/--.txt")
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Script added ['+text+']')

# Add mob to the list
def btnRemMob_clicked():
	selected = QtBind.text(gui,lstMobs)
	if selected and QtBind_ItemsContains(selected,lstMobs):
		QtBind.remove(gui,lstMobs,selected)
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Script removed ['+selected+']')

# Return True if text exist at the list
def ListContains(text,lst):
	for i in range(len(lst)):
		if lst[i].lower() == text.lower():
			return True
	return False

# Return True if item exists
def QtBind_ItemsContains(text,lst):
	return ListContains(text,QtBind.getItems(gui,lst))
    
# Inject Packet (Use return scroll)
def inject_useReturnScroll():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if item['name'] == 'Return Scroll' or item['name'] == 'Special Return Scroll' or item['name'] == 'Token Return Scroll' or item['name'] == 'Beginner instant recall scroll':
                Packet = bytearray()
                Packet.append(slot) # Inventory slot
                Packet.append(0x30) # Always constant = 0x0C30
                Packet.append(0x0C) 
                Packet.append(0x03) # RETURN SCROLL ID = 0x0103
                Packet.append(0x01)
                inject_joymax(0x704C, Packet, True)
                log('Plugin: Using "'+item['name']+'" ')
                return
    log('Plugin: "Return Scroll" not found at your inventory')
    
def leave_party(args):
    if len(args) == 2:
        if args[1]:
            inject_joymax(0x7061, b'', False)
            return 2000
            log("[Plugin] Leaving party")

def get_npc(name):
	npcs = get_npcs()
	for k, v in npcs.items():
		if v['name'].strip().lower() == name.strip().lower() or v['servername'].strip().lower() == name.strip().lower():
			return (k, v)
	return None

def get_npc_item(model, item):
	goods = get_npc_goods(model)
	if goods:
		for p, s in goods.items():
			for _s, i in s.items():
				if i['name'].strip().lower() == item.strip().lower() or i['servername'].strip().lower() == item.strip().lower():
					return (p, _s)
	return None

def npc_select(args):
	if len(args) == 2:
		n = get_npc(args[1])
		if n:
			inject_joymax(0x7045, struct.pack('I', n[0]), False)
			return 2000
	return 0

def npc_enter(args):
	if len(args) == 2:
		n = get_npc(args[1])
		if n:
			inject_joymax(0x7046, struct.pack('IB', n[0], 1), False)
			return 2000
	return 0

# CH job npc
def npc_buy(args):
    if len(args) == 4:
        n = get_npc(args[1])
        if n:
            goods = get_npc_item(n[1]['model'], args[2])
            if goods:
                packet = struct.pack('B', 8)
                packet += struct.pack('B', goods[0]) 		# page
                packet += struct.pack('B', goods[1]) 		# slot
                packet += struct.pack('H', int(args[3]))	# quantity
                packet += struct.pack('I', n[0]) 			# npc
                inject_joymax(0x7034, packet, False)
                log("Plugin: item ["+args[2]+"] alınıyor")
                return 2000
    return 0

# EU Job npc
def npceu_buy(args):
    if len(args) == 4:
        n = get_npc(args[1])
        if n:
            goods = get_npc_item(n[1]['model'], args[2])
            if goods:
                packet = struct.pack('B', 8)
                packet += struct.pack('B', goods[0]) 		# page
                packet += struct.pack('B', goods[1]) 		# slot
                packet += struct.pack('H', int(args[3]))	# quantity
                packet += struct.pack('I', n[0]) 			# npc
                inject_joymax(0x7034, packet, False)
                log("Plugin: item EU ["+args[2]+"] alınıyor")
                return 2000
    return 0

# 822: {'name': 'Smuggler Isutade', 'model': 35157, 'servername': 'NPC_KT_COMMERCE2'} - Thief
# 809: {'name': 'Trader Sabonue', 'model': 35152, 'servername': 'NPC_KT_COMMERCE1'},  - Hunter
def npc_exit(args):
	if len(args) == 2:
		n = get_npc(args[1])
		if n:
			inject_joymax(0x704B, struct.pack('I', n[0]), False)
			return 2000
	return 0

def elbise():
    if os.path.exists(getConfig()):
        with open(getConfig(),"r") as f:
            data = json.load(f)
            elbisex = data["lstIgnore"]
        if elbisex[0] == "5":
            elbisem = "ITEM_CH_M_NEW_TRADE_HUNTER_01"
        elif elbisex[0] == "6":
            elbisem = "ITEM_CH_W_NEW_TRADE_HUNTER_01"
        elif elbisex[0] == "7":
            elbisem = "ITEM_CH_M_NEW_TRADE_THIEF_01"
        elif elbisex[0] == "8":
            elbisem = "ITEM_CH_W_NEW_TRADE_THIEF_01"
        elif elbisex[0] == "4":
            elbisem = "ITEM_EU_M_NEW_TRADE_HUNTER_01"
        elif elbisex[0] == "3":
            elbisem = "ITEM_EU_W_NEW_TRADE_HUNTER_01"
        elif elbisex[0] == "9":
            elbisem = "ITEM_EU_M_NEW_TRADE_THIEF_01"
        elif elbisex[0] == "2":
            elbisem = "ITEM_EU_W_NEW_TRADE_THIEF_01"
        else:
            Log("Job Seçilmedi")
    return elbisem

def inject_jobSuit():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if item['servername'] == elbise():
                set_training_script(scriptAyarlama()[1]) #job giydirip scripte başla
                log('Plugin: Suit var ')
                return
    set_training_script(scriptAyarlama()[2]) #komut satırı oluştur do_something() gibi
    log('Plugin: Suit YOK almaya gidiyor')

#öldüğünde slota git
def handle_event(t,data):
    if t == 3:
        set_training_script(scriptAyarlama()[3])
        log("Plugin: Pet öldü mob slot ayarlandı.")

# suit aldıktan sonra scripti 1 ayarla
def gotSuit(args):
    if len(args) == 2:
        set_training_script(scriptAyarlama()[1])
        inject_useReturnScroll()
    return 2000

#kervan bitti slota git
def kervan_bitti(args):
    if len(args) == 2:
        set_training_script(scriptAyarlama()[0])
        inject_useReturnScroll()
        log("Plugin: Kervan Bitti Slotan dönülüyor")
    return 2000

def scriptAyarlama():
    if os.path.exists(getConfig()):
        with open(getConfig(),"r") as f:
            data = json.load(f)
            script = data["lstMobs"]
            return script

def otoKervana():
    if os.path.exists(getConfig()):
        with open(getConfig(),"r") as f:
            data = json.load(f)
            kervan = data["selfKervan"]
            return kervan
        
def kapasite():
    kapasite = get_job_pouch()["size"]
    kapasite *= 5 #çantanın kapasitesi
    return kapasite
    
#çanta adet kontrol
def pounchKontrol():
    inventory = get_job_pouch()["items"]
    total = 0
    for e in inventory:
        if e != None:
            total += e["quantity"]
        else:
            total = 0        
    return total

def fenasi():
    global pFull
    pFull = False
    inject_useReturnScroll()
    inject_jobSuit()

def bosluk():
    global pBoss
    pBoss = False
    set_training_script(scriptAyarlama()[0])
    log("Plugin: Çanta boş")
    
def event_loop():
    Time = datetime.utcnow()
    Hours = int(Time.strftime('%H'))
    Minutes = int(Time.strftime('%M'))
    
    global delayCounter,delaMsg
    if inGame:
        if delayCounter%delayMsg == 0:
            if int(len(otoKervana()[0])) == 3:
                if Hours == 4 and Minutes <= 59:
                    if pounchKontrol() == kapasite():
                        if pFull:
                            log("Plugin: Pounch Dolu")
                            fenasi()
                else:
                    return Hours and Minutes
                
                if Hours > 5 and Minutes >= 30:
                    if pounchKontrol() < kapasite():
                        if pBoss:
                            bosluk()
                else:
                    return Hours and Minutes
        delayCounter += 500
      
#joined_game()
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')