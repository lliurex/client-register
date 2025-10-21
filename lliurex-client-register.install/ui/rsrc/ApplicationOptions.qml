import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:160
        Layout.minimumHeight:230
        Layout.preferredHeight:230
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:2 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:wifiItem
                optionText:i18nd("lliurex-client-register","Configuration")
                optionIcon:"/usr/share/icons/breeze/actions/22/configure.svg"
                optionEnabled:true
                Connections{
                    function onMenuOptionClicked(){
                        clientRegisterBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("lliurex-client-register","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        clientRegisterBridge.openHelp();
                    }
                }
            }
        }
    }

    StackView{
        id: optionsView
        property int currentIndex:clientRegisterBridge.currentOptionsStack
        Layout.fillWidth:true
        Layout.fillHeight: true
        Layout.alignment:Qt.AlignHCenter
       
        initialItem:settingsView

        onCurrentIndexChanged:{
            switch (currentIndex){
                case 0:
                    optionsView.replace(settingsView)
                    break;
             }
        }

        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 60
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 60
            }
        }

        Component{
            id:settingsView
            Settings{
                id:settings
            }
        }

    }
}

