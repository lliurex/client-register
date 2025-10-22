import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-client-register","Laptop cart configuration")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        width:parent.width-10
        anchors.left:parent.left

        Kirigami.InlineMessage {
            id: messageLabel
            visible:clientRegisterBridge.showSettingsMessage[0]
            text:getMessageText(clientRegisterBridge.showSettingsMessage[1])
            type:getMessageType(clientRegisterBridge.showSettingsMessage[2])
            Layout.minimumWidth:490
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            columns: 2
            flow: GridLayout.LeftToRight
            columnSpacing:10
            Layout.topMargin: messageLabel.visible?0:50

            Text{
                id:registrationText
                text:i18nd("lliurex-client-register","Laptop assigned to the cart:")
                font.family: "Quattrocento Sans Bold"
                font.pointSize:10
                Layout.bottomMargin:10
                Layout.alignment:Qt.AlignRight
            }

            ComboBox{
                id:cartsValues
                currentIndex:clientRegisterBridge.currentClientCart
                model:clientRegisterBridge.maxNumCart
                delegate:ItemDelegate{
                    width:40
                    text:index+1
                }
                displayText:currentIndex
                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:10
                Layout.preferredWidth:60
                onActivated:{
                    console.log(cartsValues.currentIndex)
                    clientRegisterBridge.updateCart(cartsValues.currentIndex+1)
                }
            }


        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-client-register","Apply")
            Layout.preferredHeight:40
            enabled:clientRegisterBridge.settingsClientChanged?true:false 
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                closeTimer.stop()
                clientRegisterBridge.applyChanges()
                
            }
        }
        Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-client-register","Cancel")
            Layout.preferredHeight: 40
            enabled:clientRegisterBridge.settingsClientChanged?true:false 
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                closeTimer.stop()
                clientRegisterBridge.cancelChanges()
            }
        }
    } 

    ChangesDialog{
        id:wifiChangesDialog
        dialogTitle:"Lliurex Client Register"+" - "+i18nd("lliurex-wifi-gva-control","Cart configuration")
        dialogVisible:clientRegisterBridge.showChangesDialog
        dialogMsg:i18nd("lliurex-client-register","The are pending changes to apply.\nDo you want apply the changes or discard them?")
        btnAcceptVisible:true
        btnDiscardText:i18nd("lliurex-client-register","Discard")
        btnDiscardVisible:true
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("lliurex-client-register","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:wifiChangesDialog
            function onDialogApplyClicked(){
                applyChanges()
                clientRegisterBridge.manageChangesDialog("Accept")
            }
            function onDiscardDialogClicked(){
                discardChanges()
                clientRegisterBridge.manageChangesDialog("Discard")
            }
            function onCancelDialogClicked(){
                closeTimer.stop()
                clientRegisterBridge.manageChangesDialog("Cancel")
            }

        }
    }

    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:delayTimer
    }

    function delay(delayTime,cb){
        delayTimer.interval=delayTime;
        delayTimer.repeat=true;
        delayTimer.triggered.connect(cb);
        delayTimer.start()
    }

    Timer{
        id:waitTimer
    }

    function wait(delayTime,cb){
        waitTimer.interval=delayTime;
        waitTimer.repeat=true;
        waitTimer.triggered.connect(cb);
        waitTimer.start()
    }


    function getMessageText(code){

        var msg="";
        switch (code){
            case 10:
                msg=i18nd("lliurex-client-register","Changes applied successfully");
                break;
            case -10:
                msg=i18nd("lliurex-client-register","Error assigning laptop to cart")
                break;
            default:
                break;
        }
        return msg;

    }

    function getMessageType(type){

        switch (type){
            case "Info":
                return Kirigami.MessageType.Information
            case "Success":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
        }

    } 


    function applyChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-client-register", "Apply changes. Wait a moment...")
        delayTimer.stop()
        delay(500, function() {
            if (clientRegisterBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()
            }
        })
    } 

    function discardChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-client-register", "Restoring previous values. Wait a moment...")
        delayTimer.stop()
        delay(1000, function() {
            if (clientRegisterBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()

            }
        })
    }  
} 
