var ajax_notification_timeout;
function notification_cleanup(time){
    clearTimeout(ajax_notification_timeout);
        ajax_notification_timeout = setTimeout(function() {
            $('.notification-box').fadeOut();
        }, time);
}
function show_notification(type, title, content, time){
	$('.notification-box').fadeIn();
	$('#notif-title').html(title);
	$('#notif-content').html(content);
	$('.notif-type').addClass(type)
    if (time) notification_cleanup(time);
}
$(document).ready(function(){
    var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/notifications/');
    socket.onmessage = function (event) {
    	var data = JSON.parse(event.data);
        show_notification(data.type, data.title, data.content, 5000);
    }

    $('.notif-box-close').click(function(){
    	$('#notification-box').hide();
    });
});

