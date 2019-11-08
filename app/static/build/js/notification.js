setInterval(function(){ getNotification(); }, 2000);

var firstNotification = 0;
var secondNotification = 0;
var thirdNotification = 0;
var fourthNotification = 0;
var fifthNotification = 0;

function getNotification()
{
    var userType = $("#userType").val();
    $.ajax({
            type: "GET",
            data: {"userType":userType},
            url: '/getNotification',
            dataType: 'json',
            success: function (data) {
                var obj = JSON.parse(data);
                $("#notificationMenu").empty();
                var notificationDisplay = "";
                var newCount = 0;
                firstNotification = 0;
                lastNotification = 0;
                for(i=0; i <obj.length; i++){
                    //Display till max 5 only
                    if(i==5)
                    {
                        i = obj.length;
                        break;
                    }

                    if(!obj[i].fields.Read){
                        if(firstNotification==0)
                            firstNotification = obj[i].pk;
                        else if(secondNotification==0)
                            secondNotification = obj[i].pk;
                        else if(thirdNotification==0)
                            thirdNotification = obj[i].pk;
                        else if(fourthNotification==0)
                            fourthNotification = obj[i].pk;
                        else if(fifthNotification==0)
                            fifthNotification = obj[i].pk;

                        newCount+=1;
                        notificationDisplay += "<li style='background-color:lightblue'>";
                    }
                    else
                        notificationDisplay += "<li>";

                    notificationDisplay += "<a href='inbox.html'><span class='image'><img src='/static/images/img.jpg' alt='Profile Image' /></span><span>";
                    notificationDisplay += "<span>" + obj[i].fields.Title +"</span><span class='time'>just now</span></span>";
                    notificationDisplay += "<span class='message'>" + obj[i].fields.Description + "</span></a></li>";
                }
                notificationDisplay += "<li><div class='text-center'><a><strong>See All Alerts</strong>";
                notificationDisplay += "<i class='fa fa-angle-right'></i></a></div></li>";

                $("#notificationMenu").append(notificationDisplay);
                $("#notifyNo").html(newCount);

                if(newCount != 0 && $('body').find(".ui-pnotify").length == 0)
                {
                    new PNotify({
                        title: 'Notification',
                        text: 'You have ' + newCount + ' new Notification!',
                        type: 'success',
                        styling: 'bootstrap3'
                    });
                }

            },
             error: function(err) {
             }
        });
}

$("#notificationButton").click(function() {
    if($('#notificationButton').attr('aria-expanded') != "true")
    {
        if(firstNotification!=0 || secondNotification!=0 ||thirdNotification!=0 ||fourthNotification!=0 ||fifthNotification!=0){
            $.ajax({
                type: "GET",
                data: {"firstNotify":firstNotification,"secondNotify":secondNotification,"thirdNotify":thirdNotification,"fourthNotify":fourthNotification,"fifthNotify":fifthNotification},
                url: '/updateNotification',
                dataType: 'json',
                success: function () {
                }
            });
        }
    }
});
