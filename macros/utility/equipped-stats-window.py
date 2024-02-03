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
        self.refreshButton.Click += self.refresh
        self.refresh()


    def refresh(self, sender = None, event = None):
        self.listView.Items.Clear()

        cliloc_value_total = {}
        cliloc_map = {}
        for layer in layers:
            serial = Engine.Player.GetLayer(layer)
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
        c.ShowDialog()
    except Exception as e:
        # if you don't catch these, an exception will likely take down CUO/CA
        print(e)

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()

print("Window Closing")