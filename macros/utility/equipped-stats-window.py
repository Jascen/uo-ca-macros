"""
Name: Equipment calculator
Description: Used to add up all Property values on a paperdoll
Author: Tsai (Ultima Adventures)
Version: v2.0

*****Warnings*****
- It does not handle Diminishing returns
  - 70 resist should be approximately 128 total resist
*****Warnings*****
"""

import clr
import System
clr.AddReference("System.Core")
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('WindowsBase')
clr.ImportExtensions(System.Linq)
from System import Uri
from System.Windows import Window, ResourceDictionary, SizeToContent
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState

from Assistant import Engine
from ClassicAssist.UO.Data import Layer


layers = [
    Layer.OneHanded,
    Layer.TwoHanded,
    Layer.Shoes,
    Layer.Pants,
    Layer.Shirt,
    Layer.Helm,
    Layer.Gloves,
    Layer.Ring,
    Layer.Talisman,
    Layer.Neck,
    Layer.Waist,
    Layer.InnerTorso,
    Layer.Bracelet,
    Layer.MiddleTorso,
    Layer.Earrings,
    Layer.Arms,
    Layer.Cloak,
    Layer.OuterTorso,
    Layer.OuterLegs,
    Layer.InnerLegs,
]

xaml = """
<Grid xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto"/>
        <RowDefinition Height="*"/>
    </Grid.RowDefinitions>
    <Button Content="Refresh" Grid.Row="0" Margin="10, 10" x:Name="refreshButton"/>
    <ListView Grid.Row="1" x:Name="listView">
        <ListView.View>
            <GridView>
                <GridViewColumn Header="Property Name" DisplayMemberBinding="{Binding Name}" Width="150"/>
                <GridViewColumn Header="Value" DisplayMemberBinding="{Binding Value}" Width="50"/>
            </GridView>
        </ListView.View>
    </ListView>
</Grid>
"""


class InteractionUtils:
    @classmethod
    def Prompt(cls, title, content, footer):
        result = ConfirmPrompt(
            "<center>{}</center>".format(title)
            + content
            + "<br><br>"
            + footer
            )
        
        Pause(350) # Small pause to let the user realize the window has changed

        return result


class Property:
    def __init__(self, name, value):
        self.Name = name
        self.Value = value


class XamlWindow(Window):
    def __init__(self):
        rd = ResourceDictionary()
        rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
        self.Resources.MergedDictionaries.Add(rd)
        self.Background = self.Resources["ThemeWindowBackgroundBrush"]      
        
        self.Content = XamlReader.Parse(xaml)
        self.Title = "Equipped Items"
        self.Topmost = True
        self.SizeToContent = SizeToContent.Width
        self.Height = 600
        self.listView = self.Content.FindName("listView")
        self.refreshButton = self.Content.FindName("refreshButton")
        self.mobile = None
        self.refreshButton.Click += self.refresh

    def initialize(self):
        confirmed = False
        target_serial = None
        targeted = None
        while True:
            alias = '$mobile_target'
            if not confirmed: target_serial = PromptMacroAlias(alias)
            else: target_serial = None
            if targeted and not target_serial: break
            if not target_serial: continue

            targeted = Engine.Mobiles.GetMobile(GetAlias(alias))
            if not targeted: continue

            # Auto-confirm if targeting self
            if targeted.Serial == Engine.Player.Serial: break

            confirmed = InteractionUtils.Prompt(
                "<center>Confirm Mobile</center>",
                "{}<br>".format(targeted.Name.upper()) +
                "The paperdoll must be open to get latest equipment.",
                "Press OKAY to confirm your target."
            )
            if not confirmed: targeted = None
            UseObject(targeted.Serial)
            Pause(1000)

        self.mobile = targeted
        self.refresh()

    def refresh(self, sender = None, event = None):
        self.listView.Items.Clear()

        cliloc_value_total = {}
        cliloc_map = {}
        for layer in layers:
            serial = self.mobile.GetLayer(layer)
            if not serial: continue

            item = Engine.Items.GetItem(serial)
            if not item: continue

            self.PluckPercentProperties(item, cliloc_value_total, cliloc_map)

        properties = []
        for cliloc, name in cliloc_map.items():
            value = str(cliloc_value_total[cliloc])
            properties.append(Property(name.title(), value))
        
        for item in properties.OrderBy(lambda i: i.Name):
            self.listView.Items.Add(item)


    def PluckPercentProperties(self, item, cliloc_value_total, cliloc_map):
        if not item: return
        
        if not item.Properties:
            print("Failed to get item stats. Item '{}' ({}) has no properties.".format(item.Serial, item.Name))
            return

        for prop in item.Properties:
            if not prop.Arguments: continue
            if not prop.Cliloc: continue

            value = prop.Arguments[0]
            if not value.isdecimal(): continue

            if not cliloc_map.get(prop.Cliloc):
                cliloc_value_total[prop.Cliloc] = 0
                value_index = prop.Text.rfind(value)
                if value_index < 0: continue
                
                cliloc_map[prop.Cliloc] = prop.Text[:value_index].strip()
            
            cliloc_value_total[prop.Cliloc] += int(value)


def ShowWindow():
    try:
        c = XamlWindow()
        c.initialize()
        c.ShowDialog()
    except Exception as e:
        # if you don't catch these, an exception will likely take down CUO/CA
        print(e)

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()

print("Window Closing")